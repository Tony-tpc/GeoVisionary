<template>
  <!--  首页 -->
  <section>
    <div class="container section1">
      <video src="../assets/videos/Galaxy.mp4" loop autoplay muted loading="lazy" class="video1"></video>
    </div>
    <div class="section1-title">
      星系
    </div>
    <div class="section1-subtitle">
      是夜空中跨越时空的华章，谱写着恒星与能量交织的永恒诗篇。
    </div>
  </section>
  <!--  展示页 -->
  <section>
    <div class="container section2">
      <ShowSolar />
    </div>
  </section>
</template>

<script setup>
import ShowSolar from "@/objects/ShowSolar.vue";
</script>

<style scoped>
/* 公共容器 */
.container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

/* 视频背景 */
.section1 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
}

/* 首页视频 */
.video1 {
  width: 100%;
  height: 100%;
  object-fit: fill;
}

/* 首页大标题 */
.section1-title {
  position: absolute;
  top: 17%;
  left: 15%;
  font-size: 64px;
  font-weight: bold;
  color: #fff;
  z-index: 2;
  mix-blend-mode: difference;
}

/* 首页副标题 */
.section1-subtitle {
  position: absolute;
  top: 30%;
  left: 15%;
  font-size: 32px;
  color: #fff;
  z-index: 2;
  mix-blend-mode: difference;
}

/* 第二屏 */
.section2 {
  position: absolute;
  top: 100vh;
  left: 0;
  height: 100vh;
}
</style>