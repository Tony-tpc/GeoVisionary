<template>
<!--  导航栏开始-->
      <div class="navigator" id="navigator">
          <div style="padding-left: 80px">
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
              <div class="navigator-logo">
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
              <div class="menu-items">
                <el-sub-menu index="/"
                             :class="['regular', 'custom-sub-menu', { 'dark-theme': data.isDarkMode }]"
                             :style="{ marginLeft: data.margin + 'px' }"
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
                  <el-menu-item index="/navigator/galaxy"
                                :class="[{ 'active-item-3': data.activeIndex === '/navigator/galaxy' }]"
                  >
                    <span class="menu-fonts" :style="{ color: data.activeIndex === '/navigator/galaxy' ? '#fffdf3' : '#0d534b' }">星系</span>
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
                  <span :class="['menu-fonts',{ 'dark-theme': data.isDarkMode }]" :style="{ color: data.activeIndex === '/navigator/geo-graph' ? '#fffdf3' : 'var(--text-color)' }">万象图谱</span>
                </el-menu-item>
                <el-menu-item index="/navigator/insight-lab"
                              :class="['regular',{ 'dark-theme': data.isDarkMode },{ 'active-item-3': data.activeIndex === '/navigator/insight-lab' }]"
                >
                  <span :class="['menu-fonts',{ 'dark-theme': data.isDarkMode }]" :style="{ color: data.activeIndex === '/navigator/insight-lab' ? '#fffdf3' : 'var(--text-color)' }">探知问学</span>
                </el-menu-item>
                <el-menu-item index="/navigator/smart-recs"
                              :class="['regular',{ 'dark-theme': data.isDarkMode },{ 'active-item-4': data.activeIndex === '/navigator/smart-recs' }]"
                              :style="{ marginRight: data.margin + 'px' }"
                >
                  <span :class="['menu-fonts',{ 'dark-theme': data.isDarkMode }]" :style="{ color: data.activeIndex === '/navigator/smart-recs' ? '#fffdf3' : 'var(--text-color)' }">智荐学堂</span>
                </el-menu-item>
<!--                <el-button text style="align-items: center;height: 55px">-->
<!--                  <el-icon size="30px"><Search /></el-icon>-->
<!--                </el-button>-->
                <!--  已经登录  -->
                <div v-if="isLoggedIn" class="user">
                  <el-dropdown>
                    <span :class="['logged-in',{ 'dark-theme': data.isDarkMode }]">
                      <img v-if="userState.user.avatar" :src="userState.user.avatar" alt="头像">
                      <span v-else>{{ userState.user.username }}</span>
                    </span>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item><span class="menu-fonts" style="font-size: 16px">个人中心</span></el-dropdown-item>
                        <el-dropdown-item><span class="menu-fonts" style="font-size: 16px">设置</span></el-dropdown-item>
                        <el-dropdown-item @click="handleLogout"><span class="menu-fonts" style="font-size: 16px">退出</span></el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
                <!--  暂未登录  -->
                <div v-else class="user">
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
import { reactive, onMounted, provide, ref, watch, nextTick, onBeforeUnmount } from "vue";
import { User } from "@element-plus/icons-vue";
import router from "@/router/index.js";
import { useRoute } from "vue-router";
import { userState, isLoggedIn, clearUser, autoLogin } from "@/store/userStore";
import lightLogo from "@/assets/mountain-fffdf3.svg";
import darkLogo from "@/assets/mountain-0d534b.svg";
import { throttle } from "lodash";
import { gsap } from "gsap";

const data = reactive({
  activeIndex: router.currentRoute.value.path,    // 保持选中menu选项常量
  isDarkMode : false,                             // 切换主题
  logo: lightLogo,                                // 切换logo配色
  scrollY: 0,                                     // 主题切换判据
  margin: 346,                                    // 导航栏左右边距
});

// 获取当前路由
const route = useRoute();

// Home第三屏切换主题色
const TopChangeMode = ref(6200);
const isLoading = ref(false);
const showAnimation = ref(false);
provide('TopChangeMode',TopChangeMode);
provide('isLoading',isLoading);

// 防止频繁触发（延迟200ms）
let ticking = false;

