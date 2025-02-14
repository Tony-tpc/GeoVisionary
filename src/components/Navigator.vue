<template>
<!--  导航栏开始-->
      <div class="navigator">
          <div style="padding-left: 200px">
            <el-menu
                class="menu-no-border"
                mode="horizontal"
                :ellipsis="false"
                @select="handleSelect"
                :default-active="router.currentRoute.value.path"
                router
                unique-opened
                :default-openeds="['/navigator']"
                style="background-color: transparent"
            >
              <el-affix>
              <div>
                <el-link href="/navigator/home"
                         :underline="false"
                >
                  <img
                      style="width: 50px"
                      :src="data.logo"
                      alt="智绘山河logo"
                  />
                </el-link>
              </div>
              </el-affix>
              <div class="menu-items">
                <el-sub-menu index="/"
                             :class="['regular', 'custom-sub-menu', { 'dark-theme': data.isDarkMode }]"
                >
                  <template #title>
                    <span :class="['menu-fonts',{ 'dark-theme': data.isDarkMode }]">智绘天地</span>
                  </template>
                  <el-menu-item index="/navigator/landform"
                                :class="[{ 'active-item-1': data.activeIndex === '/navigator/landform' }]"
                  >
                    <span class="menu-fonts" :style="{ color: data.activeIndex === '/navigator/landform' ? '#fffdf3' : '#0d534b' }">地形</span>
                  </el-menu-item>
                  <el-menu-item index="/navigator/moon-phase"
                                :class="[{ 'active-item-2': data.activeIndex === '/navigator/moon-phase' }]"
                  >
                    <span class="menu-fonts" :style="{ color: data.activeIndex === '/navigator/moon-phase' ? '#fffdf3' : '#0d534b' }">月相</span>
                  </el-menu-item>
                  <el-menu-item index="/navigator/climate"
                                :class="[{ 'active-item-3': data.activeIndex === '/navigator/climate' }]"
                  >
                    <span class="menu-fonts" :style="{ color: data.activeIndex === '/navigator/climate' ? '#fffdf3' : '#0d534b' }">气候</span>
                  </el-menu-item>
                  <el-menu-item index="/navigator/world-map"
                                :class="[{ 'active-item-4': data.activeIndex === '/navigator/world-map' }]"
                  >
                    <span class="menu-fonts" :style="{ color: data.activeIndex === '/navigator/world-map' ? '#fffdf3' : '#0d534b' }">地图</span>
                  </el-menu-item>
                </el-sub-menu>
                <el-menu-item index="/navigator/geo-graph"
                              :class="['regular',{ 'dark-theme': data.isDarkMode },{ 'active-item-1': data.activeIndex === '/navigator/geo-graph' }]"
                >
                  <span :class="['menu-fonts',{ 'dark-theme': data.isDarkMode }]" :style="{ color: data.activeIndex === '/navigator/geo-graph' ? '#fffdf3' : 'var(--text-color)' }">知象图谱</span>
                </el-menu-item>
                <el-menu-item index="/navigator/insight-lab"
                              :class="['regular',{ 'dark-theme': data.isDarkMode },{ 'active-item-3': data.activeIndex === '/navigator/insight-lab' }]"
                >
                  <span :class="['menu-fonts',{ 'dark-theme': data.isDarkMode }]" :style="{ color: data.activeIndex === '/navigator/insight-lab' ? '#fffdf3' : 'var(--text-color)' }">探知问学</span>
                </el-menu-item>
                <el-menu-item index="/navigator/smart-recs"
                              :class="['regular',{ 'dark-theme': data.isDarkMode },{ 'active-item-4': data.activeIndex === '/navigator/smart-recs' }]"
                >
                  <span :class="['menu-fonts',{ 'dark-theme': data.isDarkMode }]" :style="{ color: data.activeIndex === '/navigator/smart-recs' ? '#fffdf3' : 'var(--text-color)' }">智荐学堂</span>
                </el-menu-item>
<!--                <el-button text style="align-items: center;height: 55px">-->
<!--                  <el-icon size="30px"><Search /></el-icon>-->
<!--                </el-button>-->
                <div class="user">
                  <el-button link :icon="User" :class="['register',{ 'dark-theme' : data.isDarkMode }]" @click="router.push('/register-login')">
                    <span>注册/登录</span>
                  </el-button>
                </div>
              </div>
            </el-menu>
          </div>
      </div>
  <!--  导航栏结束-->
  <!--  主体区域-->
      <div class="full-screen-container" id="main">
        <RouterView />
      </div>
