<template>
  <!--  首页 -->
  <section>
    <div class="container section1">
      <img src="../assets/home-images/地形.jpg" loading="lazy" class="video1" alt=""/>
    </div>
    <div class="section1-title">
      地形
    </div>
    <div class="section1-subtitle">
      它是自然之手在大地上的瑰丽画卷，描绘出山川、谷地与平原。
    </div>
  </section>
  <!--  引导图片  -->
  <ScrollButton sectionName="#section2"></ScrollButton>
  <!--  展示页 -->
  <section>
    <div style="background-color: #2c2e3a;position: absolute;top: 100vh;width: 100%;height: 20vh;" id="section2"></div>
    <div class="container section2" @click="logActivity('study')">
      <WaterfallApp />
    </div>
  </section>
</template>

<script setup>
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { onMounted } from "vue";
import { logActivity } from "@/store/usefulFunction.js";
// import ShowGITF from "@/objects/ShowGITF.vue";
import WaterfallApp from '@/components/WaterfallApp.vue'
import ScrollButton from "@/components/ScrollButton.vue";
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

    // 启用全局滚动
    ScrollTrigger.config({
    autoRefresh: true,
    ignoreMobileResize: true
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
}

/* 首页副标题 */
.section1-subtitle {
  position: absolute;
  top: 30%;
  left: 15%;
  font-size: 32px;
  color: #fff;
  z-index: 2;
}

/* 第二屏 */
.section2 {
  position: absolute;
  top: 110vh;
  left: 0;
  height: auto;
}
</style>