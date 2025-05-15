<template>
  <!-- 历史记录侧边栏 -->
  <div class="history-sidebar" :class="{ visible: isHistoryOpen }">

    <div class="history-list">
      <h3>历史记录</h3>

      <template v-if="HistoryPreview.today?.length">
        <h4>今天</h4>
        <div v-for="item in HistoryPreview.today" :key="item.precursor_id" class="history-item"
             @click="loadHistoryById(item.precursor_id)" :class="{ active: activeHistoryId === item.precursor_id }">
          {{ formatPreview(item.user_msg) }}
          <span class="timestamp">{{ formatTime(item.timestamp) }}</span>
        </div>
      </template>

      <template v-if="HistoryPreview.last7days?.length">
        <h4>近7天</h4>
        <div v-for="item in HistoryPreview.last7days" :key="item.precursor_id" class="history-item"
             @click="loadHistoryById(item.precursor_id)" :class="{ active: activeHistoryId === item.precursor_id }">
          {{ formatPreview(item.user_msg) }}
          <span class="timestamp">{{ formatTime(item.timestamp) }}</span>
        </div>
      </template>

      <template v-if="HistoryPreview.last30days?.length">
        <h4>近30天</h4>
        <div v-for="item in HistoryPreview.last30days" :key="item.precursor_id" class="history-item"
             @click="loadHistoryById(item.precursor_id)" :class="{ active: activeHistoryId === item.precursor_id }">
          {{ formatPreview(item.user_msg) }}
          <span class="timestamp">{{ formatTime(item.timestamp) }}</span>
        </div>
      </template>

      <template v-if="HistoryPreview.earlier?.length">
        <h4>更早</h4>
        <div v-for="item in HistoryPreview.earlier" :key="item.precursor_id" class="history-item"
             @click="loadHistoryById(item.precursor_id)" :class="{ active: activeHistoryId === item.precursor_id }">
          {{ formatPreview(item.user_msg) }}
          <span class="timestamp">{{ formatTime(item.timestamp) }}</span>
        </div>
      </template>

    </div>
  </div>

  <div class="chat-container">
    <!-- 主聊天区域 -->
    <div class="chat-main">

      <!-- 遮罩层 -->
      <div class="overlay" v-if="isHistoryOpen" @click="toggleHistory"></div>
      <div class="chat-header">
        <button @click="toggleHistory" class="history-toggle-btn">☰</button>
        <h2>地理知识助手</h2>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <!-- 欢迎介绍 -->
        <div class="welcome-message" v-if="messages.length === 0">
          <div class="welcome-card">
            <DomeIcon class="welcome-content" theme="outline" size="48" fill="#0d534b" :strokeWidth="3" />
            <p>您好！我是地理通，我可以：</p>
            <ul>
              <p>📍 解析地理位置坐标</p>
              <p>🗺️ 解释地理特征与人文信息</p>
              <p>📌 提供行政区划详细信息</p>
              <p>🌦️ 查询地区气候与环境数据</p>
            </ul>
            <div class="example-questions">
              <ul>
                <p>试试问我：</p>
                <li @click="handleExampleClick('巴黎的经纬度是多少？')">👉 "巴黎的经纬度是多少？"</li>
                <li @click="handleExampleClick('长江流经哪些省份？')">👉 "长江流经哪些省份？"</li>
                <li @click="handleExampleClick('东京的气候特点是什么？')">👉 "东京的气候特点是什么？"</li>
              </ul>
            </div>
          </div>
        </div>

        <div v-for="(msg, index) in messages" :key="index"
             :class="['message', msg.role, { 'streaming': isStreaming && index === messages.length - 1 }]">
          <div class="message-header">
            <span v-if="msg.role === 'user'">我</span>
            <span v-else>AI助手</span>
          </div>
          <!-- 思维链区域 -->
          <div class="reasoning-container" v-if="msg.reasoning">
            <div class="reasoning-header" @click="toggleReasoning(index)">
              <span class="toggle-icon">{{ msg.isReasoningExpanded ? '−' : '+' }}</span>
              <span class="toggle-text">推理过程</span>
            </div>
            <transition name="slide">
              <div class="reasoning-content" v-show="msg.isReasoningExpanded" v-html="renderMarkdown(msg.reasoning)">
              </div>
            </transition>
          </div>

          <!-- text -->
          <div class="message-content" :key="msg.content + updateFlag"
               v-html="renderMarkdown(msg.displayContent || msg.content)">
          </div>


          <div v-if="isStreaming && index === messages.length - 1" class="typing-indicator">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
        </div>
      </div>


      <div class="input-area">
        <div class="chat-control-area" :class="chatControlClass">

          <!-- 新聊天按钮 -->
          <button class="button" @click="() => RefreshChat()" :disabled="isLoading" @mouseenter="showTooltip('zoom')"
                  @mouseleave="hideTooltip('zoom')">
            <div class="button-box">
              <span class="button-elem">
                <svg viewBox="0 0 46 40" xmlns="http://www.w3.org/2000/svg">
                  <path
                      d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z">
                  </path>
                </svg>
              </span>
              <span class="button-elem">
                <svg viewBox="0 0 46 40">
                  <path
                      d="M46 20.038c0-.7-.3-1.5-.8-2.1l-16-17c-1.1-1-3.2-1.4-4.4-.3-1.2 1.1-1.2 3.3 0 4.4l11.3 11.9H3c-1.7 0-3 1.3-3 3s1.3 3 3 3h33.1l-11.3 11.9c-1 1-1.2 3.3 0 4.4 1.2 1.1 3.3.8 4.4-.3l16-17c.5-.5.8-1.1.8-1.9z">
                  </path>
                </svg>
              </span>
            </div>
          </button>

          <!-- 输入框 -->
          <textarea v-model="inputText" @keydown.enter.exact.prevent="() => sendMessage()"
                    placeholder="输入地理位置问题，例如：巴黎的经纬度是多少？..." :disabled="isLoading" />

          <!-- 发送按钮 -->
          <button @click="() => sendMessage()" :disabled="isLoading">
            <span v-if="isLoading">发送中...</span>
            <span v-else>发送</span>
          </button>
          <div class="tooltips">
            <div class="zoom-tooltip" :ref="(el) => tooltips.zoom = el">回到主页</div>
            <div class="refresh-tooltip" :ref="(el) => tooltips.refresh = el">重置输出框</div>
            <div class="convenient-tooltip" :ref="(el) => tooltips.convenient = el">
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, nextTick, onMounted, onUnmounted, computed } from 'vue'
import { marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import { Dome as DomeIcon } from "@icon-park/vue-next"
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { userState, setUser } from '@/store/userStore'


onMounted(() => {
  getHistoryPreview()
})

gsap.registerPlugin(ScrollTrigger)

const props = defineProps({
  worldContent: {
    type: String,
    required: true
  }
})

/**
 * @description 变量说明
 */
// 配置后端地址
const WS_URL = 'ws://localhost:8040/ws/chat/'
// 响应式数据
const isConnecting = ref(false)
const reconnectAttempts = ref(0)
const MAX_RECONNECT_ATTEMPTS = 3
const messages = reactive([])
const inputText = ref('')
const isLoading = ref(false)
const isStreaming = ref(false)
const messagesContainer = ref(null)
const isHistoryOpen = ref(false)
const HistoryPreview = ref([])
const coordinates = ref([])
const updateFlag = ref(0)
const isOldchat = ref(0)
const hasInput = computed(() => inputText.value.trim() !== '')
const activeHistoryId = ref('')



/**
 * @description 历史记录相关
 */
const getHistoryPreview = async () => {
  const ws = new WebSocket(WS_URL)
  ws.onopen = () => {
    try {
      if (JSON.parse(localStorage.getItem('isApiavailable'))) {
        const payload = {
          user_id: userState?.user?.user_id || null,
          task: "get_preview",
          source: "world_map"
        }
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify(payload))
        } else {
          console.error('WebSocket is not open')
        }
      }
      else {
        console.log("API不可用")
      }
    } catch (error) {
      console.error('请求失败:', error)
      ws.close();
    } finally {
      // extractCoordinates(assistantMessage.content)
    }
  }
  ws.onmessage = (event) => {
    HistoryPreview.value = reactive(JSON.parse(event.data))
    console.log(HistoryPreview.value);
    HistoryPreview.value = groupHistoryByTime()
    console.log(HistoryPreview.value);
    ws.close();
  }
}

