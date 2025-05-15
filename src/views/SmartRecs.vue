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
      <!--  概要卡片  -->
      <div class="general-synopsis-container" v-if="data.userChoice !== 'articles' && data.userChoice !== 'videos'">
        <div class="card" @click="selectContent('articles')">
          <img src="../assets/smart-images/book-opened.jpg" alt="图文" class="card-img" />
          <img src="../assets/smart-images/mountain-river-3D.jpg" alt="山水" class="card-3D-img" />
          <span class="card-words">图文推荐</span>
        </div>

        <div class="card" @click="selectContent('videos')">
          <img src="../assets/smart-images/online-lesson.jpg" alt="视频" class="card-img" />
          <img src="../assets/smart-images/videos-3D.jpg" alt="播放" class="card-3D-img" />
          <span class="card-words">视频推荐</span>
        </div>
      </div>

      <div class="information-display">
        <!--  视频部分  -->
        <div class="videos-container" v-if="data.userChoice === 'videos'">
          <div class="video-indent"></div>
          <div class="videos-title"></div>
          <BilibiliVideos :videos="displayVideos" :currentPage="currentPage"></BilibiliVideos>
          <div class="pagination-block">
            <el-pagination
                v-model:current-page="currentPage"
                hide-on-single-page
                :page-size="pageSize"
                :size="'default'"
                :disabled="disabled"
                background
                layout="total, prev, pager, next, jumper"
                :total="total"
                @current-change="handleCurrentChange"
            />
          </div>
        </div>

        <!--  图文内容  -->
        <div class="img-articles-container" v-if="data.userChoice === 'articles'" ref="articlesContainer">
          <div>
            <BaiduBaike @update-bg="updateBackground"
                        :keyword="data.keywordList"/>
          </div>
        </div>

        <!--  返回按钮  -->
        <div class="reverse-button" v-if="data.userChoice === 'videos' || data.userChoice === 'articles'">
          <el-tooltip
              popper-class="tooltips"
              effect="dark"
              content="返回"
              placement="top"
          >
            <el-button class="circular-button" @click="handleBackButton">
              <el-icon size="30"><Back /></el-icon>
            </el-button>
          </el-tooltip>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { reactive, onMounted, ref, computed } from "vue";
import ph1 from '@/assets/smart-images/Rec-1.jpeg';
import ph2 from '@/assets/smart-images/Rec-2.jpeg';
import ph3 from '@/assets/smart-images/Rec-3.jpeg';
import ph4 from '@/assets/smart-images/Rec-4.jpeg';
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { gsap } from "gsap";
import ColorThief from "colorthief";
import { Back } from "@element-plus/icons-vue";
import BaiduBaike from "@/components/BaiduBaike.vue";
import BilibiliVideos from "@/components/BilibiliVideos.vue";
import ScrollButton from "@/components/ScrollButton.vue";
import Loading from "@/components/Loading.vue"
import { getRecommendations } from "@/store/usefulFunction.js";

gsap.registerPlugin(ScrollTrigger);

const data = reactive({
  carouselItems:[ph1,ph2,ph3,ph4], // 轮播图
  videos:[], // 视频信息
  keywordList: [], // 关键词列表
  userChoice: '',
})

const currentPage = ref(1); // 当前页面
const disabled = ref(false); // 禁用分页
const total = computed(() => data.videos.length) // 视频总数量
const pageSize = ref(12); // 页面视频数量
const lastIndex = computed(() => currentPage.value * pageSize.value); // 当前页最后一个视频下标（不包括）

// 展示视频内容
const displayVideos = computed(() => data.videos.slice(lastIndex.value - pageSize.value, lastIndex.value))

const articlesContainer = ref(null); // 图文容器
const colorThief = new ColorThief() // 颜色聚合算法类

// 处理页面切换
const handleCurrentChange = (val) => {
  currentPage.value = val;
}

