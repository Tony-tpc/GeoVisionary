<template>
  <!--  首页 -->
  <section>
    <div class="container section1">
      <video src="@/assets/climate.mp4" loop autoplay muted loading="lazy" class="video1"></video>
    </div>
    <div class="section1-title">
      气候
    </div>
    <div class="section1-subtitle">
      是风雨、寒暑交织成的长卷，塑造了大地与生灵的命运共舞。
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
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { onMounted } from "vue";

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
  color: rgba(255,255,255,0.8);
  z-index: 2;
}

/* 首页副标题 */
.section1-subtitle {
  position: absolute;
  top: 30%;
  left: 15%;
  font-size: 32px;
  color: rgba(255, 255, 255, 0.85);
  z-index: 2;
  text-shadow: 0 0 8px rgba(255,255,255,0.6);
}

/* 第二屏 */
.section2 {
  position: absolute;
  top: 100vh;
  left: 0;
  height: 100vh;
}
</style>