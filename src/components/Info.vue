<template>
  <div>
    <el-card>
      <el-descriptions class="margin-top" title="简介" :column="2" border>
        <template #extra>
          <el-button type="primary" @click="handleEdit">操作</el-button>
        </template>
        <el-descriptions-item>
          <template #label>
            <i class="el-icon-picture-outline"></i>
            头像
          </template>
          <img class="img" :src="avatar" alt="" />
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <i class="el-icon-user"></i>
            账户名
          </template>
          {{ account }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <i class="el-icon-s-custom"></i>
            昵称
          </template>
          {{ nickname }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <i class="el-icon-odometer"></i>
            年级
          </template>
          {{ ageConfig[age]}}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <i class="el-icon-male"></i>
            <i class="el-icon-female"></i>
            性别
          </template>
          <el-tag size="small">{{ sexConfig[sex] }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <i class="el-icon-message"></i>
            邮箱Email
          </template>
          {{ email }}
        </el-descriptions-item>


        <!-- <el-descriptions-item>
          <template #label>
            <i class="el-icon-basketball"></i>
            正确问题数
          </template>
          {{ correct_problems }}
        </el-descriptions-item> -->
        <el-descriptions-item>
          <template #label>
            <i class="el-icon-magic-stick"></i>
            个性签名
          </template>
          {{ design }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <i class="el-icon-date"></i>
            注册日期
          </template>
          {{ createDate }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import multiavatar from '@multiavatar/multiavatar';
import { userState } from '@/store/userStore.js';

// 响应式数据
const avatar = ref('');
const account = ref('');
const age = ref('');
const email = ref('');
const mobilePhoneNumber = ref('');
const createDate = ref('');
const nickname = ref('');
const sex = ref('');
const design = ref('');
const emit = defineEmits(['edit']);

// 性别配置
const sexConfig = {
  M: '男',
  F: '女',
  O: '保密',
}

// 年级配置
const ageConfig = {
  G1: '高一',
  G2: '高二',
  G3: '高三',
}

// 加载个人信息
const load = () => {
  // 从 store 初始化数据
  createDate.value = new Date(userState.user.created_at).toISOString().split('T')[0];
  email.value = userState.user.email;
  sex.value = userState.user.gender ? userState.user.gender : "未完善";
  age.value = userState.user.grade ? userState.user.grade : "未完善";
  design.value = userState.user.remarks ? userState.user.remarks : "未完善";
  account.value = userState.user.username;
  nickname.value = userState.user.username;

  // 生成头像
  const svg = multiavatar(userState.user.user_id);
  avatar.value = `data:image/svg+xml;base64,${btoa(svg)}`;
}

// 抛出信息编辑事件
const handleEdit = () => {
  emit('edit');
}

// 生命周期钩子
onMounted(() => {
  load();
})
</script>

<style scoped>
:deep(.el-card) {
  background: rgba(255, 255, 255, 0.95);
  border: 2px solid #e8f4ff;
  border-radius: 16px;
  backdrop-filter: blur(12px);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 8px 32px rgba(13, 83, 75, 0.1);
}

:deep(.el-card:hover) {
  box-shadow: 0 12px 48px rgba(13, 83, 75, 0.2);
}

.img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 3px solid #337870;
  padding: 4px;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(97, 147, 142, 0.2);
}

.img:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 24px rgba(2, 167, 115, 0.3);
}

:deep(.el-descriptions__title) {
  color: #2c3e50;
  font-size: 1.6rem;
  letter-spacing: 0.5px;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

:deep(.el-descriptions__label) {
  color: #34495e !important;
  font-weight: 500;
  font-size: 1rem;
}

:deep(.el-descriptions__content) {
  color: #7f8c8d;
  font-size: 1rem;
}

:deep(.el-icon) {
  color: #00c3ff;
  margin-right: 10px;
  font-size: 1.2rem;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #00c3ff 0%, #0066ff 100%);
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 500;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 195, 255, 0.3);
}

@media (max-width: 768px) {
  :deep(.el-descriptions--column) {
    grid-template-columns: repeat(1, 1fr) !important;
  }
  
  .img {
    width: 100px;
    height: 100px;
  }
  
  :deep(.el-descriptions__title) {
    font-size: 1.3rem;
  }
}
</style>
