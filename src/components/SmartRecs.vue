<template>
  <!--  首页  -->
  <section>
    <!--  加载背景  -->
    <Loading title=".section1-title" subtitle=".section1-subtitle"></Loading>
    <!--  正文  -->
    <div class="container section1">
      <el-carousel indicator-position="outside" height="100vh" :pause-on-hover="false" :interval="4000" class="carousel">
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
    <ScrollButton sectionName="#section2" style="z-index: 60"></ScrollButton>
  </section>
  <!--  推荐页  -->
  <section>
    <div class="container section2" id="section2">
      <div class="videos-container">
        <div class="videos-title"></div>
        <BilibiliVideos :videos="data.videos"></BilibiliVideos>
        <div class="demo-pagination-block">
          <el-pagination
              v-model:current-page="currentPage4"
              :page-size="12"
              :size="size"
              :disabled="disabled"
              background
              layout="total, prev, pager, next, jumper"
              :total="48"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
          />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { reactive, onMounted, ref } from "vue";
import ph1 from '@/assets/test/Rec-test-1.jpeg';
import ph2 from '@/assets/test/Rec-test-2.jpeg';
import ph3 from '@/assets/test/Rec-test-3.jpeg';
import ph4 from '@/assets/test/Rec-test-4.jpeg';
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { gsap } from "gsap";
gsap.registerPlugin(ScrollTrigger)

const data = reactive({
  carouselItems:[ph1,ph2,ph3,ph4],
  videos:[{'bvid': 'BV1RN4y1f7Hn','p': 2},{'bvid': 'BV1RN4y1f7Hn','p': 3},{'bvid': 'BV1RN4y1f7Hn','p': 4},
    {'bvid': 'BV1RN4y1f7Hn','p': 5},{'bvid': 'BV1RN4y1f7Hn','p': 6},{'bvid': 'BV1RN4y1f7Hn','p': 7},
    {'bvid': 'BV1RN4y1f7Hn','p': 8},{'bvid': 'BV1RN4y1f7Hn','p': 9},{'bvid': 'BV1RN4y1f7Hn','p': 10},
  ],
})

const currentPage4 = ref(4)
const size = ref('default')
const disabled = ref(false)

const handleSizeChange = (val) => {
  console.log(`${val} items per page`)
}
const handleCurrentChange = (val) => {
  console.log(`current page: ${val}`)
}

onMounted(() => {
  // 视差滚动
  gsap.fromTo('.carousel',{
    y: `-${window.innerHeight / 2}px`
  },{
    y:`${window.innerHeight / 2}px`,
    ease:'none',
    scrollTrigger: {
      trigger: '.section1',
      start: 'top bottom',
      end: 'bottom top',
      scrub:true,
    }
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
  font-size: 64px;
  font-weight: bold;
  text-align: center;
  position: absolute;
  top: 35%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff;
  text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.6);
}

/* 首页副标题 */
.section1-subtitle {
  font-size: 20px;
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #ddd;
  background: rgba(0, 0, 0, 0.5);
  padding: 10px 20px;
  border-radius: 8px;
  max-width: 60%;
}

/* 第二屏 */
.section2 {
  position: absolute;
  top: 100vh;
  left: 0;
  height: 100vh;
}

.videos-container {
  position: relative;
  top: 20%;
}
</style>