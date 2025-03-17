<template>
  <!--  vanta背景  -->
  <div class="vanta-container" ref="vantaSection"></div>
  <div class="prompt">
    <!--  提交提示  -->
    <el-alert :title="data.failurePrompt" type="warning" show-icon center v-if="data.failureMessage" :closable="false"/>
    <el-alert :title="data.successPrompt" type="success" show-icon center v-else :closable="false"/>
  </div>
  <!--  父级容器 -->
  <div class="container">
    <!--  前页注册  -->
    <div class="register">
      <!--    注册标题  -->
      <div class="register-title">
        创&nbsp;建&nbsp;账&nbsp;号
      </div>
      <br><br>
      <!--    注册表单  -->
      <div class="register-form">
        <el-form
            ref="ruleFormRefReg"
            style="max-width: 600px"
            :model="ruleFormReg"
            :rules="rulesReg"
            label-width="auto"
            class="demo-ruleForm"
            :size="formSize"
            status-icon
        >
          <el-form-item label="用户名" prop="username">
            <el-input v-model="ruleFormReg.username" placeholder="请输入用户名"/>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="ruleFormReg.password" type="password" show-password autocomplete="off" placeholder="长度至少6位"/>
          </el-form-item>
          <el-form-item label="确认密码" prop="checkPass">
            <el-input v-model="ruleFormReg.checkPass" type="password" show-password autocomplete="off" placeholder="******"/>
          </el-form-item>
          <el-form-item label="电子邮箱" prop="email">
            <el-input v-model="ruleFormReg.email" placeholder="name@example.com"/>
          </el-form-item>
          <el-form-item label="年级" prop="grade">
            <el-select v-model="ruleFormReg.grade" placeholder="请选择年级">
              <el-option label="高一" value="G1" />
              <el-option label="高二" value="G2" />
              <el-option label="高三" value="G3" />
            </el-select>
          </el-form-item>
          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="ruleFormReg.gender">
              <el-radio value="M">男</el-radio>
              <el-radio value="F">女</el-radio>
              <el-radio value="O">保密</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="个人签名" prop="desc">
            <el-input v-model="ruleFormReg.desc"  type="textarea" :autosize="{ minRows:2 , maxRows:4 }" :maxlength="100" resize="none" show-word-limit placeholder="彰显您的风格"/>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitFormReg(ruleFormRefReg)" :disabled="data.isDisabled">
              注册
            </el-button>
            <el-button @click="resetFormReg(ruleFormRefReg)">
              重置
            </el-button>
            <div>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              已有账号？去
            </div>
            <el-button class="transition-button" @click="transitionToSignin">
              登录
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <!--  后页登录  -->
    <div class="sign-in">
      <div class="sign-in-title">
        登&nbsp;入&nbsp;账&nbsp;号
      </div>
      <div class="sign-in-form">
        <el-form
            ref="ruleFormRefSign"
            style="max-width: 600px"
            :model="ruleFormSign"
            :rules="rulesSign"
            label-width="auto"
            class="demo-ruleForm"
            :size="formSize"
        >
          <el-form-item label="用户名/邮箱" prop="input">
            <el-input v-model="ruleFormSign.input" placeholder="请输入用户名或者邮箱"/>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="ruleFormSign.password" type="password" show-password autocomplete="off" placeholder="******"/>
          </el-form-item>
          <el-form-item>
            <el-button class="passForgetButton" @click=""><div>忘记密码？</div></el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitFormSign(ruleFormRefSign)" :disabled="data.isDisabled">
              登录
            </el-button>
            <el-button @click="resetFormSign(ruleFormRefSign)">
              重置
            </el-button>
            <div>
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
              还没有账号？去
            </div>
            <el-button class="transition-button" @click="transitionToRegister">
              注册
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, reactive, computed } from 'vue';
import { gsap } from "gsap";
import router from "@/router/index.js";
import { setUser } from '../store/userStore.js'

const data = reactive({
  isDisabled: false,
  timeLeft: 3,
  successPrompt:computed(() => `${data.pattern}成功！还剩 ${data.timeLeft} 秒自动跳转到首页`),
  failurePrompt:computed(() => `${data.pattern}失败！${data.failureMessage}`),
  failureMessage:'',
  pattern:'',
})

// Vanta背景初始化
const vantaEffect = ref(null);
const vantaSection = ref(null);

const setVanta = () => {
  if (window.VANTA) {
    vantaEffect.value = window.VANTA.GLOBE({
      el: vantaSection.value,
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: 0xd1174f,
      size: 0.9,
      backgroundColor: 0x251444,
    });
  }
};

