<template>
  <div class="parent-container">
    <div class="prompt">
      <el-alert :title="data.failurePrompt" type="warning" show-icon center v-if="data.failureMessage"
        :closable="false" />
      <el-alert :title="data.successPrompt" type="success" show-icon center v-else :closable="false" />
    </div>
    <el-dialog title="修改个人信息" v-model="dialogVisible" width="60%" :before-close="handleClose">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="150px">
        <div class="updateinfo">
          <div class="left">
            <el-form-item label="头像" prop="avatar">
              <img style="width:150px;height:110px" :src="form.avatar" />
            </el-form-item>
            <el-form-item label="账号密码" prop="password">
              <el-input v-model="form.password"></el-input>
            </el-form-item>
            <el-form-item label="昵称" prop="nickname">
              <el-input v-model="form.nickname"></el-input>
            </el-form-item>
            <el-form-item label="年级" prop="age">
              <el-input v-model="form.age"></el-input>
            </el-form-item>
          </div>
          <div class="right">
            <el-form-item label="用户编号" prop="id">
              <el-input v-model="form.id" disabled></el-input>
            </el-form-item>
            <el-form-item label="账号" prop="account">
              <el-input v-model="form.account" disabled></el-input>
            </el-form-item>
            <el-form-item label="个性签名" prop="design">
              <el-input v-model="form.design"></el-input>
            </el-form-item>
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="form.email"></el-input>
            </el-form-item>
            <el-form-item label="性别" prop="sex">
              <el-switch v-model="form.sex" active-color="#13ce66" inactive-color="#ff4949" active-text="男"
                inactive-text="女" :active-value="1" :inactive-value="0" />
            </el-form-item>
          </div>
        </div>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="handleClose">取 消</el-button>
        <el-button type="primary" @click="submit">提 交</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount, reactive, computed } from 'vue';
import multiavatar from '@multiavatar/multiavatar';
import { userState, setUser } from '@/store/userStore';
import { gsap } from 'gsap';

export default {
  name: "PersonalDia",
  setup() {
    const data = reactive({
      isDisabled: false,
      timeLeft: 3,
      successPrompt: computed(() => `${data.pattern}成功！还剩 ${data.timeLeft} 秒自动跳转到首页`),
      failurePrompt: computed(() => `${data.pattern}失败！${data.failureMessage}`),
      failureMessage: '',
      pattern: '',
    });
    const dialogVisible = ref(false);
    const form = ref({
      avatar: "",
      password: "",
      nickname: "",
      age: "",
      email: "",
      mobilePhoneNumber: "",
      sex: "",
      id: null,
      account: "",
      area: "",
      hobby: "",
      work: "",
      design: "",
    });

    const rules = {
      nickname: [{ required: true, message: "昵称不能为空", trigger: "blur" }],
      password: [{ required: true, message: "账号密码不能为空", trigger: "blur" }],
    };

    const load = () => {
      form.value.correct_problems = userState.user.correct_problems;
      form.value.email = userState.user.email;
      form.value.sex = userState.user.gender ? userState.user.gender : "";
      form.value.age = userState.user.grade ? userState.user.grade : "";
      form.value.design = userState.user.remarks ? userState.user.remarks : "";
      form.value.account = userState.user.username;
      form.value.nickname = userState.user.username;
      form.value.id = userState.user.user_id;
      form.value.createDate = new Date(userState.user.created_at).toISOString().split('T')[0];
      form.value.avatar = `data:image/svg+xml;base64,${btoa(multiavatar(userState.user.user_id))}`;
    };

    const open = () => {
      dialogVisible.value = true
      load() // 每次打开时加载最新数据
    }

    const submit = async () => {
      const formData = new FormData();
      formData.append("access_token", userState.access_token);
      if (form.value.password) formData.append("password", form.value.password);
      if (form.value.email) formData.append("email", form.value.email);
      if (form.value.sex) formData.append("gender", form.value.sex);
      if (form.value.age) formData.append("grade", form.value.age);
      if (form.value.design) formData.append("remarks", form.value.design);

      try {
        const response = await fetch("http://127.0.0.1:8040/api/update/", {
          method: "POST",
          body: formData,
        });
        const userResponse = await response.json();
        if (!response.ok) {
          throw new Error(userResponse.errors?.email ? '邮箱已存在' : '用户名已存在');
        }

        if (userResponse.access_token && userResponse.refresh_token) {
          setUser(userResponse);
        } else {
          throw new Error("注册成功但未返回令牌");
        }
      } catch (error) {
        console.error("注册错误:", error.message);
        data.failureMessage = error.message || "注册失败";
        data.isDisabled = false;
        gsap.timeline()
          .to(".prompt", { y: "+=50", opacity: 1 })
          .to(".prompt", { y: "-=50", opacity: 0, delay: 3 });
      }
    };

    const handleClose = () => {
      dialogVisible.value = false;
    };

    onMounted(load);

    return { dialogVisible, form, rules, submit, handleClose, open,data };
  },
};
</script>

<style scoped>
.parent-container {
  position: relative;
}

.updateinfo {
  height: 300px;
  overflow: auto;
}

.left {
  float: left;
}

.right {
  overflow: hidden;
}

/* 提示词 */
.prompt {
  position: absolute;
  top: 8%;
  left: 15%;
  width: 550px;
  height: auto;
  opacity: 0;
  z-index: 99999;
}
</style>
