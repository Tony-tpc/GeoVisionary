<template>
  <div id="video-particles" class="particles-container"></div>
  <!--  <div class="test-fixed">我是测试 Fixed</div>-->
<!--  <div class="page2" id="earth-background">-->
<!--    <el-button type="primary" style="position: absolute;top: 250px;left: 300px">基本按钮</el-button>-->
<!--  </div>-->
<!--  <div class="page3">-->
<!--    <div style="position: absolute;top: 2000px;left: 100px;font-weight: bold;font-size: 30px">THIS IS MY WORLD!</div>-->
<!--  </div>-->
<!--  <div class="page4" id="star-background">-->

<!--  </div>-->

<!--  <section>-->
<!--    <div class="container section1">-->
<!--      <div class="earth" id="earth-background"></div>-->
<!--      <div class="page1" id="star-background"></div>-->
<!--      <div class="buttons" style="top: 600px;left: 350px">-->
<!--        <el-button type="primary" @click="changeSpeed">-->
<!--          <span v-if="data.rotateSpeed > 0">停止转动</span>-->
<!--          <span v-else>继续转动</span>-->
<!--        </el-button>-->
<!--      </div>-->
<!--      <div class="hero-title glowing-title floating-title">-->
<!--        智绘山河-->
<!--      </div>-->
<!--      <div class="line1 hero-subtitle">AI 赋能探索</div>-->
<!--      <div class="line2 hero-subtitle">让地理更智慧</div>-->
<!--      <div class="line3 hero-subtitle">用科技丈量世界</div>-->
<!--    </div>-->
<!--  </section>-->
<!--  <section>-->

<!--    <div class="container section2">-->
<!--      &lt;!&ndash;    过渡文字  &ndash;&gt;-->
<!--      <div class="transition-words">-->
<!--        <span class="c1">探索</span>-->
<!--        <span class="c2">世界，</span>-->
<!--        <span class="c3">从</span>-->
<!--        <span class="c4">这里</span>-->
<!--        <span class="c5">启程。</span>-->
<!--      </div>-->
<!--      &lt;!&ndash;    智绘天地介绍  &ndash;&gt;-->
<!--      <div class="page2">-->
<!--        <h2 class="section-title">🌍 直观可视化，探索地理奥秘</h2>-->
<!--        <div class="step-indicator">Step 1: 了解</div>-->
<!--        <p class="section-subtitle">沉浸式 3D 体验，让你身临其境</p>-->
<!--        <p class="section-content">通过 3D 交互地球、气候模型等，让地理知识变得生动形象。</p>-->
<!--      </div>-->
<!--      &lt;!&ndash;    进度条  &ndash;&gt;-->
<!--      <el-progress-->
<!--          :percentage="data.percentage[0]"-->
<!--          :text-inside="true"-->
<!--          :stroke-width="30"-->
<!--          striped-->
<!--          striped-flow-->
<!--          :duration="5"-->
<!--          class="progress"-->
<!--      >-->
<!--        <span v-if="data.percentage[0] < 25">智绘天地</span>-->
<!--        <span v-else-if="data.percentage[0] < 50">知象图谱</span>-->
<!--        <span v-else-if="data.percentage[0] < 75">探知问学</span>-->
<!--        <span v-else>智荐学堂</span>-->
<!--        <span>{{ parseInt(data.percentage[0]) }}%</span>-->
<!--      </el-progress>-->
<!--      &lt;!&ndash;    知象图谱介绍  &ndash;&gt;-->
<!--      <div class="page3">-->
<!--        <h2 class="section-title">📊 知识图谱 + AI 互动</h2>-->
<!--        <div class="step-indicator">Step 2: 学习</div>-->
<!--        <p class="section-subtitle">结构化知识，AI 助教解答</p>-->
<!--        <p class="section-content">利用 AI 技术构建地理知识图谱，ChatGPT 即时答疑。</p>-->
<!--      </div>-->
<!--      &lt;!&ndash;    探知问学介绍  &ndash;&gt;-->
<!--      <div class="page4">-->
<!--        <h2 class="section-title">📝 智能测评，精准诊断</h2>-->
<!--        <div class="step-indicator">Step 3: 测试</div>-->
<!--        <p class="section-subtitle">找到薄弱点，针对性提升</p>-->
<!--        <p class="section-content">个性化智能习题，AI 自动解析，助你突破难点。</p>-->
<!--      </div>-->
<!--      &lt;!&ndash;    智荐学堂介绍  &ndash;&gt;-->
<!--      <div class="page5">-->
<!--        <h2 class="section-title">🎯 个性化推荐，定制学习路线</h2>-->
<!--        <div class="step-indicator">Step 4: 巩固</div>-->
<!--        <p class="section-subtitle">智能推荐，学习不再盲目</p>-->
<!--        <p class="section-content">根据你的学习轨迹，AI 自动推送最适合的资源。</p>-->
<!--      </div>-->
<!--    </div>-->
<!--  </section>-->
</template>

