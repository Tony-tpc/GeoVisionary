<script setup>
import { ref } from "vue";
import { gsap } from "gsap"
import {Aim, Calendar, Document} from "@element-plus/icons-vue";
const isCollapsed = ref(true); // 折叠菜单栏
const emit = defineEmits(["menu-select"]); // 事件初始化
let selectedItem = ref('');

// 题目分类数据
const categories = ref([
  {
    id: "1-1",
    name: "2024",
    type: "年份",
    value: { year: 2024, category: "year" }
  },
  {
    id: "1-2",
    name: "2023",
    type: "年份",
    value: { year: 2023, category: "year" }
  },
  {
    id: "1-3",
    name: "2022",
    type: "年份",
    value: { year: 2022, category: "year" }
  },
  {
    id: "1-4",
    name: "2021",
    type: "年份",
    value: { year: 2021, category: "year" }
  },
  {
    id: "2-1",
    name: "物质运动和能量交换",
    type: "知识点",
    value: { topic: "第三章：自然环境中的物质运动和能量交换", category: "topic" }
  },
  {
    id: "2-2",
    name: "生产活动与地域联系",
    type: "知识点",
    value: { topic: "第七章：生产活动与地域联系", category: "topic" }
  },
  {
    id: "2-3",
    name: "地理环境与人类活动",
    type: "知识点",
    value: { topic: "第九章：区域地理环境与人类活动", category: "topic" }
  },
  {
    id: "2-4",
    name: "区域可持续发展",
    type: "知识点",
    value: { topic: "第十章：区域可持续发展", category: "topic" }
  },
  {
    id: "2-5",
    name: "自然灾害与防治",
    type: "知识点",
    value: { topic: "第十五章：自然灾害与防治", category: "topic" }
  },
  {
    id: "2-6",
    name: "中国地理",
    type: "知识点",
    value: { topic: "第十三章：中国地理", category: "topic" }
  },
  {
    id: "2-7",
    name: "世界地理",
    type: "知识点",
    value: { topic: "第十二章：世界地理", category: "topic" }
  },
  {
    id: "3-1",
    name: "新课标 I 卷",
    type: "来源",
    value: { source: "新课标 I 卷", category: "source"}
  },
  {
    id: "3-2",
    name: "新课标 II 卷",
    type: "来源",
    value: { source: "新课标 II 卷", category: "source" }
  },
  {
    id: "3-3",
    name: "全国甲卷",
    type: "来源",
    value: { source: "全国甲卷", category: "source" }
  },
  {
    id: "3-4",
    name: "全国乙卷",
    type: "来源",
    value: { source: "全国乙卷", category: "source" }
  }
]);

const collapseAnimation = () => {
  gsap.timeline()
      .to('.side-nav-title',{left: 10})
      .to('.menu-column', {width: 100},"<")
}

const expandAnimation = () => {
  gsap.timeline()
      .to('.side-nav-title',{left: 65})
      .to('.menu-column', {width: 220},"<")
}

const handleSelect = (index) => {
  selectedItem = categories.value.find(item => item.id === index);
  if (selectedItem) {
    emit("menu-select", selectedItem.value); // 传递对象
  }
}

const handleMouseEnter = () => {
  isCollapsed.value = false;
  expandAnimation();
}

const handleMouseLeave = () => {
  if (!selectedItem.value) {
    isCollapsed.value = true;
    collapseAnimation();
  }
}
</script>

<template>
  <section>
    <h2 class="side-nav-title">
      试题分类
    </h2>
    <el-col :span="6"
            class="menu-column"
            @mouseenter="handleMouseEnter"
            @mouseleave="handleMouseLeave"
    >
      <h2>&nbsp;</h2>
      <el-menu
          :unique-opened="true"
          :collapse="isCollapsed"
          @select="handleSelect"
      >
        <el-sub-menu index="1">
          <template #title>
            <el-icon><Calendar /></el-icon>
            <span>年份</span>
          </template>
          <el-menu-item v-for="item in categories.filter(c => c.type === '年份')"
                        :key="item.id"
                        :index="item.id">
            {{ item.name }}
          </el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="2">
          <template #title>
            <el-icon><Aim /></el-icon>
            <span>知识点</span>
          </template>
          <el-menu-item v-for="item in categories.filter(c => c.type === '知识点')"
                        :key="item.id"
                        :index="item.id">
            {{ item.name }}
          </el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="3">
          <template #title>
            <el-icon><Document /></el-icon>
            <span>来源</span>
          </template>
          <el-menu-item v-for="item in categories.filter(c => c.type === '来源')"
                        :key="item.id"
                        :index="item.id">
            {{ item.name }}
          </el-menu-item>
        </el-sub-menu>
      </el-menu>
    </el-col>
  </section>
</template>

<style scoped>
/* 整个菜单栏外框 */
.menu-column {
  position: absolute;
  top: 10%;
  left: 0;
  height: 88%;
  background: var(--bg-color); /* 适配你的主题色 */
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 轻微阴影，增加立体感 */
}

/* 试题分类伪标题 */
.menu-column h2 {
  font-size: 18px;
  font-weight: bold;
  color: var(--text-color);
  text-align: center;
  margin-bottom: 10px;
}
/* 标题 */
.side-nav-title {
  position: absolute;
  top: 12%;
  left: 10px;
  z-index: 1;
  pointer-events: none;
}

/* 侧边栏菜单 */
.el-menu {
  background: transparent !important; /* 让菜单栏背景透明 */
  border: none;
}

/* 每个子菜单（如年份 / 难度 / 来源） */
.el-sub-menu__title {
  font-size: 16px;
  font-weight: bold;
  color: var(--text-color);
  padding: 12px;
  transition: all 0.3s ease-in-out;
}

/* 子菜单悬停效果 */
.el-sub-menu__title:hover {
  background: rgba(0, 0, 0, 0.05) !important;
  border-radius: 8px;
}

/* 菜单项 */
.el-menu-item {
  font-size: 14px;
  color: var(--text-color);
  padding: 10px 16px;
  transition: all 0.3s ease-in-out;
}

/* 子菜单项悬停 */
.el-menu-item:hover {
  background: rgba(0, 0, 0, 0.1) !important;
  border-radius: 8px;
}

/* 选中状态 */
.el-menu-item.is-active {
  background: #40a2f6 !important; /* 适配你的主题色 */
  color: white !important;
  border-radius: 8px;
  font-weight: bold;
}

/* 图标 */
.el-icon {
  color: #0d0f1a;
  margin-right: 6px;
}
</style>