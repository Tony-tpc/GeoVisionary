<script setup>
import { ref, onMounted, computed } from "vue";
import { userState } from "@/store/userStore.js";

// 收藏数据
const baikeList = ref([]);
const videoList = ref([]);
const nullNotice = ref(false);

// 分页数据
const pageSize = 3; // 每页显示条数

// 图文分页
const currentBaikePage = ref(1);
const paginatedBaikeList = computed(() => {
  const start = (currentBaikePage.value - 1) * pageSize
  return baikeList.value.slice(start, start + pageSize)
});

// 视频分页
const currentVideoPage = ref(1);
const paginatedVideoList = computed(() => {
  const start = (currentVideoPage.value - 1) * pageSize
  return videoList.value.slice(start, start + pageSize)
});

// 总页数
const baikeTotalPages = computed(() => Math.ceil(baikeList.value.length / pageSize));
const videoTotalPages = computed(() => Math.ceil(videoList.value.length / pageSize));

// 请求函数封装
const domain = "http://localhost:8040";
const backendAPI = domain + "/proxy/proxy-image/"; // 后端图片代理接口

// 格式化时间戳
const formatTimestamp = (timestamp) => {
  const date = new Date(timestamp * 1000);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}
          ${String(date.getHours()).padStart(2, "0")}:${String(date.getMinutes()).padStart(2, "0")}`;
};

// 格式化视频长度
const formatDuration = (seconds) => {
  const min = Math.floor(seconds / 60);
  const sec = seconds % 60;
  return `${min}:${sec.toString().padStart(2, "0")}`;
};

// 获取 B 站视频信息，并写入列表
const getBilibiliVideoInfo = async (bvid, p) => {
  const apiUrl = `${domain}/proxy/bilibili/?bvid=${bvid}&p=${p}`;
  try {
    const response = await fetch(apiUrl);
    const data = await response.json();
    if (data.code !== 0) return;

    const video = data.data;
    videoList.value.push({
      title: video.pages[p - 1].part,
      cover: video.pages[p - 1].first_frame,
      duration: formatDuration(video.pages[p - 1].duration),
      author: video.owner.name,
      authorAvatar: video.owner.face,
      authorUrl: `https://space.bilibili.com/${video.owner.mid}`,
      videoUrl: `https://www.bilibili.com/video/${bvid}?p=${p}`,
      publishTime: formatTimestamp(video.pubdate),
    });
  } catch (err) {
    console.error("获取 Bilibili 视频信息失败", err);
  }
};

