<template>
  <!--  加载部分 -->
  <section>
    <div v-if="data.isLoading" class="container loading-section">
      <!--    背景 -->
      <div class="background"></div>
      <!--    网格背景 -->
      <canvas class="grid-background" id="gridCanvas"></canvas>
      <!--    装Logo的中盒子 -->
      <div class="boxLogo">
        <!--      半透明Logo -->
        <svg t="1738290868042" class="transparentLogo" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="7044" width="200" height="200">
          <path d="M784.64 784c-48 0-73.6-22.4-96-38.4-16-16-28.8-25.6-54.4-25.6-25.6 0-35.2 9.6-54.4 25.6-19.2 19.2-44.8 38.4-96 38.4-48 0-73.6-22.4-96-38.4-16-16-28.8-25.6-54.4-25.6-25.6 0-35.2 9.6-54.4 25.6-19.2 19.2-44.8 38.4-96 38.4-48 0-73.6-22.4-96-38.4-16-16-28.8-25.6-54.4-25.6-19.2 0-32-12.8-32-32s12.8-32 32-32c48 0 73.6 22.4 96 38.4 16 16 28.8 25.6 54.4 25.6 25.6 0 35.2-9.6 54.4-25.6 19.2-19.2 44.8-38.4 96-38.4s73.6 22.4 96 38.4c16 16 28.8 25.6 54.4 25.6 25.6 0 35.2-9.6 54.4-25.6 19.2-19.2 44.8-38.4 96-38.4 48 0 73.6 22.4 96 38.4 16 16 28.8 25.6 54.4 25.6 25.6 0 35.2-9.6 54.4-25.6 19.2-19.2 44.8-38.4 96-38.4 19.2 0 32 12.8 32 32s-12.8 32-32 32c-25.6 0-35.2 9.6-54.4 25.6-22.4 16-48 38.4-96 38.4z m-147.2 176c-48 0-76.8-22.4-96-38.4-19.2-16-28.8-25.6-54.4-25.6-25.6 0-38.4 9.6-54.4 25.6-19.2 19.2-48 38.4-96 38.4s-73.6-22.4-96-38.4c-19.2-16-28.8-25.6-54.4-25.6-19.2 0-32-12.8-32-32s12.8-32 32-32c48 0 73.6 22.4 96 38.4 16 16 28.8 25.6 54.4 25.6 25.6 0 38.4-9.6 54.4-25.6 19.2-19.2 48-38.4 96-38.4s76.8 22.4 96 38.4c16 16 28.8 25.6 54.4 25.6 25.6 0 38.4-9.6 54.4-25.6 19.2-19.2 48-38.4 96-38.4 19.2 0 32 12.8 32 32s-12.8 32-32 32c-25.6 0-38.4 9.6-54.4 25.6-22.4 16-48 38.4-96 38.4z m294.4-371.2h-547.2l217.6-371.2c12.8-19.2 35.2-32 57.6-32 25.6 0 48 12.8 57.6 32l214.4 371.2z m-438.4-64h326.4l-160-275.2h-6.4l-160 275.2z m-35.2 64h-416l307.2-553.6c9.6-22.4 32-35.2 57.6-35.2s48 12.8 57.6 35.2l153.6 275.2-160 278.4z m-307.2-64h268.8l124.8-214.4L410.24 64h-3.2l-3.2 3.2-252.8 457.6z"
                fill="rgba(255,255,255,0.5)"
                p-id="7045"
                class="iconBox"
          >
          </path>
        </svg>
        <!--      小盒子 -->
        <div class="smallBox"></div>
        <!--      亮色Logo -->
        <svg t="1738290868042"
             class="logo"
             viewBox="0 0 1024 1024"
             version="1.1"
             xmlns="http://www.w3.org/2000/svg"
             p-id="7044"
             width="200"
             height="200"
        >
          <path d="M784.64 784c-48 0-73.6-22.4-96-38.4-16-16-28.8-25.6-54.4-25.6-25.6 0-35.2 9.6-54.4 25.6-19.2 19.2-44.8 38.4-96 38.4-48 0-73.6-22.4-96-38.4-16-16-28.8-25.6-54.4-25.6-25.6 0-35.2 9.6-54.4 25.6-19.2 19.2-44.8 38.4-96 38.4-48 0-73.6-22.4-96-38.4-16-16-28.8-25.6-54.4-25.6-19.2 0-32-12.8-32-32s12.8-32 32-32c48 0 73.6 22.4 96 38.4 16 16 28.8 25.6 54.4 25.6 25.6 0 35.2-9.6 54.4-25.6 19.2-19.2 44.8-38.4 96-38.4s73.6 22.4 96 38.4c16 16 28.8 25.6 54.4 25.6 25.6 0 35.2-9.6 54.4-25.6 19.2-19.2 44.8-38.4 96-38.4 48 0 73.6 22.4 96 38.4 16 16 28.8 25.6 54.4 25.6 25.6 0 35.2-9.6 54.4-25.6 19.2-19.2 44.8-38.4 96-38.4 19.2 0 32 12.8 32 32s-12.8 32-32 32c-25.6 0-35.2 9.6-54.4 25.6-22.4 16-48 38.4-96 38.4z m-147.2 176c-48 0-76.8-22.4-96-38.4-19.2-16-28.8-25.6-54.4-25.6-25.6 0-38.4 9.6-54.4 25.6-19.2 19.2-48 38.4-96 38.4s-73.6-22.4-96-38.4c-19.2-16-28.8-25.6-54.4-25.6-19.2 0-32-12.8-32-32s12.8-32 32-32c48 0 73.6 22.4 96 38.4 16 16 28.8 25.6 54.4 25.6 25.6 0 38.4-9.6 54.4-25.6 19.2-19.2 48-38.4 96-38.4s76.8 22.4 96 38.4c16 16 28.8 25.6 54.4 25.6 25.6 0 38.4-9.6 54.4-25.6 19.2-19.2 48-38.4 96-38.4 19.2 0 32 12.8 32 32s-12.8 32-32 32c-25.6 0-38.4 9.6-54.4 25.6-22.4 16-48 38.4-96 38.4z m294.4-371.2h-547.2l217.6-371.2c12.8-19.2 35.2-32 57.6-32 25.6 0 48 12.8 57.6 32l214.4 371.2z m-438.4-64h326.4l-160-275.2h-6.4l-160 275.2z m-35.2 64h-416l307.2-553.6c9.6-22.4 32-35.2 57.6-35.2s48 12.8 57.6 35.2l153.6 275.2-160 278.4z m-307.2-64h268.8l124.8-214.4L410.24 64h-3.2l-3.2 3.2-252.8 457.6z"
                fill="#fffdf3"
                p-id="7045"
          >
          </path>
        </svg>
      </div>
    </div>
  </section>
  <!--  主页部分 -->
  <!--  欢迎页 -->
  <section>
    <div class="container section1">
      <div class="earth" id="earth-background"></div>
      <div class="page1" id="star-background"></div>
      <div class="buttons-1" style="top: 600px;left: 350px">
        <el-button type="primary" @click="changeSpeed">
          <span v-if="data.rotateSpeed > 0">停止转动</span>
          <span v-else>恢复转动</span>
        </el-button>
      </div>
      <div class="section1-title glowing-title">
        智绘山河
      </div>
      <div class="line1 section1-subtitle">AI 赋能探索</div>
      <div class="line2 section1-subtitle">让地理更智慧</div>
      <div class="line3 section1-subtitle">用科技丈量世界</div>
    </div>
  </section>
  <!--  功能概览页 -->
  <section>
    <div class="container section2">
      <!--    过渡文字  -->
      <div class="transition-words">
        <span class="c1">探</span>
        <span class="c2">索</span>
        <span class="c3">世</span>
        <span class="c4">界</span>
        <span class="c5">，</span>
        <span class="c6">从</span>
        <span class="c7">这</span>
        <span class="c8">里</span>
        <span class="c9">启</span>
        <span class="c10">程</span>
        <span class="c11">。</span>
      </div>
      <!--    进度条  -->
      <el-progress
          :percentage="data.percentage[0]"
          :text-inside="true"
          :stroke-width="30"
          striped
          striped-flow
          :duration="15"
          class="progress"
          :color="customColorMethod"
      >
        <span v-if="data.percentage[0] < 25" class="progress-font">智绘天地</span>
        <span v-else-if="data.percentage[0] < 50" class="progress-font">知象图谱</span>
        <span v-else-if="data.percentage[0] < 75" class="progress-font">探知问学</span>
        <span v-else class="progress-font">智荐学堂</span>
        <span class="progress-font">{{ parseInt(data.percentage[0]) }}%</span>
      </el-progress>
      <!--    智绘天地介绍  -->
      <div class="page2">
        <h2 class="section2-title">直观可视化，探索地理奥秘</h2>
        <div class="step-item">Step 1: 了解</div>
        <p class="section2-subtitle">沉浸式 3D 体验，让你身临其境</p>
        <p class="section2-text">通过智能化的3D地形和动态气候等模型，用户能够亲身体验到地理知识的变化与奥秘。在虚拟环境中，学生可以随时与地球进行互动，感受地形、气候、月相等自然现象的真实变化。这种互动式的学习方式不再仅仅局限于书本和图表，让知识更加生动、直观，激发学习兴趣，提升学习效率。</p>
        <img src="@/assets/Landform-test.png" alt="智绘天地" loading="lazy" class="section2-img1"/>
        <img src="@/assets/Moon-phase-test.png" alt="智绘天地" loading="lazy" class="section2-img2"/>
      </div>
      <!--    知象图谱介绍  -->
      <div class="page3">
        <h2 class="section2-title">知识图谱 + AI 互动</h2>
        <div class="step-item">Step 2: 学习</div>
        <p class="section2-subtitle">结构化知识，AI 助教解答</p>
        <p class="section2-text">地理知识图谱通过结构化的方式帮助学生全面理解地理学科的知识体系。借助AI技术，我们将复杂的地理学概念和数据组织成图谱，学生可以通过图谱轻松获取相关知识。在学习过程中，AI助教会实时解答学生的问题，结合大数据分析为学生提供定制化学习路径，帮助学生在最短时间内掌握所需知识。</p>
        <img src="@/assets/Geo-graph-test.png" alt="知象图谱" loading="lazy" class="section2-img1"/>
        <img src="@/assets/Geo-graph-test-2.jpeg" alt="知象图谱" loading="lazy" class="section2-img2"/>
      </div>
      <!--    探知问学介绍  -->
      <div class="page4">
        <h2 class="section2-title">智能测评，精准诊断</h2>
        <div class="step-item">Step 3: 测试</div>
        <p class="section2-subtitle">找到薄弱点，针对性提升</p>
        <p class="section2-text">智能测评系统能够实时监控学生的学习进度，分析学生在不同知识点上的掌握程度。当学生进行习题测试时，系统不仅会自动批改，还会针对性地提供详细的解析和学习建议。通过深入分析学生的错误，AI系统会帮助学生找出薄弱环节，精准定位知识盲区，提供个性化的学习方案，帮助学生快速提升。</p>
        <img src="@/assets/Insight-lab-test.png" alt="探知问学" loading="lazy" class="section2-img1"/>
        <img src="@/assets/Insight-lab-test-2.png" alt="探知问学" loading="lazy" class="section2-img2"/>
      </div>
      <!--    智荐学堂介绍  -->
      <div class="page5">
        <h2 class="section2-title">个性化推荐，定制学习路线</h2>
        <div class="step-item">Step 4: 巩固</div>
        <p class="section2-subtitle">智能推荐，学习不再盲目</p>
        <p class="section2-text">学习不再是一成不变的重复过程，通过AI技术分析学生的学习轨迹，我们能够为每个学生量身定制学习路线。基于学生的学习进度和掌握情况，系统自动推荐最适合的学习资源，包括习题、文章、视频等。这样的个性化推荐让学生能够在正确的时间接触到最有价值的内容，从而有效巩固所学知识，进一步提升学习效率。</p>
        <img src="@/assets/Smart-recs-test-1.png" alt="智荐学堂" loading="lazy" class="section2-img1"/>
        <img src="@/assets/Smart-recs-test-2.png" alt="智荐学堂" loading="lazy" class="section2-img2"/>
      </div>
      <!--    第二屏与第三屏过渡文字  -->
      <div class="transition-words-2">
        <span class="c12">世界&nbsp;&nbsp;&nbsp;</span>
        <span>不止于</span>
        <span class="c12">&nbsp;&nbsp;&nbsp;平面</span>
      </div>
    </div>
  </section>
  <!--  可视化展示页 -->
  <section>
    <div class="container section3" :style="{ top: `${data.section3Top}px`}">
        <!--    粒子背景 + 上、下、左、右四个视频  -->
        <div id="video-particles" class="particles-container">
          <div class="upper-left">
            <video src="@/assets/Cesium-test.mp4" autoplay muted loop loading="lazy" class="video1"></video>
          </div>
          <div class="upper-right">
            <video src="@/assets/Verge3D-Web-Interactive.mp4" autoplay muted loop loading="lazy" class="video2"></video>
          </div>
          <div class="lower-left">
            <video src="@/assets/climate.mp4" autoplay muted loop loading="lazy" class="video3"></video>
          </div>
          <div class="lower-right">
            <video src="@/assets/worldMap.mp4" autoplay muted loop loading="lazy" class="video4"></video>
          </div>
          <!--   文字介绍  -->
          <div>
            <p class="video-text-1">地形</p>
            <p class="video-text-2">月相</p>
            <p class="video-text-3">气候</p>
            <p class="video-text-4">地图</p>
          </div>
        </div>
    </div>
  </section>
  <!--  CTA 页 -->
  <section>
    <div class="container section4" :style="{ top: `${data.section4Top}px`}">
      <!--    轮播图  -->
      <div>
        <div class="box">
          <planet-icon theme="outline" size="18" fill="#f94604" :strokeWidth="3"/>
          <span>&nbsp;&nbsp;天体</span>
        </div>
        <div class="box">
          <wind-icon theme="outline" size="18" fill="#f94604" :strokeWidth="3"/>
          <span>&nbsp;&nbsp;气候</span>
        </div>
        <div class="box">
          <landscape-icon theme="outline" size="18" fill="#f94604" :strokeWidth="3"/>
          <span>&nbsp;&nbsp;地形</span>
        </div>
        <div class="box">
          <water-icon theme="outline" size="18" fill="#f94604" :strokeWidth="3"/>
          <span>&nbsp;&nbsp;水源</span>
        </div>
        <div class="box">
          <sapling-icon theme="outline" size="18" fill="#f94604" :strokeWidth="3"/>
          <span>&nbsp;&nbsp;农业</span>
        </div>
        <div class="box">
          <chimney-icon theme="outline" size="18" fill="#f94604" :strokeWidth="3"/>
          <span>&nbsp;&nbsp;工业</span>
        </div>
        <div class="box">
          <pavilion-icon theme="outline" size="18" fill="#f94604" :strokeWidth="3"/>
          <span>&nbsp;&nbsp;人文</span>
        </div>
        <div class="box">
          <local-icon theme="outline" size="18" fill="#f94604" :strokeWidth="3"/>
          <span>&nbsp;&nbsp;GIS</span>
        </div>
      </div>
      <!--    CTA + 跳转按钮 -->
      <div>
        <div>
          <h2 class="section4-title">探索地理的奥秘，从这里开始</h2>
          <p class="section4-subtitle">通过我们的平台，轻松了解全球地理变化，掌握知识，随时随地享受学习乐趣！</p>
        </div>
        <div class="buttons-container">
          <el-button class="buttons-4" type="success" @click="router.push('/navigator/landform')">地形</el-button>
          <el-button class="buttons-4" type="primary" @click="router.push('/navigator/moon-phase')">月相</el-button>
          <el-button class="buttons-4" type="warning" @click="router.push('/navigator/climate')">气候</el-button>
          <el-button class="buttons-4" type="info" @click="router.push('/navigator/world-map')">地图</el-button>
        </div>
      </div>
    </div>
  </section>
  <!--  此部分用于动画补时，无实际意义 -->
  <div class="nothing" style="display:none;"></div> 
