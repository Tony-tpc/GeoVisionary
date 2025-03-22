<script setup>
import { onMounted } from "vue";
import { gsap } from "gsap";
import { ScrollToPlugin } from "gsap/ScrollToPlugin";
gsap.registerPlugin(ScrollToPlugin);

const props = defineProps({
  size: {
    type: Number,
    required: false,
    default: 80
  },
  sectionName: {
    type: String,
    required: true,
  }
})

const scrollToOtherSection = () => {
  console.log('props.sectionName', props.sectionName);
  gsap.to(window,{
    scrollTo:props.sectionName,
    duration:0.8,
  })
};

onMounted(() => {
  // 引导动画
  gsap.timeline({repeat:-1})
      .from('.continue-photo',{y:'-=30',opacity:0,duration:0.9,ease:'none'})
      .to('.continue-photo',{y:'+=30',opacity:0,duration:0.9,ease:'none'})
})
</script>

<template>
  <!--  引导图片  -->
  <div class="continue-div">
    <el-button class="continue-button" @click="scrollToOtherSection">
      <img src="../assets/continue.svg" alt="继续" loading="lazy" class="continue-photo"/>
    </el-button>
  </div>
</template>

<style scoped>
/* 引导背景 */
.continue-div {
  position: absolute;
  bottom: 5%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: calc(v-bind('props.size') * 1px);
  height: calc(v-bind('props.size') * 1px);
  align-items: center;
  justify-content: center;
  border-radius: 100%;
  background-color: #fffdf3;
  z-index: 3;
  border: 1px solid #0d0f1a;
}

/* 引导按钮 */
.continue-button {
  width: 100%;
  height: 100%;
  background-color: transparent;
  border: none;
  border-radius: 100%;
}
</style>