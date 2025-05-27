<template>
  <div class="path-container">
    <h2>学习路径</h2>
    <div ref="networkContainer" class="graph-container"></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { Network } from 'vis-network/standalone/esm/vis-network'
import 'vis-network/styles/vis-network.css'

const networkContainer = ref(null)

// 用户完成的考点 ID（未来替换为后端返回数据）
const completedNodes = ref([1, 2, 3, 4, 5, 6, 7])

// 知识点（节点）定义
const topics = [
  { id: 1, label: '宇宙中的地球' },
  { id: 2, label: '地球和地图' },
  { id: 3, label: '自然环境中的物质运动和能量交换' },
  { id: 4, label: '自然环境的整体性和差异性' },
  { id: 5, label: '自然环境对人类活动的影响' },
  { id: 6, label: '区域地理环境与人类活动' },
  { id: 7, label: '中国地理' },
  { id: 8, label: '世界地理' },
  { id: 9, label: '人口与城市' },
  { id: 10, label: '生产活动与地域联系' },
  { id: 11, label: '旅游地理' },
  { id: 12, label: '区域可持续发展' },
  { id: 13, label: '环境保护' },
  { id: 14, label: '自然灾害与防治' },
  { id: 15, label: '地理信息技术的应用' },
  { id: 16, label: '人类与地理环境的协调发展' }
]

// 节点连接关系（边）
const edges = [
  { from: 1, to: 2 },
  { from: 2, to: 3 },
  { from: 3, to: 4 },
  { from: 4, to: 5 },
  { from: 5, to: 6 },
  { from: 6, to: 7 },
  { from: 6, to: 8 },
  { from: 7, to: 9 },
  { from: 8, to: 9 },
  { from: 9, to: 10 },
  { from: 10, to: 11 },
  { from: 10, to: 12 },
  { from: 12, to: 13 },
  { from: 5, to: 14 },
  { from: 15, to: 16 },
  { from: 13, to: 16 },
  { from: 12, to: 16 }
]

onMounted(() => {
  const nodes = topics.map(topic => ({
    id: topic.id,
    label: topic.label,
    shape: 'box',
    color: {
      background: completedNodes.value.includes(topic.id) ? '#A5D6A7' : '#FFF9C4',
      border: completedNodes.value.includes(topic.id) ? '#388E3C' : '#FBC02D',
    },
    font: {
      color: '#333',
      size: 16,
      bold: {
        color: '#000',
        size: 18,
      }
    }
  }))

  const container = networkContainer.value

  const data = {
    nodes,
    edges
  }

  const options = {
    layout: {
      hierarchical: {
        direction: 'UD',
        sortMethod: 'directed',
        nodeSpacing: 200,
        levelSeparation: 150
      }
    },
    interaction: {
      hover: true,
      zoomView: true,
      dragView: true
    },
    nodes: {
      borderWidth: 2,
      shape: 'box'
    },
    edges: {
      arrows: {
        to: { enabled: true, scaleFactor: 0.8 }
      },
      smooth: true
    },
    physics: false
  }

  const network = new Network(container, data, options)

  // 默认放大视图
  network.once('afterDrawing', () => {
    network.moveTo({
      scale: 1.5,
      position: { x: 0, y: 0 }
    })
  })

  // 节点点击交互示例
  network.on('click', (params) => {
    if (params.nodes.length > 0) {
      const nodeId = params.nodes[0]
      // const topic = topics.find(t => t.id === nodeId)
      // alert(`你点击了知识点「${topic.label}」，后续可跳转详情页`)
      if (completedNodes.value.indexOf(nodeId) !== -1) {
        completedNodes.value.splice(completedNodes.value.indexOf(nodeId), 1)
      } else {
        completedNodes.value.push(nodeId)
      }
    }
  })
})
</script>

<style scoped>
.path-container {
  padding: 24px;
}

.graph-container {
  width: 100%;
  height: 720px;
  border: 2px solid #ccc;
  border-radius: 12px;
  background: #fafafa;
}
</style>