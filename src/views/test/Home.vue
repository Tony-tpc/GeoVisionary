<template>
  <div style="margin-bottom:20px ">
    <RouterLink to="/manager/test"> 跳转到Test.vue页面</RouterLink>
  </div>

  <div style="margin-bottom: 20px">
    <el-button type="primary" @click="router.push('/manager/test')">跳转到新的页面</el-button>
  </div>

  <div style="margin-bottom: 20px">
    <el-button type="primary" @click="router.push({ path:'/manager/test',query:{ id:2,name:'情歌' } })">路由传参id=2&name=情歌</el-button>
  </div>

  <div>
<!--    此处如果不设置宽度则默认整行宽    -->
    <el-input v-model="data.input"
              style="width: 240px"
              placeholder="请输入想要查询的内容"
              :prefix-icon="Search"
              clearable
    />
    {{ data.input }}
  </div>
  <div>
    <el-input v-model="data.input2" style="width: 240px"
              placeholder="请输入想要查询的日期" :suffix-icon="Calendar"
              disabled
    />
  </div>
  <div>
    <el-input
        v-model="data.descr"
        style="width: 240px"
        :rows="2"
        type="textarea"
        placeholder="Please input"
        readonly
    />
  </div>

  <div style="margin: 20px">
    <el-select
        multiple
        v-model="data.value"
        placeholder="Select"
        size="large"
        style="width: 240px"
    >
      <el-option
          v-for="item in data.options"
          :key="item.value"
          :label="item.label"
          :value="item.value"
      />
    </el-select>
    {{ data.value }}
  </div>

  <div style="margin: 20px">
    <el-button @click="getProvince">点击获取省份信息</el-button>
    <span id="province"></span>
  </div>

  <div class="mb-2 ml-4">
    <el-radio-group v-model="data.sex">
      <el-radio value="男" size="large">男</el-radio>
      <el-radio value="女" size="large">女</el-radio>
    </el-radio-group>
  </div>
<!--  <div class="my-2 ml-4">
    <el-radio-group v-model="radio2">
      <el-radio value="1">Option 1</el-radio>
      <el-radio value="2">Option 2</el-radio>
    </el-radio-group>
  </div>
  <div class="my-4 ml-4">
    <el-radio-group v-model="radio3">
      <el-radio value="1" size="small">Option 1</el-radio>
      <el-radio value="2" size="small">Option 2</el-radio>
    </el-radio-group>
  </div>-->
  <div>
    <el-radio-group v-model="data.tag" size="large">
      <el-radio-button label="我发布的内容" value="1" />
      <el-radio-button label="我点赞的内容" value="2" />
      <el-radio-button label="我评论的内容" value="3" />
      <el-radio-button label="我收藏的内容" value="4" />
    </el-radio-group>
  </div>

  <div style="margin: 20px">
    <el-checkbox-group v-model="data.checkList">
      <el-checkbox v-for="item in data.options"
      :key="item.id"
      :label="item.label"
      :value="item.value"
      />
    </el-checkbox-group>
    <span style="margin: 20px">{{ data.checkList }}</span>
  </div>

  <div class="demo-image__preview">
    <el-image
        style="width: 100px; height: 100px"
        :src="imgSrc"
        :zoom-rate="1.2"
        :max-scale="7"
        :min-scale="0.2"
        :preview-src-list="data.srcList"
        :initial-index="4"
        fit="cover"
    />
  </div>

  <div style="margin: 20px 0">
    <el-carousel height="400px" style="width: 500px">
      <el-carousel-item v-for="item in data.imgs" :key="item">
        <img style="width: 100%;height: 400px" :src="item" alt="">
      </el-carousel-item>
    </el-carousel>
  </div>

  <div style="margin: 20px">
    <el-date-picker
        v-model="data.day"
        type="date"
        placeholder="请选择日期"
        :size="data.size"
        format="YYYY/MM/DD"
        value-format="YYYY/MM/DD"
    />
    {{ data.day }}

    <el-date-picker
        v-model="data.time"
        type="datetime"
        placeholder="请选择时间"
        :size="data.size"
        format="HH:mm:ss"
        value-format="HH:mm:ss"
    />

    <el-date-picker
        v-model="data.dateRange"
        type="daterange"
        range-separator="到"
        start-placeholder="请选择开始日期"
        end-placeholder="请选择结束日期"
        :size="data.size"
        format="YYYY/MM/DD"
        value-format="YYYY/MM/DD"
    />
    {{ data.dateRange?.length ? data.dateRange[0]:''}}
    {{ data.dateRange?.length ? data.dateRange[1]:''}}
  </div>

  <div style="margin: 20px">
    <el-table :data="data.tableData" style="width: 100%" stripe>
      <el-table-column prop="date" label="日期" width="180" head-align="center"/>
      <el-table-column prop="name" label="姓名" width="180" />
      <el-table-column prop="address" label="住址" />
      <el-table-column label="操作">
        <template #default="scope">
          <el-button type="primary" circle
                     @click="edit(scope.row)">
            <el-icon><Edit /></el-icon>
          </el-button>
          <el-button type="danger" circle
                     @click="del(scope.row.id)">
            <el-icon><Delete /></el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>

  <div style="padding: 10px 0">
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
<!--    @size-change="handleSizeChange"
        @current-change="handleCurrentChange"     此部分将利用后台分页-->
  </div>

  <el-dialog
      v-model="data.dialogVisible"
      title="编辑行对象"
      width="500"
  >
    <div style="margin: 10px">日期：{{ data.row.date }}</div>
    <div style="margin: 10px">名称：{{ data.row.name }}</div>
    <div>地址：{{ data.row.address }}</div>
    <template #footer>
      <div>
        <el-button @click="data.dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="data.dialogVisible = false">
          Confirm
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {reactive} from "vue";
import {Calendar, Search} from "@element-plus/icons-vue";
import imgSrc from '@/assets/logo.png'
import lun1 from '@/assets/logo.png'
import lun2 from '@/assets/logo.png'
import lun3 from '@/assets/logo.png'
import router from "@/router/index.js";
import axios from "axios";

const data = reactive({
  input:'',
  input2:null,
  descr:'用于输入多行文本信息可缩放的输入框。 添加 type="textarea" ' +
        '属性来将 input 元素转换为原生的 textarea 元素。',
  options:[{
    id:1,
    value:9,
    label:'苹果'
  },{
    id:2,
    value:16,
    label:'香蕉'
  },{
    id:3,
    value:25,
    label:'桃子'
  }],
  value:null,
  sex:null,
  tag:'4',
  checkList:[],
  srcList:['','',''],
  imgs:[lun1,lun2,lun3],
  day:null,
  day1:null,
  time:null,
  dateRange:null,
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
  currentPage:null,
  pageSize:5,
  background:true,
  size:'default',
  disabled:false,
  dialogVisible:false,
  row:null,
})
const del = (id) => {
  alert('删除ID=' + id + '的数据')
}
const edit = (row) => {
  data.row = row
  data.dialogVisible = true
}

const getProvince = () => {
  axios({
    url:'https://hmajax.itheima.net/api/province'
  }).then(result => {
    console.log(result)
    console.log(result.data.list)
    console.log(result.data.list.join('<br>'))
    document.getElementById('province').innerHTML = result.data.list.join('<br>')
  })
}
/*
const handleSizeChange = (val) => {
  console.log(`${val} items per page`)
}
const handleCurrentChange = (val) => {
  console.log(`current page: ${val}`)
}
*/
// data.tableData = data.tableData.slice(0,5) 假数据处理
</script>