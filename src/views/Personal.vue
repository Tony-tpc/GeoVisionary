<template>
  <section>
    <!--  顶部信息栏  -->
    <header class="personTop">
      <div style="height: 80px;padding-left: 25px">
        <img :src="avatar" alt="头像" class="personTop-img">
      </div>
      <!--  左侧基本信息  -->
      <div class="personTop-text">
        <div class="user-text">
          <div class="user-name">
            <span> {{ username }} </span>
          </div>
          <div class="user-design">
            <span> {{ remarks }}</span>
          </div>
        </div>
        <!--  右侧数据展示  -->
        <div class="user-num">
          <div>
            <span class="num-text">正确问题</span>
            <div class="num-number">{{ goodCounts }}</div>
          </div>
        </div>
      </div>
    </header>
    <!--  主体部分  -->
    <main class="person-body">
      <div class="person-body-left">
        <el-card class="box-card">
          <!-- 左侧菜单标题 -->
          <div class="clearfix">
            <span class="person-body-list">个人中心</span>
          </div>
          <!-- 左侧菜单主体 -->
          <el-menu class="el-menu-vertical-demo" :default-active="activeIndex" @select="handleMenuClick">
            <el-menu-item index="info">
              <el-icon><User /></el-icon>
              <span>个人简介</span>
            </el-menu-item>

            <el-menu-item index="stats">
              <el-icon><PieChart /></el-icon>
              <span>学习数据</span>
            </el-menu-item>

            <el-menu-item index="errors">
              <el-icon><CircleClose /></el-icon>
              <span>错题记录</span>
            </el-menu-item>

            <el-menu-item index="favorites">
              <el-icon><Star /></el-icon>
              <span>我的收藏</span>
            </el-menu-item>

            <el-menu-item index="study">
              <el-icon><Guide /></el-icon>
              <span>学习路径</span>
            </el-menu-item>

            <el-menu-item index="feedback">
              <el-icon><Edit /></el-icon>
              <span>意见反馈</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </div>
      <!-- 个人简介 -->
      <div class="person-body-right" v-if="activeIndex === 'info'">
        <Info @edit="edit"/>
      </div>
      <!-- 学习数据 -->
      <div class="person-body-right" v-if="activeIndex === 'stats'" style="padding: 2rem 0 0 0">
        <StudyStats />
      </div>
      <!-- 错题记录 -->
      <div class="person-body-right" v-if="activeIndex === 'errors'" style="padding: 10px 20px">
        <ErrorDisplay />
      </div>
      <!-- 我的收藏 -->
      <div class="person-body-right" v-if="activeIndex === 'study'">
        <LearningPath />
      </div>
      <!-- 学习路径 -->
      <div class="person-body-right" v-if="activeIndex === 'favorites'">
        <FavoriteDisplay />
      </div>
      <!-- 意见反馈 -->
      <div class="person-body-right" v-if="activeIndex === 'feedback'">
        <FeedbackForm />
      </div>
    </main>
  </section>
  <!-- 个人信息修改弹窗 -->
  <section>
    <personal-dia ref="personalDiaRef"/>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import multiavatar from '@multiavatar/multiavatar';
import PersonalDia from "../components/PersonalDia.vue";
import Info from "../components/Info.vue";
import { userState } from '@/store/userStore';
import {User, Edit, CircleClose, PieChart, Star, Guide} from "@element-plus/icons-vue";
import StudyStats from "@/components/StudyStats.vue";
import FeedbackForm from "@/components/FeedbackForm.vue";
import ErrorDisplay from "@/components/ErrorDisplay.vue";
import FavoriteDisplay from "@/components/FavoriteDisplay.vue";
import LearningPath from "@/components/LearningPath.vue";

// 用户信息数据
const avatar = ref('');
const username = ref('');
const remarks = ref('');
const goodCounts = ref('');
const createDate = ref('');
const email = ref('');
const gender = ref('');
const grade = ref('');
const account = ref('');

