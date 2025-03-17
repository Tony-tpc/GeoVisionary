<script setup>
import { onMounted, watch} from "vue";

const props = defineProps({
  bvid: {
    type: String,
    default: '',
  },
  p: {
    type: Number,
    default: 1,
  },
  videos: {
    type: Array,
    default: () => [{'bvid':"BV1RN4y1f7Hn","p":1}],
  },
  currentPage: {
    type: Number,
    default: 1,
  }
})

function formatTimestamp(timestamp) {
  const date = new Date(timestamp * 1000); // 转换为毫秒
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0"); // 月份从 0 开始
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const seconds = String(date.getSeconds()).padStart(2, "0");

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

async function getBilibiliVideoInfo(bvid = "BV1RN4y1f7Hn", p = 1, index) {
  const apiUrl = `http://localhost:8040/proxy/bilibili/?bvid=${bvid}&p=${p}`;
  try {
    const response = await fetch(apiUrl);
    const data = await response.json();
    if (data.code !== 0) {
      console.error("Bilibili API 返回错误", data);
      return;
    }

    const video = data.data;

    // 解析所需信息
    const videoInfo = {
      title: video.pages[p-1].part, // 标题加上 P 信息
      cover: video.pages[p-1].first_frame, // 视频封面
      duration: formatDuration(video.pages[p-1].duration), // 时长格式化
      author: video.owner.name,
      authorAvatar: video.owner.face,
      authorUrl: `https://space.bilibili.com/${video.owner.mid}`,
      videoUrl: `https://www.bilibili.com/video/${bvid}?p=${p}`, // 分 P 视频链接
      publishTime: formatTimestamp(video.pubdate) // 添加格式化后的发布时间
    };

    // 渲染到页面
    displayVideoPreview(videoInfo,index);
  } catch (error) {
    console.error("获取 Bilibili 视频信息失败", error);
  }
}

// 格式化视频时长（秒 -> mm:ss）
function formatDuration(seconds) {
  const min = Math.floor(seconds / 60);
  const sec = seconds % 60;
  return `${min}:${sec.toString().padStart(2, "0")}`;
}

// 将视频信息渲染到 HTML
function displayVideoPreview(info,index) {
  const container = document.getElementById(`bilibili-preview${index}`);
  container.innerHTML = `
    <a href="${info.videoUrl}" target="_blank" style="text-decoration: none; color: inherit;">
        <div style="display: flex; align-items: center; gap: 5px; border: 1px solid #ddd; padding: 5px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
            <img src="http://localhost:8040/proxy/proxy-image?url=${info.cover}" alt="视频封面" width="140" height="90" style="border-radius: 6px;">
            <div style="flex: 1;">
                <h3 style="margin: 2px 0; font-size: 14px;">${info.title}</h3>
                <p style="margin: 2px 0; font-size: 12px;">时长: ${info.duration}</p>
                <p style="margin: 2px 0; font-size: 12px;">发布时间: ${info.publishTime}</p>
                <div style="display: flex; align-items: center; gap: 5px;">
                    <img src="http://localhost:8040/proxy/proxy-image?url=${info.authorAvatar}" alt="作者头像" width="24" height="24" style="border-radius: 50%;">
                    <a href="${info.authorUrl}" target="_blank" class="a-link" style="color: #33aaeb; text-decoration: none; font-weight: bold; font-size: 12px;">
                        ${info.author}
                    </a>
                </div>
            </div>
        </div>
    </a>
`;
}

onMounted(() => {
  if (props.bvid) {
    getBilibiliVideoInfo(props.bvid, props.p, 1);
  } else {
    props.videos.forEach((video, index) => {
      console.log(video)
      getBilibiliVideoInfo(video.bvid, video.p, index);
    })
  }
})

watch(() => props.currentPage, () => {
  props.videos.forEach((video, index) => {
    getBilibiliVideoInfo(video.bvid, video.p, index);
  })
})

</script>

<template>
  <div class="bilibili-container">
    <div v-if="props.bvid" class="video" id="bilibili-preview1"></div>
    <div v-else v-for="(video,index) in props.videos" :id="`bilibili-preview${index}`" class="video"></div>
  </div>
</template>

<style scoped>
/* 父级容器，每4个视频换行 */
.bilibili-container {
  position: relative;
  width: 100%;
  height: 100%;
  margin: 0 10px;
  display: flex;
  flex-wrap: wrap;
}

/* 视频配置，每个元素（包括间距）占据1/4的宽度 */
.video {
  width: calc(25% - 15px); /* 25% 减去 gap */
  height: auto; /* 自动高度适应内容 */
  margin: 5px 7px; /* 控制上下间距 */
  box-sizing: border-box;
  display: flex;
  flex-direction: column; /* 确保内容纵向排列 */
  align-items: stretch;
}

p {
  margin: 2px 0; /* 减小默认间距 */
}
</style>