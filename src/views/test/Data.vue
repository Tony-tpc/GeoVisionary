<template>
  <div>
    <div class="card" style="margin-bottom: 5px">
        <el-input style="width: 240px;margin-right: 10px"
                  v-model="data.input"
                  placeholder="请输入名称查询"
                  prefix-icon="Search"
                  clearable
        >
        </el-input>
      <el-button type="primary">查 询</el-button>
      <el-button type="warning" @click="data.input=null">重 置</el-button>
    </div>
    <div class="card" style="margin-bottom: 5px">
      <el-button type="primary">新 增</el-button>
      <el-button type="danger">批量删除</el-button>
      <el-button type="info">导入</el-button>
      <el-button type="success">导出</el-button>
    </div>
    <div class="card" style="margin-bottom: 5px">
      <el-table :data="data.tableData" stripe>
        <el-table-column label="日期" prop="date" />
        <el-table-column label="名称" prop="name" />
        <el-table-column label="住址" prop="address" />
      </el-table>
      <div style="margin-top: 15px">
        <el-pagination
            v-model:current-page="data.currentPage"
            v-model:page-size="data.pageSize"
            :page-sizes="[5, 10, 15, 20]"
            :size="data.size"
            :disabled="data.disabled"
            :background="data.background"
            layout="total, sizes, prev, pager, next, jumper"
            :total="data.tableData.length"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import { Search } from "@element-plus/icons-vue";

const data = reactive({
  input:null,
  tableData:[{
    id:1,
    date: '2016-05-03',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },{
    id:2,
    date: '2016-05-02',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },{
    id:3,
    date: '2016-05-04',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  }, {
    id:4,
    date: '2016-05-05',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },{
    id:5,
    date: '2016-05-06',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  },{
    id:6,
    date: '2016-05-08',
    name: 'Tom',
    address: 'No. 189, Grove St, Los Angeles',
  }],
  currentPage:1,
  pageSize:5,
  size:'default',
  background:true,
  disabled:false,
})
</script>

<style scoped>

</style>