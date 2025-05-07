<template>
  <!-- 提示词信息框 -->
  <div class="prompt">
    <el-alert :title="data.failurePrompt" type="warning" show-icon center v-if="data.failureMessage"
              :closable="false" />
    <el-alert :title="data.successPrompt" type="success" show-icon center v-else :closable="false" />
  </div>
  <!-- 个人信息 -->
  <div class="parent-container">
    <el-dialog title="修改个人信息" v-model="dialogVisible" width="60%" :before-close="handleClose">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="150px">
        <div class="updateInfo">
          <div class="left">
            <el-form-item label="头像" prop="avatar">
              <img style="width:150px;height:110px" :src="form.avatar" alt="头像"/>
            </el-form-item>
<!--            <el-form-item label="账号密码" prop="password">-->
<!--              <el-input v-model="form.password"></el-input>-->
<!--            </el-form-item>-->
            <el-form-item label="昵称" prop="nickname">
              <el-input v-model="form.nickname"></el-input>
            </el-form-item>
            <el-form-item label="年级" prop="grade">
              <el-select v-model="form.grade">
                <el-option label="高一" value="G1" />
                <el-option label="高二" value="G2" />
                <el-option label="高三" value="G3" />
              </el-select>
            </el-form-item>
          </div>
          <div class="right">
            <el-form-item label="用户编号" prop="id">
              <el-input v-model="form.id" disabled></el-input>
            </el-form-item>
            <el-form-item label="个性签名" prop="remarks">
              <el-input v-model="form.remarks"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email"></el-input>
            </el-form-item>
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="form.gender">
                <el-radio value="M">男</el-radio>
                <el-radio value="F">女</el-radio>
                <el-radio value="O">保密</el-radio>
              </el-radio-group>
            </el-form-item>
          </div>
        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose">取 消</el-button>
        <el-button type="primary" @click="submit" :disabled="data.isDisabled">提 交</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import multiavatar from '@multiavatar/multiavatar';
import { userState, setUser } from '@/store/userStore.js';
import { gsap } from 'gsap';

// 响应式状态
const dialogVisible = ref(false);
const data = reactive({
  isDisabled: false,
  successPrompt: '个人信息修改成功',
  failurePrompt: '个人信息修改失败',
});

// 表单
const form = ref({
  avatar: "",
  password: "",
  nickname: "",
  grade: "",
  email: "",
  mobilePhoneNumber: "",
  gender: "",
  id: null,
  hobby: "",
  work: "",
  remarks: "",
})

// 验证规则
const rules = {
  nickname: [{ required: true, message: "昵称不能为空", trigger: "blur" }],
  password: [{ required: true, message: "账号密码不能为空", trigger: "blur" }],
}

// 加载用户信息
const load = () => {
  form.value.correct_problems = userState.user.correct_problems;
  form.value.email = userState.user.email;
  form.value.gender = userState.user.gender || "";
  form.value.grade = userState.user.grade || "";
  form.value.remarks = userState.user.remarks || "";
  form.value.nickname = userState.user.username;
  form.value.id = userState.user.user_id;
  form.value.createDate = new Date(userState.user.created_at).toISOString().split('T')[0];
  form.value.avatar = `data:image/svg+xml;base64,${btoa(multiavatar(userState.user.user_id))}`;
}

// 打开个人信息对话框方法
const open = () => {
  dialogVisible.value = true;
  load();
}

// 提交信息更改
const submit = async () => {
  const formData = new FormData();
  formData.append("access_token", userState.access_token);
  if (form.value.password) formData.append("password", form.value.password);
  if (form.value.email) formData.append("email", form.value.email);
  if (form.value.gender) formData.append("gender", form.value.gender);
  if (form.value.grade) formData.append("grade", form.value.grade);
  if (form.value.remarks) formData.append("remarks", form.value.remarks);
  data.isDisabled = true;

  try {
    const response = await fetch("http://127.0.0.1:8040/api/update/", {
      method: "POST",
      body: formData,
    })
    const userResponse = await response.json();

    if (!response.ok) {
      throw new Error(userResponse.errors?.email ? '邮箱已存在' : '用户名已存在');
    }

    if (userResponse.access_token && userResponse.refresh_token) {
      setUser(userResponse);
      gsap.timeline()
          .to(".prompt", { y: "+=20", opacity: 1 })
          .to(".prompt", { y: "-=20", opacity: 0, delay: 3 })
      setTimeout(() => {
        handleClose();
        data.isDisabled = false;
      },1000);
    } else {
      throw new Error("修改信息成功但未返回令牌");
    }
  } catch (error) {
    console.error("修改信息错误:", error.message);
    data.failurePrompt = "个人信息修改失败：" + (error.message || "发生未知错误！");
    data.isDisabled = false;
    gsap.timeline()
        .to(".prompt", { y: "+=20", opacity: 1 })
        .to(".prompt", { y: "-=20", opacity: 0, delay: 3 })
  }
}

// 关闭对话框
const handleClose = () => {
  dialogVisible.value = false;
}

onMounted(load);
// 暴露方法给父组件
defineExpose({
  open
})
</script>

<style scoped>
/* 父容器 */
.parent-container {
  position: relative;
}

/* 信息对话框（分左右侧） */
.updateInfo {
  min-height: 250px;
  overflow: auto;
}

.left {
  float: left;
}

.right {
  overflow: hidden;
  min-width: 250px;
}

/* 提示词 */
.prompt {
  position: absolute;
  top: 10%;
  left: 37%;
  width: 26%;
  height: auto;
  opacity: 0;
  z-index: 10000;
}
</style>
