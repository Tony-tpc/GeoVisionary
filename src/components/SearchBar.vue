<template>
  <div class="search-bar">
    <div v-if="props.searchType === 'collection'">
      <el-select v-model="searchType" placeholder="选择内容类型" size="default" style="width: 120px">
        <el-option label="图文" value="text" />
        <el-option label="视频" value="video" />
      </el-select>
    </div>
    <el-input
        v-model="query"
        :placeholder="placeholderMap[searchType]"
        clearable
        size="default"
        style="flex: 1"
        @keyup.enter.native="onSearch"
    />

    <el-button type="primary" icon="Search" @click="onSearch">搜索</el-button>
    <el-button icon="Refresh" @click="onReset">复原</el-button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  searchType: {
    type: String,
    required: true,
  }
})
const emit = defineEmits(['search','reset']) // 向父组件传递搜索参数

const searchType = ref(props.searchType)
const query = ref('')

const placeholderMap = {
  text: '请输入标题、关键词或摘要',
  video: '请输入视频标题',
}

function onSearch() {
  if (!query.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  emit('search', {
    type: searchType.value,
    keyword: query.value.trim(),
  })
}

function onReset() {
  emit('reset')
}
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding: 10px;
}
</style>
