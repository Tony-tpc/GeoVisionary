<template>
    <div ref="container" class="canvas-container">
        <!-- 观察窗口canvas将通过JS动态添加 -->
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
const container = shallowRef(null)
let scene, camera, renderer, controls, moonRenderer
const moon = shallowRef(null)
const earth = shallowRef(null)
const star = shallowRef(null)
const textureLoader = new THREE.TextureLoader()


// 时间轴参数
// 时间线相关变量
const nowValue = ref("0:00");
const yearArr = ref([]);
const hourArr = ref([]);

// 画中画相关变量
let moonCamera, moonScene
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
    initMoonViewport()

    // 摄像机控制
    camera.position.set(0, 20, -20)
    controls = new OrbitControls(camera, renderer.domElement)
}

// 时间线变化事件
const handleNowValueChange = (hourArr) => {
    moon.value.position.x = Math.cos(hourArr * 2 * Math.PI) * ORBIT_RADIUS
    moon.value.position.z = -Math.sin(hourArr * 2 * Math.PI) * ORBIT_RADIUS
};

function initMoonViewport() {
    // 画中画摄像机
    moonCamera = new THREE.PerspectiveCamera(
        15,
        moonViewportSize.width / moonViewportSize.height,
        0.1,
        1000
    )

}

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
    await initScene()

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
    top: 20px;
    right: 20px;
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
</style>
