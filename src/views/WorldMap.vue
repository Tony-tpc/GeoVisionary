<template>
  <!--  首页 -->
  <section>
    <div class="container section1">
      <video src="../assets/videos/worldMap.mp4" loop autoplay muted loading="lazy" class="video1"></video>
    </div>
    <div class="section1-title">
      地图
    </div>
    <div class="section1-subtitle">
      一幅连接世界与思想的神奇画布，引导着我们的探索之旅。
    </div>
  </section>
  <!--  展示页 -->
  <section>
    <div class="container section2">
      <ShowWorld />
    </div>
  </section>
</template>

<script setup>
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { onMounted } from "vue";
import ShowWorld from "@/objects/ShowWorld.vue";
gsap.registerPlugin(ScrollTrigger)

onMounted(() => {
  // 展示模型动画
  ScrollTrigger.create({
    trigger:'.section2',
    start:'top-=200 top',
    end:'+=200',
    scrub:true,
    animation:
        gsap.timeline()
            .to('.section1',{opacity:0})
  });
  ScrollTrigger.create({
    trigger:'.section1',
    start:'top top',
    end:'+=300',
    scrub:true,
    animation:
        gsap.timeline()
            .from('.section2',{opacity:0})
  });
});

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