<script setup>
import {onBeforeUnmount, onMounted, reactive} from "vue";
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import MeteorClass from "@/classes/meteor.js";
import * as THREE from "three";
import {gsap} from "gsap";
import {ScrollTrigger} from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger)

let resize

const data = reactive({
  percentage:0,

})

onMounted(() => {
  /* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
  particlesJS("video-particles", {
    particles: {
      number: { value: 60 },
      size: { value: 2 },
      move: { speed: 2 },
      opacity: { anim: { enable: true, speed: 0.5 } },
    },
  });
  // ScrollTrigger.create({
  //   trigger: '.section2',
  //   start: 'top+=50 top',
  //   end: '+=5000',
  //   scrub: true,
  //   pin:true,
  //   animation:
  //       gsap.timeline()
  //           .to('.transition-words',{opacity:0},0)
  //           .from('.progress',{opacity:0},0)
  //           .from('.page2',{opacity:0,duration:1},0)
  //           .to(data.percentage,{endArray:[100],duration:8,ease:'none'},1)
  //           .to('.page2',{x:() => '-=' + document.querySelector('.section2').offsetWidth},3)
  //           .from('.page3',{x:() => '+=' + document.querySelector('.section2').offsetWidth},3)
  //           .to('.page3',{x:() => '-=' + document.querySelector('.section2').offsetWidth},5)
  //           .from('.page4',{x:() => '+=' + document.querySelector('.section2').offsetWidth},5)
  //           .to('.page4',{x:() => '-=' + document.querySelector('.section2').offsetWidth},7)
  //           .from('.page5',{x:() => '+=' + document.querySelector('.section2').offsetWidth},7)
  // })
  // const scene = new THREE.Scene();
  // const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  // camera.position.set(0, 0, 5);
  //
  // const renderer = new THREE.WebGLRenderer({ antialias: true });
  // renderer.setSize(window.innerWidth, window.innerHeight);
  // renderer.setClearColor(new THREE.Color(0x404040))
  // document.getElementById('earth-background').appendChild(renderer.domElement);
  //
  // const controls = new OrbitControls(camera, renderer.domElement);
  // controls.enableDamping = true;
  // controls.dampingFactor = 0.05;

// // 地球
//   const textureLoader = new THREE.TextureLoader();
//   const earthTexture = textureLoader.load('/src/assets/2k_earth_daymap.jpg');
//   const earthGeometry = new THREE.SphereGeometry(1, 32, 32);
//   const earthMaterial = new THREE.MeshStandardMaterial({ map: earthTexture });
//   const earth = new THREE.Mesh(earthGeometry, earthMaterial);
//   scene.add(earth);
//
// // 光源
//   const ambientLight = new THREE.AmbientLight(0x404040);
//   scene.add(ambientLight);
//
//   const pointLight = new THREE.PointLight(0xffffff, 50);
//   pointLight.position.set(5, 5, 5);
//   scene.add(pointLight);
//
// // 星空
//   const starsGeometry = new THREE.SphereGeometry(50, 64, 64);
//   const starsMaterial = new THREE.MeshBasicMaterial({
//     map: textureLoader.load('https://api.allorigins.win/get?url=' + encodeURIComponent('https://example.com/stars_texture.jpg')),
//     side: THREE.BackSide,
//   });
//   const stars = new THREE.Mesh(starsGeometry, starsMaterial);
//   scene.add(stars);
//
// // 动画
//   function animate() {
//     requestAnimationFrame(animate);
//     earth.rotation.y += 0.005;
//     controls.update();
//     renderer.render(scene, camera);
//   }
//
//   animate();

  // // 创建星空部分
  // (function (){
  //   const starScene = new THREE.Scene();
  //   const starCamera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
  //   const starRenderer = new THREE.WebGLRenderer({ alpha: true });
  //   starRenderer.setSize(
  //       document.getElementById('star-background').offsetWidth,
  //       document.getElementById('star-background').offsetHeight
  //   );
  //   starRenderer.setClearColor(0x0d0f1a)
  //   document.getElementById('star-background').appendChild(starRenderer.domElement);
  //   // 创建星空粒子
  //   const starsGeometry = new THREE.BufferGeometry();
  //   const starsVertices = [];
  //   for (let i = 0; i < 800; i++) {  // 800 颗星星
  //     let x = (Math.random() - 0.5) * 2000;
  //     let y = (Math.random() - 0.5) * 2000;
  //     let z = (Math.random() - 0.5) * 2000;
  //     starsVertices.push(x, y, z);
  //   }
  //   starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
  //   const starsMaterial = new THREE.PointsMaterial({ color: 0xffffff, size: 2 });
  //   const starField = new THREE.Points(starsGeometry, starsMaterial);
  //   starScene.add(starField);
  //
  //   const meteors = []; // 用于存储流星实例
  //
  //   const meteorConfigs = [
  //     { color: { left: new THREE.Color("#0000ff"), right: new THREE.Color("#00ffff") }, duration: 1.2, hideDuration: 1, position: new THREE.Vector3(25,  25, -150), target: new THREE.Vector3(250,30, -150) }, // 左侧
  //     { color: { left: new THREE.Color("#00aaff"), right: new THREE.Color("#ffffff") }, duration: 1.8, hideDuration: 0.6, position: new THREE.Vector3(50,  17, 0),  target: new THREE.Vector3(430,430, 0) }, // 中间
  //     { color: { left: new THREE.Color("#ffffff"), right: new THREE.Color("#0000ff") }, duration: 1.9, hideDuration: 0.7, position: new THREE.Vector3(60,  -6, 0),  target: new THREE.Vector3(400, 400, 0) } // 右侧
  //   ];
  //
  //   meteorConfigs.forEach(config => {
  //     const meteor = new MeteorClass(
  //         1000,
  //         config.target, // 目的地
  //         config.color, // 颜色
  //         1,
  //         config.duration, // 飞行时长
  //         config.hideDuration, // 消失时长
  //     );
  //     starScene.add(meteor.group);
  //     // 将流星组的位置设置为配置中的位置
  //     meteor.group.position.set(config.position.x, config.position.y, config.position.z);
  //     // 旋转流星组
  //     meteor.group.rotateZ(Math.PI / 0.9);
  //     meteors.push(meteor);
  //   });
  //
  //   starCamera.position.z = 50;
  //   function starAnimate() {
  //     requestAnimationFrame(starAnimate);
  //     starField.rotation.y += 0.0002;  // 缓慢旋转
  //     meteors.forEach(meteor => meteor.update()); // 更新所有流星
  //     starRenderer.render(starScene, starCamera);
  //   }
  //   starAnimate();
  //
  //   // 添加 resize 事件监听器以及时调整窗口大小
  //   resize = () => {
  //     const width = document.getElementById('star-background').offsetWidth;
  //     const height = document.getElementById('star-background').offsetHeight;
  //
  //     starRenderer.setSize(width, height);
  //     starCamera.aspect = width / height;
  //     starCamera.updateProjectionMatrix();
  //   };
  //   window.addEventListener('resize', resize);
  //   resize(starRenderer,starCamera);
  //
  // })();
})

onBeforeUnmount( () => {
  // window.removeEventListener('resize',resize);
});
</script>

<style scoped>

.background {
  position: absolute;
  display: block;
  top: 0;
  left: 0;
  z-index: 0;
}


.page2 {
  position: absolute;
  width: 100%;
  height: 100vh;
  top: 100vh;
}


/* 第二部分，根据需要加长 */
.section2 {
  position: absolute;
  top: 100vh;
  height: 170vh;
}
/* 过渡文字 */
.transition-words {
  position: absolute;
  top: 12%;
  left: 35%;
  height: auto;
  font-size: 48px;
  font-weight: bold;
  color: rgba(0,0,0,0.5);
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.8);
}
/* 过渡文字中需要强调的文字 */
.c1,.c2,.c5 {
  color: #f94604;
}
.container {
  position: relative;
  width: 100%;
  height: 100vh;
  background-color: var(--bg-color);
  overflow: hidden;
}
/* 进度条 */
.progress {
  position: absolute;
  top: 50%;
  left: 15%;
  width: 75%;
  height: auto;
  z-index: 5;
}

.step-indicator {
  display: inline-block;
  padding: 6px 16px;
  background: var(--secondary-color);
  color: white;
  font-size: 16px;
  font-weight: bold;
  border-radius: 20px;
}
.section-content {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.8);
  max-width: 600px;
  line-height: 1.6;
  text-align: left;
  transform: translateY(20px);
}
.section-subtitle {
  font-size: 24px;
  font-weight: 400;
  color: #e0e0e0;
  transform: translateY(20px);
}
.section-title {
  font-size: 48px;
  font-weight: bold;
  color: white;
  text-shadow: 0 0 12px rgba(255, 255, 255, 0.8);
}

.page2,.page3,.page4,.page5 {
  position: absolute;
  top: 45px;
  left: 0;
  height: 100vh;
  width: 100%;
  background-color: #333333;
  z-index: 0;
}
.page3 {
  background-color: #999999;
}
.page4 {
  background-color: red;
}
.page5 {
  background-color: blue;
}
.test-fixed {
  position: fixed;
  top: 50px;
  left: 50px;
  background: red;
  color: white;
  padding: 10px;
  z-index: 9999;
}
</style>