// 注册表单信息
const formSize = ref('default');
const ruleFormRefReg = ref(null);
const ruleFormReg = reactive({
  username: '',
  password:'',
  email:'',
  gender: '',
  grade: '',
  avatar:'',
  checkPass:'',
  desc: '',
});

// 注册表单校验
// 用户名合法校验
const namePattern = /^[\u4e00-\u9fa5A-Za-z0-9_]+$/;
const validateName = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入用户名'));
  } else if (!namePattern.test(value)) {
    callback(new Error('用户名只能包含汉字、字母、数字和下划线'));
  } else {
    callback();
  }
};

// 密码校验
const passwordPattern = /^[A-Za-z0-9_]+$/;
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'));
  } else if (!passwordPattern.test(value)) {
    callback(new Error('密码只能包含数字、字母和下划线'));
  } else {
    if (ruleFormReg.checkPass !== '') {
      if (!ruleFormRefReg.value) return;
      ruleFormRefReg.value.validateField('checkPass');
    }
    callback();
  }
};

// 确认密码校验
const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'));
  } else if (value !== ruleFormReg.password) {
    callback(new Error("两次密码输入不一致"));
  } else {
    callback();
  }
};

// 邮箱校验
const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const validateEmail = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入电子邮箱'));
  } else if (!emailPattern.test(value)) {
    callback(new Error('不合法的电子邮箱'));
  } else {
    callback();
  }
}

// 校验规则
const rulesReg = reactive({
  username: [
    { required: true, validator: validateName, trigger: 'blur' },
    { min: 2, max: 20, message: '用户名应为2-20个字符', trigger: 'blur' },
  ],
  password: [
      { required: true,validator: validatePass, trigger: 'blur' },
      { min:6, max: 25, message:'密码应为6-25字符', trigger: 'blur'}
  ],
  checkPass: [
      { required: true,validator: validatePass2, trigger: 'blur' }
  ],
  grade: [
    {
      required: false,
      message: '请选择年级',
      trigger: 'change',
    },
  ],
  gender: [
    {
      required: false,
      message: '请选择性别',
      trigger: 'change',
    },
  ],
  email: [
    {
      required: true,
      validator: validateEmail,
      trigger: 'blur',
    },
  ],
  desc: [
    { required: false },
  ],
});

// 注册AJAX
const registerUser = async (userData) => {
  data.pattern = '注册';
  const formData = new FormData();
  formData.append("username", userData.username);
  formData.append("password", userData.password);
  formData.append("email", userData.email);
  if (userData.gender) formData.append("gender", userData.gender);
  if (userData.grade) formData.append("grade", userData.grade);
  if (userData.desc) formData.append("desc", userData.desc);
  if (userData.avatar) formData.append("avatar", userData.avatar);

  try {
    const response = await fetch("http://127.0.0.1:8040/api/register/", {
      method: "POST",
      body: formData, // FormData 会自动设置正确的 `Content-Type`
    });
    const userResponse = await response.json();
    if (!response.ok) {
      let errors;
      if (userResponse.errors.username && userResponse.errors.email) {
        errors = '用户名和邮箱均已存在';
      } else if (userResponse.errors.email) {
        errors = '邮箱已存在';
      } else {
        errors = '用户名已存在';
      }
      throw new Error(errors);
    }

    console.log(`response = ${JSON.stringify(userResponse)}`);

    // 确保包含 access_token 和 refresh_token
    if (userResponse.access_token && userResponse.refresh_token) {
      setUser(userResponse);
    } else {
      throw new Error("注册成功但未返回令牌");
    }

    data.isDisabled = true;
    gsap.to(".prompt", { y: "+=50", opacity: 1 });

    // 3秒后跳转首页
    let timer = setInterval(() => {
      if (data.timeLeft > 0) {
        data.timeLeft -= 1;
      } else {
        clearInterval(timer);
        router.push("/");
      }
    }, 1000);
  } catch (error) {
    console.error("注册错误:", error.message);

    // 处理错误信息
    data.failureMessage = error.message || "注册失败";
    data.isDisabled = false;
    gsap.timeline()
        .to(".prompt", { y: "+=50", opacity: 1})
        .to(".prompt", { y: "-=50", opacity: 0,delay: 3})
  }
};

// 注册按钮
const submitFormReg = async (formEl) => {
  if (!formEl) return;
  await formEl.validate((valid, fields) => {
    if (valid) {
      registerUser(Object.assign({}, ruleFormReg));
    }
  });
};

