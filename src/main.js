import { createApp,defineAsyncComponent } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import '@icon-park/vue-next/styles/index.css'
import '@/assets/global.css'
import { userState } from "./store/userStore";  // 引入 userStore

const app = createApp(App)

app.use(router)
app.use(ElementPlus,{
    locale:zhCn,
})
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
// 全局检查 localStorage，保持用户登录状态
if (localStorage.getItem("user")) {
    userState.user = JSON.parse(localStorage.getItem("user"));
    userState.access_token = localStorage.getItem("access_token");
    userState.refresh_token = localStorage.getItem("refresh_token");
}

const ChatContent = defineAsyncComponent(() => {
    import('./components/ChatContent.vue')
})

app.component('ChatContent', ChatContent)
app.mount('#app')