const formatPreview = (msg) => {
  return msg.length > 20 ? msg.slice(0, 20) + '...' : msg;
};
const formatTime = (timestamp) => {
  const date = new Date(timestamp.replace(/-/g, '/'));
  date.setHours(date.getHours() + 8); // 修正时区

  const now = new Date();
  const pad = (n) => n.toString().padStart(2, '0');

  const isToday = date.toDateString() === now.toDateString();
  const isThisYear = date.getFullYear() === now.getFullYear();

  if (isToday) {
    return `${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
  } else if (isThisYear) {
    return `${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
  } else {
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
  }
};

const toggleHistory = () => {
  isHistoryOpen.value = !isHistoryOpen.value
}

const tooltips = reactive({});
// 按钮信息提示（悬停触发）
// 显示 tooltip
const showTooltip = (key) => {
  if (!tooltips[key]) return;
  gsap.to(tooltips[key], {
    opacity: 1,
    duration: 0.2,
  });
};
// 隐藏 tooltip
const hideTooltip = (key) => {
  if (!tooltips[key]) return;
  gsap.to(tooltips[key], {
    opacity: 0,
    duration: 0.3,
  });
};

const groupHistoryByTime = () => {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const oneDay = 24 * 60 * 60 * 1000;

  const result = {
    today: [],
    last7days: [],
    last30days: [],
    earlier: [],
  };

  HistoryPreview.value.preview?.forEach(item => {
    const itemDate = new Date(item.timestamp.replace(/-/g, '/'));
    itemDate.setHours(itemDate.getHours() + 8);
    const diffDays = Math.floor((itemDate - today) / oneDay);
    if (diffDays === 0) {
      result.today.push(item);
    } else if (diffDays >= -6) {
      result.last7days.push(item);
    } else if (diffDays >= -29) {
      result.last30days.push(item);
    } else {
      result.earlier.push(item);
    }
  });

  const sortByTimestampDesc = (a, b) => new Date(b.timestamp) - new Date(a.timestamp);
  result.today.sort(sortByTimestampDesc);
  result.last7days.sort(sortByTimestampDesc);
  result.last30days.sort(sortByTimestampDesc);
  result.earlier.sort(sortByTimestampDesc);
  return result;
};


const loadHistoryById = async (id) => {
  activeHistoryId.value = id;
  const ws = new WebSocket(WS_URL)
  ws.onopen = () => {
    try {
      if (JSON.parse(localStorage.getItem('isApiavailable'))) {
        const payload = {
          user_id: userState?.user?.user_id || null,
          task: "get_full_history",
          precursor_id: id,
        }
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify(payload))
        } else {
          console.error('WebSocket is not open')
        }
      }
      else {
        console.log("API不可用")
      }
    } catch (error) {
      console.error('请求失败:', error)
      ws.close();
    } finally {
    }
  }
  ws.onmessage = (event) => {
    const newMessages = JSON.parse(event.data).history;
    isOldchat.value = JSON.parse(event.data).isOldchat
    console.log(isOldchat.value);
    messages.splice(0, messages.length, ...newMessages);
    ws.close();
    toggleHistory();
  }
}