</template>

<script setup>
import {onMounted, reactive, onBeforeUnmount, onUnmounted, inject } from "vue";
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import MeteorClass from "@/classes/meteor.js";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { throttle } from "lodash";
import router from "@/router/index.js";
import { ChinesePavilion as PavilionIcon, Local as LocalIcon, Planet as PlanetIcon, Wind as WindIcon,
    Landscape as LandscapeIcon, Water as WaterIcon, Sapling as SaplingIcon, Chimney as ChimneyIcon
} from "@icon-park/vue-next";// IDE问题，此部分代码均有用

gsap.registerPlugin(ScrollTrigger);

const data = reactive({
  rotateSpeed: 0.001,           // 地球转动速度
  percentage: [0],              // 进度条进度
  isLoading: true,              // 加载动画
  section3Top: 0,               // 第三屏位置
  section4Top: 0,               // 第四屏位置
});

// 禁用滚动
const disableScroll = () => {
  document.documentElement.style.overflow = "hidden"; // 禁止滚动
  document.documentElement.style.pointerEvents = "none"; // 禁止交互
}

// 恢复滚动
const enableScroll = () => {
  document.documentElement.style.overflow = "auto";
  document.documentElement.style.pointerEvents = "auto";
  document.documentElement.style.overflowX = "hidden";
}

