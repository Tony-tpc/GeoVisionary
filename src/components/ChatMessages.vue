<script setup>
import { computed } from "vue";
import ChatContent from './ChatContent.vue';

const props = defineProps({
  messages: {
    type: Array,
    required: true,
    validator: (value) => {
      return value.every(msg =>
          msg.content && typeof msg.content === 'string' &&
          msg.sender && ['user', 'llm'].includes(msg.sender)
      )
    }
  },
  userConfig: {
    type: Object,
    default: () => ({
      name: 'You',
      bgColor: '#007bff',
      textColor: '#0d0f1a'
    })
  },
  llmConfig: {
    type: Object,
    default: () => ({
      name: 'Assistant',
      bgColor: '#2d2d2d',
      textColor: '#0d0f1a',
      errorColor: '#ff4444',
    })
  },
  showLlmCursor: {
    type: Boolean,
    default: false
  }
});

// 计算最后一个AI消息的索引
const lastLlmIndex = computed(() => {
  for (let i = props.messages.length - 1; i >= 0; i--) {
    if (props.messages[i].sender === 'llm') {
      return i
    }
  }
  return -1
})
</script>

<template>
  <div class="chat-messages-container">
    <div
        v-for="(message, index) in messages"
        :key="index"
        class="message-wrapper"
        :class="[message.sender]"
    >
      <div class="message-bubble">
        <div
            class="username"
            :style="{
            color: message.sender === 'user' ? userConfig.textColor : llmConfig.textColor
          }"
        >
          {{ message.sender === 'user' ? userConfig.name : llmConfig.name }}
        </div>
        <div
            class="content-wrapper"
            :style="{
            backgroundColor: message.sender === 'user' ? userConfig.bgColor : llmConfig.bgColor,
            color: message.sender === 'user' ? userConfig.textColor : llmConfig.textColor
          }"
        >
          <ChatContent
              :content="message.content"
              :index="index"
              :show-cursor="message.sender === 'llm' &&
                        showLlmCursor &&
                        index === lastLlmIndex"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 禁用滚动的同时确保内容扩展 */
.chat-messages-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1rem;
  min-height: 100%;
  overflow-y: visible;
  box-sizing: border-box;
}

.message-wrapper {
  flex: 0 0 auto;
}

.message-wrapper.user {
  margin-left: auto;
  justify-content: flex-end;
}

.message-wrapper.llm {
  justify-content: flex-start;
}

.message-bubble {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: 3rem;
}

.username {
  font-size: 0.8rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  padding: 0 0.5rem;
}

.content-wrapper {
  padding: 0.5rem;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  line-height: 1.6;
}

.message-wrapper.user .content-wrapper {
  border-top-right-radius: 0;
}

.message-wrapper.llm .content-wrapper {
  border-top-left-radius: 0;
}

/* 错误状态样式 */
.message-error {
  border: 1px solid v-bind('llmConfig.errorColor');
  animation: error-shake 0.5s;
}

@keyframes error-shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-3px); }
  75% { transform: translateX(3px); }
}
</style>