/**
 * @description 聊天记录相关
 */
// Markdown 配置
marked.setOptions({
  highlight: (code, lang) => {
    const language = hljs.getLanguage(lang) ? lang : 'plaintext'
    return hljs.highlight(code, { language }).value
  },
})
// 消息发送逻辑
const sendMessage = async (latitude = null, longitude = null) => {
  const ws = new WebSocket(WS_URL)
  var startcontent = false
  var Requireregion = false
  var question = ""
  var Showquestion = ""
  if (latitude && longitude) // 存在经纬度
  {
    Requireregion = true
    question = {
      "type": "latlng",
      "lat": latitude,
      "lng": longitude
    }
    Showquestion = `请告诉我纬度${latitude}，经度${longitude}的信息`
  }
  else {
    question = {
      "type": "text",
      "text": inputText.value.trim(),
    }
    Showquestion = inputText.value.trim()
  }
  if (!question || isLoading.value) return

  isLoading.value = true
  isStreaming.value = true
  // 添加用户消息
  messages.push({
    role: 'user',
    displayContent: Showquestion, // 显示内容
    actualContent: question // 实际发送内容
  });
  // 创建助理消息占位
  const assistantMessage = { role: 'assistant', content: '', reasoning: '', isReasoningExpanded: true }

  watch(messages, () => {
    scrollToBottom();
  });
  ws.onopen = () => {
    try {
      if (JSON.parse(localStorage.getItem("isApiavailable"))) {
        messages.push(assistantMessage)
        // 构造WebSocket消息
        const payload = {
          user_id: userState?.user?.user_id || null,
          message: question,
          isOldchat: isOldchat.value,
          source: "world_map"
        }
        // 消息发送
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify(payload))
          isOldchat.value = 0
        } else {
          console.error('WebSocket is not open')
        }
      }
      else {
        isLoading.value = false
        isStreaming.value = false
        ws.close();
        messages.push({
          role: 'system',
          content: `请求错误: 未登录的用户`
        })
      }
      console.log(userState.user);

      if (!userState.user) {
        localStorage.setItem("isApiavailable", false);
      }
      isOldchat.value = 0
    } catch (error) {
      console.error('请求失败:', error)
      isLoading.value = false
      isStreaming.value = false
      ws.close();
      messages.push({
        role: 'system',
        content: `请求错误: ${error.message}`
      })
    } finally {
      // 仅当是输入框提交时才清空
      if (!latitude) inputText.value = ''

      // extractCoordinates(assistantMessage.content)
    }
  }

  ws.onmessage = (event) => {
    const chunk = JSON.parse(event.data);
    console.log(chunk);
    if (chunk.content) {
      if (!startcontent) {
        assistantMessage.isReasoningExpanded = false;
        startcontent = true
      }
      assistantMessage.content += chunk.content
      updateFlag.value++ // 触发内容更新
    }
    if (chunk.reasoning) {
      assistantMessage.reasoning += chunk.reasoning
      updateFlag.value++ // 触发推理更新
    }
    if (chunk.completed) {
      isLoading.value = false
      isStreaming.value = false
      if (!isOldchat.value) {
        getHistoryPreview()
      }
      isOldchat.value = chunk.session_id
      ws.close();
      if (!userState.user) {
        localStorage.setItem("isApiavailable", false);
      }
    }
  }

  ws.onerror = (error) => {
    // 将错误输出到内容中
    console.error('WebSocket 错误:', error);
    isLoading.value = false
    isStreaming.value = false
    messages.push({
      role: 'system',
      content: `好像发生错误了呢，再试一次吧`
    })
    ws.close();
  };
}
/**
 * @description 页面控制相关
 */

