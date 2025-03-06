<script setup>
import { ref } from 'vue';
import {userState} from "@/store/userStore.js";

const text = ref('');
const audioUrl = ref('');
const loading = ref(false);
let ws = null;

const isGenerating = ref(false); // 控制加载状态
const conversation = ref([  { sender: 'llm', content: '您好呀，我是您的专属AI助教，请问有什么可以帮到您？' },]); // 对话记录
const streamingMessageRef = ref(null); // 当前流式消息的引用

const chatHistory = ref([
  { role: "system", content: "你是一位经验丰富的高中地理老师，你的学生目前遇到了一些地理问题，你需要耐心地帮助他解决问题，并通俗易懂地讲解。记住，你只能用中文思考和回答。如果他输入的是其他方面的问题，也请像个老师一样耐心教导他。" }
]);

function generateSpeech() {
  if (!text.value) {
    alert('请输入文本内容');
    return;
  }
  loading.value = true;
  audioUrl.value = '';
  const userMessage = { role: "user", content: text.value };
  chatHistory.value.push(userMessage);
  conversation.value.push({ // 同时添加到对话列表
    sender: 'user',
    content: text.value,
  });
  // 创建并添加流式消息占位符
  const streamMessage = {
    sender: 'llm',
    content: '',
    isStreaming: true
  };
  conversation.value.push(streamMessage);
  streamingMessageRef.value = streamMessage; // 保存当前流式消息引用

  // 这里改成你的 Django 后端地址
  ws = new WebSocket('ws://127.0.0.1:8040/ws/tts/');

  ws.onopen = () => {
    console.log('WebSocket 连接已建立');
    // 发送文本内容给后端
    ws.send(JSON.stringify({ text: text.value, messages: chatHistory.value}));
  };

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data); // 先解析 JSON
    if (data.type === 'audio') {
      const base64Audio = data.content;

      try {
        const byteString = atob(base64Audio); // 解码 Base64
        const uint8Array = new Uint8Array(byteString.length);

        for (let i = 0; i < byteString.length; i++) {
          uint8Array[i] = byteString.charCodeAt(i);
        }

        const audioBlob = new Blob([uint8Array], { type: 'audio/wav' });
        audioUrl.value = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        audio.play();
        console.log("音频生成成功");
      } catch (e) {
        console.error("Base64 解码失败:", e);
      }
    }
    if (data.type === 'text') {
      console.log(data.content);
      if (data.content === "[DONE]") {
        console.log("流式结束");
        ws.close(); // 停止流式读取
      }
      streamingMessageRef.value.content += data.content;
    }
  };

  ws.onerror = (error) => {
    console.error('WebSocket 错误:', error);
    alert('生成失败，请检查服务是否正常运行');
    loading.value = false;
  };

  ws.onclose = () => {
    console.log('WebSocket 连接已关闭');
    loading.value = false;
  };
}
</script>

<template>
  <div class="tts-container">
    <h2>CosyVoice 测试</h2>
    <textarea v-model="text" placeholder="请输入文本"></textarea>
    <button @click="generateSpeech" :disabled="loading">生成语音</button>

    <audio v-if="audioUrl" :src="audioUrl" controls></audio>
    <p v-if="loading">音频生成中，请稍等...</p>
  </div>
  <!--  输出区域  -->
  <div class="outputArea" ref="outputAreaRef">
    <ChatMessages
        :messages="conversation"
        :user-config="{
                name: `${userState.user? userState.user.username : '用户'}`,
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
</template>

<style scoped>
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
</style>
