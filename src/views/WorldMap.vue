<template>
  <!--  首页 -->
  <section>
    <div class="container section1">
      <img src="../assets/home-images/地图.jpg" loading="lazy" class="video1" alt=""/>
    </div>
    <div class="section1-title">
      地图
    </div>
    <div class="section1-subtitle">
      一幅连接世界与思想的神奇画布，引导着我们的探索之旅。
    </div>
    <ScrollButton sectionName="#section2" effect="light"></ScrollButton>
  </section>
  <!--  展示页 -->
  <section>
    <div class="container section2" id="section2">
      <ShowWorld />
    </div>
  </section>
</template>

<script setup>
import ShowWorld from "@/objects/ShowWorld.vue";
import ScrollButton from "@/components/ScrollButton.vue";
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
  height: auto;
}
</style>