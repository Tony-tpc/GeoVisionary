<template>
  <el-card class="feedback-card" shadow="hover">
    <h2>意见反馈</h2>
    <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
      <el-form-item label="反馈内容" prop="content" style="margin-bottom: 24px">
        <el-input
            type="textarea"
            v-model="form.content"
            placeholder="请留下您宝贵的意见或遇到的问题"
            :rows="7"
            maxlength="500"
            show-word-limit
            :resize="'none'"
            style="font-size: 15px"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitFeedback">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";
import {userState} from "@/store/userStore.js";

const formRef = ref();
const form = ref({
  content: "",
  contact: "",
});
const domain = "http://localhost:8040/";

const rules = {
  content: [
    { required: true, message: "请输入反馈内容", trigger: "blur" },
    { min: 5, message: "内容不少于5个字", trigger: "blur" }
  ]
};

const submitFeedback = () => {
  formRef.value.validate( async (valid) => {
    if (valid) {
      const content = form.value.content;
      console.log("提交内容：", content);
      const url = domain + "api/save-feedback/";
      const response = await fetch(url,{
        method: "POST",
        body: JSON.stringify({
          user: userState.user,
          content: content,
        }),
        headers: {
          "Content-Type": "application/json"
        }
      })
      const data = await response.json();
      console.log(data);

      if (!response.ok) {
        ElMessage.error(data);
        throw new Error(data);
      }

      ElMessage.success("反馈已提交，感谢您的支持！");
      resetForm();
    }
  });
};

const resetForm = () => {
  formRef.value.resetFields();
};
</script>

<style scoped>
.feedback-card {
  max-width: 1000px;
  margin: 0 auto;
  padding: 10px 20px 20px 20px;
}
</style>