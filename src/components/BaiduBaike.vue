<script setup>
import {onMounted, ref, reactive, computed, nextTick, onUnmounted, markRaw} from "vue";
import {throttle} from "lodash";
import { logActivity, logRatings, loadRatings } from "@/store/usefulFunction.js";
import HeartEmpty from "@/components/icons/HeartEmpty.vue"
import HeartFilled from "@/components/icons/HeartFilled.vue";

const heartEmptyIcon = markRaw(HeartEmpty);
const heartFilledIcon = markRaw(HeartFilled);

const props = defineProps({
  keyword: {
    type: Array,
    default: () => ['地理']
  }
})

const emit = defineEmits(["update-bg"]); // 抛出事件
const keywordList = computed(() => props.keyword.length > 0 ? props.keyword : ['地理']); // 关键词列表
const baikeList = ref([]); // 百科响应数据列表
const backendAPI = "http://localhost:8040/proxy/proxy-image/"; // 后端图片代理接口
const divContainer = ref(null);

const ratings = reactive({}); // 评分对象
const favorites = reactive({}); // 收藏对象

const handleRateChange = (keyword, value) => {
  ratings[keyword] = value; // 记录评分
  console.log("评分数据:", ratings);
};

const handleFavoriteChange = (keyword, value) => {
  favorites[keyword] = value; // 记录收藏
  console.log(`收藏数据:`, favorites);
}

const getBaikeInfo = async (keyword, attempt = 1, maxAttempts = 5) => {
  const requestUrl = "http://localhost:8040/proxy/baidu-baike/?keyword=" + keyword;

  try {
    // 请求关键词并拿到数据
    const response = await fetch(requestUrl);

    if (response.ok) {
      const data = await response.json();
      // 解析数据
      baikeList.value.push({
        keyword: keyword,
        targetUrl: data.url,
        imageUrl: data.image,
        description: data.abstract,
        imageHeight: data.imageHeight,
        imageWidth: data.imageWidth,
      });
      console.log(`第 ${attempt} 次请求成功: ${keyword}`);
    } else {
      console.warn(`第 ${attempt} 次请求失败: ${response.status}`);
      if (attempt < maxAttempts) {
        console.log(`重试中...`);
        await getBaikeInfo(keyword, attempt + 1, maxAttempts);
      } else {
        console.error(`请求失败，已达到最大重试次数：${keyword}`);
      }
    }
  } catch (err) {
    console.error(`第 ${attempt} 次请求发生错误:`, err);
    if (attempt < maxAttempts) {
      console.log(`重试中...`);
      await getBaikeInfo(keyword, attempt + 1, maxAttempts);
    } else {
      console.error(`请求失败，已达到最大重试次数：${keyword}`);
    }
  }
};

// 抛出图片元素以更新背景
const handleMouseEnter = (event) => {
  const img = event.currentTarget.querySelector("img"); // 获取图片元素
  if (img) {
    emit("update-bg", img);
  }
};

// 清空背景
const handleMouseLeave = () => {
  emit("update-bg", null);
}

// 设置瀑布流布局
const setPositions = () => {
  const parentDivWidth = 320;
  const info = cal(parentDivWidth);
  const nextTops = new Array(info.columns); // 数组长度为列数，每一项表示该列的下一个容器的纵坐标
  nextTops.fill(0);

  for (let i = 0; i < divContainer.value.children.length; i++) {
    const item = divContainer.value.children[i];
    // 找到 nextTops 中的最小值作为当前图片的纵坐标
    const minTop = Math.min.apply(null, nextTops);
    item.style.top = (minTop + 0.11 * window.innerHeight) + "px";
    // 重新设置数组这一项的下一个 top 值
    const index = nextTops.indexOf(minTop); // 得到使用的是第几列的 top 值
    nextTops[index] += item.offsetHeight + info.space;
    // 横坐标
    const left = (index + 1) * info.space + index * item.offsetWidth;
    item.style.left = left + "px";
  }
  const max = Math.max.apply(null, nextTops);
  divContainer.value.style.height = (max + 0.11 * window.innerHeight) + "px"; // 设置容器的高度
}