// 重置按钮
const resetFormReg = (formEl) => {
  if (!formEl) return;
  formEl.resetFields();
}

// 转换动画
const transitionToSignin = () => {
  gsap.timeline()
      .to('.register',{display:'none',opacity:0})
      .to('.sign-in',{display:'block',opacity:1});
}

// 登录表单
// 登录表单信息
const ruleFormRefSign = ref(null);
const ruleFormSign = reactive({
  input: '',
  password: '',
  email:'',
  username:'',
});

// 输入校验
const validateInput = (rule, value, callback) => {
  if (emailPattern.test(value)) {
    ruleFormSign.email = value;
  } else {
    ruleFormSign.username = value;
  }
  callback();
}

// 校验规则
const rulesSign = reactive({
  input: [
    { required: false, validator: validateInput,trigger: 'change' },
  ],
  password: [
    { required: false,validator: validatePass, trigger: 'change' },
    { min:6, max: 25, message:'密码应为6-25字符', trigger: 'blur'}
  ],
});

// 登录AJAX
const loginUser = async (userData) => {
  data.pattern = '登录';
  const formData = new FormData();
  if (userData.username) formData.append("username", userData.username);
  if (userData.email) formData.append("email", userData.email);
  formData.append("password", userData.password);
  try {
    const response = await fetch("http://127.0.0.1:8040/api/login/", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error('用户名或密码错误');
    }

    const userResponse = await response.json();
    setUser(userResponse);

    data.isDisabled = true;
    gsap.to(".prompt", { y: "+=50", opacity: 1 });

    // 3秒后跳转首页
    let timer = setInterval(() => {
      if (data.timeLeft > 0) {
        data.timeLeft -= 1;
      } else {
        clearInterval(timer);
        router.push("/");
      }
    }, 1000);
  } catch (error) {
    console.error(error.message);

    data.failureMessage = error.message || "登录失败";
    data.isDisabled = false;
    gsap.timeline()
        .to(".prompt", { y: "+=50", opacity: 1 })
        .to(".prompt", { y: "-=50", opacity: 0,delay: 3})
  }
}

// 登录按钮
const submitFormSign = async (formEl) => {
  if (!formEl) return;
  await formEl.validate((valid, fields) => {
    if (valid) {
      loginUser(Object.assign({}, ruleFormSign));
    } else {
      console.log('error submit!', fields);
    }
  });
};

// 重置按钮
const resetFormSign = (formEl) => {
  if (!formEl) return;
  formEl.resetFields();
}

// 转换动画
const transitionToRegister = () => {
  gsap.timeline()
      .to('.sign-in',{display:'none',opacity:0})
      .to('.register',{display:'block',opacity:1});
}

onMounted(() => {
  setVanta();
});

onBeforeUnmount(() => {
  if (vantaEffect.value) {
    vantaEffect.value.destroy();
  }
});


</script>

<style scoped>
/* vanta背景 */
.vanta-container {
  width: 100%;
  height: 100vh;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
  pointer-events: none;
}

/* 提示词 */
.prompt {
  position: absolute;
  top: 8%;
  left: 15%;
  width: 550px;
  height: auto;
  z-index: 5;
  opacity: 0;
}

/* 大容器 */
.container {
  position: absolute;
  top: 10%;
  left: 12%;
  width: 600px;
  height: 70%;
  padding: 25px;
  background-color: #ecf0f3;
  border-radius: 12px;
  overflow: hidden;
  transition: 1.25s;
}

/* 注册标题 */
.register-title {
  position: absolute;
  top: 5%;
  left: 36%;
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  z-index: 2;
}

/* 注册表单 */
.register-form {
  position: absolute;
  top: 17%;
  left: 22%;
  z-index: 2;
}

/* 注册登录转换按钮 */
.transition-button {
  border: none;
  background-color: transparent;
  padding: 0;
  color: #f94604;
}

/* 登录 */
.sign-in {
  display: none;
  opacity: 0;
}

/* 登录标题 */
.sign-in-title {
  position: absolute;
  top: 25%;
  left: 36%;
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  z-index: 2;
}

/* 登录表单 */
.sign-in-form {
  position: absolute;
  top: 40%;
  left: 22%;
  z-index: 2;
}

/* 忘记密码按钮 */
.passForgetButton {
  position: absolute;
  right: 0;
  border: none;
  background-color: transparent;
  text-align: right;
}
</style>