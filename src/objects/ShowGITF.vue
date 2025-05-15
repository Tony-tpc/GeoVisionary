<template>
    <div ref="container" id="threeContainer"></div>
    <LoadingProgress
      v-if="isLoading"
      :progress="progress"
      class="loading-progress"
    />
    <div class="TimeLineBox">
        <div class="TimeLineBox_content">
            <TimeLine bgcolor="light" :second=10 :nowValue="nowValue" :yearArr="yearArr"
                @handleNowValueChange="handleNowValueChange" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, onBeforeMount, computed, toRefs, provide,reactive } from "vue";
import { useRoute } from "vue-router";
import TimeLine from "@/components/TimeLine.vue";
import LoadingProgress from "@/components/LoadingProgress.vue";
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { Sky } from 'three/addons/objects/Sky.js';
import config from '@/store/config.json'
const loadingProgress = ref(0);
const loadingRef = ref(null);
const isLoading = ref(true);
const progress = ref(0);

// 时间线相关变量
const nowValue = ref("0:00");
const yearArr = ref([]);
const container = ref(null);
let directionalLight, ambientLight, hemisphereLight;
const sunColor = new THREE.Color();
const currentTime = ref({ 0:12, 1:0 }); // 默认中午12点
// Three.js 相关变量
let scene, camera, renderer, controls, model;
const route = useRoute();
let { query } = route

// 天空系统相关
let sky, sun;
const skyParams = reactive({
  turbidity: 10,    // 提高浊度使天空更明显
  rayleigh: 3,      // 增强瑞利散射
  mieCoefficient: 0.005,
  mieDirectionalG: 0.7,
  elevation: 45,    // 初始高度角
  azimuth: 180
});

// 初始化时间线数据
onBeforeMount(() => {
    setTimeout(() => {
        yearArr.value = ["0:00", "6:00", "12:00", "18:00", "24:00"];
    }, 100);
});

// Three.js 初始化
onMounted(() => {
    initThree();
    loadModel();
    animate();
    updateLighting();
});

