import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from "unplugin-vue-components/resolvers"
import ElementPlus from "unplugin-element-plus/vite"
import compression from 'vite-plugin-compression'
import fs from 'fs'

export default defineConfig(({ mode }) => {
  // 读取 .env.local 里的环境变量
  const env = loadEnv(mode, process.cwd(), '')
  const needTools = env.VITE_DEVTOOLS === 'true' // 确保值是布尔类型

  return {
    plugins: [
      vue(),
      needTools ? vueDevTools() : null, // 根据 needTools 确定是否启用 Vue DevTools
      ElementPlus({
        useSource: true,
      }),
      AutoImport({
        resolvers: [ElementPlusResolver({ importStyle: 'sass' })],
      }),
      Components({
        resolvers: [ElementPlusResolver({ importStyle: 'sass' })],
      }),
      compression({
        ext: '.gz', // 生成 .gz 文件
        algorithm: 'gzip',
        threshold: 10240, // 10KB 以上才压缩
      }),
    ].filter(Boolean), // 过滤掉 null 值，防止插件数组出错

    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },

    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `@use "@/assets/index.scss" as *;`,
        },
      },
    },

    server: {
      // https: {
      //   key: fs.readFileSync("certificates/localhost-key.pem"),
      //   cert: fs.readFileSync("certificates/localhost.pem")
      // },
      proxy: {
        '/qqmap': {
          target: 'https://apis.map.qq.com',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/qqmap/, ''),
        },
      },
    },
  }
})
