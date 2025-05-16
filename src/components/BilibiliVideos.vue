<script setup>
import {onMounted, ref, watch, reactive, markRaw, onUnmounted} from "vue";
import HeartEmpty from "@/components/icons/HeartEmpty.vue"
import HeartFilled from "@/components/icons/HeartFilled.vue";
import {loadRatings, logActivity, logRatings} from "@/store/usefulFunction.js";
import {debounce} from "lodash";

const heartEmptyIcon = markRaw(HeartEmpty);
const heartFilledIcon = markRaw(HeartFilled);
const loading = ref(true);

const props = defineProps({
  bvid: { type: String, default: "" },
  p: { type: Number, default: 1 },
  videos: { type: Array, default: () => [{ bvid: "BV1RN4y1f7Hn", p: 1 }] },
  currentPage: { type: Number, default: 1 },
});

const videoInfos = ref([]);
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


const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp * 1000);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}
          ${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
};

const formatDuration = (seconds) => {
  const min = Math.floor(seconds / 60);
  const sec = seconds % 60;
  return `${min}:${sec.toString().padStart(2, "0")}`;
};

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const getBilibiliVideoInfo = async (bvid, p, maxRetries = 3, retryDelay = 1000) => {
  const apiUrl = `http://localhost:8040/proxy/bilibili/?bvid=${bvid}&p=${p}`;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(apiUrl);

      if (!response.ok) {
        throw new Error(`HTTP 错误状态码：${response.status}`);
      }

      const data = await response.json();
      if (data.code !== 0) {
        throw new Error(`Bilibili API 返回错误：${JSON.stringify(data)}`);
      }

      const video = data.data;
      return {
        title: video.pages[p - 1].part,
        cover: video.pages[p - 1].first_frame,
        duration: formatDuration(video.pages[p - 1].duration),
        author: video.owner.name,
        authorAvatar: video.owner.face,
        authorUrl: `https://space.bilibili.com/${video.owner.mid}`,
        videoUrl: `https://www.bilibili.com/video/${bvid}?p=${p}`,
        publishTime: formatTimestamp(video.pubdate),
        contentKey: bvid + '-' + p,
      };
    } catch (error) {
      console.warn(`第 ${attempt} 次请求失败：${error.message}`);
      if (attempt < maxRetries) {
        await sleep(retryDelay); // 等待后重试
      } else {
        console.error("获取 Bilibili 视频信息失败，已达到最大重试次数", error);
        return null;
      }
    }
  }
};


const fetchVideos = async () => {
  loading.value = true;
  const promises = props.bvid
      ? [getBilibiliVideoInfo(props.bvid, props.p)]
      : props.videos.map((video) => getBilibiliVideoInfo(video.bvid, video.p));

  videoInfos.value = (await Promise.all(promises)).filter(Boolean);
  loading.value = false;
};
const debouncedFetchVideos = debounce(fetchVideos, 300);

onMounted(() => {
  fetchVideos();
  loadRatings("video", "rating").then(result => {
    result.forEach((item) => {
      const [[key, value]] = Object.entries(item);
      ratings[key] = value;
    })
  });
  loadRatings("video", "favorite").then(result => {
    result.forEach((item) => {
      favorites[item] = 1;
    })
  });
});
onUnmounted(() => {
  logRatings("video","rating",ratings);
  logRatings("video","favorite",favorites);
})
watch(() => props.currentPage, debouncedFetchVideos);
</script>

