<script setup>
import { ref } from 'vue'
import {Close} from "@element-plus/icons-vue";
const props = defineProps({
  input: {
    type: String,
    default: '',
  },
  bottom: {
    type: Number,
    default: 0,
  },
  left: {
    type: Number,
    default: 0,
  }
})

let textInput = ref(props.input);
// 定义并在关闭标签后抛出事件
const emit = defineEmits(['inputBoxClosed']);
const handleCloseInputBox = () => {
  const text = textInput.value;
  textInput.value = '';
  emit('inputBoxClosed', text);
}

</script>

<template>
  <div v-if="textInput" class="input-box-container">
    <span class="content">{{ textInput }}
      <el-button type="primary" @click="handleCloseInputBox" class="close-input-box">
        <el-icon  ><Close /></el-icon>
      </el-button>
    </span>
  </div>
</template>

<style scoped>
.input-box-container {
  display: inline-block;
  position: absolute;
  bottom: calc(v-bind('props.bottom') * 1px);
  left: calc(v-bind('props.left') * 1px);
  min-width: 20px;
  max-width: 80vw; /* 最大宽度限制 */
  margin-left: 10px;
}

.content {
  display: inline-block;
  font-size: 15px;
  line-height: 30px;
  padding: 0 10px;
  background-color: #40a2f6;
  color: #fffdf3;
  border-radius: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.close-input-box,.close-input-box:hover {
  background-color: transparent;
  border: none;
  padding: 0;
}
</style>