</template>

<script setup>
import { reactive, onMounted, provide,ref } from "vue";
import { User } from "@element-plus/icons-vue";
import router from "@/router/index.js";
import lightLogo from "@/assets/mountain-fffdf3.svg";
import darkLogo from "@/assets/mountain-0d534b.svg";
import { throttle } from "lodash";
import { gsap } from "gsap";

const data = reactive({
  activeIndex: router.currentRoute.value.path,    // 保持选中menu选项常量
  isDarkMode : false,                             // 切换主题
  logo: lightLogo,                                // 切换logo配色
  scrollY: 0,                                     // 主题切换判据
});

// Home第三屏切换主题色
const TopChangeMode = ref(6200);
const isLoading = ref(false);
provide('TopChangeMode',TopChangeMode);
provide('isLoading',isLoading)

// 防止频繁触发（延迟200ms）
let ticking = false;

// 更换主题
const updateTheme = throttle(() => {
  // 之后可根据需要改变主题切换逻辑
  if (data.activeIndex === '/navigator/geo-graph') {
    data.isDarkMode = true;
    data.logo = darkLogo;
  } else {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(() => {
        data.scrollY = window.scrollY;
        data.isDarkMode = (data.scrollY > 640 && data.scrollY < (TopChangeMode.value - 50))
            || data.scrollY > (TopChangeMode.value + 6.3 * window.innerHeight - 140); // 进入第二屏或第四屏时，切换深色模式
        data.logo = data.isDarkMode? darkLogo : lightLogo;
        ticking = false;
      });
    }
  }
},200);

// 保持选中菜单颜色
const handleSelect = (index) => {
  data.activeIndex = index;
};

const savedIndex = localStorage.getItem('activeIndex');
if (savedIndex) {
  data.activeIndex = savedIndex;
}

onMounted(() => {
  // 自动调节主题色
  window.addEventListener('scroll',updateTheme);
  // 配合加载动画
  if (isLoading.value)
    gsap.to('.navigator',{opacity:1,duration:1.5},2.6);
  else
    document.querySelector('.navigator').style.opacity = 1;
})

</script>

<style scoped>
/* 导航栏 */
.navigator {
  position: fixed;
  top: 15px;
  left: 0;
  width: 100%;
  padding: 0;
  z-index: 5;
  opacity: 0;
}

/* 去掉菜单项之间的分界线 */
.menu-no-border {
  border-bottom: none !important;
  display: flex;
  justify-content: space-between;
  align-items: center;
  overflow: hidden;
}

/* 菜单项 */
.regular {
  display: flex;
  justify-content: center;
  align-items: center;
  left: 0;
  top: 0;
  width: 135px;
  height: 42px;
  border-radius: 51px;
  color: var(--text-color);
  background-color: var(--bg-color);
  margin-left: 25px;
}

/* 自定义子目录 */
.custom-sub-menu {
  position: relative;
  padding: 0;
  overflow: hidden;
}

/* 添加过渡动画，与其他目录项保持一致 */
.el-sub-menu {
  transition: 0.25s;
}

/* 目的同上 */
.el-sub-menu__title:hover {
  background-color: var(--el-menu-hover-bg-color) !important;
  color: var(--el-menu-hover-text-color) !important;
}

/*由菜单项选中颜色和菜单项文本颜色组成*/
.active-item-1 {
  background-color: #46b61f !important;
}
.active-item-2 {
  background-color: #0066bc !important;
}
.active-item-3 {
  background-color: #ffad00 !important;
}
.active-item-4 {
  background-color: #5e41b8 !important;
}

/* 菜单项 */
.menu-items {
  display: flex;
  margin-right: 25px;
  text-align: center;
}

/* 菜单字体 */
.menu-fonts {
  font-size: 18px;
  font-weight: bold;
  color: var(--text-color);
  text-align: center;
}

/* 用户 */
.user {
  margin:0 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 注册/登录项，与菜单项风格作区分 */
.register {
  height: 42px;
  width: 135px;
  background-color: transparent;
  border-radius: 51px;
  border: 1px solid var(--primary-color);
  color: var(--bg-color);/* 此样式文字与背景主题互换 */
  font-size: 16px;
  font-weight: bold;
}
.register:hover {
  border-color: var(--bg-color) !important;
  color: var(--bg-color);
}

/* 主页全屏显示 */
.full-screen-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: 1;
  padding: 0;
}
</style>