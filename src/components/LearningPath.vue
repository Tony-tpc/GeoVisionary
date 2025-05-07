<template>
  <div class="dag-container" ref="containerRef"></div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { Graph } from '@antv/x6'

const containerRef = ref(null)

onMounted(() => {
  const graph = new Graph({
    container: containerRef.value,
    grid: true,
    panning: true,
    background: {
      color: '#f8f8f8',
    },
  })

  const node1 = graph.addNode({
    x: 40, y: 80, width: 120, height: 40,
    label: '地球的形状与大小',
    attrs: {
      body: { stroke: '#4caf50', fill: '#e8f5e9', rx: 8, ry: 8 },
      label: { fill: '#333', fontSize: 14 },
    },
  })

  const node2 = graph.addNode({
    x: 240, y: 60, width: 120, height: 40,
    label: '经纬线划分',
    attrs: {
      body: { stroke: '#2196f3', fill: '#e3f2fd', rx: 8, ry: 8 },
    },
  })

  const node3 = graph.addNode({
    x: 240, y: 160, width: 120, height: 40,
    label: '地球运动',
  })

  const node4 = graph.addNode({
    x: 440, y: 110, width: 120, height: 40,
    label: '地图的判读',
  })

  // 连线
  graph.addEdge({ source: node1, target: node2 })
  graph.addEdge({ source: node2, target: node4 })
  graph.addEdge({ source: node2, target: node3 })
})
</script>

<style scoped>
.dag-container {
  width: 100%;
  height: 400px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
</style>