const onInput = () => {
}

const chatControlClass = computed(() => {
  if (isOldchat.value && !hasInput.value) {
    return 'slide-right' // 展示新聊天按钮
  } else {
    return 'slide-left'  // 展示发送按钮
  }
})
// 添加折叠切换方法
const toggleReasoning = (index) => {
  messages[index].isReasoningExpanded = !messages[index].isReasoningExpanded
}
// 坐标提取逻辑
const extractCoordinates = (content) => {
  const coordinatePattern = /\[(-?\d+\.\d+),\s*(-?\d+\.\d+)\]/g
  const matches = [...content.matchAll(coordinatePattern)]

  coordinates.value = matches.map(match => ({
    lat: parseFloat(match[1]),
    lng: parseFloat(match[2])
  }))
}

const handleExampleClick = (example) => {
  if (isLoading.value) return;

  // 清理问题中的引导符号
  const cleanedQuestion = example.replace(/^["“”]|["“”]$/g, '');
  inputText.value = cleanedQuestion;
  sendMessage();
};

// 通用功能
const renderMarkdown = (content) => marked(content)

const RefreshChat = () => {
  isOldchat.value = 0
  messages.splice(0, messages.length)
}
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTo({
        top: messagesContainer.value.scrollHeight,
        behavior: 'smooth'
      })
    }
  })
}


// 暴露增强后的方法
defineExpose({
  sendMessage,
  clearChat: () => messages.splice(0, messages.length)
});
</script>

<style scoped>
/* 优化后的样式 */
.chat-container {
  --primary-color: #2c3e50;
  --assistant-bg: #fffbf2;
  --user-bg: #d3e0d1;
  --streaming-bg: #f3f4ff;
  flex-direction: column;
  height: 100vh;
  display: flex;
}

.overlay {
  position: absolute;
  /* 改成相对于 .chat-main */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  z-index: 10;
}

