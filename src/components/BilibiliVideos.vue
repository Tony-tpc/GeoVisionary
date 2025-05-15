<script setup>
import {onMounted, ref, watch, reactive, markRaw, onUnmounted} from "vue";
import HeartEmpty from "@/components/icons/HeartEmpty.vue"
import HeartFilled from "@/components/icons/HeartFilled.vue";
import {loadRatings, logActivity, logRatings} from "@/store/usefulFunction.js";

const heartEmptyIcon = markRaw(HeartEmpty);
const heartFilledIcon = markRaw(HeartFilled);

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

const getBilibiliVideoInfo = async (bvid, p) => {
  const apiUrl = `http://localhost:8040/proxy/bilibili/?bvid=${bvid}&p=${p}`;
  try {
    const response = await fetch(apiUrl);
    const data = await response.json();
    if (data.code !== 0) return console.error("Bilibili API 错误", data);

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
    console.error("获取 Bilibili 视频信息失败", error);
  }
};

const fetchVideos = async () => {
  const promises = props.bvid
      ? [getBilibiliVideoInfo(props.bvid, props.p)]
      : props.videos.map((video) => getBilibiliVideoInfo(video.bvid, video.p));

  videoInfos.value = (await Promise.all(promises)).filter(Boolean);
};

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
watch(() => props.currentPage, fetchVideos);
</script>

<template>
  <div class="bilibili-container">
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
  margin: 5px 7px;
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
</style>
