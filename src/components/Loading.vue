<script setup>
import { onMounted, ref } from "vue";
import { gsap } from "gsap";

const props = defineProps({
  title: {
    type: String,
    required: false,
    default: ".section1-title",
  },
  subtitle: {
    type: String,
    required: false,
    default: ".section1-subtitle",
  }
})
const isLoading = ref(true);

onMounted(() => {
  // 加载动画
  if(isLoading.value) {
    (async function () {
      // 粒子背景消逝，主页出现
      particlesJS("particles-background", {
        particles: {
          number: { value: 60 },
          size: { value: 2 },
          move: { speed: 2 },
          opacity: { anim: { enable: true, speed: 0.5 } },
        },
      });
      const t = gsap.timeline()
      t.to("#particles-background", {opacity:0,duration:1.3,delay:0.7})
          .set('#particles-background', {zIndex:-10})

      // 主标题上升，副标题变上升变出现
      t.from([props.title,props.subtitle], {opacity:0,y:'+=100',duration:1.6},1)

      // logo移动至与导航栏重合并消失
      t.to('.loading-logo',{left:105,top:45,duration:1.1,width:50},0.7)
      // 重启滚动
      await t.set('.loading-logo',{display:'none',delay:0.4})
      isLoading.value = false;
    })();
  } else {
    gsap.set(['.loading-logo','#particles-background'], {display:'none'});
  }
})
</script>

<template>
  <div v-if="isLoading">
    <!--  加载背景  -->
    <div class="loading-background" id="particles-background"></div>
    <img src="../assets/logos/mountain-fffdf3.svg" alt="logo" class="loading-logo" />
  </div>
</template>

<style scoped>
/* 加载动画背景 */
.loading-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: 900;
  background-color: #0d0f1a;
}

/* 加载背景logo */
.loading-logo {
  position: fixed;
  top: 50%;
  left: 50%;
  width: 13%;
  height: auto;
  transform: translate(-50%, -50%);
  z-index: 910;
}
</style>