/* 历史记录侧边栏 */
.history-sidebar {
  position: absolute;
  top: 0;
  right: 0;
  width: 280px;
  height: 100%;
  background: #fff;
  transform: translateX(100%);
  transition: transform 0.3s ease-in-out;
  z-index: 20;
  box-shadow: -4px 0 8px rgba(0, 0, 0, 0.2);
  color: #000000;
  overflow-y: auto;
}

.history-sidebar.visible {
  transform: translateX(0);
}

.history-list {
  padding: 10px;

  max-height: 100vh;
}

.history-item {
  padding: 12px;
  margin: 8px 0;
  border-radius: 8px;
  background: #f5f5f5;
  cursor: pointer;
  transition: all 0.2s;
}

.history-item:hover {
  background: #ececec;
}

.history-item.active {
  background: #d8d8d8;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: linear-gradient(180deg, #FFFFFF 0%, #F6F7F9 100%);
  transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
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
  padding: 20px;
  overflow-y: auto;
  background: #fcfbf9;
  padding-bottom: 60px;
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
  padding: 16px;
  border-radius: 12px;
  max-width: 75%;
  animation: messageAppear 0.3s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.message.user {
  background: var(--user-bg);
  margin-left: auto;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  color: #000000;
}

.message.assistant {
  background: var(--assistant-bg);
  margin-right: auto;
  color: #000000;
}

.message.system {
  background: var(--assistant-bg);
  margin-right: auto;
  color: #ff0000;
}

.message.streaming {
  background: var(--streaming-bg);
  position: relative;
  color: #000000;
}

.message-content {
  line-height: 1.6;
  font-size: 15px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  padding: 8px 0;
}

.dot {
  width: 6px;
  height: 6px;
  margin: 0 3px;
  background: #666;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.dot:nth-child(2) {
  animation-delay: 0.2s
}

.dot:nth-child(3) {
  animation-delay: 0.4s
}

.input-area {
  position: sticky;
  bottom: 0;
  display: flex;
  gap: 15px;
  background: #fff;
  padding: 16px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.03);
}

textarea {
  flex: 1;
  padding: 12px 10px;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  min-height: 48px;
  max-height: 120px;
  font-size: 16px;
  line-height: 1.5;
  background: #f8f9fa;
  transition: all 0.2s;
  width: 260px;
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
  gap: 4px;
  min-height: 48px;
}

button:active {
  transform: scale(0.96);
}

button::before {
  content: "➤";
  font-size: 14px;
}

.chat-control-area {
  display: flex;
  align-items: center;
  gap: 20px;
  width: 300%;
  /* 让滑动区域能左右偏移 */
  transition: transform 0.4s ease;
}

/* 滑动到左侧，露出“发送按钮” */
.chat-control-area.slide-left {
  transform: translateX(-20.33%);
}

/* 滑动到右侧，露出“新聊天按钮” */
.chat-control-area.slide-right {
  transform: translateX(0%);
}


.reasoning-container {
  margin: 8px 0;
  border: 1px solid #eee;
  border-radius: 6px;
  overflow: hidden;
}

.reasoning-header {
  padding: 6px 12px;
  background-color: #f8f9fa;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: background-color 0.2s;
}

.reasoning-header:hover {
  background-color: #f1f3f5;
}

.toggle-icon {
  font-size: 14px;
  width: 20px;
  color: #666;
  transition: transform 0.2s;
}

.toggle-text {
  color: #666;
  font-size: 0.9em;
}

.reasoning-content {
  padding: 10px 12px;
  font-style: italic;
  color: #666;
  line-height: 1.5;
  background: white;
  border-top: 1px solid #eee;
  font-size: 0.9em;
  white-space: pre-wrap;
  word-break: break-word;
}

/* 添加折叠动画 */
.reasoning-content {
  transition: all 0.3s ease;
  max-height: 400px;
  overflow-y: scroll;
}

/* 展开状态 */
.reasoning-content[v-show="true"] {
  max-height: 800px;
  /* 根据实际内容调整 */
  padding: 10px 12px;
}

/* 过渡动画 */
.slide-enter-active,
.slide-leave-active {
  transition: max-height 0.3s ease, padding 0.3s ease;
}

