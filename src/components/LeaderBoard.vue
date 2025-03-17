<template>
  <main class="leaderboard" v-loading="loading">
    <section class="leaderboard-header">
      <span style="font-size: 28px;margin-right: 10px;text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);padding-top: 5px">🏆</span>
      <h2 class="leaderboard-title" style="padding-top: 5px">排行榜</h2>
    </section>
    <section class="leaderboard-shell">
      <table class="leaderboard-table">
        <thead>
        <tr>
          <th>排名</th>
          <th>用户名</th>
          <th>答对题数</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(item, index) in sortedTableData" :class="['leaderboard-row', { first: index === 0, second: index === 1, third: index === 2, even: index % 2 !== 0 }]">
          <td :style="{ padding: '20px'}">{{ index + 1 > 3 ? index + 1 : rateEmoji[index]}}</td>
          <td>{{ item.username }}</td>
          <td>{{ item.correctProblems }}</td>
        </tr>
        <!-- 固定行，显示本人信息 -->
        <tr v-if="userState.user" :class="['leaderboard-user-row', { first: userRate(userState.user.username) === 1, second: userRate(userState.user.username) === 2, third: userRate(userState.user.username) === 3 }]">
          <td>{{ userRate(userState.user.username) <= 3 ? rateEmoji[userRate(userState.user.username) - 1] : userRate(userState.user.username) }}</td>
          <td>{{ userState.user.username }}</td>
          <td>{{ userState.user.correct_problems }}</td>
        </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { userState } from "@/store/userStore.js";

const domainName = import.meta.env.VITE_DOMAIN_NAME;

const tableData = ref([]);
const loading = ref(computed(() => tableData.value.length === 0));
const rateEmoji = ['🥇','🥈','🥉']

const sortedTableData = computed(() => {
  return tableData.value.sort((a, b) => b.correctProblems - a.correctProblems);
});

const getLeaderboard = async () => {
  const response = await fetch(`http://${domainName}/api/get-leaderboard`, { method: "GET" });

  if (!response.ok || !response.body) throw new Error("请求失败");
  const data = await response.json();
  const userObject = data.user_object;

  Object.entries(userObject).forEach(([key, value]) => {
    tableData.value.push({ username: key, correctProblems: value.correct_problems, avatar: value.avatar ? value.avatar : "" });
  });
}

const userRate = (username) => {
  const userIndex = sortedTableData.value.findIndex(user => user.username === username);
  return userIndex !== -1 ? userIndex + 1 : 0;
}
onMounted(() => {
  getLeaderboard();
})
</script>

<style scoped>
/* 排行榜 */
.leaderboard {
  position: absolute;
  top: 12%;
  right: 7%;
  width: 500px;
  padding: 20px 0;
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  box-shadow: 0 8px 16px #0005;
  height: 80%;
  overflow: hidden;
  font-size: 16px;
}

/* 标题 */
.leaderboard-title {
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  font-family: cursive,"Arial", sans-serif;
  letter-spacing: 2px;
  color: #fffdf3;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

/* 表格 */
.leaderboard-table {
  width: 100%;
  background-color: transparent !important;
  overflow-x: hidden;
}

/* 表头容器 */
.leaderboard-header {
  width: 100%;
  height: 10%;
  padding-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 主体容器 */
.leaderboard-shell {
  width: 95%;
  max-height: calc(90% - 25px);
  background-color: #fffb;
  margin: 12px auto;
  border-radius: 10px;
  overflow: auto;
}
.leaderboard-shell::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

/* 表格 */
table {
  width: 100%;
}
table, th, td {
  border-collapse: collapse;
  padding: 20px;
  text-align: center;
}

/* 用户头像 */
td img {
  width: 36px;
  height: 36px;
  margin-right: 10px;
  border-radius: 50%;
  vertical-align: middle;
}

/* 表头 */
thead th {
  position: sticky;
  top: 0;
  left: 0;
  background-color: #d5d1defe;
  font-size: 20px;
}

/* 偶数行背景色 */
tbody tr.even {
  background-color: #f8f8f8;
}

tbody tr:hover {
  background-color: rgb(212, 212, 212) !important;
}

/* 前三名特殊样式 */
tbody tr.first {
  color: rgb(255, 176, 46);
  font-weight: bold;
  font-size: 28px;
  animation: glow-first 2s infinite alternate none;
}

tbody tr.second {
  color: rgb(168, 168, 168);
  font-weight: bold;
  font-size: 25px;
  text-shadow: 0 1px 2px rgba(121, 118, 118, 0.6);
}

tbody tr.third {
  color: rgb(206, 138, 68);
  font-weight: bold;
  font-size: 20px;
  text-shadow: 0 1px 1px rgba(121, 118, 118, 0.6);
}

/* 第一名发光动画 */
@keyframes glow-first {
  0% { text-shadow: 0 1px 1px rgba(255, 223, 87, 0.8); }
  100% { text-shadow: 0 1px 3px rgba(255, 159, 67, 1); }
}

/* 用户排名表格 */
.leaderboard-user-row {
  position: sticky;
  bottom: 0;
  background: rgba(255, 255, 255, 1);
  font-weight: bold;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.2); /* 增加顶部阴影，提升层次感 */
  z-index: 2;
}

/* 让单独一行对齐表格 */
.leaderboard-user-row td {
  padding: 20px;
  text-align: center;
}

/* 加载蒙层 */
:deep(.el-loading-mask) {
  z-index: 899;
}
</style>

