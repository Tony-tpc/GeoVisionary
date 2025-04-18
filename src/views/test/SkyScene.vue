<template>
  <div ref="container" class="scene-container">
    <div class="info">Vue + Three.js 动态天空系统</div>
  </div>
</template>

<script setup>
import { ref, shallowRef, onMounted, onUnmounted, inject, markRaw,watchEffect } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'
import { Sky } from 'three/examples/jsm/objects/Sky.js'

// DOM 引用
const container = ref(null)

// Three.js 对象 (使用 shallowRef + markRaw)
const scene = shallowRef(null)
const camera = shallowRef(null)
const renderer = shallowRef(null)
const controls = shallowRef(null)
const sky = shallowRef(null)
const moon = shallowRef(null)
const sun = shallowRef(markRaw(new THREE.Vector3()))

// 响应式状态 (带默认值的安全注入)
const state = inject('skyState', ref({
  turbidity: 10,
  rayleigh: 3,
  mieCoefficient: 0.005,
  mieDirectionalG: 0.7,
  elevation: 2,
  azimuth: 180,
  exposure: 0.5
}))

// 动画循环控制
const animationFrame = ref(null)
const isMounted = ref(false)

// 场景初始化
const initScene = () => {
  try {
    // 场景
    scene.value = markRaw(new THREE.Scene())

    // 相机
    const rawCamera = new THREE.PerspectiveCamera(
        60,
        window.innerWidth / window.innerHeight,
        100,
        2e6
    )
    rawCamera.position.set(0, 100, 2000)
    camera.value = markRaw(rawCamera)

    // 渲染器
    const rawRenderer = new THREE.WebGLRenderer({
      antialias: true,
      powerPreference: "high-performance"
    })
    rawRenderer.setPixelRatio(window.devicePixelRatio)
    rawRenderer.setSize(window.innerWidth, window.innerHeight)
    rawRenderer.toneMapping = THREE.ACESFilmicToneMapping
    renderer.value = markRaw(rawRenderer)
    container.value.appendChild(rawRenderer.domElement)

    // 天空
    const skyObj = new Sky()
    skyObj.scale.setScalar(450000)
    sky.value = markRaw(skyObj)
    scene.value.add(skyObj)

    // 月亮
    const moonGeometry = new THREE.SphereGeometry(15, 32, 32)
    const moonMaterial = new THREE.MeshBasicMaterial({
      color: 0xeeeeee,
      transparent: true,
      opacity: 0.8
    })
    const moonMesh = new THREE.Mesh(moonGeometry, moonMaterial)
    moonMesh.visible = false
    moon.value = markRaw(moonMesh)
    scene.value.add(moonMesh)

    // 辅助网格
    const gridHelper = new THREE.GridHelper(1e4, 20, 0xffffff, 0xffffff)
    gridHelper.material.opacity = 0.2
    gridHelper.material.transparent = true
    scene.value.add(gridHelper)

    // 控制器
    const orbitControls = new OrbitControls(rawCamera, rawRenderer.domElement)
    orbitControls.minDistance = 500
    orbitControls.maxDistance = 5000
    controls.value = markRaw(orbitControls)

  } catch (e) {
    console.error('场景初始化失败:', e)
    throw new Error('Three.js 初始化失败')
  }
}

// 天体位置更新
const updateCelestialPositions = () => {
  try {
    if (!sky.value?.material || !state.value || !moon.value) return

    const uniforms = sky.value.material.uniforms
    const currentState = state.value

    // 状态安全解构
    const {
      elevation = 0,
      azimuth = 180,
      turbidity = 10,
      rayleigh = 3,
      mieCoefficient = 0.005,
      mieDirectionalG = 0.7,
      exposure = 0.5
    } = currentState

    // 日夜切换逻辑
    if (elevation < 0) {
      uniforms.turbidity.value = 2
      uniforms.rayleigh.value = 0.5
      uniforms.mieCoefficient.value = 0.001

      // 月亮位置计算
      const moonElevation = Math.abs(elevation)
      const moonAzimuth = (azimuth + 180) % 360
      const moonPhi = THREE.MathUtils.degToRad(90 - moonElevation)
      const moonTheta = THREE.MathUtils.degToRad(moonAzimuth)

      moon.value.position.setFromSphericalCoords(450000, moonPhi, moonTheta)
      moon.value.lookAt(camera.value.position)
      moon.value.visible = true
    } else {
      moon.value.visible = false
      uniforms.turbidity.value = turbidity
      uniforms.rayleigh.value = rayleigh
      uniforms.mieCoefficient.value = mieCoefficient
    }

    // 太阳位置计算
    const sunPhi = THREE.MathUtils.degToRad(90 - elevation)
    const sunTheta = THREE.MathUtils.degToRad(azimuth)
    sun.value.setFromSphericalCoords(1, sunPhi, sunTheta)
    uniforms.sunPosition.value.copy(sun.value)
    uniforms.mieDirectionalG.value = mieDirectionalG

    // 曝光设置
    renderer.value.toneMappingExposure = exposure

  } catch (e) {
    console.error('天体位置更新失败:', e)
  }
}

// 渲染循环
const animate = () => {
  try {
    if (!isMounted.value || !scene.value || !camera.value || !renderer.value) return

    updateCelestialPositions()
    renderer.value.render(scene.value, camera.value)
    animationFrame.value = requestAnimationFrame(animate)
  } catch (e) {
    console.error('渲染循环错误:', e)
  }
}

// 窗口大小调整
const onWindowResize = () => {
  if (!camera.value || !renderer.value) return

  camera.value.aspect = window.innerWidth / window.innerHeight
  camera.value.updateProjectionMatrix()
  renderer.value.setSize(window.innerWidth, window.innerHeight)
}

// 生命周期
onMounted(() => {
  isMounted.value = true
  try {
    initScene()
    window.addEventListener('resize', onWindowResize)
    animate()
  } catch (e) {
    console.error('组件挂载失败:', e)
  }
})

onUnmounted(() => {
  isMounted.value = false

  // 清理资源
  window.removeEventListener('resize', onWindowResize)
  if (animationFrame.value) {
    cancelAnimationFrame(animationFrame.value)
  }

  // 深度清理场景
  const disposeScene = (scene) => {
    scene.traverse(obj => {
      if (obj.isMesh) {
        if (obj.material) {
          obj.material.dispose()
          if (obj.material.map) obj.material.map.dispose()
        }
        if (obj.geometry) obj.geometry.dispose()
      }
    })
    scene.clear()
  }

  if (scene.value) {
    disposeScene(scene.value)
    scene.value = null
  }

  if (controls.value) {
    controls.value.dispose()
    controls.value = null
  }

  if (renderer.value) {
    renderer.value.dispose()
    renderer.value.forceContextLoss()
    const gl = renderer.value.domElement.getContext('webgl2')
    if (gl) gl.getExtension('WEBGL_lose_context')?.loseContext()
    container.value?.removeChild(renderer.value.domElement)
    renderer.value = null
  }
})

// 响应式更新
watchEffect(() => {
  if (sky.value?.material && state.value) {
    updateCelestialPositions()
  }
})
</script>

<style scoped>
.scene-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: #000;
}

.info {
  position: absolute;
  top: 20px;
  width: 100%;
  text-align: center;
  color: white;
  font-family: Arial, sans-serif;
  font-size: 14px;
  pointer-events: none;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8);
  z-index: 100;
}
</style>