// 切换转动速度
const changeSpeed = () => {
  if(data.rotateSpeed)
    data.rotateSpeed = 0
  else
    data.rotateSpeed = 0.001
}

// 切换进度条颜色
const customColorMethod = (percentage) => {
  if (percentage < 25) {
    return '#0066bc';
  } else if (percentage < 50) {
    return '#46b61f';
  } else if (percentage < 75) {
    return '#ffad00';
  } else {
    return '#5e41b8';
  }
}

let resize;   // 自动调整星空背景大小
// 提升变量作用域，可供销毁
let scene,camera,renderer,animation,controls,starScene,starCamera,starRenderer,starAnimation,saveScrollPosition;

// 加载部分虚线网格背景
const drawDashedGrid = () => {
  const canvas = document.getElementById("gridCanvas");
  const ctx = canvas.getContext("2d");

  // 设置 Canvas 尺寸
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  ctx.strokeStyle = "rgba(255, 255, 255, 0.75)"; // 线条颜色
  ctx.lineWidth = 1; // 线条宽度
  ctx.setLineDash([5, 5]); // 设定虚线样式：5px 实线，5px 间隔

  const gridSize = 40; // 网格间隔大小

  // 画垂直线
  for (let x = 0; x < canvas.width; x += gridSize) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
  }

  // 画水平线
  for (let y = 0; y < canvas.height; y += gridSize) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(canvas.width, y);
    ctx.stroke();
  }
};

