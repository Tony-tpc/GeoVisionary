import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path:'/', redirect:'/navigator/home' },
    { path:'/manager', component: () => import('../views/test/Manager.vue'),children:[
        { path: 'home', name: 'home1', meta:{ title:'主页' }, component: () => import('../views/test/Home.vue'), },
        { path: 'test', name: 'test', meta:{ title:'测试数据页面' }, component: () => import('../views/test/Test.vue'), },
        { path: 'data', name: 'data', meta:{ title:'数据展示页面' }, component: () => import('../views/test/Data.vue'), },
    ]},
    { path: '/navigator', name: 'navigator',meta:{ title:'智绘山河' }, component: () => import('../components/Navigator.vue'),children:[
        { path: 'home', name: 'home', meta:{ title:'智绘山河' }, component: () => import('../components/Home.vue'), },
        { path: 'landform', name: 'landform', meta:{ title:'地形 | 智绘山河' }, component: () => import('../views/Landform.vue'), },
        { path: 'moon-phase', name: 'moonPhase', meta:{ title:'月相 | 智绘山河' }, component: () => import('../views/MoonPhase.vue'), },
        { path: 'climate', name: 'climate', meta:{ title:'气候 | 智绘山河' }, component: () => import('../views/Climate.vue'), },
        { path: 'world-map', name: 'worldMap', meta:{ title:'地图 | 智绘山河' }, component: () => import('../views/WorldMap.vue'), },
        { path: 'geo-graph', name: 'geo-graph', meta:{ title:'知象图谱 | 智绘山河' }, component: () => import('../components/GeoGraph.vue'), },
        { path: 'insight-lab', name: 'insight-lab', meta:{ title:'探知问学 | 智绘山河' }, component: () => import('../components/InsightLab.vue'), },
        { path: 'smart-recs', name: 'smart-recs', meta:{ title:'智荐学堂 | 智绘山河' }, component: () => import('../components/SmartRecs.vue'), },
    ]},
    { path: '/quizzes', name: 'quizzes', meta:{ title:'测试 | 智绘山河' }, component: () => import('../views/Quizzes.vue'), },
    { path: '/register-login', name: 'register-login', meta:{ title:'登录 | 智绘山河' }, component: () => import('../views/Register-Login.vue'), },
    { path: '/loading', name: 'loading-test', meta:{ title:'加载 | 智绘山河' }, component: () => import('../views/test/Loading.vue'), },
    { path: '/test', name: 'test', meta:{ title:'各种测试' }, component: () => import('../views/TestEarth1.vue'), },
    { path: '/404', name: '404',meta:{ title:'该页面不存在' }, component: () => import('../views/404.vue'),},
    { path:'/:pathMatch(.*)', redirect:'/404' }
  ],
    scrollBehavior(to,from,savedPosition) {
        if (savedPosition) {
            return savedPosition; // 返回上次保存的位置
        } else {
            return { top: 0 }; // 每次路由切换时滚动到顶部
        }
    },
})

// beforeEach表示跳转之前的一些操作
router.beforeEach((to,from,next) => {
    document.title = to.meta.title;
    next()  // 必须调用这个函数实现跳转
})

export default router
