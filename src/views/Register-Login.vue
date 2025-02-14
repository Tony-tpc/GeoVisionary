<template>
  <!--  vanta背景  -->
  <div class="vanta-container" ref="vantaSection"></div>
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
          <el-form-item label="用户名" prop="name">
            <el-input v-model="ruleFormReg.name" placeholder="请输入用户名"/>
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
              <el-option label="高一" value="High-1" />
              <el-option label="高二" value="High-2" />
              <el-option label="高三" value="High-3" />
            </el-select>
          </el-form-item>
          <el-form-item label="性别" prop="gender">
            <el-radio-group v-model="ruleFormReg.gender">
              <el-radio value="male">男</el-radio>
              <el-radio value="female">女</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="备注" prop="desc">
            <el-input v-model="ruleFormReg.desc"  type="textarea" :autosize="{ minRows:2 , maxRows:4 }" :maxlength="100" resize="none" show-word-limit placeholder="我们期待了解您希望在我们的平台上实现的目标。"/>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitFormReg(ruleFormRefReg)">
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
            <el-button type="primary" @click="submitFormSign(ruleFormRefSign)">
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
import { ref, onMounted, onBeforeUnmount, reactive } from 'vue';
import { gsap } from "gsap";

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
  name: '',
  grade: '',
  gender: '',
  email:'',
  password:'',
  checkPass:'',
  desc: '',
});

// 注册表单校验
// 密码校验
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请输入密码'));
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
    callback(new Error("两次密码输入不一致！"));
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
    callback(new Error('不合法的电子邮箱！'));
  } else {
    callback();
  }
}

// 校验规则
const rulesReg = reactive({
  name: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
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

// 注册按钮
const submitFormReg = async (formEl) => {
  if (!formEl) return;
  await formEl.validate((valid, fields) => {
    if (valid) {
      console.log('submit!');
    } else {
      console.log('error submit!', fields);
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
  name:'',
});

// 输入校验
const validateInput = (rule, value, callback) => {
  if (emailPattern.test(value)) {
    ruleFormSign.email = value;
  } else {
    ruleFormSign.name = value;
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

// 登录按钮
const submitFormSign = async (formEl) => {
  if (!formEl) return;
  await formEl.validate((valid, fields) => {
    if (valid) {
      // 此处需分析是否为用户名
      console.log('submit!');
    } else {
      console.log('error submit!', fields);
    }
    console.log(`formEl:${formEl}`)
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