onMounted(() => {
  // 加载动画
  (function () {
    // 保存当前滚动位置
    saveScrollPosition = () => {
      sessionStorage.setItem('scrollPosition', window.scrollY);
    };

    // 恢复滚动位置
    const restoreScrollPosition = () => {
      const savedScrollY = sessionStorage.getItem('scrollPosition');
      data.isLoading = !(savedScrollY !== null && savedScrollY !== '0');
    };
    restoreScrollPosition();
    window.addEventListener('beforeunload', saveScrollPosition);

    if (data.isLoading) {
      drawDashedGrid();
      disableScroll(); // 禁用滚动
      const isLoading = inject('isLoading');
      isLoading.value = data.isLoading;

      gsap.context(() => {
        const t = gsap.timeline()
        // 背景颜色变化
        t.from([".background",".boxLogo",".smallBox"], {
          backgroundColor: "#000000",
          duration: 1,
        });

        // 背景缩放
        t.from(".grid-background", {
          scale: 2,
          duration: 2,
          transformOrigin: "center center",
          ease: "power4.out",
        },"<");

        t.from(".boxLogo", {
          scale: 4,
          duration: 2,
          transformOrigin: "center center",
          ease: "power4.out",
        },"<");

        // 半透明Logo升起
        t.from(".transparentLogo",{
          y: "100vh",
          duration: 1,
        },"<");

        // 相同背景色的盒子向上移动模拟图标自下向上填色
        t.to(".smallBox",{
          y:-175,
          duration: 1.25,
          ease:"power2.inOut"
        },">-=0.35");

        // 快速闪烁暗示网页加载完毕
        t.to(".boxLogo",{
          opacity:0,
          yoyo:true,
          repeat:16,
          duration:0.04,
        },">");

        // 移除加载页面，呈现主页
        t.to(".loading-section",{
          y:"-100vh",
          duration: 1.1,
          ease:"power2.in",
        },1.9);

        // 主页上升
        t.from('.section1',{
          y:'100vh',
          duration: 1.1,
          ease:"power2.in",
          onComplete: () => {
            data.isLoading = false;
            isLoading.value = false;
            enableScroll();
          }
        },"<");

        // 大标题出现
        t.from('.section1-title',{
          y:'-=30',
          opacity: 0,
          duration: 1.1,
        })

        // 大标题浮动
        t.to('.section1-title',{
          y: '+=5',
          repeat: -1,
          duration: 1.5,
          yoyo: true,
          ease: "none"
        },">")

        // 第一行副标题出现
        t.from('.line1',{
          opacity: 0,
          y:"+=30",
          duration: 0.6,
        },"<-=0.3")

        // 第二行副标题出现
        t.from('.line2',{
          opacity: 0,
          y:"+=30",
          duration: 0.6,
        })

        // 第三行副标题出现
        t.from('.line3',{
          opacity: 0,
          y:"+=30",
          duration: 0.6,
        })
      });
    }
  })();

  // 创建地球
  (function (){
    // 初始化布景
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    camera.position.set(0, 0, 40);
    camera.lookAt(0,0,0);

    renderer = new THREE.WebGLRenderer({ antialias: true,alpha: true });
    renderer.setSize(650, 650);
    document.getElementById('earth-background').appendChild(renderer.domElement);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.enableZoom = false;

    const loader = new THREE.TextureLoader();
    const group = new THREE.Group();

    // 增加环境光
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7); // 环境光强度提高
    scene.add(ambientLight);

    // 增加多个平行光源
    const directionalLight1 = new THREE.DirectionalLight(0xffffff, 1); // 第一个平行光
    directionalLight1.position.set(5, 5, 5).normalize();
    scene.add(directionalLight1);

    const directionalLight2 = new THREE.DirectionalLight(0xffffff, 1); // 第二个平行光
    directionalLight2.position.set(-5, -5, -5).normalize();
    scene.add(directionalLight2);

    // 添加聚光灯
    const spotLight = new THREE.SpotLight(0xffffff, 1);
    spotLight.position.set(10, 10, 10);
    spotLight.castShadow = true;
    scene.add(spotLight);

    // 创建本体
    const earthGeometry = new THREE.SphereGeometry(20, 30, 30);   // 创建球形几何体
    const earthMaterial = new THREE.MeshPhongMaterial({    // 创建材质
      map: loader.load('/src/assets/2k_earth_daymap(1).jpg'),        // 基础纹理
      specularMap: loader.load('/src/assets/specular.png'),  // 高光纹理，指定物体表面中哪部分比较闪亮，哪部分相对暗淡
      normalMap: loader.load('/src/assets/normal.png'),   // 法向纹理，创建更加细致的凹凸和褶皱
      normalScale: new THREE.Vector2(3, 3),
      color: 0xffffff
    });
    const sphere = new THREE.Mesh(earthGeometry, earthMaterial);   // 创建基础球体
    group.add(sphere);

    // 顶点着色器
    const VSHADER_SOURCE = `
  varying vec2 v_Uv;
  void main () {
    v_Uv = uv;       //顶点纹理坐标
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4( position, 1.0 );
  }
`;

    // 片元着色器
    const FSHADER_SOURCE = `
  uniform float time;      //时间变量
  uniform sampler2D fTexture;    //大气纹理图像
  uniform sampler2D nTexture;    //噪声纹理图像
  varying vec2 v_Uv;              //片元纹理坐标
  void main () {
    vec2 new_Uv= v_Uv + vec2( 0, 0.02 ) * time;   //向量加法，根据时间变量计算新的纹理坐标

    //利用噪声随机使纹理坐标随机化
    vec4 noise_Color = texture2D( nTexture, new_Uv );
    new_Uv.x += noise_Color.r * 0.2;
    new_Uv.y += noise_Color.g * 0.2;

    gl_FragColor = texture2D( fTexture, new_Uv );  //提取大气纹理图像的颜色值（纹素）
  }
`;

    const flowTexture = loader.load('/src/assets/flow.png');
    flowTexture.wrapS = THREE.RepeatWrapping;
    flowTexture.wrapT = THREE.RepeatWrapping;

    const noiseTexture = loader.load('/src/assets/noise.png');
    noiseTexture.wrapS = THREE.RepeatWrapping;
    noiseTexture.wrapT = THREE.RepeatWrapping;

    // 着色器材质
    const flowMaterial = new THREE.ShaderMaterial({
      uniforms: {
        fTexture: {
          value: flowTexture,
        },
        nTexture: {
          value: noiseTexture,
        },
        time: {
          value: 0.0
        },
      },
      // 顶点着色器
      vertexShader: VSHADER_SOURCE,
      // 片元着色器
      fragmentShader: FSHADER_SOURCE,
      transparent: true
    });
    const fgeometry = new THREE.SphereGeometry(20.01, 30, 30);   // 创建比基础球体略大的球状几何体
    const fsphere = new THREE.Mesh(fgeometry, flowMaterial);    // 创建大气球体
    group.add(fsphere);
    scene.add(group);

    // 创建 Glow Shader（蓝色光晕）
    const GlowShaderMaterial = new THREE.ShaderMaterial({
      uniforms: {
        glowColor: { value: new THREE.Color(0x66ccff) }, // 设置蓝色光晕
        c: { value: 0.98 },  // 亮度控制
        p: { value: 3.5 }   // 扩散度
      },
      vertexShader: `
        varying vec3 vNormal;
        varying vec3 vViewPosition;
        void main() {
            vNormal = normalize(normalMatrix * normal);
            vViewPosition = normalize(modelViewMatrix * vec4(position, 1.0)).xyz;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
      fragmentShader: `
        uniform vec3 glowColor;
        uniform float c;
        uniform float p;
        varying vec3 vNormal;
        varying vec3 vViewPosition;
        void main() {
            float intensity = pow(c - dot(vNormal, vViewPosition), p);
            gl_FragColor = vec4(glowColor, 0.8) * intensity;
        }
    `,
      side: THREE.BackSide, // 让光晕向外扩散
      blending: THREE.AdditiveBlending, // 让光晕更自然
      transparent: true
    });

    // 创建 Glow 球体
    const glowGeometry = new THREE.SphereGeometry(20.1, 30, 30); // 比地球略大
    const glowSphere = new THREE.Mesh(glowGeometry, GlowShaderMaterial);
    group.add(glowSphere); // 添加光晕到地球 Group
    scene.add(group);

    // 渲染循环
    const animate = function () {
      animation = requestAnimationFrame(animate);
      const delta = data.rotateSpeed === 0 ? 0 : 0.003;
      group.rotation.y -= data.rotateSpeed;      // 整体转动
      flowMaterial.uniforms.time.value += delta;  // 改变uniforms.time的值，用于片元着色器中的纹理坐标计算
      controls.update();
      renderer.render(scene, camera);
    };
    animate();

  })();

  // 创建星空
  (function (){
    // 初始化布景
    starScene = new THREE.Scene();
    starCamera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
    starRenderer = new THREE.WebGLRenderer({ alpha: true });
    starRenderer.setSize(
        document.getElementById('star-background').offsetWidth,
        document.getElementById('star-background').offsetHeight
    );
    starRenderer.setClearColor(0x0d0f1a)
    document.getElementById('star-background').appendChild(starRenderer.domElement);

    // 创建星空粒子
    const starsGeometry = new THREE.BufferGeometry();
    const starsVertices = [];
    for (let i = 0; i < 500; i++) {  // 500 颗星星
      let x = (Math.random() - 0.5) * 2000;
      let y = (Math.random() - 0.5) * 2000;
      let z = (Math.random() - 0.5) * 2000;
      starsVertices.push(x, y, z);
    }
    starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
    const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 2 });
    const starField = new THREE.Points(starsGeometry, starsMaterial);
    starScene.add(starField);

    starCamera.position.z = 50;

    // 创建流星
    const meteors = []; // 用于存储流星实例

    const meteorConfigs = [
      { color: { left: new THREE.Color("#0000ff"), right: new THREE.Color("#00ffff") }, duration: 1.8, hideDuration: 1, position: new THREE.Vector3(95,  75, -75),  target: new THREE.Vector3(220,-310, -25) },
      { color: { left: new THREE.Color("#00aaff"), right: new THREE.Color("#ffffff") }, duration: 2.7, hideDuration: 0.8, position: new THREE.Vector3(70,  25, 0),  target: new THREE.Vector3(150, 25, 75) },
      { color: { left: new THREE.Color("#0000ff"), right: new THREE.Color("#00ffff") }, duration: 1.8, hideDuration: 1, position: new THREE.Vector3(70,  0, 0),  target: new THREE.Vector3(150, 25, 75) },
    ];

    meteorConfigs.forEach(config => {
      const meteor = new MeteorClass(
          1000,
          config.target, // 目的地
          config.color, // 颜色
          1,
          config.duration, // 飞行时长
          config.hideDuration, // 消失时长
      );
      starScene.add(meteor.group);
      meteor.group.position.set(config.position.x, config.position.y, config.position.z); // 设置起始位置
      meteor.group.rotateZ(Math.PI / 0.9); // 旋转角度
      meteors.push(meteor);
    });

    starCamera.position.z = 50;
    function starAnimate() {
      starAnimation = requestAnimationFrame(starAnimate);
      starField.rotation.y += 0.0002;  // 缓慢旋转
      meteors.forEach(meteor => meteor.update()); // 更新所有流星
      starRenderer.render(starScene, starCamera);
    }
    starAnimate();

    // 添加 resize 事件监听器以及时调整窗口大小
    resize = throttle(() => {
      const width = document.getElementById('star-background').offsetWidth;
      const height = document.getElementById('star-background').offsetHeight;
      starRenderer.setSize(width, height);
      starCamera.aspect = width / height;
      starCamera.updateProjectionMatrix();
    }, 200);
    window.addEventListener('resize', resize);
    resize(starRenderer,starCamera);

  })();

  // 第二屏滚动动画
  (function (){
    // 主标题上升 + 逐字出现
    ScrollTrigger.create({
      trigger:'.section2',
      start:'top center',
      end:'+=450',
      scrub:true,
      animation:
          gsap.timeline()
              .from('.transition-words',{y:'+=100',duration:2})
              .from('.c1', {opacity: 0, duration: 1.2}, "<")
              .from('.c2', {opacity: 0, duration: 1.2})
              .from('.c3', {opacity: 0, duration: 1.2})
              .from('.c4', {opacity: 0, duration: 1.2})
              .from('.c5', {opacity: 0, duration: 1.2})
              .from('.c6', {opacity: 0, duration: 1.2})
              .from('.c7', {opacity: 0, duration: 1.2})
              .from('.c8', {opacity: 0, duration: 1.2})
              .from('.c9', {opacity: 0, duration: 1.2})
              .from('.c10', {opacity: 0, duration: 1.2})
              .from('.c11', {opacity: 0, duration: 1.2})
    })

    // 主标题消失，主要内容出现
    ScrollTrigger.create({
      trigger: '.section2',
      start: 'top+=80 top',
      end: '+=5100',
      scrub: true,
      pin:true,
      animation:
          gsap.timeline()
              .to('.transition-words',{opacity:0},0)
              .from(['.page2','.progress'],{opacity:0,duration:1,scale:1.2,y:'+=80'},">")
              .to(data.percentage,{endArray:[100],duration:20.5,ease:'none'},2)
              .to('.section2-img1',{top:'18%',right:'15%',rotate:'-15deg',zIndex:1,duration:2},3)
              .to('.section2-img2',{top:'21%',right:'10%',rotate:'0',zIndex:2,duration:2},"<")
              .to('.page2',{ease:'none',x:() => '-=' + document.querySelector('.section2').offsetWidth,duration:1.5},6)
              .from('.page3',{ease:'none',x:() => '+=' + document.querySelector('.section2').offsetWidth,duration:1.5},6)
              .to('.section2-img2',{top:'18%',right:'15%',rotate:'-15deg',zIndex:1,duration:2},8.5)
              .to('.section2-img1',{top:'21%',right:'10%',rotate:'0',zIndex:2,duration:2},"<")
              .to('.page3',{ease:'none',x:() => '-=' + document.querySelector('.section2').offsetWidth,duration:1.5},11.5)
              .from('.page4',{ease:'none',x:() => '+=' + document.querySelector('.section2').offsetWidth,duration:1.5},11.5)
              .to('.section2-img1',{top:'18%',right:'15%',rotate:'-15deg',zIndex:1,duration:2},14)
              .to('.section2-img2',{top:'21%',right:'10%',rotate:'0',zIndex:2,duration:2},"<")
              .to('.page4',{ease:'none',x:() => '-=' + document.querySelector('.section2').offsetWidth,duration:1.5},17)
              .from('.page5',{ease:'none',x:() => '+=' + document.querySelector('.section2').offsetWidth,duration:1.5},17)
              .to('.section2-img2',{top:'18%',right:'15%',rotate:'-15deg',zIndex:1,duration:2},19.5)
              .to('.section2-img1',{top:'21%',right:'10%',rotate:'0',zIndex:2,duration:2},"<")
              .to(['.page5','.progress'],{opacity:0,duration:1.3})
              .to('.transition-words-2',{opacity:1,duration:2},">-=0.3")
              .to('.nothing',{opacity:0,duration:1.1}) // 用于悬停展示过渡文字
    })
  })();

  // 第三/四屏高度计算，并传回导航栏
  (function (){
    const TopChangeMode = inject("TopChangeMode");
    const firstScreenHeight = window.innerHeight; // 100vh 实际值
    const secondScreenHeight = firstScreenHeight * 0.7; // 超出 ScrollTrigger 的70vh高度
    const scrollTriggerHeight = 5400; // ScrollTrigger 占用的额外空间
    data.section3Top = firstScreenHeight + secondScreenHeight + scrollTriggerHeight;
    TopChangeMode.value = data.section3Top;
    data.section4Top = data.section3Top + 6.3 * window.innerHeight;
  })();

  // 第三屏动画
  (function (){
    // 粒子背景
    particlesJS("video-particles", {
      particles: {
        number: { value: 60 },
        size: { value: 2 },
        move: { speed: 2 },
        opacity: { anim: { enable: true, speed: 0.5 } },
      },
    });

    // 滚动动画
    ScrollTrigger.create({
      trigger:'.particles-container',
      start:'top top',
      end:'+=5000',
      scrub:true,
      pin:true,
      animation:
          gsap.timeline()
              .to('.upper-left',{left:"14%",top:"15%",height:"70%",width:"70%",zIndex:3,yoyo:true,filter: "blur(0px)",duration:0.7,opacity:1,repeat:1,repeatDelay:1,boxShadow: "0px 0px 20px rgba(255, 255, 255, 0.8)"})
              .to('.video-text-1',{opacity:1,duration:0.7,repeat:1,repeatDelay:1,yoyo:true},"<")
              .to('.upper-right',{left:"14%",top:"15%",height:"70%",width:"70%",zIndex:3,yoyo:true,filter: "blur(0px)",duration:0.7,opacity:1,repeat:1,repeatDelay:1,boxShadow: "0px 0px 20px rgba(255, 255, 255, 0.8)"})
              .to('.video-text-2',{opacity:1,duration:0.7,repeat:1,repeatDelay:1,yoyo:true},"<")
              .to('.lower-left',{left:"14%",top:"15%",height:"70%",width:"70%",zIndex:3,yoyo:true,filter: "blur(0px)",duration:0.7,opacity:1,repeat:1,repeatDelay:1,boxShadow: "0px 0px 20px rgba(255, 255, 255, 0.8)"})
              .to('.video-text-3',{opacity:1,duration:0.7,repeat:1,repeatDelay:1,yoyo:true},"<")
              .to('.lower-right',{left:"14%",top:"15%",height:"70%",width:"70%",zIndex:3,yoyo:true,filter: "blur(0px)",duration:0.7,opacity:1,repeat:1,repeatDelay:1,boxShadow: "0px 0px 20px rgba(255, 255, 255, 0.8)"})
              .to('.video-text-4',{opacity:1,duration:0.7,repeat:1,repeatDelay:1,yoyo:true},"<")
              .to('.nothing',{opacity:0,duration:2},">+=0.7")
    })

  })();

  // 第四屏动画
  (function (){
    // 页面出现
    ScrollTrigger.create({
      trigger:'.section4',
      start:'top-=500 top',
      end:'+=400',
      scrub:true,
      animation:
          gsap.timeline()
              .to('.section4',{y:'-=100',opacity:1,duration:2})
              .from(['.section4-title','.section4-subtitle','.buttons-container'],{scale:0.5,duration:2},"<")
    })

    // 轮播图
    gsap.set(".box", {
      x: (i) => i * 202
    });
    gsap.to(".box", {
      duration: 7,
      ease: "none",
      x: '+=' + (window.innerWidth + 120) ,
      modifiers: {
        x: gsap.utils.unitize(x => parseFloat(x) % (window.innerWidth + 120))
      },
      repeat: -1
    });
  })();
})

onBeforeUnmount(() => {
  window.removeEventListener('resize',resize);
  window.removeEventListener('beforeunload', saveScrollPosition);
});

onUnmounted(() => {
  enableScroll(); // 确保组件卸载时恢复滚动
  ScrollTrigger.getAll().forEach(trigger => trigger.kill());
  // 取消 requestAnimationFrame
  cancelAnimationFrame(animation);
  cancelAnimationFrame(starAnimation);

  // 移除 resize 监听器
  if (resize) {
    window.removeEventListener('resize', resize);
  }

  // 彻底释放 WebGL 资源
  if (renderer) {
    renderer.forceContextLoss();
    renderer.dispose();
    renderer.domElement.remove();
  }
  if (starRenderer) {
    starRenderer.forceContextLoss();
    starRenderer.dispose();
    starRenderer.domElement.remove();
  }

  scene.traverse((object) => {
    if (object.geometry) object.geometry.dispose();
    if (object.material) {
      if (Array.isArray(object.material)) {
        object.material.forEach((material) => material.dispose());
      } else {
        object.material.dispose();
      }
    }
  });
  scene.clear();
  starScene.clear();
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

/* 网格背景 */
.grid-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9995;
}

/* 背景块 */
.background {
  background-color: #f94604;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9994;
}

/* 装中央Logo的中等大小背景盒 */
.boxLogo {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 350px;
  height: 450px;
  background-color: #f94604;
  border: 1px solid rgba(255, 255, 255, 0.5);
  z-index: 9996;
  overflow: hidden;
}

/* 半透明Logo，层级最高防止被小盒子遮盖 */
.transparentLogo{
  position: absolute;
  width: 175px;
  height: 175px;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
  z-index: 9999;
}

/* 亮色Logo，层级位于小盒子之下，在小盒子移走后显示 */
.logo {
  position: absolute;
  width: 175px;
  height: 175px;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
  z-index: 9997;
}

/* 小盒子，用于遮盖亮色Logo */
.smallBox {
  position: absolute;
  background-color: #f94604;
  width: 175px;
  height: 175px;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
  z-index: 9998;
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

/* 地球位置 */
.earth {
  position: absolute;
  top: 10px;
  left: 70px;
  width: 100%;
  height: 100vh;
  z-index: 2;
}

/* 星空背景 */
.page1,#star-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: 1;
}

/* 首页按钮 */
.buttons-1 {
  position: absolute;
  width: 100px;
  height: auto;
  z-index: 4;
}

/* 首页大标题 */
.section1-title {
  position: absolute;
  top: 27%;
  right: 35%;
  font-size: 64px;
  font-weight: bold;
  color: white;
  z-index: 2;
}

/* 首页副标题 */
.section1-subtitle {
  position: absolute;
  color: rgba(255, 255, 255, 0.85);
  z-index: 2;
  text-shadow: 0 0 8px rgba(255,255,255,0.6);
}

/* 文字光晕 */
.glowing-title {
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.9),
  0 0 18px rgba(0, 180, 255, 0.7),
  0 0 24px rgba(0, 180, 255, 0.5);
}

/* 右上角-副标题 */
.line1 {
  font-size: 24px;
  top: 30%;
  left: 85%;
}

/* 页面中间偏右-副标题 */
.line2 {
  font-size: 28px;
  top: 53%;
  left: 66%;
}

/* 左下角-副标题 */
.line3 {
  font-size: 32px;
  top: 87%;
  left: 40%;
}

/* 第二屏 */
.section2 {
  position: absolute;
  top: 100vh;
  height: 170vh;
  z-index: 10;
}

/* 过渡文字 */
.transition-words {
  position: absolute;
  top: 15%;
  left: 35%;
  height: auto;
  font-size: 48px;
  font-weight: bold;
  color: rgba(0,0,0,0.5);
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.8);
}

/* 过渡文字中需要强调的文字 */
.c1,.c2,.c3,.c4,.c9,.c10,.c12 {
  color: #f94604;
}

/* 进度条 */
.progress {
  position: absolute;
  top: 56%;
  left: 15%;
  width: 75%;
  height: auto;
  z-index: 12;
}

/* 进度条文字 */
.progress-font {
  color: #fffdf3;
}

/* 第二屏大标题 */
.section2-title {
  position: absolute;
  top: 9%;
  left: 15%;
  font-size: 50px;
  font-weight: bold;
  color: #0d0f1a; /* 深色标题，提升对比度 */
  text-shadow: 0 0 8px rgba(0, 0, 0, 0.2); /* 轻微光晕，增加科技感 */
}

/* 第二屏副标题 */
.section2-subtitle {
  position: absolute;
  top: 23%;
  left: 15%;
  font-size: 24px;
  color: #333333;
  font-weight: 500;
  border-bottom: 2px solid rgba(0, 0, 0, 0.4);
  padding-bottom: 5px;
  display: inline-block;
}

/* 第二屏正文 */
.section2-text {
  position: absolute;
  top: 45%;
  left: 15%;
  font-size: 18px;
  color: #444444;
  line-height: 1.6;
  max-width: 600px;
  margin: 20px auto;
  opacity: 0.8;
}

/* 四步进度条 */
.step-item {
  position: absolute;
  top: 40%;
  left: 15%;
  font-size: 30px;
  font-weight: bold;
  color: #333333; /* 默认深色 */
}

/* 第二屏图1 */
.section2-img1 {
  position: absolute;
  top: 21%;
  right: 10%;
  width: 300px;
  height: 400px;
  z-index: 2;
}

/* 第二屏图2 */
.section2-img2 {
  position: absolute;
  top: 18%;
  right: 15%;
  width: 300px;
  height: 400px;
  rotate: -15deg;
  z-index: 1;
}

/* 四页内容 */
.page2,.page3,.page4,.page5 {
  position: absolute;
  top: 60px;
  left: 0;
  height: 100vh;
  width: 100%;
  z-index: 0;
}

/* 过渡文字2 */
.transition-words-2 {
  position: absolute;
  left: 35%;
  top: 30%;
  height: auto;
  font-size: 48px;
  font-weight: bold;
  color: rgba(0,0,0,0.5);
  opacity: 0;
}

/* 第三屏 */
.section3 {
  position: absolute;
  left: 0;
  height: 100vh;
}

/* 粒子背景 */
.particles-container {
  position: absolute;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1;
  background-color: #0d0f1a;
}

/* 四个视频区域 */
.upper-left,.upper-right,.lower-left,.lower-right {
  position: absolute;
  left: 180px;
  top: 80px;
  height: 250px;
  width: 502px;
  z-index: 2;
  filter: blur(5px);
  opacity: 0.5;
}
.upper-right,.lower-right {
  left: 780px;
}
.lower-left,.lower-right {
  top: 380px;
}

/* 四个视频 */
.video1,.video2,.video3,.video4 {
  height: 100%;
  width: 100%;
  object-fit: fill;
  z-index: 2;
}

/* 视频内容文字 */
.video-text-1,.video-text-2,.video-text-3,.video-text-4 {
  position: absolute;
  bottom: 5%;
  left: 50%;
  transform: translateX(-51%);
  text-align: center;
  width: 100%;
  font-size: 32px;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.8);
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.6);
  opacity: 0;
}

/* 第四屏 */
.section4 {
  position: absolute;
  left: 0;
  height: 100vh;
  background-color: var(--bg-color);
  opacity: 0;
  z-index: 6;
}

/* 轮播图盒子 */
.box{
  position:absolute;
  top: 12%;
  left: -120px;
  width:120px;
  height:40px;
  border:1px solid rgba(0,0,0,0.2);
  border-radius: 30px;
  font-size:16px;
  line-height:40px;
  text-align:center;
  z-index: 15;
  color: #f94604;
}

/* 第四屏大标题 */
.section4-title {
  position: absolute;
  top: 30%;
  left: 34%;
  font-size: 36px;
  font-weight: bold;
  color: #0d534b;
}

/* 第四屏副标题 */
.section4-subtitle {
  position: absolute;
  top: 45%;
  left: 29.5%;
  font-size: 18px;
  color: #666;
}

/* 按钮容器 */
.buttons-container {
  position: absolute;
  top: 60%;
  left: 30%;
  width: 40%;
  display: flex;
  justify-content: space-around;
}

/* 第四屏按钮 */
.buttons-4 {
  width: 90px;
  height: 45px;
  font-size: 20px;
}
</style>