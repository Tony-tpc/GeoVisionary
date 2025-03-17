<template>
  <!--  首页 -->
  <section>
    <!--  加载背景  -->
    <Loading title=".section1-title" subtitle=".section1-subtitle"></Loading>
    <!--  正文  -->
    <div class="container section1">
      <!--   背景图   -->
      <img src="@/assets/test/Quiz-test.jpg" alt="探知问学" loading="lazy" class="background-photo"/>
      <!--   标题   -->
      <div class="section1-title">
        探知问学
      </div>
      <div class="section1-subtitle">
        在这片智慧的天地里，每一道问题都是通往大自然奥秘的钥匙。通过测试与解析，你将踏上心灵之旅，深挖地理的千丝万缕，揭开知识的面纱。
      </div>
      <!--  引导图片  -->
      <ScrollButton sectionName="#section2"></ScrollButton>
    </div>
  </section>
  <!--  测试 + 解析 -->
  <section>
    <div class="container section2" id="section2">
      <!--  侧边导航栏  -->
      <div @mouseenter="handleEnterNav"
           @mouseleave="handleLeaveNav"
      >
        <SideNavigationBar
            @menu-select="fetchQuestions"
        />
      </div>

      <!-- 中间内容部分 -->
      <div class="content">
        <div class="intro">
          <h2 class="intro-title">📍 探知问学 - 挑战你的地理思维！</h2>

          <p class="intro-text">
            🧭 <strong>地理学，不只是记忆，更是探索！</strong>
            <br>🌏 在这里，我们提供精选地理题目，涵盖 <strong>高考真题、区域地理、综合分析</strong> 等不同类别，助你提升地理思维。
          </p>

          <div class="intro-section">
            <h3>📖 如何使用？</h3>
            <ul>
              <li>🔹 在左侧导航栏选择感兴趣的 <strong>题目分类</strong>，系统将自动加载相关试题。</li>
              <li>🔹 右侧 <strong>排行榜</strong> 展示了做对题目最多的用户，快来挑战他们吧！</li>
              <li>🔹 选择题目后，认真思考，作答提交，系统将自动批改，并提供详细解析。</li>
            </ul>
          </div>

          <p class="intro-highlight">🚀 <strong>挑战自我，提升地理素养！</strong></p>
          <p class="intro-call-to-action">立即选择一个题目类别，开启你的地理探索之旅吧！🔍🌎</p>
        </div>
      </div>

      <!--  试题组件  -->
      <div class="display-question">
        <QuestionsDisplay :isLoading="isLoading"/>
      </div>

      <!--  排行榜  -->
      <div class="leaderboard-component">
        <LeaderBoard />
      </div>
    </div>
  </section>
</template>

<script setup>
import { onMounted,ref } from "vue";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { gsap } from "gsap";
gsap.registerPlugin(ScrollTrigger);

const selectedCategory = ref(null); // 选中类别
const isLoading = ref(false); // 控制加载

// 处理鼠标移入导航栏
const handleEnterNav = () => {
  // 介绍文字收缩
  if (!selectedCategory.value) {
    gsap.to('.content',{width: '35%',left: '15%'})
  }
}

// 处理鼠标移出导航栏
const handleLeaveNav = () => {
  // 介绍文字扩张
  if (!selectedCategory.value) {
    gsap.to('.content',{width: '47%',left: '7%'})
  }
}

// 选中菜单栏后，向后端发送请求
const fetchQuestions = (selectedItem) => {
  isLoading.value = true;
  // 隐藏介绍文字和排行榜，并展示题目（初始默认加载）
  gsap.timeline()
      .to(['.content','.leaderboard-component'], {opacity: 0})
      .set(['.content','.leaderboard-component'], {display: 'none'})
      .set(['.display-question'],{display: 'block'})
      .to('.display-question',{opacity: 1});

  // 向后端发送请求
  selectedCategory.value = selectedItem;
  console.log("请求后端的数据:", selectedCategory.value);
  // 根据选中的对象请求后端
  setTimeout(() => {
    isLoading.value = false;
  },3000)
};

onMounted(() => {
  // 视差滚动
    gsap.fromTo('.background-photo',
        { y: `-${window.innerHeight / 2}px` }, // 起始位置
        { y: `${window.innerHeight / 2}px`,
          ease: "none",
          scrollTrigger: {
            trigger: '.section1',
            start: "top bottom",
            end: "bottom top",
            scrub: true,
          }
        }
    );
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
  font-family: cursive;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
}

/* 首页副标题 */
.section1-subtitle {
  font-size: 20px;
  font-weight: normal;
  text-align: center;
  position: absolute;
  top: 49%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #fff;
  font-family: cursive;
  padding: 8px 10px;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
}

/* 背景图 */
.background-photo {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* 第二屏 */
.section2 {
  position: absolute;
  top: 100vh;
  left: 0;
  height: 100vh;
  background: url(../src/assets/insight_bg.jpg) center / cover;
}

/* 中间内容区域 */
.content {
  position: absolute;
  top: 15%;
  left: 7%;
  flex: 1;
  padding: 40px;
  text-align: center;
  width: 47%;
}

/* 介绍部分 */
.intro-title {
  font-size: 28px;
  font-weight: bold;
  color: #ffffff; /* 纯白色，确保对比度 */
  margin-bottom: 20px;
}

.intro-text {
  font-size: 18px;
  line-height: 1.8;
  color: #e6f7ff; /* 柔和的浅蓝白色 */
  max-width: 700px;
  margin: 0 auto;
}

/* 介绍的每个模块 */
.intro-section {
  background: rgba(0, 51, 102, 0.2); /* 深蓝色低透明度 */
  padding: 20px;
  border-radius: 12px;
  margin-top: 20px;
  text-align: left;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

.intro-section h3 {
  font-size: 20px;
  color: #ffdd55; /* 柔和暖黄色 */
  margin-bottom: 10px;
}

.intro-section ul {
  list-style: none;
  padding: 0;
}

.intro-section li {
  font-size: 16px;
  line-height: 1.6;
  padding-left: 20px;
  text-indent: -15px;
  color: #e6f7ff; /* 保持一致的浅蓝白色，增强可读性 */
}

/* 结尾高亮 */
.intro-highlight {
  font-size: 20px;
  font-weight: bold;
  color: #ff884d; /* 温暖橙色，突出强调 */
  margin-top: 30px;
}

/* 号召行动 */
.intro-call-to-action {
  font-size: 18px;
  font-weight: bold;
  color: #f94604; /* 明亮柔和黄色 */
  margin-top: 20px;
}

/* 试题 */
.display-question {
  opacity: 0;
  display: none;
}
</style>