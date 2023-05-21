import logging
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from docker import DockerClient, errors
from utils.config import read_conf, auto_save_conf, GLOBAL_CONFIG
from utils.terminal import CommandExecutor
from utils.monitor import get_system_info, get_status_info, upload_to_pastebin
from utils.file import upload

logging.basicConfig(format='[%(asctime)s %(levelname)s]: %(message)s')

app = Flask(__name__, template_folder='dist', static_folder='dist', static_url_path='')
socketio = SocketIO(app)

try:
    client = DockerClient(base_url='unix://var/run/docker.sock')
except errors.DockerException:
    logging.error(
        "\n无法连接 Docker！请排查以下错误: "
        "\n\t- 是否使用类 Unix 系统 (Linux, MacOS等)"
        "\n\t- Docker 是否已经安装且正在运行"
        "\n\t- 使用过时的 Docker 引擎版本导致兼容问题"
    )


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def error(_err):
    return render_template('index.html'), 200


@socketio.on('command_input')
def term_command(command):
    """处理命令"""
    executor = CommandExecutor(command)
    for output in executor.start():
        emit('command_output', output)


@socketio.on('reset_command')
def reset_command():
    """如果遇到意外情况，重置命令"""
    executor.reset()


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """上传文件"""
    return jsonify({
        'status': upload(request.files['file']),
    })


@app.route('/api/load', methods=['GET'])
def load_config():
    """读取全局配置并加载toml数据"""
    data = read_conf(GLOBAL_CONFIG)
    return jsonify({'status': True, 'data': data} if data else {'status': False})


@app.route("/api/save/<name>", methods=["POST"])
def save_config(name: str):
    """保存配置"""
    return jsonify({
        "status": auto_save_conf(name, request.json),
    })


@app.route('/api/info', methods=['GET'])
def get_system():
    return jsonify(get_system_info())


@socketio.on('status_input')
def get_status():
    emit('status_output', get_status_info())


@app.route('/api/check', methods=['GET'])
def check_error():
    """检查chatgpt是否有报错"""
    container = client.containers.get("chatgpt-qq-chatgpt-1")
    logs = container.logs(stdout=True, stderr=True, tail=200).decode('utf-8')

    if 'ERROR' in logs:
        url = upload_to_pastebin(logs)
        return jsonify(status=False, url=url)
    return jsonify(status=True)


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