// 计算一共多少列，以及每一列之间的间隙
const cal = (parentDivWidth = 320) => {
  const containerWidth = divContainer.value.clientWidth; // 容器宽度
  const columns = Math.floor(containerWidth / parentDivWidth); // 列数
  const spaceNumber = columns + 1; // 间隔数
  const leftSpace = containerWidth - columns * parentDivWidth; // 剩余空间
  const space = leftSpace / spaceNumber; // 每个间隙的空间
  return {
    space: space,
    columns: columns,
  }
}

// 确保图片加载完成再设置位置
const handleImageLoad = async () => {
  await nextTick();
  setPositions();
}

// 窗口更新尺寸时重置位置
const reset = throttle(setPositions, 200);

// 挂载以后，先获取百科列表
onMounted(() => {
  keywordList.value.forEach((keyword) => {
    getBaikeInfo(keyword);
  })
  loadRatings("text", "rating").then(result => {
    result.forEach((item) => {
      const [[key, value]] = Object.entries(item);
      ratings[key] = value;
    })
  });
  loadRatings("text", "favorite").then(result => {
    result.forEach((item) => {
      favorites[item] = 1;
    })
  });
  window.addEventListener("resize", reset);
});

onUnmounted(() => {
  window.removeEventListener("resize", reset);
  logRatings("text","rating",ratings);
  logRatings("text","favorite",favorites);
})
</script>

<template>
  <main class="baike-parent-container">
    <div class="baike-container" ref="divContainer">
      <div v-for="(baike, index) in baikeList"
           :key="index"
           class="baike-card"
           @mouseenter="handleMouseEnter"
           @mouseleave="handleMouseLeave">
        <el-link :underline="false"
                 :href="baike.targetUrl"
                 target="_blank"
                 @click="logActivity('click','text',baike.keyword)"
        >
          <div class="baike-content">
            <div class="image-wrapper">
              <img
                  :src="backendAPI + `?url=${baike.imageUrl}&type=baidu`"
                  :alt="`${baike.keyword}百科`"
                  crossorigin="anonymous"
                  loading="lazy"
                  @load="handleImageLoad"
              />
            </div>
            <div class="text-content">
              <div class="baike-title">{{ baike.keyword }}</div>
              <div class="baike-description">{{ baike.description }}</div>
            </div>
          </div>
        </el-link>
        <!-- 评分组件 -->
        <div class="baike-ratings">
          <el-rate
              v-model="ratings[baike.keyword]"
              clearable
              @change="handleRateChange(baike.keyword, ratings[baike.keyword])"
              :colors="['#ff4d4f', '#f7ba2a', '#52c41a']"
              class="baike-rating"
              :void-color="'#d5d5ff'"
          />
          <el-rate
              v-model="favorites[baike.keyword]"
              clearable
              @change="handleFavoriteChange(baike.keyword, favorites[baike.keyword])"
              :colors="['#ff4d4f','#ff4d4f','#ff4d4f']"
              :max="1"
              class="baike-favorite"
              :void-icon="heartEmptyIcon"
              :icons="[heartFilledIcon,heartFilledIcon,heartFilledIcon]"
          />
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
/* 父容器 */
.baike-parent-container {
  width: 100%;
  min-height: 100%;
  padding: 20px;
  background-color: transparent;
}

/* 弹性百科容器 */
.baike-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

/* 百科卡片 */
.baike-card {
  position: absolute;
  width: 320px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
/* 悬停效果 */
.baike-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
}

/* 正文部分 */
.baike-content {
  display: flex;
  flex-direction: column;
}

/* 图片包装 */
.image-wrapper {
  width: 100%;
  height: 180px;
  overflow: hidden;
  background-color: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-wrapper img {
  max-width: 100%;
  max-height: 100%;
  object-fit: cover;
}

.text-content {
  padding: 15px;
}

/* 标题 */
.baike-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

/* 详细描述 */
.baike-description {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

/* 独立评分组件 */
.baike-ratings {
  position: absolute;
  width: 100%;
  height: auto;
  bottom: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255,255,255,.8);
  border-radius: 12px;
  transform: translateX(0);
}
.baike-rating {
  margin-left: 15px;
}
.baike-favorite {
  margin-right: 10px;
}
</style>