// 更换主题
const updateTheme = throttle(() => {
  const noNeedForDarkTheme = data.activeIndex === '/navigator/landform' || data.activeIndex === '/navigator/moon-phase' || data.activeIndex === '/navigator/galaxy' || data.activeIndex === '/navigator/insight-lab';
  // 之后可根据需要改变主题切换逻辑
  if (data.activeIndex === '/navigator/geo-graph') {
    data.isDarkMode = true;
    data.logo = darkLogo;
  } else if ( noNeedForDarkTheme ) {
    data.isDarkMode = false;
    data.logo = lightLogo;
  } else {
    if (!ticking) {
      ticking = true;
      requestAnimationFrame(() => {
        data.scrollY = window.scrollY;
        data.isDarkMode = (data.scrollY > window.innerHeight - 50 && data.scrollY < (TopChangeMode.value - 50))
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

// 退出登录
const handleLogout = () => {
  clearUser();  // 清除用户信息
  router.push(data.activeIndex);  // 刷新页面
  window.location.reload();
};

// 配合加载动画
const loadAnimation = () => {
  const nav = document.querySelector('.navigator');

  // 强制触发 reflow，确保动画重新执行
  nav.style.opacity = '0';
  void nav.offsetHeight;
  if (isLoading.value) {
    gsap.timeline()
        .set('.navigator',{pointerEvents:'none'})
        .to('.navigator',{opacity:1,duration:1.5,delay:2.6})
        .set('.navigator',{pointerEvents: 'auto'})
  } else {
    gsap.timeline()
        .set('.navigator',{pointerEvents:'none'})
        .to('.navigator',{opacity:1,duration:1.5,delay:2})
        .set('.navigator',{pointerEvents: 'auto'})
  }
}

// 检测是否播放动画
const checkAnimationCondition = async (path) => {
  const scrollTop = localStorage.getItem('scrollPosition');
  const needLoading = path === '/navigator/smart-recs' || path === '/navigator/insight-lab' || path === '/navigator/geo-graph'
  const noNeedLoading = path === '/navigator/landform' || path === '/navigator/moon-phase' || path === '/navigator/galaxy' || path === '/navigator/world-map'
  console.log(`scrollTop = ${scrollTop}`);
  if (!noNeedLoading && (scrollTop === '0' || needLoading)) {
    showAnimation.value = true;
    loadAnimation()
    showAnimation.value = false;
  } else {
    showAnimation.value = false;
    document.querySelector('.navigator').style.opacity = 1;
  }
};

onMounted(() => {
  window.addEventListener('popstate', function(event) {
    console.log('历史记录更改:', event.state);
    data.activeIndex = event.state.current;
    if (event.state.scroll.top === 0) {
      showAnimation.value = true;
      checkAnimationCondition(data.activeIndex);
    } else {
      showAnimation.value = false;
    }
  });

  // 自动登录
  autoLogin();
  // 自动调节主题色
  updateTheme();
  window.addEventListener('scroll',updateTheme);
  // 获取左右间距
  const getMargin = () => {
    data.margin = (document.getElementById('navigator').offsetWidth - 135 * 4 - 25 * 4 - 151) / 2
  }
  getMargin();
  // 响应式调节导航栏
  window.addEventListener('resize',getMargin);
  checkAnimationCondition(router.currentRoute.value.path);
})

// 路由一发生变化就更新主题
watch(route,() => {
  updateTheme();
  nextTick(() => {
    checkAnimationCondition(router.currentRoute.value.path);
  })
});

onBeforeUnmount(() => {
  localStorage.removeItem("scrollPosition", window.scrollY);
});
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

/* 导航栏logo */
.navigator-logo {
  position: absolute;
  top: 5px;
  left: 0;
}

/* 菜单项 */
.regular {
  justify-content: center;
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
  display: flex;
  justify-content: center;
  align-items: center;
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
.menu-fonts,.el-dropdown-item {
  font-size: 18px;
  font-weight: bold;
  color: var(--text-color);
  text-align: center;
}

/* 用户 */
.user {
  position: absolute;
  right: 80px;
}

/* 注册/登录项，与菜单项风格作区分 */
.register,.logged-in {
  height: 42px;
  width: 135px;
  background-color: transparent;
  border-radius: 51px;
  border: 1px solid var(--primary-color);
  color: var(--bg-color);/* 此样式文字与背景主题互换 */
  font-size: 16px;
  font-weight: bold;
  outline: none;
}
.register:hover,.logged-in:hover {
  border-color: var(--bg-color) !important;
  color: var(--bg-color);
}

/* 登录改动(防止过长用户名) */
.logged-in {
  border: none;
  margin-top: 10px;
  height: 20px;
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