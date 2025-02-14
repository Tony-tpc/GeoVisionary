<template>
  <!--  首页 -->
  <section>
    <div class="container section1">
      <img src="@/assets/test/Quiz-test-2.jpeg" alt="探知问学" loading="lazy"/>
      <div class="section1-title">
        探知问学
      </div>
      <div class="section1-subtitle">
        在这片智慧的天地里，每一道问题都是通往大自然奥秘的钥匙。通过测试与解析，你将踏上心灵之旅，深挖地理的千丝万缕，揭开知识的面纱，一步步走向更大的领悟。
      </div>
      <img src="@/assets/test/Leader-Board-test.png" alt="排行榜" loading="lazy" class="leaderBoard">
    </div>
  </section>
  <!--  测试 + 解析 -->
  <section>
    <div class="container section2">
      <div style="position:absolute;top: 20%;left: 20%;font-size: 32px;font-weight: bold;color: #0d0f1a;width: 500px;">此处展示测试内容</div>
    </div>
  </section>
</template>

<script setup>
import {onMounted} from "vue";
import {ScrollTrigger} from "gsap/ScrollTrigger";
import {gsap} from "gsap";
gsap.registerPlugin(ScrollTrigger);

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
  width: 43%;
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

/* 排行榜 */
.leaderBoard {
  position: absolute;
  top: 15%;
  right: 10%;
  height: 70%;
  width: 30%;
  z-index: 5;
}
</style>