// 清理资源
onBeforeUnmount(() => {
  if (renderer) {
    renderer.forceContextLoss();
    renderer.dispose();
    renderer.domElement.remove();
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
});

function initThree() {
    // 创建场景
    scene = new THREE.Scene();

    // 创建相机
    camera = new THREE.PerspectiveCamera(
        75,
        container.value.clientWidth / container.value.clientHeight,
        0.1,
        1000
    );
    camera.position.set(50, 50, 50);

    // 创建渲染器
    renderer = new THREE.WebGLRenderer({ antialias: true,logarithmicDepthBuffer:true });
    renderer.setSize(container.value.clientWidth, container.value.clientHeight);
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 0.8;
    container.value.appendChild(renderer.domElement);

    // 添加控制器
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // // 添加环境光
    // const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    // scene.add(ambientLight);

    // // 添加方向光
    // const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    // directionalLight.position.set(5, 5, 5);
    // scene.add(directionalLight);
    setupAdvancedLighting();
    initSky();
    // 窗口大小变化监听
    window.addEventListener('resize', onWindowResize);
}

function initSky() {
  // 创建天空系统
  sky = new Sky();
  sky.scale.setScalar(45000); // 根据场景调整比例
  scene.add(sky);

  // 配置天空材质
  const uniforms = sky.material.uniforms;
  uniforms['turbidity'].value = skyParams.turbidity;
  uniforms['rayleigh'].value = skyParams.rayleigh;
  uniforms['mieCoefficient'].value = skyParams.mieCoefficient;
  uniforms['mieDirectionalG'].value = skyParams.mieDirectionalG;

  // 初始化太阳位置
  sun = new THREE.Vector3();
  updateSunPosition();
}

function setupAdvancedLighting() {
  // 方向光配置（与天空同步）
  directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
  directionalLight.castShadow = true;
  directionalLight.shadow.mapSize.width = 2048;
  directionalLight.shadow.mapSize.height = 2048;
  scene.add(directionalLight);

  // 环境光配置
  ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
  scene.add(ambientLight);
}

function updateSunPosition() {
  const phi = THREE.MathUtils.degToRad(90 - skyParams.elevation);
  const theta = THREE.MathUtils.degToRad(skyParams.azimuth);

  // 更新太阳位置（天空和光源同步）
  sun.setFromSphericalCoords(1, phi, theta);
  sky.material.uniforms['sunPosition'].value.copy(sun);
  directionalLight.position.copy(sun);
}

function updateLighting() {
  const time = currentTime.value[0] + currentTime.value[1] / 96;

  // 将时间转换为太阳角度（0-24小时对应-90到+90度）
  skyParams.elevation = THREE.MathUtils.mapLinear(time, 0, 24, -75, 225);

  // 动态调整大气参数
  skyParams.turbidity = time > 6 && time < 18 ? 10 : 2;
  skyParams.rayleigh = time > 6 && time < 18 ? 3 : 0.5;

  // 更新天空参数
  const uniforms = sky.material.uniforms;
  uniforms['turbidity'].value = skyParams.turbidity;
  uniforms['rayleigh'].value = skyParams.rayleigh;
  uniforms['mieCoefficient'].value = skyParams.mieCoefficient;
  uniforms['mieDirectionalG'].value = skyParams.mieDirectionalG;

  updateSunPosition();
}

// 模型加载函数（保持原有逻辑，增加比例调整）
function loadModel() {
  const loader = new GLTFLoader();
  loader.load(
      `/models/${query.id}.glb`,
      (gltf) => {
        isLoading.value = false;
        model = gltf.scene;

        const posConfig = config[query.id].pos;
        const scaleConfig = config[query.id].scale;
        const cameraConfig = config[query.id].camera;
        const pos = {
          x: posConfig?.x || 0,
          y: posConfig?.y || -5,
          z: posConfig?.z || 0,
        }
        const scale = {
          x: scaleConfig?.x || 5,
          y: scaleConfig?.y || 5,
          z: scaleConfig?.z || 5,
        }

        // 调整模型比例（建议缩小以适应天空）
        model.scale.set(scale.x, scale.y, scale.z);
        model.position.set(pos.x, pos.y, pos.z);

        // 包围盒计算
        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        // 相机位置调整
        const maxDim = Math.max(size.x, size.y, size.z);
        const fov = camera.fov * (Math.PI / 180);
        const cameraZ = Math.abs(maxDim / (2 * Math.tan(fov / 2)));
        camera.position.set(center.x + cameraConfig?.x || 0, center.y + cameraConfig?.y || 10, cameraZ * 0.8);
        camera.lookAt(center);

        // 阴影处理
        model.traverse((child) => {
          if (child.isMesh) {
            child.castShadow = true;
            child.receiveShadow = true;
          }
        });

        scene.add(model);
      },
      (xhr) => {
        progress.value = xhr.loaded / xhr.total;
      },
      (error) => {
        console.error('Error loading model:', error);
      }
  );
  renderer.domElement.addEventListener('click',onCanvasClick);
}

function onCanvasClick(event) {
    // 计算鼠标位置（归一化设备坐标）
    const rect = renderer.domElement.getBoundingClientRect();
    const mouse = new THREE.Vector2(
        ((event.clientX - rect.left) / rect.width) * 2 - 1,
        -((event.clientY - rect.top) / rect.height) * 2 + 1
    );

    // 设置射线投射
    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(mouse, camera);

    // 计算相交物体
    const intersects = raycaster.intersectObjects(scene.children, true);

    if (intersects.length > 0) {
        const point = intersects[0].point;
        console.log("点击位置:", point);

        //   // 这里可以添加点击后的可视化效果
        //   const sphere = new THREE.Mesh(
        //     new THREE.SphereGeometry(0.5),
        //     new THREE.MeshBasicMaterial({ color: 0xff0000 })
        //   );
        //   sphere.position.copy(point);
        //   scene.add(sphere);
    }
}

function onWindowResize() {
  if (!container.value) return; // 防止空引用

  const width = container.value.clientWidth || 1;
  const height = container.value.clientHeight || 1;

  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

// 时间线变化事件处理
const handleNowValueChange = (hourArr) => {
    if (model) {
        let rettime = ref([0, 0])// hour minute
        rettime.value[0] = Math.floor(hourArr * 120 / 5);
        rettime.value[1] = Math.floor(hourArr * 120) % 5 * 24;

        // const intensity = hourArr.value[0] / 24;
        // model.traverse((child) => {
        //     if (child.isMesh) {
        //         child.material.emissiveIntensity = intensity;
        //     }
        // });
        currentTime.value = rettime.value;

        updateLighting();
    }
};


// 光照颜色计算函数
function calculateSunColor(time) {
    const hue = THREE.MathUtils.lerp(0.14, 0.55,
        Math.abs(time - 12) / 12
    );
    const saturation = 1 - Math.abs(time - 12) / 12 * 0.5;
    const lightness = 0.5 + Math.abs(time - 12) / 12 * 0.3;

    return sunColor.setHSL(hue, saturation, lightness);
}
</script>

<style>
#threeContainer {
    width: 100%;
    height: 100vh;
    position: relative;
    overflow: hidden;
}

.TimeLineBox {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 10;
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

canvas {
    display: block;
}

.loading-progress {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  transition: opacity 0.5s ease-out;
}

.loading-progress {
  --progress-color: #42b883;
  --jump-animation: jump 0.8s infinite alternate;
}

@keyframes jump {
  0% { transform: translateY(0); }
  100% { transform: translateY(-20px); }
}
</style>
