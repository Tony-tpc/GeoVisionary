<template>
  <!--  加载部分 -->
  <div class="container">
    <!--    背景 -->
    <div class="background"></div>
    <!--    网格背景 -->
    <div class="grid-background">
      <svg class="grid" xmlns="http://www.w3.org/2000/svg" :width="data.width" :height="data.height">
        <g>
          <!-- 外层循环生成行 -->
          <template v-for="(row, rowIndex) in data.rows" :key="'row-' + rowIndex">
            <!-- 内层循环生成列 -->
            <rect
                v-for="(col, colIndex) in data.columns"
                :key="'rect-' + rowIndex + '-' + colIndex"
                :x="colIndex * data.cellSize"
                :y="rowIndex * data.cellSize"
                :width="data.cellSize"
                :height="data.cellSize"
                fill="none"
                stroke="rgba(255, 255, 255, 0.5)"
                stroke-dasharray="3,5"
                :class="['grid-cell', `row-${rowIndex}`, `col-${colIndex}`]"
            />
          </template>
        </g>
      </svg>
    </div>
  <!--    装Logo的中盒子 -->
    <div class="box">
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
  <!--  首页部分 -->
  <div class="page1">
    <el-button type="info" style="position:absolute;top: 300px;margin-left: 350px">点击事件</el-button>
  </div>
  <div class="page2">

  </div>
</template>

<script setup>
import { onMounted,reactive,onUnmounted } from "vue";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

const data = reactive({
  width: window.innerWidth,     // SVG 宽度
  height: window.innerHeight,     // SVG 高度
  cellSize: 40,                   // 每个方格的边长
  rows: [],                       // 行数组
  columns: [],                     // 列数组
});



onMounted(() => {
  data.rows = Array.from({ length: Math.ceil(data.height / data.cellSize) }); // 生成行数组
  data.columns = Array.from({ length: Math.ceil(data.width / data.cellSize) }); // 生成列数组

  const t = gsap.timeline()
  // 背景颜色变化
  t.from([".background",".box",".smallBox"], {
    backgroundColor: "#000000",
    duration: 1,
  });

  // 背景缩放
  t.from([".grid-background",".box"], {
    scale: 2,
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
  t.to(".box",{
    opacity:0,
    yoyo:true,
    repeat:15,
    duration:0.04,
  },">");

  // 移除加载页面，呈现主页
  t.to(".container",{
    y:"-200vh",
    duration: 1.1,
    ease:"power2.in",
  },1.9);

  t.to(".page1",{
    y: "-100vh",
    duration: 1.1,
    ease:"power2.in",
  },"<");

});


</script>

<style scoped>
/* 父容器 */
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
  z-index: 2;
}

/* 背景块 */
.background {
  background-color: #f94604;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

/* 装中央Logo的中等大小背景盒 */
.box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 350px;
  height: 450px;
  background-color: #f94604;
  border: 1px solid rgba(255, 255, 255, 0.5);
  z-index: 3;
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
  z-index: 6;
}

/* 亮色Logo，层级位于小盒子之下，在小盒子移走后显示 */
.logo {
  position: absolute;
  width: 175px;
  height: 175px;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
  z-index: 4;
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
  z-index: 5;
}

.page1, .page2{
  position: absolute;
  top: 100vh;
  width: 100%;
  height: 100vh;
  z-index: 0;
}
</style>
