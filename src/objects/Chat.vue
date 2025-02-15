<template>
  <div class="chat-container">
    <!-- 历史记录侧边栏 -->
    <div class="history-sidebar" :class="{ 'visible': isHistoryOpen }">
      <div class="history-header">
        <h3>历史记录</h3>
        <button @click="toggleHistory">×</button>
      </div>
      <div class="history-list">
        <!-- 历史记录内容 -->
      </div>
    </div>

    <!-- 主聊天区域 -->
    <div class="chat-main">
      <div class="chat-header">
        <button @click="toggleHistory" class="history-toggle-btn">☰</button>
        <h2>Chat with AI</h2>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
          <div v-html="renderMarkdown(msg.content)" class="message-content"></div>
        </div>
      </div>

      <div class="input-area">
        <textarea v-model="inputText" @keydown.enter.exact.prevent="sendMessage" placeholder="输入你的消息..." />
        <button @click="sendMessage" :disabled="isLoading">
          {{ isLoading ? '发送中...' : '发送' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted, nextTick, toRaw } from 'vue'
import CryptoJS from 'crypto-js'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

// 配置参数
const API_KEY = import.meta.env.VITE_API_KEY
const API_SECRET = import.meta.env.VITE_API_SECRET
const APPID = import.meta.env.VITE_APP_APPID
const HOST = 'spark-api.xf-yun.com'
const PATH = '/v4.0/chat'

// 数据
const messages = reactive([])
const inputText = ref('')
const isLoading = ref(false)
const props = defineProps(['messages'])
const messagesContainer = ref(null)
const ws = ref(null)
const isHistoryOpen = ref(false)
const chatHistory = ref(JSON.parse(localStorage.getItem('chatHistory')) || [])
const coordinates = ref([])
// 初始化 Markdown 渲染器
marked.setOptions({
  highlight: (code, lang) => {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext'
    return hljs.highlight(code, { language }).value
  },
})

// 渲染 Markdown
const renderMarkdown = (content) => {
  return marked(content)
}

// 生成鉴权 URL
const generateAuthUrl = () => {
  const date = new Date().toUTCString()
  const signature_origin = `host: ${HOST}\ndate: ${date}\nGET ${PATH} HTTP/1.1`
  const signature_sha = CryptoJS.HmacSHA256(signature_origin, API_SECRET)
  const signature = CryptoJS.enc.Base64.stringify(signature_sha)
  const authorization_origin = `api_key="${API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="${signature}"`
  const authorization = btoa(authorization_origin)
  return `wss://${HOST}${PATH}?authorization=${authorization}&date=${date}&host=${HOST}`
}

// 初始化 WebSocket
const initWebSocket = () => {
  const url = generateAuthUrl()
  ws.value = new WebSocket(url)

  ws.value.onopen = () => {
    console.log('WebSocket connected')
  }

  ws.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.header.code !== 0) {
      console.error('Error:', data.header)
      return
    }

    const text = data.payload.choices.text[0].content

    const lastMessage = messages[messages.length - 1]

    if (lastMessage.role === 'assistant') {
      lastMessage.content += text
    } else {

      messages.push({ role: 'assistant', content: text })
    }

    nextTick(() => {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    })

    if (data.header.status === 2) {
      isLoading.value = false
      ws.value.close()
      saveHistory()
      extractCoordinates(...messages.slice(-1).map(msg => ({ role: msg.role, content: msg.content })));

    }
  }

  ws.value.onerror = (error) => {
    console.error('WebSocket error:', error)
    isLoading.value = false
  }
}

// 发送消息
const sendMessage = async () => {
  if (!inputText.value.trim() || isLoading.value) return

  isLoading.value = true
  handleAIResponse(inputText.value)
  const question = inputText.value
  inputText.value = ''
  // extractCoordinates()

}


const handleAIResponse = async (data) => {
  messages.push({ role: 'user', content: data })
  if (!ws.value || ws.value.readyState !== WebSocket.OPEN) {
    initWebSocket()
  }

  await new Promise(resolve => {
    if (ws.value.readyState === WebSocket.OPEN) {
      resolve()
    } else {
      ws.value.addEventListener('open', resolve)
    }
  })

  const requestData = {
    header: {
      app_id: APPID,
      uid: "12345"
    },
    parameter: {
      chat: {
        domain: "4.0Ultra",
        temperature: 0.3,
        max_tokens: 4096
      }
    },
    payload: {
      message: {
        text: [
          ...messages.slice(0, -1).map(msg => ({ role: msg.role, content: msg.content })),
          {
            "role": "system", "content": "你是一个地理小助手，能够根据用户提供的经纬度或地名，极其精确地判断该地位置，返回该地的详细地理信息和人文特点。\
          现在你的面前有一张世界地图，如果用户询问你地形、地名、城市等地理特征在何处时，你可以返回经纬度，其格式为[纬度：float，纬度：float]，不能出现任何在ascii码之外的符号，你可以返回多个地点，但必须详细解释" },
          { role: "user", content: data + "如果用户询问你地形、地名、城市等地理特征在何处时，你可以返回经纬度，其格式为[纬度：float，纬度：float]，必须详细说明该地" },
        ]
      }
    }
  }

  ws.value.send(JSON.stringify(requestData))
  messages.push({ role: 'assistant', content: '' })
  scrollToBottom()


}
// 保存历史记录
const saveHistory = () => {
  const timestamp = new Date().toLocaleString()
  chatHistory.value.push({ timestamp, messages: [...messages] })
  localStorage.setItem('chatHistory', JSON.stringify(chatHistory.value))
}

