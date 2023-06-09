<script setup lang='ts'>
import { reactive, ref } from 'vue'
import type { Ref } from 'vue'
import axios from 'axios'
import { message } from '@/assets/script/utils'

const type: Ref<string> = ref('openai');


const openai = reactive({
  mode: "web",
  browserless_endpoint: "https://chatgpt-proxy.lss233.com/api/",
  api_endpoint: "https://api.openai.com/v1",
  accounts: {
    access_token: "",
    auto_remove_old_conversations: false,
    title_pattern: "",
    proxy: "",
    api_key: "",
  }
})
const bing = reactive({
  wss_link: "wss://sydney.bing.com/sydney/ChatHub",
  bing_endpoint: "https://edgeservices.bing.com/edgesvc/turing/conversation/create",
  show_suggestions: false,
  show_references: false,
  show_remaining_count: false,
  use_drawing: false,
  accounts: {
    cookie_content: '',
    proxy: "",
  }
})
const bard = reactive({
  accounts: {
    cookie_content: '',
    proxy: ""
  }
})
const yiyan = reactive({
  accounts: {
    BDUSS: '',
    BAIDUID: '',
    proxy: ""
  },
})
const chatglm = reactive({
  accounts: {
    api_endpoint: "http://127.0.0.1:8000",
    max_turns: 10,
    timeout: 360,
  },
})
const poe = reactive({
  accounts: {
    p_b: "",
    proxy: ""
  }
})
const claude = reactive({
  accounts: {
    channel_id: "",
    access_token: "",
    proxy: "",
  },
})

const selector: Record<string, Record<string, string | number | boolean | Record<string, any> | undefined>> = {
  openai,
  bing,
  bard,
  chatglm,
  poe,
  claude
}


const loader = ref(false);
function submit() {
  loader.value = true;
  const data: Record<string, Record<string, any>> = {}, q = {...selector[type.value]};  // deep-copy
  if (q.accounts !== undefined) q.accounts = [q.accounts, ];
  if (type.value === "openai") delete q['mode'];
  data[type.value] = q;
  axios.post('/api/save/ai', data)
    .then(() => {
      loader.value = false;
      message({
        type: 'success',
        message: `保存成功！`,
      });
    })
    .catch(() => {
      loader.value = false;
      message({
        type: 'error',
        message: `保存时出错！`,
      });
    })
}

axios.get('api/load/ai')
  .then(res => {
    const data = res.data.data;
    for (const query in data) {
      const obj = selector[query], conf = data[query];
      conf.accounts = conf.accounts[0];
      for (let key in conf) obj[key] = conf[key];
      type.value = query;
    }
  })
</script>