@keyframes messageAppear {
  from {
    opacity: 0;
    transform: translateY(10px);
  }

  to {
    opacity: 1;
    transform: none;
  }
}

@keyframes typing {

  0%,
  60%,
  100% {
    transform: translateY(0)
  }

  30% {
    transform: translateY(-4px)
  }
}

.chat-messages {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.embedded-welcome {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 160px);
  padding: 20px;
}

.welcome-content {
  max-width: 680px;
  width: 100%;

}

.welcome-card {
  background: rgba(255, 255, 255, 0.98);
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(0, 0, 0, 0.05);
  animation: slideUp 0.6s ease-out;
}

.welcome-content h2 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 24px;
  font-size: 1.8em;
}

.welcome-card p {
  color: #34495e;
  line-height: 1.6;
  margin: 16px 0;
  font-size: 1.1em;
}

.welcome-card ul {
  margin: 24px 0;
  padding: 0;
  list-style: none;
}

.welcome-card li {
  padding: 12px 24px;
  margin: 8px 0;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  transition: transform 0.2s ease;
}

.welcome-card li:hover {
  transform: translateX(8px);
}

.icon {
  font-size: 1.2em;
  margin-right: 12px;
  min-width: 32px;
  text-align: center;
}

.examples {
  margin-top: 32px;
  border-top: 1px solid #eee;
  padding-top: 24px;
}

.examples p {
  color: #7f8c8d;
  margin-bottom: 16px;
}

.example-bubble {
  padding: 12px 20px;
  margin: 8px 0;
  background: #f1f3f5;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.example-bubble:hover {
  background: #e9ecef;
  transform: scale(1.02);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: none;
  }
}

/* 添加点击效果 */
.example-questions li {
  cursor: pointer;
  transition: all 0.2s ease;
  padding: 8px 16px;
  border-radius: 20px;
  margin: 6px 0;
}

.example-questions li:hover {
  background: #f0f2f5;
  transform: translateX(4px);
}

/* 为正在加载时添加禁用状态 */
.example-questions li.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* From Uiverse.io by xopc333 */
.button {
  display: block;
  position: relative;
  width: 56px;
  height: 56px;
  margin: 0;
  overflow: hidden;
  outline: none;
  background-color: transparent;
  cursor: pointer;
  border: 0;
  margin-left: 10px;
}

.button:before,
.button:after {
  content: "";
  position: absolute;
  border-radius: 50%;
  inset: 7px;
}

.button:before {
  border: 4px solid #19998a;
  transition: opacity 0.4s cubic-bezier(0.77, 0, 0.175, 1) 80ms,
  transform 0.5s cubic-bezier(0.455, 0.03, 0.515, 0.955) 80ms;
}

.button:after {
  border: 4px solid #026055;
  transform: scale(1.3);
  transition: opacity 0.4s cubic-bezier(0.165, 0.84, 0.44, 1),
  transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  opacity: 0;
}

.button:hover:before,
.button:focus:before {
  opacity: 0;
  transform: scale(0.7);
  transition: opacity 0.4s cubic-bezier(0.165, 0.84, 0.44, 1),
  transform 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.button:hover:after,
.button:focus:after {
  opacity: 1;
  transform: scale(1);
  transition: opacity 0.4s cubic-bezier(0.77, 0, 0.175, 1) 80ms,
  transform 0.5s cubic-bezier(0.455, 0.03, 0.515, 0.955) 80ms;
}

.button-box {
  display: flex;
  position: absolute;
  top: 0;
  left: 0;
}

.button-elem {
  display: block;
  width: 20px;
  height: 20px;
  margin: 17px 18px 0 18px;
  transform: rotate(180deg);
  fill: #0d534b;
}

.button:hover .button-box,
.button:focus .button-box {
  transition: 0.4s;
  transform: translateX(-56px);
}

/* 悬停提示文字 */
.refresh-tooltip,
.zoom-tooltip,
.convenient-tooltip {
  position: fixed;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 8px 10px;
  border-radius: 4px;
  pointer-events: none;
  opacity: 0;
  right: 84%;
  z-index: 102;
  width: 60px;
}

.refresh-tooltip {
  bottom: 80%;
}

.zoom-tooltip {
  bottom: 82%;
}

.convenient-tooltip {
  top: 10%;
  right: 2.5%;
}
</style>
