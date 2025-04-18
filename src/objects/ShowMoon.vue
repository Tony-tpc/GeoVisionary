<template>
  <div ref="container" class="canvas-container">
  </div>
  <div class="page1" id="star-background"></div>
  <div class="info-box">
    <transition name="phase-fade" mode="out-in">
      <div :key="currentPhase" class="phase-content">
        <h2 class="phase-title">{{ phaseData[currentPhase]?.title }}</h2>
        <p class="phase-desc">{{ phaseData[currentPhase]?.description }}</p>
        <div class="phase-custom">
          <span class="highlight">{{ phaseData[currentPhase].custom }}</span>
        </div>
      </div>
    </transition>
  </div>
  <div class="TimeLineBox">
    <div class="TimeLineBox_content">
      <TimeLine bgcolor="light" second="10" :nowValue="nowValue" :yearArr="yearArr"
                @handleNowValueChange="handleNowValueChange" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, shallowRef } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import TimeLine from "@/components/TimeLine.vue";
import {throttle} from "lodash";
const container = shallowRef(null)
let scene, camera, renderer, controls, moonRenderer
const moon = shallowRef(null)
const earth = shallowRef(null)
const star = shallowRef(null)
const textureLoader = new THREE.TextureLoader()
const currentPhase = ref('新月');
const phaseData = {
  "新月": {
    title: "🌑 新月",
    description: "月球位于地球和太阳之间，不可见阶段",
    custom: "   传统上，新月象征着新的开始，人们常在此时许愿祈福，祈求心愿达成。在农历中，新月常为每月初一，许多节日和祭祖仪式也会选择此时举行，寓意重生与希望。科学上，新月是进行深空观测的黄金时期。"
  },
  "上弦月": {
    title: "🌓 上弦月",
    description: "右侧被照亮，月相呈D形增长",
    custom: "   上弦月时期，正值农历初七至初八，是传统农耕社会播种、栽种作物的重要时节，寓意着万物生长的力量增强。潮汐渐退，渔民亦会根据月相调整出海时间，保证收成与安全。同时此时身体阳气上升，适宜养阳健体。"
  },
  "满月": {
    title: "🌕 满月",
    description: "月球完全被太阳照亮，最佳观测时机",
    custom: "   满月是中国文化中团圆与丰收的象征，最具代表性的是中秋节，全家团聚共赏明月、品尝月饼、吟诵诗词。古人也常借满月抒发思乡之情。民间认为此时月华最盛，适合祈福纳祥，亦是举行月神祭祀的吉日。"
  },
  "下弦月": {
    title: "🌗 下弦月",
    description: "左侧被照亮，月相逐渐消退",
    custom: "   下弦月通常出现在农历二十二左右，是传统中调养身体、收敛心神的阶段，讲究“静养内收”。古代航海者则利用较为平稳的潮汐选择此时远行。民间习俗中也有在此时整理家务、反思总结、准备新周期的传统。"
  }
};


// 时间轴参数
const nowValue = ref("0:00");
const yearArr = ref([]);

// 画中画相关变量
let moonCamera, starCamera, starScene, starRenderer, starAnimation, resize;
const moonViewportSize = { width: 200, height: 200 }

// 天文参数
const EARTH_RADIUS = 5
const MOON_RADIUS = 1.5
const ORBIT_RADIUS = 15

const clock = new THREE.Clock()

async function initScene() {
  const [earthTex, moonTex] = await Promise.all([
    textureLoader.loadAsync('/textures/earth.webp'),
    textureLoader.loadAsync('/textures/moon.webp')
  ])

  // 主场景初始化
  scene = new THREE.Scene()
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.outputEncoding = THREE.sRGBEncoding
  renderer.setSize(window.innerWidth, window.innerHeight)
  renderer.setClearColor("0x000000",0)
  container.value.appendChild(renderer.domElement)

  // 光照设置
  const ambientLight = new THREE.AmbientLight(0x404040, 2)
  scene.add(ambientLight)
  const directionalLight = new THREE.DirectionalLight(0xffffff, 2)
  directionalLight.position.set(100, 0, 0)
  scene.add(directionalLight)

  // 地球
  const earthGeometry = new THREE.SphereGeometry(EARTH_RADIUS, 32, 32)
  const earthMaterial = new THREE.MeshPhongMaterial({
    map: earthTex,
    specular: 0x222222,
    shininess: 100
  })
  earth.value = new THREE.Mesh(earthGeometry, earthMaterial)
  scene.add(earth.value)

  // 月球
  const moonGeometry = new THREE.SphereGeometry(MOON_RADIUS, 32, 32)
  const moonMaterial = new THREE.MeshPhongMaterial({
    map: moonTex,
    specular: 0x111111,
    shininess: 30
  })
  moon.value = new THREE.Mesh(moonGeometry, moonMaterial)
  moon.value.position.set(ORBIT_RADIUS, 0, 0)
  // 调整月轴倾斜（真实月球有约6.68°的轴向倾角）
  moon.value.rotation.y = THREE.MathUtils.degToRad(-6.68)
  scene.add(moon.value)
  // 添加地球天轴（倾斜23.5度）
  const axisGeometry = new THREE.CylinderGeometry(0.05, 0.05, EARTH_RADIUS * 3, 8)
  const axisMaterial = new THREE.MeshBasicMaterial({
    color: 0xffffff,
    transparent: true,
    opacity: 1.0
  })
  const earthAxis = new THREE.Mesh(axisGeometry, axisMaterial)
  earthAxis.rotation.z = THREE.MathUtils.degToRad(23.5)
  earth.value.add(earthAxis) // 将天轴作为地球的子对象

  // 添加月球轨道指示线
  const orbitGeometry = new THREE.RingGeometry(
      ORBIT_RADIUS - 0.1,
      ORBIT_RADIUS + 0.1,
      64
  )
  const orbitMaterial = new THREE.MeshBasicMaterial({
    color: 0x888888,
    side: THREE.DoubleSide,
    transparent: true,
    opacity: 0.3
  })
  const orbit = new THREE.Mesh(orbitGeometry, orbitMaterial)
  orbit.rotation.x = Math.PI / 2 // 平铺在XZ平面
  scene.add(orbit)

  // 启用阴影支持
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap

  // 配置地球和月球的阴影
  earth.value.castShadow = true
  earth.value.receiveShadow = true
  moon.value.castShadow = true
  moon.value.receiveShadow = true
  // 初始化画中画系统
  // 画中画摄像机
  moonCamera = new THREE.PerspectiveCamera(
      15,
      moonViewportSize.width / moonViewportSize.height,
      0.1,
      1000
  )

  // 摄像机控制
  camera.position.set(0, 20, -20)
  controls = new OrbitControls(camera, renderer.domElement)
}