<template>
  <el-radio-group v-model='type'>
    <el-radio label='openai'>ChatGPT</el-radio>
    <el-radio label='bing'>New Bing</el-radio>
    <el-radio label='bard'>Google Bard</el-radio>
    <el-radio label='yiyan'>文心一言</el-radio>
    <el-radio label='chatglm'>chatGLM</el-radio>
    <el-radio label='poe'>Poe</el-radio>
    <el-radio label='claude'>Claude</el-radio>
  </el-radio-group><br><br>
  <div>
    <template v-if='type == "bard"'><el-alert type='warning' :closable='false' show-icon>Bard 目前仅允许美国的 IP 访问，所以你很有可能需要设置代理。</el-alert><br></template>
    <template v-else-if='type == "yiyan"'><el-alert type='warning' :closable='false' show-icon>请注意：该方法有封号风险(但是过一段时间就会解封)，具体原因未知，请自行取舍。</el-alert><br></template>
    <el-form :model='openai' v-if='type == "openai"'>
      <el-form-item label='接入模式'>
        <el-radio-group v-model='openai.mode'>
          <el-radio-button label='web'>网页版</el-radio-button>
          <el-radio-button label='api'>API版</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <template v-if='openai.mode == "web"'>
        <el-form-item label='Token'><el-input placeholder='ey********' v-model='openai.accounts.access_token' /></el-form-item>
        <el-form-item label='接入点'><el-input placeholder='网页版 ChatGPT 接入点' v-model='openai.browserless_endpoint' /></el-form-item>
        <el-form-item label='会话标题'><el-input placeholder='qq-{session_id}' v-model='openai.accounts.title_pattern' /></el-form-item>
        <el-form-item label='对话记录自动删除'><el-switch v-model='openai.accounts.auto_remove_old_conversations' /></el-form-item>
      </template>
      <template v-else>
        <el-form-item label='API Key'><el-input placeholder='sk-*****' v-model='openai.accounts.api_key' /></el-form-item>
        <el-form-item label='接入点'><el-input placeholder='API版 ChatGPT 接入点' v-model='openai.api_endpoint' /></el-form-item>
      </template>
      <el-form-item label='Proxy'><el-input placeholder='可选, 留空默认系统设置' v-model='openai.accounts.proxy' /></el-form-item>
      <a href='https://chatgpt-qq.lss233.com/pei-zhi-wen-jian-jiao-cheng/jie-ru-ai-ping-tai/jie-ru-openai-de-chatgpt' target='_blank'>
        <el-link type='primary'>ChatGPT 文档</el-link>
      </a>
    </el-form>
    <el-form :model='bing' v-else-if='type == "bing"'>
      <el-form-item label='Cookie'><el-input type='textarea' placeholder='[{"domain": ".bing.com", ...}]' :autosize="{ minRows: 6, maxRows: 14 }" v-model='bing.accounts.cookie_content' /></el-form-item>
      <el-form-item label='Proxy'><el-input placeholder='可选, 留空默认系统设置或者使用接入点' v-model='bing.accounts.proxy' /></el-form-item>
      <el-form-item label='WebSocket 接入点'><el-input placeholder='https://' v-model='bing.wss_link' /></el-form-item>
      <el-form-item label='会话创建接入点'><el-input placeholder='wss://' v-model='bing.bing_endpoint' /></el-form-item>
      <el-form-item label='显示建议'><el-switch v-model='bing.show_suggestions' /></el-form-item>
      <el-form-item label='显示引用资料'><el-switch v-model='bing.show_references' /></el-form-item>
      <el-form-item label='显示剩余次数'><el-switch v-model='bing.show_remaining_count' /></el-form-item>
      <el-form-item label='Bing 绘图'><el-switch v-model='bing.use_drawing' /></el-form-item>
      <a href='https://chatgpt-qq.lss233.com/pei-zhi-wen-jian-jiao-cheng/jie-ru-ai-ping-tai/jie-ru-new-bing-sydney' target='_blank'>
        <el-link type='primary'>Bing 文档</el-link>
      </a>
    </el-form>
    <el-form :model='bard' v-else-if='type == "bard"'>
      <el-form-item label='Cookie'><el-input placeholder='Bard Cookie' v-model='bard.accounts.cookie_content' /></el-form-item>
      <el-form-item label='Proxy'><el-input placeholder='可选, 留空默认系统设置' v-model='bard.accounts.proxy' /></el-form-item>
      <a href='https://chatgpt-qq.lss233.com/pei-zhi-wen-jian-jiao-cheng/jie-ru-ai-ping-tai/jie-ru-google-bard' target='_blank'>
        <el-link type='primary'>Bard 文档</el-link>
      </a>
    </el-form>
    <el-form :model='yiyan' v-else-if='type == "yiyan"'>
      <el-form-item label='BDUSS'><el-input placeholder='Baidu USS' v-model='yiyan.accounts.BDUSS' /></el-form-item>
      <el-form-item label='BAIDUID'><el-input placeholder='Baidu ID' v-model='yiyan.accounts.BAIDUID' /></el-form-item>
      <el-form-item label='Proxy'><el-input placeholder='可选' v-model='yiyan.accounts.proxy' /></el-form-item>
      <a href='https://chatgpt-qq.lss233.com/pei-zhi-wen-jian-jiao-cheng/jie-ru-ai-ping-tai/jie-ru-wen-xin-yi-yan' target='_blank'>
        <el-link type='primary'>文心一言 文档</el-link>
      </a>
    </el-form>
    <el-form :model='chatglm' v-else-if='type == "chatglm"'>
      <el-form-item label='接入点'><el-input placeholder='ChatGLM 接口地址' v-model='chatglm.accounts.api_endpoint' /></el-form-item>
      <el-form-item label='单会话最大轮数'><el-input-number placeholder='最大记忆的对话轮数 (ContextWindow大小)' v-model='chatglm.accounts.max_turns' /></el-form-item>
      <el-form-item label='请求超时时间 (s)'><el-input-number placeholder='可选' v-model='chatglm.accounts.timeout' /></el-form-item>
      <a href='https://chatgpt-qq.lss233.com/pei-zhi-wen-jian-jiao-cheng/jie-ru-ai-ping-tai/jie-ru-chatglm' target='_blank'>
        <el-link type='primary'>ChatGLM 文档</el-link>
      </a>
    </el-form>
    <el-form :model='poe' v-else-if='type == "poe"'>
      <el-form-item label='p_b'><el-input placeholder='Cookie中的 p_b 字段' v-model='poe.accounts.p_b' /></el-form-item>
      <el-form-item label='Proxy'><el-input placeholder='可选, 留空默认系统设置' v-model='poe.accounts.proxy' /></el-form-item>
      <a href='https://chatgpt-qq.lss233.com/pei-zhi-wen-jian-jiao-cheng/jie-ru-ai-ping-tai/jie-ru-poe.com' target='_blank'>
        <el-link type='primary'>Poe 文档</el-link>
      </a>
    </el-form>
    <el-form :model='claude' v-else-if='type == "claude"'>
      <el-form-item label='Channel ID'><el-input placeholder='C0XXXXXX' v-model='claude.accounts.channel_id' /></el-form-item>
      <el-form-item label='Access Token'><el-input placeholder='XXXX' v-model='claude.accounts.access_token' /></el-form-item>
      <el-form-item label='Proxy'><el-input placeholder='可选, 留空默认系统设置' v-model='claude.accounts.proxy' /></el-form-item>
      <a href='https://chatgpt-qq.lss233.com/pei-zhi-wen-jian-jiao-cheng/jie-ru-ai-ping-tai/jie-ru-claude' target='_blank'>
        <el-link type='primary'>Claude 文档</el-link>
      </a>
    </el-form>
    <el-button type='primary' plain class='save-button' @click='submit' :disabled='loader'>保存</el-button>
  </div>
</template>

<style>
@import "@/assets/style/main.css";
</style>
