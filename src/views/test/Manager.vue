<template>
  <div>
    <!--  头部开始  -->
    <div style="height: 60px;background-color: #40a2f6;display: flex;align-items: center">
      <div style="margin-left:20px;width: 200px;display:flex;align-items: center">
        <img style="width: 40px" src="../../assets/re-data.png" alt="logo">
        <span style="font-size: 20px;color: white;margin-left: 5px">后台管理系统</span>
      </div>
      <div style="flex: 1"></div>
      <div style="width: 150px;display: flex;align-items: center;padding-right: 10px">
        <img src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
             alt="UserAvatar"
        style="width: 40px;height: 40px"
        >
        <span style="margin-left: 5px;color: white">{{ data.UserName }}</span>
      </div>
    </div>
    <!--  头部结束  -->

    <!--  下面部分开始  -->
    <div style="display: flex">
      <!--   左侧导航菜单开始   -->
      <div style="width: 200px;border-right: 1px solid #ddd;min-height: calc(100vh - 60px)">
        <el-menu router :default-active="router.currentRoute.value.path" :default-openeds="['2']" style="border: 0" @select="handleSelect">
<!--            default-active="2"-->
<!--            @open="handleOpen"-->
<!--            @close="handleClose"
        >-->
          <!-- 目录主体 -->
          <el-menu-item index="/manager/home">
            <el-icon><House /></el-icon>
            <span>系统首页</span>
          </el-menu-item>

          <!-- 第一级目录(数据统计) -->
          <el-menu-item index="/manager/data">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据统计</span>
          </el-menu-item>

          <el-sub-menu index="2">
            <!-- 第一级目录(用户管理)  -->
            <template #title>
              <el-icon><User /></el-icon>
              <span>用户管理</span>
            </template>
            <!-- 用户管理子目录 -->
              <el-menu-item index="2-1">
                <span>管理员信息</span>
              </el-menu-item>
              <el-menu-item index="2-2">
                <span>普通用户信息</span>
              </el-menu-item>

          </el-sub-menu>

          <el-menu-item index="3">
            <el-icon><UserFilled /></el-icon>
            <span>个人信息</span>
          </el-menu-item>

          <el-menu-item index="4">
            <el-icon><SwitchButton /></el-icon>
            <span>退出登录</span>
          </el-menu-item>

        </el-menu>
      </div>
      <!--   左侧导航菜单结束   -->
      <!--   右侧主体区域开始   -->
      <div style="flex: 1; width: 0; background-color: #f5f7ff;padding: 15px">
        <RouterView />
      </div>
      <!--   右侧主体区域结束   -->
    </div>
    <!--  下面部分结束  -->

  </div>
</template>

<script setup>
import {reactive} from "vue";
import router from "@/router/index.js";


const data = reactive({
  UserName:'Admin',

})

const handleSelect = () => {
  console.log(router.currentRoute.value.path)
}

// 闲置函数
// const handleOpen = (key, keyPath) => {
//   console.log(key, keyPath)
// }
// const handleClose = (key, keyPath) => {
//   console.log(key, keyPath)
// }
</script>

<style scoped>
.el-menu .is-active {
  background-color: #e6f0f8 !important;
}
</style>




<!-- 闲置导航栏 -->
<!--            <el-menu-item-group title="Group Two">-->
<!--              <el-menu-item index="2-3">第三项</el-menu-item>-->
<!--            </el-menu-item-group>-->

<!--            <el-sub-menu index="2-4">-->
<!--              <template #title>第四项</template>-->
<!--              <el-menu-item index="2-4-1">第一节</el-menu-item>-->
<!--            </el-sub-menu>-->
<!--          <el-menu-item index="4" disabled>-->
<!--            <el-icon><document /></el-icon>-->
<!--            <span>Navigator Three</span>-->
<!--          </el-menu-item>-->

<!--          <el-menu-item index="5">-->
<!--            <el-icon><setting /></el-icon>-->
<!--            <span>Navigator Four</span>-->
<!--          </el-menu-item>-->

<!-- 闲置路由嵌套 -->
<!--
<div style="background-color: #eee">
   <div style="font-size: large;font-weight: bold">这是父级页面，可以嵌套其他的子路由页面</div>
   <div style="width: 50% ;margin:30px auto;padding: 20px;border: 1px solid #ccc;background-color: white">
   <RouterView />
   </div>
</div>
-->