// 获取百科信息
const getBaikeInfo = async (keyword, attempt = 1,maxAttempts = 5) => {
  const requestUrl = `${domain}/proxy/baidu-baike/?keyword=${keyword}`;

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

// 主请求函数
const favoriteRequest = async () => {
  const url = domain + "/api/get-favorites/";
  const response = await fetch(url, {
    method: "POST",
    body: JSON.stringify({
      user: userState.user,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });

  const data = await response.json();
  if (data === "用户没有收藏任何内容！") {
    nullNotice.value = true;
    return;
  }
  const baikeFavorites = [];
  const bilibiliFavorites = [];

  // 图文视频分别处理
  for (const item of data) {
    const itemList = item.toString().split('-')
    const contentType = itemList[0].trim();
    if (contentType === "图文") {
      // 由于原先内容含有较多空格以及一些额外说明，故作此调整
      let keyword = itemList[1].trim().split(' ')[0]
      baikeFavorites.push(keyword);
    } else if (contentType === "视频") {
      let bvid = itemList[1].trim();
      let p = itemList[2].split(" ")[0];
      bilibiliFavorites.push({bvid: bvid, p: p});
    }
  }

  // 遍历关键词和（bvid，p）列表，获取信息
  for (const keyword of baikeFavorites) {
    await getBaikeInfo(keyword);
  }

  for (const item of bilibiliFavorites) {
    const { bvid, p } = item;
    await getBilibiliVideoInfo(bvid, p);
  }
};

onMounted(() => {
  favoriteRequest();
});
</script>

<template>
  <div class="parent-container">
    <div v-if="nullNotice" class="no-favorite-notice">
      <img src="/empty-box.svg" alt="empty" class="empty-icon" />
      <p>您还没有收藏任何内容</p>
      <a href="/navigator/smart-recs" class="go-explore-btn">去探索精彩内容</a>
    </div>

    <section v-if="baikeList.length">
      <h2>图文收藏</h2>
      <div class="baike-grid">
        <div class="baike-card" v-for="item in paginatedBaikeList" :key="item.keyword">
          <img :src="backendAPI + `?url=${item.imageUrl}`" alt="baike" class="baike-image" />
          <div class="baike-content">
            <a :href="item.targetUrl" target="_blank" class="card-link"><h3>{{ item.keyword }}</h3></a>
            <p>{{ item.description }}</p>
          </div>
        </div>
      </div>
      <div class="pagination">
        <button @click="currentBaikePage--" :disabled="currentBaikePage === 1">上一页</button>
        <span>{{ currentBaikePage }} / {{ baikeTotalPages }}</span>
        <button @click="currentBaikePage++" :disabled="currentBaikePage === baikeTotalPages">下一页</button>
      </div>
    </section>

    <section v-if="videoList.length">
      <h2>视频收藏</h2>
      <div class="video-grid">
        <div class="video-card" v-for="video in paginatedVideoList" :key="video.videoUrl">
          <a :href="video.videoUrl" target="_blank" class="card-link">
            <img :src="backendAPI + `?url=${video.cover}`" alt="cover" class="video-cover" />
          </a>
          <div class="video-info">
            <a :href="video.videoUrl" target="_blank" class="card-link"><h3>{{ video.title }}</h3></a>
            <p>作者：<a :href="video.authorUrl" target="_blank" class="card-link">{{ video.author }}</a></p>
            <p>时长：{{ video.duration }}</p>
            <p>发布时间：{{ video.publishTime }}</p>
          </div>
        </div>
      </div>
      <div class="pagination">
        <button @click="currentVideoPage--" :disabled="currentVideoPage === 1">上一页</button>
        <span>{{ currentVideoPage }} / {{ videoTotalPages }}</span>
        <button @click="currentVideoPage++" :disabled="currentVideoPage === videoTotalPages">下一页</button>
      </div>
    </section>
  </div>
</template>

<style scoped>
.parent-container {
  padding: 20px;
}

.no-favorite-notice {
  text-align: center;
  margin-top: 4rem;
  color: #666;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.empty-icon {
  width: 120px;
  margin-bottom: 1rem;
  opacity: 0.6;
}

.go-explore-btn {
  margin-top: 1rem;
  padding: 8px 16px;
  background-color: #4caf50;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  transition: background-color 0.3s;
}

.go-explore-btn:hover {
  background-color: #388e3c;
}

h2 {
  margin-top: 2rem;
  color: #333;
  border-bottom: 2px solid #ddd;
  padding-bottom: 5px;
}

.card-link {
  text-decoration: none;
  color: #0088FE;
  display: block;
  transition: transform 0.2s;
}

.card-link:hover {
  transform: translateY(-4px);
}

.baike-grid, .video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.baike-card, .video-card {
  border: 1px solid #eee;
  border-radius: 10px;
  overflow: hidden;
  background: #fff;
  transition: box-shadow 0.3s;
}

.baike-card:hover, .video-card:hover {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.baike-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.baike-content {
  padding: 10px;
}

.video-cover {
  width: 100%;
  height: 160px;
  object-fit: cover;
}

.video-info {
  padding: 10px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 1rem;
}

.pagination button {
  padding: 6px 12px;
  border: none;
  background-color: #1976d2;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.pagination button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

.pagination span {
  font-weight: bold;
  color: #333;
}
</style>