<!--
 * @Description:
 * @Version: 2.0
 * @Author: Yaowen Liu
 * @Date: 2021-10-14 10:20:21
 * @LastEditors: Yaowen Liu
 * @LastEditTime: 2023-04-10 12:45:28
-->
<template>
  <div class="h-screen flex overflow-hidden">
    <!-- 子列表 -->
    <DialogList v-model:visible="dialogVisible" :options="options" />

    <!-- 左侧列表 -->
    <div class="flex-auto overflow-y-auto">
      <WaterfallList :options="options" @cardClick="dialogVisible = true" style="height: 100%; width:100%" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import loading from '../assets/loading.png'
import error from '../assets/error.png'
import DialogList from './DialogList.vue'
import WaterfallList from './WaterfallList.vue'


// 侧边栏控制
function useSlideBar() {
  const isOpen = ref(true)
  function handleToggleController(flag: boolean) {
    isOpen.value = flag
  }

  return {
    isOpen,
    handleToggleController,
  }
}

// 侧边栏控制
const { isOpen, handleToggleController } = useSlideBar()

const options = reactive({
  // 唯一key值
  rowKey: 'id',
  // 卡片之间的间隙
  gutter: 10,
  // 是否有周围的gutter
  hasAroundGutter: true,
  // 卡片在PC上的宽度
  width: 320,
  // 自定义行显示个数，主要用于对移动端的适配
  breakpoints: {
    1200: {
      // 当屏幕宽度小于等于1200
      rowPerView: 4,
    },
    800: {
      // 当屏幕宽度小于等于800
      rowPerView: 3,
    },
    500: {
      // 当屏幕宽度小于等于500
      rowPerView: 2,
    },
  },
  // 动画效果
  animationEffect: 'animate__fadeInUp',
  // 动画时间
  animationDuration: 1000,
  // 动画延迟
  animationDelay: 300,
  animationCancel: false,
  // 背景色
  backgroundColor: '#2C2E3A',
  // imgSelector
  imgSelector: 'src.original',
  // 加载配置
  loadProps: {
    loading,
    error,
    ratioCalculator: (width: number, height: number) => {
      // 我设置了最小宽高比
      const minRatio = 3 / 4
      const maxRatio = 4 / 3
      return Math.random() > 0.5 ? minRatio : maxRatio
    },
  },
  // 是否懒加载
  lazyload: true,
  align: 'center',
})

const dialogVisible = ref(false)
</script>

<style>
/* 添加全局样式 */
html,
body {
  margin: 0;
  padding: 0;
  overflow-y: scroll;
  width: 100%;
  height: 100vh;
}

#app {
  height: 100%;
  width: 100%;
}
</style>