// 加载历史记录
const loadHistory = (history) => {
  messages.splice(0, messages.length, ...history.messages)
  isHistoryOpen.value = false
}

// 切换历史记录侧边栏
const toggleHistory = () => {
  isHistoryOpen.value = !isHistoryOpen.value
}

// 增强滚动方法
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight + 100;
      // 添加平滑滚动效果
      messagesContainer.value.scrollTo({
        top: messagesContainer.value.scrollHeight,
        behavior: 'smooth'
      });
    }
  });
}

// 匹配经纬度
const extractCoordinates = (msg) => {

  console.log(msg.content);
  const pattern = /纬度\s*([-+]?\d+(?:\.\d+)?)[，,]\s*经度\s*([-+]?\d+(?:\.\d+)?)/g
  const matches = [msg.content.matchAll(pattern)]
  console.log(matches);
  
  var sd = matches.map(match => ({
    lat: parseFloat(match[1]),
    lng: parseFloat(match[2]),
    original: match[0]
  }))
  console.log(sd);

}

// 坐标验证
const isValidCoordinate = (coord) => {
  return Math.abs(coord.lat) <= 90 && Math.abs(coord.lng) <= 180
}
// 监听消息变化自动滚动
watch(() => props.messages, () => {
  nextTick(() => {
    scrollToBottom()
  })
}, { deep: true })

defineExpose({
  handleAIResponse
});


</script>

<style scoped>
.chat-container {
  --primary-color: #6173FF;
  --assistant-bg: #F3F4FF;
  --user-bg: #FFFFFF;
  --border-color: #E4E7ED;
  /* display: flex; */
  flex-direction: column;
  height: 100vh;
}

.history-sidebar {
  width: 300px;
  height: 100vh;
  position: fixed;
  right: -300px;
  top: 0;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  background: #fff;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.15);
}

.history-sidebar.visible {
  transform: translateX(-300px);
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: linear-gradient(180deg, #FFFFFF 0%, #F6F7F9 100%);
  transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-header {
  position: sticky;
  top: 0;
  padding: 12px 16px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  z-index: 10;
}

.chat-header h2 {

  font-size: 18px;
  font-weight: 600;
  color: #1a1a1a;
  margin-left: 12px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 60px;
  /* 给输入框留出空间 */
}

/* 滚动条美化 */
.chat-messages::-webkit-scrollbar {
  width: 4px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #ebeef5;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #409eff;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(97, 115, 255, 0.3);
  border-radius: 2px;
}

.message {
  border-radius: 16px;
  margin: 12px 8px;
  max-width: 88%;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

@keyframes messageAppear {
  to {
    opacity: 1;
    transform: none;
  }
}

.assistant {
  background: var(--assistant-bg);
  border: 1px solid var(--border-color);
}

.user {
  background: var(--user-bg);
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 8px rgba(97, 115, 255, 0.1);
}



.message-content {
  max-width: 450;
  margin: 0 auto;
  width: calc(100% - 32px);
}

.message-content :deep(pre) {
  background: rgba(0, 0, 0, 0.05);
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
}

.message-content :deep(code) {
  font-family: 'SFMono-Regular', Consolas, monospace;
  font-size: 14px;
}


.input-area {
  position: sticky;
  bottom: 0;
  display: flex;
  gap: 12px;
  background: #fff;
  padding: 16px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.03);
}

textarea {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid #e5e5e5;
  border-radius: 24px;
  min-height: 48px;
  max-height: 120px;
  font-size: 16px;
  line-height: 1.5;
  background: #f8f9fa;
  transition: all 0.2s;
}

textarea:focus {
  background: #fff;
  border-color: #0d534b;
  outline: none;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

button {
  padding: 10px 16px;
  background: #0d534b;
  color: white;
  border: none;
  border-radius: 24px;
  font-weight: 500;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}

button:active {
  transform: scale(0.96);
}

button::before {
  content: "➤";
  font-size: 14px;
}

@media (max-width: 768px) {
  .chat-header {
    padding: 12px;
  }

  .message {
    max-width: 90%;
    padding: 10px 14px;
  }

  .message-content {
    font-size: 15px;
  }

  .input-area {
    padding: 12px;
  }

  textarea {
    font-size: 15px;
    padding: 10px 14px;
  }
}
</style>