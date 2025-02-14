<template>
  <div class="box">
    <svg t="1738290868042" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="7044" width="200" height="200">
      <defs>
        <!-- 定义遮罩 -->
        <mask id="fillMask" style="z-index: 6;">
          <rect ref="maskRect" x="000" y="0" width="925" height="1000" fill="white"/>
        </mask>
      </defs>
      <path d="M784.64 784c-48 0-73.6-22.4-96-38.4-16-16-28.8-25.6-54.4-25.6-25.6 0-35.2 9.6-54.4 25.6-19.2 19.2-44.8 38.4-96 38.4-48 0-73.6-22.4-96-38.4-16-16-28.8-25.6-54.4-25.6-25.6 0-35.2 9.6-54.4 25.6-19.2 19.2-44.8 38.4-96 38.4-48 0-73.6-22.4-96-38.4-16-16-28.8-25.6-54.4-25.6-19.2 0-32-12.8-32-32s12.8-32 32-32c48 0 73.6 22.4 96 38.4 16 16 28.8 25.6 54.4 25.6 25.6 0 35.2-9.6 54.4-25.6 19.2-19.2 44.8-38.4 96-38.4s73.6 22.4 96 38.4c16 16 28.8 25.6 54.4 25.6 25.6 0 35.2-9.6 54.4-25.6 19.2-19.2 44.8-38.4 96-38.4 48 0 73.6 22.4 96 38.4 16 16 28.8 25.6 54.4 25.6 25.6 0 35.2-9.6 54.4-25.6 19.2-19.2 44.8-38.4 96-38.4 19.2 0 32 12.8 32 32s-12.8 32-32 32c-25.6 0-35.2 9.6-54.4 25.6-22.4 16-48 38.4-96 38.4z m-147.2 176c-48 0-76.8-22.4-96-38.4-19.2-16-28.8-25.6-54.4-25.6-25.6 0-38.4 9.6-54.4 25.6-19.2 19.2-48 38.4-96 38.4s-73.6-22.4-96-38.4c-19.2-16-28.8-25.6-54.4-25.6-19.2 0-32-12.8-32-32s12.8-32 32-32c48 0 73.6 22.4 96 38.4 16 16 28.8 25.6 54.4 25.6 25.6 0 38.4-9.6 54.4-25.6 19.2-19.2 48-38.4 96-38.4s76.8 22.4 96 38.4c16 16 28.8 25.6 54.4 25.6 25.6 0 38.4-9.6 54.4-25.6 19.2-19.2 48-38.4 96-38.4 19.2 0 32 12.8 32 32s-12.8 32-32 32c-25.6 0-38.4 9.6-54.4 25.6-22.4 16-48 38.4-96 38.4z m294.4-371.2h-547.2l217.6-371.2c12.8-19.2 35.2-32 57.6-32 25.6 0 48 12.8 57.6 32l214.4 371.2z m-438.4-64h326.4l-160-275.2h-6.4l-160 275.2z m-35.2 64h-416l307.2-553.6c9.6-22.4 32-35.2 57.6-35.2s48 12.8 57.6 35.2l153.6 275.2-160 278.4z m-307.2-64h268.8l124.8-214.4L410.24 64h-3.2l-3.2 3.2-252.8 457.6z"
            fill="rgba(255,255,255,0.5)"
            p-id="7045"
            mask="url(#fillMask)">
      </path>
    </svg>
  </div>
  <div>
    <div style="margin-bottom: 20px">
      <el-button type="primary" @click="router.back()">返回主页</el-button>
    </div>
    <div style="font-size: 20px;font-weight: bold;color: red;text-decoration: underline;font-style: italic;margin-bottom: 20px;">
      欢迎
    </div>

    <div style="font-size: 30px">
      <!--      此处尝试Vue3基础语法 -->
      {{ a }} {{ b }}
    </div>

    <div style="margin-bottom: 20px">
      {{ data.a }}
      {{ data.b }}
    </div>

    <div style = "margin-bottom: 20px">
      <input v-model = "data.a" />
    </div>

    <div style="margin-bottom: 20px">
      <span style="color: red" v-if = "data.name === '凤雏'">卧龙凤雏</span>
      <span style="color: aqua" v-if = "data.name === '元直'">水镜元直</span>
      <span style="color: pink" v-else>abcd</span>
    </div>

    <div style="display: flex">
      <div style="width: 300px;height: 300px;text-align: center;
      line-height: 300px;font-size: 30px;margin: 10px;
      background-color: green" v-for="item in data.arr">{{ item }}</div>
    </div>

    <div>
      <select style="width: 200px">
        <option v-for="item in data.arr">{{ item }}</option>
      </select>
    </div>

    <div style="margin-bottom: 20px">
      <button @click="click()">点我！</button>
    </div>

    <div style="margin-bottom: 20px">
      <div :style="data.box"></div>
      <div>
        <img :src="data.img">
      </div>
    </div>

    <div style="margin: 30px">
      <el-button @click="clickData" color="#41b883" :style="{ 'color':'red' }" :loading="data.loading">启动</el-button>
      <el-button type="primary">Primary</el-button>
      <el-button type="success">Success</el-button>
      <el-button type="info">Info</el-button>
      <el-button type="warning">Warning</el-button>
      <el-button type="danger">Danger</el-button>
    </div>

    <div style="margin: 30px">
      <el-icon :size="20">
        <Edit />
      </el-icon>
      <span style="margin: 30px">
      <el-icon :size="15" style="top: 2px">
        <View />
      </el-icon>100
      </span>
      <el-input
          v-model="data.a"
          style="width: 240px"
          placeholder="Type something"
          :prefix-icon="Search"
      />
    </div>

    <div>
      <el-input v-model="data.input" style="width: 240px" placeholder="Please input" />
    </div>

  </div>



</template>

<script setup>
import {reactive, ref,onMounted} from "vue";
import {Search} from "@element-plus/icons-vue";
import router from "@/router/index.js";

const a = ref(1)
const b = ref("测试用字符串")
/* 推荐以下reactive渲染数据，一次性完成多个渲染 */
const data = reactive({
  id:router.currentRoute.value.query.id,
  name:router.currentRoute.value.query.name,
  a:123,
  b:"A String",
  // name: '元直3',
  loading:false,
  arr: ['苹果','香蕉','橘子'],
  box: {
    width: '100px',
    height: '100px',
    backgroundColor: 'red'
  },
  img :'https://www.runoob.com/wp-content/uploads/2017/01/vue.png',
  input:'',
})

console.log('获取到传递过来的id=' + data.id + ',name=' + data.name)

onMounted(() => {
  console.log('页面加载完成')
})
const click = () => {
  alert("好运+1")
}

const clickData = async () => {
  data.loading = true
  try {
    // 模拟一个异步操作，例如 API 请求
    await new Promise((resolve) => setTimeout(resolve, 2000));
  } catch (error) {
    console.error(error);
  } finally {
    data.loading = false; // 操作完成后将 loading 设置为 false
  }
}

</script>

<style scoped>
.box {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 260px;
  height: 344px;
  background-color: #f94604;
  border: 1px solid rgba(255, 255, 255, 0.5);
  z-index: 3;
  overflow: hidden;
}

.icon, #fillMask{
  position: absolute;
  width: 125px;
  height: auto;
  top: 50%;
  left: 50%;
  transform: translate(-50%,-50%);
}

</style>