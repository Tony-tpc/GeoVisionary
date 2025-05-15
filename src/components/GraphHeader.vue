<template>
  <div class="graph-header">
    <button class="nav-btn small" @click="goToPrevious">❮</button>
    <div class="graph-title">{{ currentTitle }}</div>
    <button class="nav-btn small" @click="goToNext">❯</button>
  </div>
</template>

<script setup>
import { ref, computed, defineEmits, watch } from 'vue'
import {throttle} from "lodash";

// 参数接受父组件的图谱对象与当前图谱下标
const props = defineProps({
  neo4jQuery: {
    type: Object,
    default: {
      earthAndMap: "...",
      earthInSpace: "...",
      energyExchange: "...",
      sameAndDiff: "...",
    }
  },
  modelValue: {
    type: Number,
    default: 0,
  }
})
const emit = defineEmits(['update:modelValue']) // 实时修改父组件值
// throttle：每 500ms 最多触发一次 emit
const throttledEmit = throttle((val) => {
  emit('update:modelValue', val)
}, 500)

const keys = Object.keys(props.neo4jQuery) // 图谱键名
const keymap = {
  earthAndMap: "地球和地图",
  earthInSpace: "宇宙中的地球",
  energyExchange: "自然环境中的物质运动和能量交换",
  sameAndDiff: "自然环境的整体性和差异性",
  environmentImpact: "自然环境对人类活动的影响",
  populationAndCity: "人口与城市",
  productionAndLink: "生产活动与地域联系",
  harmony: "人类与地理环境的协调发展",
  regionAndActivity: "区域地理环境与人类活动",
  sustainable: "区域可持续发展",
  geoTech: "地理信息技术的应用",
  worldGeo: "世界地理",
  chinaGeo: "中国地理",
  tourism: "旅游地理",
  disaster: "自然灾害与防治",
  environmentProtect: "环境保护",
} // 键名与中文映射
const currentIndex = ref(props.modelValue)

const currentTitle = computed(() => keymap[keys[currentIndex.value]])

function goToPrevious() {
  if (currentIndex.value > 0) {
    currentIndex.value--
  } else {
    currentIndex.value = keys.length - 1
  }
  throttledEmit(currentIndex.value)
}

function goToNext() {
  if (currentIndex.value < keys.length - 1) {
    currentIndex.value++
  } else {
    currentIndex.value = 0
  }
  throttledEmit(currentIndex.value)
}

watch(() => props.modelValue, (val) => {
  currentIndex.value = val
})
</script>

<style scoped>
.graph-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin: 16px 0;
}

.graph-title {
  font-size: 18px;
  width: 160px;
  text-align: center;
  color: #0d534b;
  font-weight: 600;
  padding: 4px 12px;
  background-color: #e3f5f0;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(13, 83, 75, 0.1);
}

.nav-btn.small {
  background-color: #e3f5f0;
  color: #0d534b;
  border: none;
  font-size: 18px;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(13, 83, 75, 0.1);
}

.nav-btn.small:hover {
  background-color: #c3ebe3;
  transform: scale(1.05);
}

.nav-btn.small:active {
  background-color: #aadfd4;
  transform: scale(0.95);
}
</style>
