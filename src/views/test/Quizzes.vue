<script setup>
import { ref } from 'vue';
import { userState } from "@/store/userStore.js";

const text = ref('');
const audioQueue = ref([]); // 音频缓存区
let isPlaying = false; // 控制音频播放
const loading = ref(false);
const conversation = ref([
  { sender: 'llm', content: '您好呀，我是您的专属AI助教，请问有什么可以帮到您？' }
]);
const chatHistory = ref([
  { role: "system", content: "你是一位经验丰富的高中地理老师，你的学生目前遇到了一些地理问题，你需要耐心地帮助他解决问题，并通俗易懂地讲解。记住，你只能用中文思考和回答。如果他输入的是其他方面的问题，也请像个老师一样耐心教导他。" }
]);
let ws = null;

const streamingMessageRef = ref(null);
const summaryRef = ref(null);
const isGenerating = ref(false);
const thinkingContent = ref('');

const typeEffect = async () => {
  summaryRef.value.innerHTML = '';

  for (let i = 0; i < thinkingContent.value.length; i++) {
    summaryRef.value.innerHTML += thinkingContent.value[i];
    await new Promise(resolve => setTimeout(resolve, 250)); // 等待 250ms 再继续
  }
}

let isThinkingActive = false; // 标志变量，防止重复执行
const waitForThinking = async () => {
  let i = 0;
  const timeout = 500;
  isThinkingActive = true;  // 标记动画开始

  while(!thinkingContent.value && isThinkingActive) {
    if (i % 4 === 0) {
      summaryRef.value.innerHTML = '思考中';
    } else {
      summaryRef.value.innerHTML += '.';
    }
    await new Promise(resolve => setTimeout(resolve, timeout));
    i++;
  }
}

const generateSpeech = () => {
  if (!text.value) {
    alert('请输入文本内容');
    return;
  }

  loading.value = true;
  const userMessage = { role: "user", content: text.value };
  chatHistory.value.push(userMessage);
  conversation.value.push({ sender: 'user', content: text.value });

  const streamMessage = { sender: 'llm', content: '', isStreaming: true };
  conversation.value.push(streamMessage);
  streamingMessageRef.value = streamMessage;

  ws = new WebSocket('ws://127.0.0.1:8040/ws/tts/');
  thinkingContent.value = '';
  waitForThinking();

  ws.onopen = () => {
    console.log("WebSocket 连接已建立");
    isThinkingActive = true;  // 允许动画运行
    ws.send(JSON.stringify({ text: text.value, messages: chatHistory.value }));
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.type === 'text') {
      if (data.content === "[DONE]") {
        console.log("流式结束");
        ws.close();
      }
      streamingMessageRef.value.content += data.content;
    }

    if (data.type === 'summary') {
      console.log("📌 概括内容:", data.content);

      if (!thinkingContent.value) {
        thinkingContent.value = data.content;
        typeEffect();  // 调用异步打字机效果
      }

      if (data.audio) {
        audioQueue.value.push(base64ToAudioUrl(data.audio));
        playAudioQueue();
      }
    }

    if (data.type === 'audio') {
      console.log("🔊 主音频已忽略（仅概括生成音频）");
    }
  };

  ws.onerror = (error) => {
    console.error('WebSocket 错误:', error);
    alert('生成失败，请检查服务是否正常运行');
    isThinkingActive = false;  // 停止动画
    loading.value = false;
  };

  ws.onclose = () => {
    console.log('WebSocket 连接已关闭');
    isThinkingActive = false;  // 停止动画
    loading.value = false;
  };
}

function base64ToAudioUrl(base64) {
  const byteString = atob(base64);
  const uint8Array = new Uint8Array(byteString.length);
  for (let i = 0; i < byteString.length; i++) {
    uint8Array[i] = byteString.charCodeAt(i);
  }
  const audioBlob = new Blob([uint8Array], { type: 'audio/wav' });
  return URL.createObjectURL(audioBlob);
}

function playAudioQueue() {
  if (isPlaying || audioQueue.value.length === 0) return;
  isPlaying = true;

  const audio = new Audio(audioQueue.value.shift());
  audio.onended = () => {
    isPlaying = false;
    playAudioQueue();
  };
  audio.play();
}
</script>

<template>
  <div class="tts-container">
    <h2>CosyVoice 测试</h2>
    <textarea v-model="text" placeholder="请输入文本"></textarea>
    <button @click="generateSpeech" :disabled="loading">
      {{ loading ? "生成中..." : "生成语音" }}
    </button>
  </div>

  <div class="outputArea">
    <ChatMessages
        :messages="conversation"
        :user-config="{
          name: `${userState.user ? userState.user.username : '用户'}`,
          bgColor: '#d3e0d1',
          textColor: '#fffdf3'
        }"
        :llm-config="{
          name: 'AI助教',
          bgColor: '#f7f2eb',
          textColor: '#fffdf3',
          errorColor: '#ff4444'
        }"
        :show-llm-cursor="isGenerating"
    />
  </div>

  <div class="summary-output" ref="summaryRef">你好呀，我是小春</div>
</template>


<style scoped>
/* @import url('https://fonts.googleapis.com/css2?family=ZCOOL+XiaoWei&display=swap'); /* 可爱中文字体 */
@import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');

.tts-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

textarea {
  width: 400px;
  height: 100px;
  padding: 10px;
}

button {
  padding: 10px 20px;
  background: #0d534b;
  color: white;
  border: none;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
}

.summary-output {
  position: fixed;
  bottom: 50%;
  right: 10%;
  z-index: 103;
  letter-spacing: 1px;
  background: linear-gradient(135deg, #fffdf3, #ffebcd); /* 柔和渐变背景 */
  color: #4b3f3f;
  font-family: 'ZCOOL KuaiLe', sans-serif;
  font-size: 18px;
  padding: 14px 22px;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  max-width: 300px;
  word-wrap: break-word;
  animation: fadeInUp 0.5s ease-out;
  transition: all 0.3s ease-in-out;
}

/* 🎀 气泡底部的小圆点模拟云朵 */
.summary-output::before,
.summary-output::after {
  content: "";
  position: absolute;
  bottom: -10px; /* 让装饰元素位于文本框下方 */
  background: #ffebcd;
  border-radius: 50%;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* 🎈 左侧小圆 */
.summary-output::before {
  width: 18px;
  height: 18px;
  right: 2%; /* 控制偏移 */
  bottom: -50px;
}

/* 🎈 右侧大圆 */
.summary-output::after {
  width: 25px;
  height: 25px;
  right: 20px; /* 控制偏移 */
  bottom: -30px;
}
</style>
