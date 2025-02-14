<template>
  <div>
    <h1>User Information</h1>
    <div v-if="user">
      <p>ID: {{ user.id }}</p>
      <p>Username: {{ user.username }}</p>
      <p>Email: {{ user.email }}</p>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const user = ref(null);

const fetchUser = async (userId) => {
  try {
    const response = await axios.get(`http://localhost:8080/api/users/${userId}/`);
    user.value = response.data;
  } catch (error) {
    console.error('Error fetching user:', error);
  }
};

// 在组件挂载时调用 fetchUser
onMounted(() => {
  fetchUser(1); // 替换为您想查询的用户 ID
});
</script>