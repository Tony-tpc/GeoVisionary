<template>
  <div class="parent-container">
    <el-card
        class="error-card"
        v-for="(error, index) in paginatedData"
        :key="index"
        shadow="always"
    >
      <template #header>
        <div class="card-header">
          <span>错题编号：{{ error.problem.id }}</span>
          <span class="tag-group">
            <el-tag v-for="cat in error.problem.categories" :key="cat.id" type="info" size="small">
              {{ cat.name }}
            </el-tag>
          </span>
        </div>
      </template>

      <div class="question-block">
        <strong>题目：</strong>{{ error.problem.question }}
      </div>

      <div class="choices">
        <div
            v-for="(text, key) in error.problem.choices"
            :key="key"
            :class="[
            'choice',
            key === error.user_answer ? 'user-wrong' : '',
            key === error.problem.answer[0] ? 'correct' : '',
          ]"
        >
          <strong>{{ key }}.</strong> {{ text }}
        </div>
      </div>

      <div class="answer-info">
        <el-tag type="danger">你的答案：{{ error.user_answer }}</el-tag>
        <el-tag type="success">正确答案：{{ error.problem.answer[0] }}</el-tag>
      </div>

      <div class="explanation">
        <strong>解析：</strong>
        <p v-html="formatExplanation(error.problem.explanation)"></p>
      </div>
    </el-card>

    <el-pagination
        background
        layout="prev, pager, next"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="errorData.length"
        @current-change="handlePageChange"
        class="pagination"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { userState } from "@/store/userStore.js";

const domain = "http://localhost:8040";
const errorData = ref([]);
// 分页相关状态
const currentPage = ref(1);
const pageSize = 4;

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize;
  const end = start + pageSize;
  return errorData.value.slice(start, end);
});

const handlePageChange = (page) => {
  currentPage.value = page;
};

// 获取错题信息
const errorQuestionRequest = async () => {
  const url = domain + "/api/load-history/";
  const response = await fetch(url, {
    method: "POST",
    body: JSON.stringify({
      user: userState.user,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  const responseData = await response.json();
  errorData.value = responseData.sort((a, b) => a.problem.id - b.problem.id);
};

const formatExplanation = (text) => {
  return text.replace(/\r\n/g, "<br>");
};

onMounted(() => {
  errorQuestionRequest();
});
</script>

<style scoped>
.parent-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  overflow-y: auto;
}
.error-card {
  width: 90%;
  height: auto;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.tag-group {
  display: flex;
  gap: 5px;
}
.question-block {
  margin: 10px 0;
  font-size: 16px;
}
.choices {
  margin-top: 10px;
}
.choice {
  margin: 5px 0;
  padding: 5px 10px;
  border-radius: 6px;
}
.user-wrong {
  background-color: #ffe6e6;
  border: 1px solid #ff9999;
}
.correct {
  background-color: #e6ffea;
  border: 1px solid #99ffbb;
}
.answer-info {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}
.explanation {
  margin-top: 10px;
  background: #f9f9f9;
  padding: 10px;
  border-left: 4px solid #409EFF;
}
</style>