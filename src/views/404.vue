<template>
  <div class="container">
    <div style="text-align: center">
      <img src="../assets/404.jpeg" style="margin-top:10px;width: 50%;height: 50%" alt="404NotFound">
    </div>
    <div class="message">
    😕哎呀！我们找不到您要访问的页面。
    </div>
  </div>
  <div style="margin: 20px;text-align: center">
    <el-button type="primary" style="height: 60px;width: 120px;font-size: 18px;font-weight: bold;border-radius: 15px" @click="goHome">返回主页</el-button>
  </div>
</template>

<script setup>
const goHome = () => {
  location.href = '/navigator/home'
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin: 0;
  font-family: Arial, sans-serif;
  color: #333; /* 字体颜色 */
}

.message {
  font-size: 24px; /* 字体大小 */
  text-align: center; /* 文本居中 */
  margin: 20px;
  padding: 10px; /* 内边距 */
  border: 2px solid #ffcc00; /* 边框颜色 */
  border-radius: 8px; /* 圆角 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 阴影效果 */
}
</style>