<template>
  <div class="bilibili-container">
    <template v-if="loading">
      <div v-for="i in 12" :key="i" class="video">
        <div class="video-link">
          <div class="video-card">
            <el-skeleton :loading="true" animated>
              <template #template>
                <div style="display: flex; align-items: center;">
                  <el-skeleton-item variant="image" class="video-cover" />
                  <div style="margin-left: 10px; flex: 1;">
                    <el-skeleton-item variant="text" class="skeleton-title" />
                    <el-skeleton-item variant="text" class="skeleton-subtext" />
                    <el-skeleton-item variant="text" class="skeleton-subtext" />
                    <div class="video-author">
                      <el-skeleton-item variant="image" class="author-avatar" />
                      <el-skeleton-item variant="text" class="skeleton-subtext" />
                    </div>
                  </div>
                </div>
              </template>
            </el-skeleton>
          </div>
        </div>
        <div class="video-ratings">
          <el-skeleton-item variant="text" style="width: 40%; height: 32px; margin-left: 15px;" />
          <el-skeleton-item variant="text" style="width: 20px; height: 32px; margin-right: 15px;" />
        </div>
      </div>
    </template>


    <template v-else>
      <div v-for="(video, index) in videoInfos" :key="index" class="video">
        <a :href="video.videoUrl" target="_blank" class="video-link"
           @click="logActivity('click','video',video.contentKey)">
          <div class="video-card">
            <img :src="`http://localhost:8040/proxy/proxy-image/?url=${video.cover}&type=bilibili`" alt="视频封面" class="video-cover">
            <div class="video-info">
              <h3 class="video-title">{{ video.title }}</h3>
              <p class="video-duration">时长: {{ video.duration }}</p>
              <p class="video-time">发布时间: {{ video.publishTime }}</p>
              <div class="video-author">
                <img :src="`http://localhost:8040/proxy/proxy-image/?url=${video.authorAvatar}&type=biliAuthor`" alt="作者头像" class="author-avatar">
                <a :href="video.authorUrl" target="_blank" class="author-name">{{ video.author }}</a>
              </div>
            </div>
          </div>
        </a>
        <div class="video-ratings">
          <el-rate
              v-model="ratings[video.contentKey]"
              clearable
              @change="handleRateChange(video.contentKey, ratings[video.contentKey])"
              :colors="['#ff4d4f', '#f7ba2a', '#52c41a']"
              class="video-rating"
              :void-color="'#d5d5ff'"
          />
          <el-rate
              v-model="favorites[video.contentKey]"
              clearable
              @change="handleFavoriteChange(video.contentKey, favorites[video.contentKey])"
              :colors="['#ff4d4f','#ff4d4f','#ff4d4f']"
              :max="1"
              class="video-favorite"
              :void-icon="heartEmptyIcon"
              :icons="[heartFilledIcon,heartFilledIcon,heartFilledIcon]"
          />
        </div>
      </div>
    </template>
  </div>
</template>
<style scoped>
.bilibili-container {
  position: relative;
  width: 100%;
  min-height: 100%;
  margin: 0 10px;
  display: flex;
  flex-wrap: wrap;
}

.video {
  width: calc(25% - 15px);
  height: auto;
  margin: 8px 7px;
  box-sizing: border-box;
}

.video-link {
  text-decoration: none;
  color: inherit;
}

.video-card {
  display: flex;
  align-items: center;
  gap: 5px;
  border: 1px solid #ddd;
  padding: 5px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.video-cover {
  width: 140px;
  height: 90px;
  border-radius: 6px;
}

.video-info {
  flex: 1;
}

.video-title {
  margin: 2px 0;
  font-size: 14px;
  line-height: 1.4;
  font-weight: bold;

  /* 为了让所有卡片统一高度 */
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 最多两行 */
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;

  /* 防止英文长词不换行 */
  word-break: break-word;
  overflow-wrap: break-word;
  white-space: normal;

  min-height: 40px; /* 与line-height匹配，两行显示高度 */
}

.video-duration,
.video-time {
  margin: 2px 0;
  font-size: 12px;
}

.video-author {
  display: flex;
  align-items: center;
  gap: 5px;
}

.author-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
}

.author-name {
  color: #33aaeb;
  text-decoration: none;
  font-weight: bold;
  font-size: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-word;
  overflow-wrap: break-word;
  white-space: normal;
}

.video-ratings {
  position: relative;
  top: 3px;
  width: 100%;
  height: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255,255,255,.8);
  border-radius: 12px;
  transform: translateX(0);
}
.video-rating {
  margin-left: 15px;
}
.video-favorite {
  margin-right: 10px;
}

.skeleton-title {
  width: 80%;
  height: 34px;
  margin: 2px 0;
}

.skeleton-subtext {
  width: 60%;
  height: 14px;
}
</style>