// 选中内容
const selectContent = async (value) => {
  await gsap.to('.general-synopsis-container',{opacity: 0})
  data.userChoice = value;
  gsap.to('.information-display',{opacity: 1})
}

// 更新背景
const updateBackground = async (img) => {
  if (!img) {
    articlesContainer.value.style.setProperty("--c1", "#fff");
    articlesContainer.value.style.setProperty("--c2", "#f0f0f0");
    articlesContainer.value.style.setProperty("--c3", "#e0e0e0");
    return;
  }

  // 确保图片已加载，否则 ColorThief 可能会报错
  if (!img.complete || img.naturalWidth === 0) return;

  try {
    const colors = await colorThief.getPalette(img, 3);
    const [c1, c2, c3] = colors.map(c => `rgb(${c[0]},${c[1]},${c[2]})`);
    articlesContainer.value.style.setProperty("--c1", c1);
    articlesContainer.value.style.setProperty("--c2", c2);
    articlesContainer.value.style.setProperty("--c3", c3);
  } catch (error) {
    console.error("ColorThief error:", error);
  }
};

// 返回上级按钮
const handleBackButton = async () => {
  await gsap.to('.information-display',{opacity: 0})
  data.userChoice = '';
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
  getRecommendations("text").then(response => {
    data.keywordList = response;
  });
  getRecommendations("video").then(response => {
    data.videos = response;
  })
});
</script>

<style scoped>
/* 在 CSS 最顶部添加 */
@layer properties {
  @property --c1 {
    syntax: "<color>";
    inherits: false;
    initial-value: #ffffff;
  }
  @property --c2 {
    syntax: "<color>";
    inherits: false;
    initial-value: #f0f0f0;
  }
  @property --c3 {
    syntax: "<color>";
    inherits: false;
    initial-value: #e0e0e0;
  }
}
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
  min-height: 100vh;
  height: auto;
}

.general-synopsis-container {
  position: absolute;
  top: calc((100vh - 400px) / 2);
  left: calc((100vw - 1300px) / 2);
  display: flex;
  gap: 50px;
  justify-content: center;
}

.card {
  position: relative;
  width: 600px;
  height: 400px;
  border-radius: 16px;
  overflow: visible;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background-color: unset;
  box-shadow: unset;
}

.card:hover .card-img{
  transform: perspective(900px) rotateX(25deg);
  box-shadow: 0 35px 35px -8px rgba(0, 0, 0, 0.75);
}

.card:hover .card-3D-img {
  opacity: 1;
  transform: perspective(900px) translate3d(0, -50px, 50px);
}

.card:hover .card-words {
  transform: perspective(900px) translate3d(0, -25px, 50px);
}

.card-words {
  position: absolute;
  bottom: 5%;
  left: 236px;
  z-index: 3;
  transition: all 0.5s ease;
  color: white;
  font-size: 32px;
  font-weight: bold;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);
}

.card-img,.card-3D-img {
  position: absolute;
  width: 600px;
  height: 400px;
  object-fit: cover;
  border-radius: 10px;
  z-index: 1;
  transition: all 0.5s ease;
}

.card-3D-img {
  width: 300px;
  height: 200px;
  z-index: 2;
  opacity: 0;
  left: 160px;
  top: 100px;
}

.video-indent {
  width: 100%;
  height: 15vh;
}
/* 视频容器 */
.videos-container {
  position: relative;
  top: 0;
  width: 100%;
  min-height: 85vh;
}

/* 图文容器 */
.img-articles-container {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(var(--c1), var(--c2), var(--c3));
  transition:
      --c1 0.5s ease-in-out,
      --c2 0.5s ease-in-out,
      --c3 0.5s ease-in-out;
}

/* 返回按钮 */
.circular-button {
  position: fixed;
  bottom: 10%;
  right: 5%;
  z-index: 2;
  width: 50px;
  height: 50px;
  border-radius: 100%;
  rotate: 0deg;
}

/* 分页组件 */
.pagination-block {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}
</style>