// 其他响应式数据
const personalDiaRef = ref(null);
const activeIndex = ref('info');

// 处理菜单点击
const handleMenuClick = (obj) => {
  if (obj.index) {
    activeIndex.value = obj.index;
  } else {
    activeIndex.value = obj;
  }
}

// 加载个人信息
const load = () => {
  goodCounts.value = userState.user.correct_problems;
  createDate.value = new Date(userState.user.created_at).toISOString().split('T')[0];
  email.value = userState.user.email;
  gender.value = userState.user.gender || "未完善";
  grade.value = userState.user.grade || "未完善";
  remarks.value = userState.user.remarks || "未完善";
  account.value = userState.user.username;
  username.value = userState.user.username;
}

// 编辑个人信息
const edit = () => {
  personalDiaRef.value.open();
}

// 随机初始化头像
const getRandomheader = () => {
  const svg = multiavatar(userState.user.user_id);
  avatar.value = `data:image/svg+xml;base64,${btoa(svg)}`;
}

// 生命周期钩子
onMounted(() => {
  load();
  getRandomheader();
})
</script>

<style scoped>
/* 主色调调整为更活力的蓝色 */
:root {
  --primary-color: #4361ee;
  --secondary-color: #3f37c9;
}

/* 顶部概要信息 */
.personTop {
  position: relative;
  width: 90%;
  max-width: 1200px;
  padding: 1rem;
  margin: 5% auto 0 auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 2rem;
  transition: all 0.3s ease;
}

.personTop-img {
  width: 80px;
  height: 80px;
  flex-shrink: 0;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid var(--background-light);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.personTop-text {
  width: 1000px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.user-name {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-dark);
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.user-design {
  color: var(--text-light);
  font-size: 0.95rem;
  margin: 0.5rem 0;
  line-height: 1.4;
}

.user-num {
  display: flex;
  gap: 3rem;
  padding-top: 0.7rem;
}

.user-num>div {
  text-align: center;
  padding: 0 1rem;
}

.user-num>div:not(:last-child)::after {
  content: "";
  position: absolute;
  right: -1.5rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1px;
  height: 40%;
  background: #e2e8f0;
}

/* 顶部右侧数字 */
.num-number {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--text-dark) !important;
  margin-bottom: 0.2rem;
}

/* 顶部右侧文本 */
.num-text {
  color: var(--text-light);
  font-size: 0.9rem;
  letter-spacing: 0.5px;
}

/* 导航菜单优化 */
.person-body {
  width: 93%;
  max-width: 1232px;
  margin: 2rem auto;
  display: flex;
  gap: 2rem;
}

.person-body-left {
  width: 200px;
  flex-shrink: 0;
}

/* 左侧菜单卡片 */
.box-card {
  border-radius: 12px;
  min-height: 463px;
  height: 100%;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  border: none;
  padding: 0;
}

.el-menu {
  border-right: none !important;
  padding: 1rem 0;
}

.el-menu-item {
  height: 48px;
  line-height: 48px;
  margin: 0.4rem 0;
  border-radius: 8px;
  transition: all 0.2s ease;
  color: var(--text-medium);
}

.el-menu-item:hover {
  background: rgba(209, 213, 216, 0.5);
}

.el-menu-item.is-active {
  color: #ffffff;
  background: #0088FE;
  font-weight: 500;
}

/* icon 与文字间隔 */
.el-menu-item i {
  margin-right: 1rem;
  font-size: 1.1rem;
}

/* 右侧内容区域 */
.person-body-right {
  flex: 1;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

/* 个人中心列表 */
.person-body-list {
  color: #2c3e50;
  font-size: 20px;
  letter-spacing: 0.5px;
  font-weight: bold;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .personTop {
    flex-direction: row;
    align-items: center;
    text-align: center;
  }

  .person-body {
    flex-direction: column;
  }

  .person-body-left {
    width: 100%;
  }

  .user-num {
    justify-content: center;
    gap: 2rem;
  }
}
</style>