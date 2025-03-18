<template>
  <div>
    <el-card>
      <el-descriptions class="margin-top" title="简介" :column="2" border>
        <template #extra>
          <el-button type="primary" >操作</el-button>
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
          {{ age }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <i class="el-icon-male"></i>
            <i class="el-icon-female"></i>
            性别
          </template>
          <el-tag size="small">{{ sex }}</el-tag>
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

<script>
import multiavatar from '@multiavatar/multiavatar'; // 引入 multiavatar
import { userState, setUser } from '@/store/userStore'
import PersonalDia from "./PersonalDia.vue"; 

// import { userInfo } from "@/api/user.js";
export default {
  name: "Info",
  data() {
    return {
      avatar: String,
      account: String,
      age: Number,
      email: String,
      mobilePhoneNumber: String,
      area: String,
      createDate: String,
      nickname: String,
      sex: String,
      work: String,
      // correct_problems: String,
      design: String,
    };
  },
  mounted() {
    this.load();
  },
  methods: {
    load() {
      // this.correct_problems = userState.user.correct_problems;
      this.createDate = new Date(userState.user.created_at).toISOString().split('T')[0];
      this.email = userState.user.email;
      this.sex = userState.user.gender ? userState.user.gender : "未完善";
      this.age = userState.user.grade ? userState.user.grade : "未完善";
      this.design = userState.user.remarks ? userState.user.remarks : "未完善";
      this.account = userState.user.username;
      this.nickname = userState.user.username;
      
      // userInfo(this.$route.params.id)
      //   .then((res) => {
      //     this.avatar = res.data.avatar;
      //     this.account = res.data.account;
      //     this.age = res.data.age;
      //     this.email = res.data.email;
      //     this.mobilePhoneNumber = res.data.mobilePhoneNumber;
      //     this.area = res.data.area;
      //     this.createDate = res.data.createDate;
      //     this.nickname = res.data.nickname;
      //     this.sex = res.data.sex == 1 ? "男" : "女";
      //     this.work = res.data.work;
      //     this.design = res.data.design;
      //     this.hobby = res.data.hobby;
      //   })
      //   .catch((err) => {
      //     console.log(err);
      //   });
      const svg = multiavatar(userState.user.user_id); // 使用 multiavatar 生成 SVG 图像
      this.avatar = `data:image/svg+xml;base64,${btoa(svg)}`;
    },
  },
};
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
