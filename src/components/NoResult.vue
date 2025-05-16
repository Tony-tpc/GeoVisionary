<template>
  <div class="no-result">
    <img :src="img || defaultImg" alt="无结果" class="no-result-img" />
    <p class="no-result-text">{{ message }}</p>
  </div>
</template>

<script setup>
defineProps({
  message: { type: String, default: '未找到相关内容，请尝试其他关键词' },
  img: { type: String, default: '' }
})

const defaultImg = new URL('@/assets/empty-state.svg', import.meta.url).href
</script>

<style scoped>
.no-result {
  width: 100%;
  padding: 12% 0 0 0;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #999;
}

.no-result-img {
  width: 200px;
  height: auto;
  opacity: 0.8;
  margin-bottom: 20px;
}

.no-result-text {
  font-size: 18px;
  color: #666;
}
</style>
