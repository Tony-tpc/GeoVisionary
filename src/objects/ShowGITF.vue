<template>
    <div ref="container" id="threeContainer"></div>
    <LoadingProgress 
      v-if="isLoading"
      :progress="progress"
      class="loading-progress"
    />
    <div class="TimeLineBox">
        <div class="TimeLineBox_content">
            <TimeLine bgcolor="light" second="10" :nowValue="nowValue" :yearArr="yearArr"
                @handleNowValueChange="handleNowValueChange" />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, onBeforeMount, computed, toRefs } from "vue";
import TimeLine from "@/components/TimeLine.vue";
import LoadingProgress from "@/components/LoadingProgress.vue";
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const loadingProgress = ref(0);
const loadingRef = ref(null);
const isLoading = ref(true);
const progress = ref(0);

import { useRoute } from "vue-router";


// 时间线相关变量
const nowValue = ref("0:00");
const yearArr = ref([]);
const container = ref(null);
let directionalLight, ambientLight, hemisphereLight;
const sunColor = new THREE.Color();
const currentTime = ref({ hour: 12, minute: 0 }); // 默认中午12点
// Three.js 相关变量
let scene, camera, renderer, controls, model;


const route = useRoute();
let { query } = route

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
});

// 清理资源
onBeforeUnmount(() => {
    if (renderer) {
        renderer.dispose();
        renderer.forceContextLoss();
    }
});

function initThree() {
    // 创建场景
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x101010);

    // 创建相机
    camera = new THREE.PerspectiveCamera(
        75,
        container.value.clientWidth / container.value.clientHeight,
        0.1,
        1000
    );
    camera.position.set(50, 50, 50);

    // 创建渲染器
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.value.clientWidth, container.value.clientHeight);
    container.value.appendChild(renderer.domElement);

    // 添加控制器
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    // // 添加环境光
    // const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    // scene.add(ambientLight);

    // // 添加方向光
    // const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    // directionalLight.position.set(5, 5, 5);
    // scene.add(directionalLight);
    setupAdvancedLighting();
    // 窗口大小变化监听
    window.addEventListener('resize', onWindowResize);
}

// 新增光照设置函数
function setupAdvancedLighting() {
    // 移除旧的光照
    if (directionalLight) scene.remove(directionalLight);
    if (ambientLight) scene.remove(ambientLight);

    // 半球光（模拟天空和地面反射）
    hemisphereLight = new THREE.HemisphereLight(0xffffff, 0x444422, 0.6);
    scene.add(hemisphereLight);

    // 方向光（模拟太阳）
    directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    scene.add(directionalLight);

    // 环境光
    ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);
}



function loadModel() {
    const loader = new GLTFLoader();
    loader.load(
        `/models/${query.id}.glb`,
        (gltf) => {
            isLoading.value = false;
            model = gltf.scene;
            model.scale.set(5, 5, 5);
            model.position.set(0, 0, 0);
            scene.add(model);

            // 自动调整相机位置
            const box = new THREE.Box3().setFromObject(model);
            const center = box.getCenter(new THREE.Vector3());
            const size = box.getSize(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            const fov = camera.fov * (Math.PI / 180);
            let cameraZ = Math.abs(maxDim / (2 * Math.tan(fov / 2)));

            camera.position.set(center.x, center.y+100, cameraZ * 0.8);
            controls.target.copy(center);
            controls.update();
            gltf.scene.traverse(child => {
                if (child.isMesh) {
                    child.castShadow = true;
                    child.receiveShadow = true;
                }
            });
        },
        (xhr) => {
            progress.value = xhr.loaded / xhr.total;
        },
        (error) => {
            console.error('Error loading model:', error);
        }
    );

    // 添加点击事件
    renderer.domElement.addEventListener('click', onCanvasClick);
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
    camera.aspect = container.value.clientWidth / container.value.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.value.clientWidth, container.value.clientHeight);
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
        console.log(currentTime.value);

        updateLighting();
    }
};

// 光照更新函数
function updateLighting() {
    const time = currentTime.value[0] + currentTime.value[1] / 60;

    // 计算太阳高度角（0-24小时映射到0-2π弧度）
    const sunAngle = (time / 24) * Math.PI * 2 - Math.PI / 2;


    // 计算太阳位置
    const sunDistance = 100;
    const sunX = 0;
    const sunY = sunDistance * Math.sin(sunAngle);
    const sunZ = sunDistance * Math.cos(sunAngle);

    // 更新方向光
    directionalLight.position.set(sunX, sunY, sunZ);
    directionalLight.target.position.set(0, 0, 0);

    // 根据时间调整光照颜色和强度，强度曲线（钟形曲线）
    const intensity = Math.max(0.5, Math.exp(-Math.pow((time - 12) / 4, 2)) * 1.5);
    const color = calculateSunColor(time);

    directionalLight.intensity = intensity * 1.5;
    directionalLight.color.set(color);

    // 调整环境光照
    ambientLight.intensity = intensity * 0.3;
    hemisphereLight.intensity = intensity * 0.5;
    // const sunHelper = new THREE.DirectionalLightHelper(directionalLight);
    // scene.add(sunHelper);
}

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
