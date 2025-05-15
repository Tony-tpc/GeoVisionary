<template>
  <!--  首页 -->
  <section>
    <div class="container section1">
      <img src="@/assets/home-images/月相（横）.jpg" alt="月相" class="image">
    </div>
    <div class="section1-title">
      月相
    </div>
    <div class="section1-subtitle">
      星空下的月亮舞蹈，随着时间不断变化的面貌，展现无限魅力。
    </div>
    <ScrollButton sectionName="#section2" effect="light"></ScrollButton>
  </section>
  <!--  展示页 -->
  <section>
    <div class="container section2" id="section2">
      <ShowMoon />
    </div>
  </section>
</template>

<script setup>
import ShowMoon from "@/objects/ShowMoon.vue";
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

/* 首页容器 */
.section1 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: rgba(0, 0, 0, 1);
}

/* 首页图片 */
.image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 2;
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
}

/* 首页副标题 */
.section1-subtitle {
  position: absolute;
  top: 30%;
  left: 15%;
  font-size: 32px;
  color: rgba(255, 255, 255, 1);
  mix-blend-mode: difference;
  z-index: 2;
}

/* 第二屏 */
.section2 {
  position: absolute;
  top: 100vh;
  left: 0;
  height: 100vh;
  z-index: -1;
}
</style>