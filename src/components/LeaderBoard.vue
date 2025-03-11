<template>
  <main class="leaderboard">
    <section class="leaderboard-header">
      <h1 class="leaderboard-title">🏆 排行榜</h1>
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
        <tr v-for="item in tableData">
          <td>{{ item.rate }}</td>
          <td>{{ item.username }}</td>
          <td>{{ item.correctProblems }}</td>
        </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>

<script setup>
const tableData = [
  {
    rate:1,
    username: 'admin',
    correctProblems: '9',
  },
  {
    rate:2,
    username: 'admin3',
    correctProblems: '9',
  },
  {
    rate:3,
    username: 'admin5',
    correctProblems: '9',
  },
  {
    rate:4,
    username: 'admin2',
    correctProblems: '8',
  },
  {
    rate:5,
    username: 'admin7',
    correctProblems: '7',
  },
  {
    rate:6,
    username: 'admin6',
    correctProblems: '6',
  },
  {
    rate:7,
    username: 'admin1',
    correctProblems: '5',
  },
]
</script>

<style scoped>
/* 排行榜 */
.leaderboard {
  position: absolute;
  top: 20%;
  right: 20%;
  width: 300px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.3); /* 半透明黑板质感 */
  border-radius: 10px;
  box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.6);
}

.leaderboard-title {
  font-size: 28px;
  font-weight: bold;
  text-align: center;
  color: #fff;
  font-family: cursive;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.leaderboard-table {
  width: 100%;
  background-color: transparent !important;
  overflow-x: hidden;
}
</style>