// 时间线变化事件
const handleNowValueChange = (hourArr) => {
  console.log(hourArr);

  moon.value.position.x = Math.cos(hourArr * 2 * Math.PI) * ORBIT_RADIUS
  moon.value.position.z = -Math.sin(hourArr * 2 * Math.PI) * ORBIT_RADIUS

  if (hourArr < 1 / 8) {
    currentPhase.value = '新月'
  } else if (hourArr < 3 / 8) {
    currentPhase.value = '上弦月'
  } else if (hourArr < 5 / 8) {
    currentPhase.value = '满月'
  } else if (hourArr < 7 / 8) {
    currentPhase.value = '下弦月'
  } else {
    currentPhase.value = '新月'
  }

};

function animate() {
  requestAnimationFrame(animate)
  moon.value.lookAt(earth.value.position)


  // 更新画中画摄像机
  updateMoonCamera()
  moonRenderer.render(scene, moonCamera) // 先渲染画中画
  renderer.render(scene, camera)            // 再渲染主场景
}

function updateMoonCamera() {
  // 从地球视角观察月球
  const earthPos = new THREE.Vector3(0, 0, 0) // 地球位于原点
  const moonPos = moon.value.position.clone()

  moonCamera.position.copy(earthPos)
  // moonCamera.position.y = EARTH_RADIUS
  moonCamera.lookAt(moonPos)

  // 动态调整剪裁平面
  const distance = earthPos.distanceTo(moonPos)
  moonCamera.far = distance * 2
  moonCamera.updateProjectionMatrix()
}

onMounted(async () => {
  setTimeout(() => {
    yearArr.value = ["新月", "上弦月", "满月", "下弦月", "新月"];
  }, 100);
  await initScene();

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
    console.log(`starRenderer: ${starRenderer}`)
    document.getElementById('star-background').appendChild(starRenderer.domElement);

    // 创建星空粒子
    const starsGeometry = new THREE.BufferGeometry();
    const starsVertices = [];
    for (let i = 0; i < 2500; i++) {  // 500 颗星星
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


    starCamera.position.z = 50;
    function starAnimate() {
      starAnimation = requestAnimationFrame(starAnimate);
      starField.rotation.y += 0.0002;  // 缓慢旋转
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

  // 创建画中画canvas
  const moonCanvas = document.createElement('canvas')
  moonCanvas.className = 'moon-viewport'
  container.value.appendChild(moonCanvas)

  // 初始化画中画渲染器
  moonRenderer = new THREE.WebGLRenderer({
    canvas: moonCanvas,
    antialias: true,
    alpha: true
  })
  moonRenderer.setSize(moonViewportSize.width, moonViewportSize.height)
  moonRenderer.setClearColor(0x000000, 0)

  // 启动动画循环
  animate()
})

onUnmounted(() => {
  // 清理资源
  if (moonRenderer) {
    moonRenderer.dispose()
  }
})
</script>

<style>
.canvas-container {
  position: relative;
  width: 100vw;
  height: 100vh;
}

.moon-viewport {
  position: fixed;
  top: 80px;
  right: 50px;
  width: 200px;
  height: 200px;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
  background: rgba(0, 0, 0, 0.3);
  pointer-events: none;
}

.TimeLineBox {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  background-color: rgba(0, 0, 0, 0);
  padding: 5px;
  border-radius: 2px;
}

.TimeLineBox_content {
  position: relative;
  width: 800px;
  height: 90px;
  margin-top: 10px;
  text-align: center;
}

.info-box {
  /* 位置调整 */
  position: fixed;
  left: 40px;
  bottom: 35%;
  width: 300px;
  height: 250px;

  /* 字体优化 */
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell;
  line-height: 1.5;
  padding: 20px;
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.phase-title {
  font-size: 1.6em;
  margin: 0 0 12px 0;
  font-weight: 600;
  letter-spacing: 0.5px;
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.phase-desc {
  font-size: 1em;
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
  line-height: 1.4;
}

/* 渐变背景 */
.info-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(18, 194, 233, 0.1) 0%, rgba(196, 113, 237, 0.1) 100%);
  border-radius: 12px;
  z-index: -1;
}

/* 淡入淡出动画 */
.phase-fade-enter-active,
.phase-fade-leave-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.phase-fade-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.phase-fade-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

.phase-custom {
  background: rgba(100, 181, 246, 0.1);
  padding: 12px;
  border-radius: 6px;
  margin-top: 15px;
}

.highlight {
  color: #FFF59D;
  font-weight: 500;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* 星空背景 */
.page1,#star-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: -1;
}
</style>
