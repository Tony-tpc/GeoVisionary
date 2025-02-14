<template>
  <!--  首页  -->
  <section>
    <div class="container section1">
      <el-carousel indicator-position="outside" height="100vh" :pause-on-hover="false" :interval="4000">
        <el-carousel-item v-for="item in data.carouselItems" :key="item">
          <img :src="item" alt="智荐学堂" loading="lazy" style="object-fit: fill;width: 100%;height: 100%;">
        </el-carousel-item>
      </el-carousel>
      <div class="section1-title">
        智荐学堂
      </div>
      <div class="section1-subtitle">
        在这里，智慧如星辰般璀璨，指引着你穿越地理的奥秘。每一次推荐都是心灵的启迪，揭开世界之书的一页页神奇篇章，引领探索者在知识的海洋中航行。
      </div>
    </div>
  </section>
  <!--  推荐页  -->
  <section>
    <div class="container section2">
      <div style="position:absolute;top: 20%;left: 20%;font-size: 32px;font-weight: bold;color: #0d0f1a;width: 500px;">此处展示推荐内容</div>
    </div>
  </section>
</template>

<script setup>
import { reactive, onMounted } from "vue";
import ph1 from '@/assets/test/Rec-test-1.jpeg';
import ph2 from '@/assets/test/Rec-test-2.jpeg';
import ph3 from '@/assets/test/Rec-test-3.jpeg';
import ph4 from '@/assets/test/Rec-test-4.jpeg';
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { gsap } from "gsap";
gsap.registerPlugin(ScrollTrigger)

const data = reactive({
  carouselItems:[ph1,ph2,ph3,ph4],
})

onMounted(() => {
  // 展示模型动画
  ScrollTrigger.create({
    trigger:'.section2',
    start:'top-=400 top',
    end:'+=200',
    scrub:true,
    animation:
        gsap.timeline()
            .to('.section1',{y:'-=100',opacity:0})
            .from('.section2',{y:'+=100',opacity:0},"<")
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

/* 第一屏 */
.section1 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: 5;
  overflow-x: hidden;
}

/* 首页大标题 */
.section1-title {
  position: absolute;
  top: 15%;
  left: 15%;
  font-size: 64px;
  font-weight: bold;
  color: #f94604;
  z-index: 10;
}

/* 首页副标题 */
.section1-subtitle {
  position: absolute;
  top: 30%;
  left: 15%;
  width: 63%;
  font-size: 24px;
  color: #0d0f1a;
  z-index: 10;
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