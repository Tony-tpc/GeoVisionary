<template>
  <section>
    <!--  加载背景  -->
    <Loading title=".section1-title" subtitle=".section1-subtitle"></Loading>
  </section>
  <section>
    <!--  固定对话内容  -->
    <div>
      <!--  Live2D -->
      <canvas ref="canvas" class="live2Dmodel"></canvas>
      <!--   输入和输出   -->
      <div class="LLM-input-output">
        <!-- 菜单 icon -->
        <el-tooltip
            popper-class="tooltips"
            effect="dark"
            :content="data.displayEverything ? '收起对话框':'展开对话框'"
            placement="right"
        >
          <div class="bookmark" @click="changeDisplay">
            <el-icon v-if="data.displayEverything"><Fold /></el-icon>
            <el-icon v-else><Expand /></el-icon>
          </div>
        </el-tooltip>
        <!-- 历史记录 icon -->
        <el-tooltip
            popper-class="tooltips"
            effect="dark"
            :content="data.displayHistory ? '关闭历史记录':'打开历史记录'"
            placement="right"
        >
          <div class="bookmark bookmark2" @click="getHistoryPreview">
            <el-icon><ChatLineSquare /></el-icon>
          </div>
        </el-tooltip>
        <el-tooltip
            popper-class="tooltips"
            effect="dark"
            :content="'新聊天'"
            placement="right"
        >
          <div class="bookmark bookmark3" @click="newConversation">
            <el-icon><Edit /></el-icon>
          </div>
        </el-tooltip>
        <el-alert title="请注意，输入不能为空" type="error" center show-icon class="warning-alert" :closable="false"/>
        <!--  背景  -->
        <div class="LLM-background"></div>
        <!--  蒙层  -->
        <div class="LLM-wrapper" @click="getHistoryPreview"></div>
        <!--  输入区域  -->
        <div style="position: relative;display: flex">
          <!-- 标签 -->
          <div class="tag-container" id="tag-container">
            <InputBox v-for="item in inputBoxes"
                      :key="item.input"
                      :input="item.input"
                      :bottom="0"
                      style="position: relative;pointer-events: auto"
                      @inputBoxClosed="handleInputBoxClosed"
            />
          </div>
          <!-- 输入框 -->
          <div ref="input-container" style="position: fixed;z-index: 12;">
            <el-input
                v-model="data.textInput"
                :rows="2"
                type="textarea"
                resize="none"
                :autosize="{minRows: 1, maxRows: 4}"
                placeholder="在这里输入您想和小助教对话的内容！"
                class="inputArea"
                @keydown="handleKeydown"
                id="textInputArea"
            />
            <el-button v-if="!isGenerating" type="primary" @click="handleChatWithLLM" class="submit-btn" :disabled="data.isDisabled">
              <el-icon  ><Top /></el-icon>
            </el-button>
            <el-button v-else type="primary" @click="handleStopLLMGeneration" class="stop-btn">
              <el-icon  ><Close /></el-icon>
            </el-button>
          </div>
        </div>
        <!--  历史记录  -->
        <div class="historyDisplay">
          <h3>历史记录</h3>

          <template v-if="HistoryPreview.today?.length">
            <h4>今天</h4>
            <div v-for="item in HistoryPreview.today" :key="item.precursor_id" class="history-item"
                 @click="loadHistoryById(item.precursor_id)" :class="{ active: activeHistoryId === item.precursor_id }">
              {{ formatPreview(item.user_msg) }}
              <span class="timestamp">{{ formatTime(item.timestamp) }}</span>
            </div>
          </template>

          <template v-if="HistoryPreview.last7days?.length">
            <h4>近7天</h4>
            <div v-for="item in HistoryPreview.last7days" :key="item.precursor_id" class="history-item"
                 @click="loadHistoryById(item.precursor_id)" :class="{ active: activeHistoryId === item.precursor_id }">
              {{ formatPreview(item.user_msg) }}
              <span class="timestamp">{{ formatTime(item.timestamp) }}</span>
            </div>
          </template>

          <template v-if="HistoryPreview.last30days?.length">
            <h4>近30天</h4>
            <div v-for="item in HistoryPreview.last30days" :key="item.precursor_id" class="history-item"
                 @click="loadHistoryById(item.precursor_id)" :class="{ active: activeHistoryId === item.precursor_id }">
              {{ formatPreview(item.user_msg) }}
              <span class="timestamp">{{ formatTime(item.timestamp) }}</span>
            </div>
          </template>

          <template v-if="HistoryPreview.earlier?.length">
            <h4>更早</h4>
            <div v-for="item in HistoryPreview.earlier" :key="item.precursor_id" class="history-item"
                 @click="loadHistoryById(item.precursor_id)" :class="{ active: activeHistoryId === item.precursor_id }">
              {{ formatPreview(item.user_msg) }}
              <span class="timestamp">{{ formatTime(item.timestamp) }}</span>
            </div>
          </template>

          <!--  无历史记录提醒  -->
          <template v-if="!HistoryPreview.today?.length
             && !HistoryPreview.last7days?.length
             && !HistoryPreview.last30days?.length
             && !HistoryPreview.earlier?.length">
            <div class="no-history">
              <i class="no-history-icon">📭</i>
              <p class="no-history-text">暂无历史记录</p>
            </div>
          </template>
        </div>
        <!--  输出区域  -->
        <div class="outputArea" ref="outputAreaRef">
          <ChatMessages
              :messages="conversation"
              :user-config="{
                name: `${userState.user? userState.user.username : '用户'}`,
                bgColor: '#d3e0d1',
                textColor: '#0d0f1a'
              }"
              :llm-config="{
                name: 'AI助教',
                bgColor: '#f7f2eb',
                textColor: '#0d0f1a',
                errorColor: '#ff4444'
              }"
              :show-llm-cursor="isGenerating"
          />
        </div>
      </div>
      <div class="summary-output" ref="summaryRef">你好呀，我是小春。<br>单击左侧标签（或图谱节点）<br>即可与我对话哟！</div>
    </div>
  </section>
  <!--  首页背景图及标题 -->
  <section>
    <div class="container section1">
      <img src="../assets/geograph-images/GeoGraph(summary).png" alt="万象图谱" loading="lazy" class="image1">
      <img src="../assets/geograph-images/GeoGraph(tourism).png" alt="万象图谱" loading="lazy" class="image2">
      <img src="../assets/geograph-images/GeoGraph(disaster).png" alt="万象图谱" loading="lazy" class="image3">
    </div>
    <div class="section1-title">
      万象图谱
    </div>
    <div class="section1-subtitle">
      在这里，大自然的智慧以线条与节点的形式呈现，连接着山川、星辰及气候的宏伟交响。每一次探索都是心灵之旅，带你穿越知识的海洋，领略地理之美的无限可能。
    </div>
    <ScrollButton sectionName="#section2" style="z-index: 9"></ScrollButton>
  </section>
  <!--  图谱展示页  -->
  <section>
    <div class="container section2" id="section2">
      <div class="switch-words">便捷模式</div>
      <div class="switch-mode-container wrapper">
        <el-tooltip
            popper-class="tooltips"
            effect="dark"
            :content="isActive ? '禁用标签自动选择' : '启用标签自动选择'"
            placement="top"
        >
          <SunMoon v-model="isActive"
                   @click="isActive = !isActive"
                   ball="gradient"
                   halo="linear"
                   finish="delay"
          />
        </el-tooltip>
      </div>
      <div class="graph-changer">
        <GraphHeader   v-model="currentIndex"
                       :neo4jQuery="neo4jQuery"/>
      </div>
      <div id="graph-container" class="graph-container"></div>
    </div>
  </section>
</template>

<script setup>
import * as PIXI from 'pixi.js';
import { Live2DModel } from 'pixi-live2d-display/cubism4';
import {ref, onMounted, onUnmounted, reactive, nextTick, watch} from 'vue';
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { Draggable } from "gsap/Draggable";
import neo4j from 'neo4j-driver';
import { Network } from 'vis-network';
import {userState} from "@/store/userStore.js";
import {ChatLineSquare, Close, Edit, Expand, Fold, Top} from "@element-plus/icons-vue";
import InputBox from "@/components/InputBox.vue";
import ChatMessages from "@/components/ChatMessages.vue";
import ScrollButton from "@/components/ScrollButton.vue";
import SunMoon from "@/components/SunMoon.vue";
import Loading from "@/components/Loading.vue"
import GraphHeader from "@/components/GraphHeader.vue";
gsap.registerPlugin(ScrollTrigger,Draggable);

window.PIXI = PIXI;

const data = reactive({
  textInput:"", // 用户输入内容
  changeArea:false, // 输出框大小更改
  displayEverything:false, // 显示/隐藏输入/输出
  isDisabled:false, // 启用/禁用提交按钮，防止连续触发
  nodeInfo:[], // neo4j 节点
  displayHistory : false, // 显示/隐藏历史记录
})

// Live2D 模型
const canvas = ref(null); // live2D 载体
const app = ref(null); // live2D 应用
const model = ref(null); // live2D 模型

// LLM 对话
const showCursor = ref(false); // 控制光标
const isGenerating = ref(false); // 控制加载状态
const conversation = ref([  { sender: 'llm', content: '您好呀，我是您的专属AI助教，请问有什么可以帮到您？' },]); // 对话记录
const streamingMessageRef = ref(null); // 当前流式消息的引用
let controller = new AbortController();  // 用于控制请求
let reader = null;  // 读取流
const autoScroll = ref(true); // 输出自动滚动到底部
const outputAreaRef = ref(null); // 拖动/复原输出框
const isOldchat = ref(0); // 是否原有对话
const isApiAvailable = ref(localStorage.getItem('isApiavailable')); // 是否允许对话
const isFirstTime = ref(false);

// 便捷按钮
const inputBoxes = ref([]); // 标签盒
const isActive = ref(true); // 切换便捷模式

// Live2D 对话
const audioQueue = ref([]); // 音频缓存区
const summaryRef = ref(null); // 概要DOM
const thinkingContent = ref(''); // 思考内容
let isThinkingActive = false; // 标志变量，防止思考动画重复执行
let audioContext; // 音频上下文
let originUpdate; // 原本 live2D 更新函数
const modelConfig = {
  llm: "dsR1",
  TTS: "Silicon",
} // 模型配置

const WS_URL = 'ws://localhost:8040/ws/chat/'; // 后端 WebSocket 地址
const HistoryPreview = ref([]); // 历史记录列表
const inAnimation = ref(false); // 是否正在播放动画（如果是，禁止用户再次点击）
const activeHistoryId = ref(''); // 当前选中历史记录 ID
const neo4jQuery = {
  earthAndMap: `MATCH (root:\`专题\` {名称:"地球和地图"})
                MATCH path=(root)-[*0..]->(node)
                RETURN path`,
  earthInSpace: `MATCH (root:\`专题\` {名称:"宇宙中的地球"})
                 MATCH path=(root)-[*0..]->(node)
                 RETURN path`,
  energyExchange: `MATCH (root:\`专题\` {名称:"自然环境中的物质运动和能量交换"})
                   MATCH path=(root)-[*0..]->(node)
                   RETURN path`,
  sameAndDiff: `MATCH (root:\`专题\` {名称:"自然环境的整体性和差异性"})
                MATCH path=(root)-[*0..]->(node)
                RETURN path`,
  environmentImpact: `MATCH (root:\`专题\` {名称:"自然环境对人类活动的影响"})
                      MATCH path=(root)-[*0..]->(node)
                      RETURN path`,
  populationAndCity: `MATCH (root:\`专题\` {名称:"人口与城市"})
                      MATCH path=(root)-[*0..]->(node)
                      RETURN path`,
  productionAndLink: `MATCH (root:\`专题\` {名称:"生产活动与地域联系"})
                      MATCH path=(root)-[*0..]->(node)
                      RETURN path`,
  harmony: `MATCH (root:\`专题\` {名称:"人类与地理环境的协调发展"})
           MATCH path=(root)-[*0..]->(node)
           RETURN path`,
  regionAndActivity: `MATCH (root:\`专题\` {名称:"区域地理环境与人类活动"})
                      MATCH path=(root)-[*0..]->(node)
                      RETURN path`,
  sustainable: `MATCH (root:\`专题\` {名称:"区域可持续发展"})
                MATCH path=(root)-[*0..]->(node)
                RETURN path`,
  geoTech: `MATCH (root:\`专题\` {名称:"地理信息技术的应用"})
           MATCH path=(root)-[*0..]->(node)
           RETURN path`,
  worldGeo: `MATCH (root:\`专题\` {名称:"世界地理"})
            MATCH path=(root)-[*0..]->(node)
            RETURN path`,
  chinaGeo: `MATCH (root:\`专题\` {名称:"中国地理"})
            MATCH path=(root)-[*0..]->(node)
            RETURN path`,
  tourism: `MATCH (root:\`专题\` {名称:"旅游地理"})
           MATCH path=(root)-[*0..]->(node)
           RETURN path`,
  disaster: `MATCH (root:\`专题\` {名称:"自然灾害与防治"})
            MATCH path=(root)-[*0..]->(node)
            RETURN path`,
  environmentProtect: `MATCH (root:\`专题\` {名称:"环境保护"})
                       MATCH path=(root)-[*0..]->(node)
                       RETURN path`,
} // 图谱请求配置
const currentIndex = ref(0); // 当前图谱下标
const nonsenseType = ['一','二','三','四','五','六','one','two','three','four'] // 无意义的边类型

// Live2D 加载逻辑
const loadLive2D = async () => {
  try {
    // 如果存在 PIXI 实例，便销毁
    if (app.value) {
      console.log("销毁旧的 PIXI 应用");
      app.value.destroy(true); // 彻底销毁 PIXI
      app.value = null;
      model.value = null;
    }

    // 初始化 PIXI 应用
    app.value = new PIXI.Application({
      view: canvas.value,
      autoStart: true,
      x: 0,
      y: 0,
      backgroundAlpha: 0,
      autoDensity: true,
      antialias: true,
      resolution: window.devicePixelRatio,
    });

    // 加载 Live2D 模型
    const live2DModelUrls = {
      haruCDN: "https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/test/assets/haru/haru_greeter_t03.model3.json",
      haru: "/haru/haru_greeter_t03.model3.json",
      maolili: "/maolili/mailili.model3.json",
      ariu: "/ariu/ariu.model3.json",
      IceGirl: "/IceGIrl Live2D/IceGirl.model3.json",
    }

    model.value = await Live2DModel.from(live2DModelUrls.haru);
    app.value.stage.addChild(model.value);

    // 调整模型大小
    model.value.scale.set(0.2);
    model.value.x = -80;

    originUpdate = model.value.internalModel.motionManager.update;
    console.log("Live2D 模型加载成功");
  } catch (error) {
    console.error("加载失败", error);
  }
}

// 更新 Live2D 位置
const updatePosition = () => {
  model.value.x = -0.05 * window.innerWidth;
};

// 历史记录
const chatHistory = ref([]);

// 模拟流式输出效果
const typeEffect = async () => {
  summaryRef.value.innerHTML = '';

  for (let i = 0; i < thinkingContent.value.length; i++) {
    summaryRef.value.innerHTML += thinkingContent.value[i];
    await new Promise(resolve => setTimeout(resolve, 250)); // 等待 250ms 再继续
  }
}

// 根据音频调整 Live2D 口型
const speaking = (audio) => {
  if (!audioContext) {
    audioContext = new AudioContext();
  }

  const analyser = audioContext.createAnalyser();
  analyser.fftSize = 512;  // 提升分析精度
  analyser.smoothingTimeConstant = 0.3;

  // 连接 Audio 标签的音频流到 analyser
  const source = audioContext.createMediaElementSource(audio);
  source.connect(analyser);
  analyser.connect(audioContext.destination); // 保证音频能正常播放

  const updateMouth = () => {
    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    analyser.getByteFrequencyData(dataArray);

    const volume = dataArray.reduce((a, b) => a + b) / dataArray.length;
    const mouthOpen = Math.min(1, volume / 50); // 根据实际情况调整分母

    if (model?.value) {
      model.value.internalModel.motionManager.expressionManager = null;
      model.value.internalModel.motionManager.update = () => {}; // 强行打开嘴型
      model.value.internalModel.coreModel.setParameterValueById('ParamMouthOpenY', mouthOpen); // 设置口型参数
    }

    if (!audio.paused && !audio.ended) {
      requestAnimationFrame(updateMouth);
    } else {
      model.value.internalModel.motionManager.update = originUpdate;
    }
  };

  updateMouth();
};

// 播放音频队列
const playAudioQueue = () => {
  if (audioQueue.value.length === 0) return;

  if (!audioContext) {
    audioContext = new AudioContext();
  }

  const audioUrl = audioQueue.value.shift(); // 取出队列中的音频
  const audio = new Audio(audioUrl);

  audio.addEventListener('play', () => {
    console.log("开始播放音频");
    speaking(audio); // 绑定口型同步
  });

  audio.addEventListener('ended', () => {
    console.log("音频播放结束");
    if (model?.value) {
      model.value.internalModel.coreModel.setParameterValueById('ParamMouthOpenY', 0); // 关闭嘴巴
      model.value.internalModel.motionManager.startMotion("Idle", Math.floor(Math.random() * 3));
    }
    if (audioQueue.value.length > 0) {
      playAudioQueue(); // 继续播放下一个音频
    }
  });

  audio.play();
};

const playPromptAudio = (prompt) => {
  const audioUrls = {
    'cancel': new URL('@/assets/audios/prompt_audio_cancel.wav', import.meta.url).href,
    'error': new URL('@/assets/audios/prompt_audio_error.wav', import.meta.url).href,
    'greeting': new URL('@/assets/audios/prompt_audio_greeting.wav', import.meta.url).href,
    'thinking': new URL('@/assets/audios/prompt_audio_thinking.wav', import.meta.url).href,
  };
  if (!audioUrls[prompt]) return;

  const audio = new Audio(audioUrls[prompt]);

  audio.addEventListener('ended', () => {
    if (model?.value) {
      model.value.internalModel.coreModel.setParameterValueById('ParamMouthOpenY', 0); // 关闭嘴巴
      model.value.internalModel.motionManager.startMotion("Idle", 0); // 恢复 Idle
    }
  });

  audio.play();
  speaking(audio); // 确保 Live2D 口型同步
}

// 解析 base64 为 URL
const base64ToAudioUrl = (base64) => {
  const byteString = atob(base64);
  const uint8Array = new Uint8Array(byteString.length);
  for (let i = 0; i < byteString.length; i++) {
    uint8Array[i] = byteString.charCodeAt(i);
  }
  const audioBlob = new Blob([uint8Array], { type: 'audio/wav' });
  return URL.createObjectURL(audioBlob);
}

// 等待思考动画
const waitForThinking = async () => {
  let i = 0;
  const timeout = 500;
  isThinkingActive = true;  // 标记动画开始
  playPromptAudio('thinking');

  while(!thinkingContent.value && isThinkingActive) {
    if (i % 4 === 0) {
      summaryRef.value.innerHTML = '思考中';
    } else {
      summaryRef.value.innerHTML += '.';
    }
    await new Promise(resolve => setTimeout(resolve, timeout));
    i++;
  }
}

// 向LLM发送流式请求
const chatWithLLM = () => {
  isGenerating.value = true; // 进入生成状态
  showCursor.value = true; // 显示光标

  // 创建 WebSocket 连接
  const ws = new WebSocket('ws://localhost:8040/ws/tts/');
  thinkingContent.value = '';
  waitForThinking();

  let doneReceived = false; // 用于标记是否收到 [DONE]

  if(data.textInput || inputBoxes.value) {
    let userContent = data.textInput;
    if (inputBoxes.value.length >= 1) {
      userContent += '（我想要了解关于:'
      for (let i = 0; i < inputBoxes.value.length - 1; i++) {
        userContent += `${inputBoxes.value[i].input}、`;
      }
      userContent += `${inputBoxes.value[inputBoxes.value.length - 1].input}的内容）`;
    }

    // 把用户输入添加到历史记录
    const userMessage = { role: "user", content: userContent };
    chatHistory.value.push(userMessage);
    conversation.value.push({
      sender: 'user',
      content: userContent
    });

    // 创建流式消息占位符
    const streamMessage = {
      sender: 'llm',
      content: '',
      isStreaming: true
    };
    conversation.value.push(streamMessage);
    streamingMessageRef.value = streamMessage;

    // 连接建立后发送请求
    ws.onopen = () => {
      if (!isApiAvailable.value) {
        ws.dispatchEvent(new Event('error'));
        streamMessage.content = "未登录的用户";
        throw new Error("未登录的用户");
      }
      isThinkingActive = true;  // 允许动画运行
      ws.send(JSON.stringify({
        isOldchat: isOldchat.value,
        message: [userMessage],
        llm: modelConfig.llm,
        user_id: userState.user.user_id,
        source: "geo_graph",
        TTS: modelConfig.TTS
      }));
    };

    // WebSocket 事件处理
    ws.onmessage = (event) => {
      try {
        const chunk = JSON.parse(event.data);
        console.log(chunk)
        if (chunk.type === 'text') {
          if (chunk.content === '[DONE]') {
            console.log("流式结束");
            doneReceived = true;
            streamingMessageRef.value.isStreaming = false;
          }
          if (!doneReceived) {
            streamingMessageRef.value.content += chunk.content;
          }
        }

        if (chunk.type === 'error') {
          streamingMessageRef.value.content += `\n[错误 : ${chunk.details}]`;
          streamingMessageRef.value.isStreaming = false;
          throw new Error(chunk.details);
        }

        if (chunk.type === 'summary') {
          console.log("概括内容:", chunk.content);

          if (!thinkingContent.value) {
            thinkingContent.value = chunk.content;
            typeEffect();  // 调用异步打字机效果
          }

          if (chunk.audio) {
            checkAndCloseWebSocket();
            audioQueue.value.push(base64ToAudioUrl(chunk.audio));
            playAudioQueue();
          }
        }

        if (chunk.type === 'audio') {
          console.log("主音频已忽略（仅概括生成音频）");
        }

        if (chunk.type === 'completed') {
          isOldchat.value = chunk.session_id;
          checkAndCloseWebSocket(); // 检查是否可以关闭 WebSocket
        }
      } catch (error) {
        console.error("WebSocket 消息处理错误:", error);

        // 触发自定义错误事件
        ws.dispatchEvent(new Event('error'));
      }
    };

    ws.onerror = (error) => {
      // 将错误输出到内容中
      console.error('WebSocket 错误:', error);
      streamingMessageRef.value.isStreaming = false;
      isThinkingActive = false;  // 停止动画
      summaryRef.value.innerHTML = '啊呀！好像发生错误了呢，再试一次吧';
      playPromptAudio('error');
      ws.close();
    };

    ws.onclose = () => {
      // 生成完成后，把 LLM 的回复加入历史记录
      if (streamingMessageRef.value?.content) {
        chatHistory.value.push({
          role: "assistant",
          content: streamingMessageRef.value.content
        });
      }
      isThinkingActive = false;  // 停止动画
      cleanup();
    };

    // 中止处理
    controller = {
      abort: () => {
        streamingMessageRef.value.content += '\n[用户终止]';
        isThinkingActive = false;  // 停止动画
        summaryRef.value.innerHTML = '是不是打错字啦？没关系的，重新输入一遍吧';
        playPromptAudio('cancel');
        ws.close();
        cleanup();
      }
    };
  }
  // 检查是否可以安全关闭 WebSocket
  const checkAndCloseWebSocket = () => {
    if (doneReceived && thinkingContent.value) {
      console.log("所有数据接收完毕，关闭 WebSocket");
      ws.close();
    }
  };

  // 清理函数
  const cleanup = () => {
    isGenerating.value = false;
    showCursor.value = false;
    streamingMessageRef.value = null;

    setTimeout(() => {
      const submitBtn = document.querySelector('.submit-btn');
      if (submitBtn) {
        submitBtn.style.display = "block";
        submitBtn.style.opacity = "1";
      }
    }, 40);
  };
};

// 中断LLM生成函数
const stopLLMGeneration = () => {
  if (isGenerating.value) {
    controller.abort();  // 终止 fetch 请求
    if (reader) reader.cancel();  // 终止流读取
    isGenerating.value = false;
    console.log("LLM 输出已中断");
  }
};

// 点击交互按钮
const handleChatWithLLM = () => {
  if (data.textInput || inputBoxes.value.length !== 0) {
    nextTick(() => {
      scrollToBottom(); // 发送后强制滚动
      autoScroll.value = true; // 确保自动滚动开启
    });
    chatWithLLM();
    data.textInput = "";
  } else  {
    data.isDisabled = true;
    gsap.to('.warning-alert',{y:'+=20',opacity:1,duration:0.7,pointerEvents:'auto',ease:'none'});
    setTimeout( async () => {
      await gsap.to('.warning-alert',{y:'-=20',opacity:0,duration:0.7,pointerEvents:'none',ease:'none'});
      data.isDisabled = false;
    },3000)
  }
}

// 点击终止按钮
const handleStopLLMGeneration = () => {
  stopLLMGeneration();
  setTimeout(() => {
    const submitBtn = document.querySelector('.submit-btn');
    if (!submitBtn) {
      console.warn("按钮不存在，无法设置样式");
      return;
    }
    submitBtn.style.display = "block";
    submitBtn.style.opacity = "1";
  }, 40);  // 让浏览器有时间渲染 `.submit-btn`
}

// 点击回车交互
const handleKeydown = (e) => {
  if (e.key === "Enter") {
    if (!e.shiftKey && !isGenerating.value) {
      e.preventDefault();
      handleChatWithLLM();
    }
  } else if (e.key === "Escape" && isGenerating.value) {
    handleStopLLMGeneration();
  }
}

// 显示/隐藏输入/输出/提交按钮
const changeDisplay = () => {
  if (inAnimation.value) return;

  if (data.displayEverything) {
    // 收回对话框
    if (data.displayHistory) {
      // 如果有历史记录，还要将历史记录收回
      gsap.timeline()
          .set(['.submit-btn','.stop-btn'],{display:'none'})
          .to(['.outputArea','.inputArea','.tag-container','.bookmark',
            '.historyDisplay','.LLM-background'],{left: "-=28%"})
          .to('.LLM-wrapper',{left:"-28%", opacity: 0},"<")
          // .to('.graph-container',{left:"0",width:"90%"},"<")
          .set(['.historyDisplay','.outputArea','.LLM-wrapper','.LLM-background'],{display:'none'})
    } else {
      // 否则收回输入输出以及标签即可
      gsap.timeline()
          .set(['.submit-btn','.stop-btn'],{display:'none'})
          .to(['.outputArea','.inputArea','.tag-container','.bookmark','.LLM-background'],{left: "-=28%"})
          // .to('.graph-container',{left:"0",width:"90%"},"<")
          .set(['.historyDisplay','.outputArea','.LLM-background'],{display:'none'})
    }
    data.displayEverything = false;
  } else {
    // 展开对话框
    if (!isFirstTime.value) {
      gsap.set('.LLM-background',{left:"-28%"})
      isFirstTime.value = true;
    }
    if (data.displayHistory) {
      // 如果有历史记录，还需要展开它
      gsap.timeline()
          .set(['.historyDisplay','.outputArea','.LLM-wrapper','.LLM-background'],{display:'block'})
          .set('.LLM-wrapper',{opacity: 1})
          .to(['.outputArea','.inputArea','.tag-container','.bookmark',
            '.historyDisplay','.LLM-wrapper','.LLM-background'],{left: "+=28%"})
          // .to('.graph-container',{left:"10%",width:"80%"},"<")
          .set(['.submit-btn','.stop-btn'],{display:'block'});
    } else {
      // 否则仅展开输入输出即可
      gsap.timeline()
          .set(['.historyDisplay','.outputArea','.LLM-background'],{display:'block'})
          .to(['.outputArea','.inputArea','.tag-container','.bookmark','.LLM-background'],{left: "+=28%"})
          // .to('.graph-container',{left:"10%",width:"80%"})
          .set(['.submit-btn','.stop-btn'],{display:'block'});
    }
    data.displayEverything = true;
  }
}

// 动态获取输入文本框的 top 值
const getInputAreaTop = () => {
  const inputElement = document.querySelector('#textInputArea');
  const tagsElement = document.querySelector('#tag-container');
  if (inputElement && tagsElement) {
    const inputTop = inputElement.getBoundingClientRect().top;
    tagsElement.style.bottom = `${window.innerHeight - inputTop + 10}px`;
  }
}

// 监听标签关闭事件
const handleInputBoxClosed = (text) => {
  const obj = {'input':text}
  const index = inputBoxes.value.findIndex((item) => JSON.stringify(item) === JSON.stringify(obj));
  if (index !== -1) {
    inputBoxes.value.splice(index, 1);
  }
}

// 处理滚动事件
const handleScroll = () => {
  const container = outputAreaRef.value;
  if (!container) return;

  const { scrollTop, clientHeight, scrollHeight } = container;
  const isAtBottom = scrollTop + clientHeight >= scrollHeight - 50;
  autoScroll.value = isAtBottom; // 离底部50px内视为自动滚动开启
};

// 按时间排序历史记录
const groupHistoryByTime = () => {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const oneDay = 24 * 60 * 60 * 1000;

  const result = {
    today: [],
    last7days: [],
    last30days: [],
    earlier: [],
  };

  HistoryPreview.value.preview?.forEach(item => {
    const itemDate = new Date(item.timestamp.replace(/-/g, '/'));
    itemDate.setHours(itemDate.getHours() + 8);
    const diffDays = Math.floor((itemDate - today) / oneDay);
    if (diffDays === 0) {
      result.today.push(item);
    } else if (diffDays >= -6) {
      result.last7days.push(item);
    } else if (diffDays >= -29) {
      result.last30days.push(item);
    } else {
      result.earlier.push(item);
    }
  });

  const sortByTimestampDesc = (a, b) => new Date(b.timestamp) - new Date(a.timestamp);
  result.today.sort(sortByTimestampDesc);
  result.last7days.sort(sortByTimestampDesc);
  result.last30days.sort(sortByTimestampDesc);
  result.earlier.sort(sortByTimestampDesc);
  return result;
};

// 处理历史记录查询
const getHistoryPreview = async () => {
  if (inAnimation.value) return;

  if (data.displayHistory) {
    // 关闭历史记录
    requestAnimationFrame(async () => {
      inAnimation.value = true;
      if (data.displayEverything) {
        await gsap.timeline()
            .to(['.historyDisplay'], { left: '-=28%'})
            .to('.LLM-wrapper',{opacity: 0},"<")
            .set(['.historyDisplay','.LLM-wrapper'], { display: 'none'})
      } else {
        await gsap.timeline()
            .set(['.historyDisplay','.LLM-wrapper'], { display: 'none'})
            .set('.LLM-wrapper',{ left: '0', opacity: 0 })
      }
      inAnimation.value = false;
    })
  }
  data.displayHistory = !data.displayHistory;
  if (data.displayHistory) {
    // 准备打开历史记录
    requestAnimationFrame(async () => {
      inAnimation.value = true;
      if (data.displayEverything) {
        // 有输入输出时，仅打开历史记录
        await gsap.timeline()
            .set(['.historyDisplay'],{ display: 'block',zIndex: 10000})
            .set('.LLM-wrapper',{display: 'block'})
            .to(['.historyDisplay'],{ left: "+=28%"})
            .to('.LLM-wrapper',{opacity: 1},"<")
      } else {
        // 否则输入输出部分也要打开
        data.displayEverything = true;
        await gsap.timeline()
            .set(['.historyDisplay'],{ display: 'block',zIndex: 10000})
            .set(['.outputArea','.LLM-wrapper','.LLM-background'],{display: 'block'})
            .to(['.historyDisplay','.inputArea',
              '.tag-container','.bookmark'],{ left: "+=28%"})
            // .to('.graph-container',{left:"10%",width:"80%"},"<")
            .to(['.outputArea','.LLM-background'],{left:"0"},"<")
            .to('.LLM-wrapper',{opacity: 1},"<")
            .from('.LLM-wrapper',{ left: "-=28%"},"<")
            .set(['.submit-btn','.stop-btn'],{display:'block'})
      }
      inAnimation.value = false;
    })
    const ws = new WebSocket(WS_URL)
    ws.onopen = () => {
      try {
        if (JSON.parse(localStorage.getItem('isApiavailable'))) {
          const payload = {
            user_id: userState?.user?.user_id || null,
            task: "get_preview",
            source: "geo_graph"
          }
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify(payload))
          } else {
            console.error('WebSocket is not open')
          }
        }
        else {
          console.log("API不可用")
        }
      } catch (error) {
        console.error('请求失败:', error)
        ws.close();
      } finally {
        // extractCoordinates(assistantMessage.content)
      }
    }
    ws.onmessage = (event) => {
      HistoryPreview.value = reactive(JSON.parse(event.data))
      console.log(HistoryPreview.value);
      HistoryPreview.value = groupHistoryByTime()
      console.log(HistoryPreview.value);
      ws.close();
    }
  }
}

// 根据前驱 id 获取历史记录
const loadHistoryById = async (id) => {
  activeHistoryId.value = id;
  const ws = new WebSocket(WS_URL)
  ws.onopen = () => {
    try {
      if (JSON.parse(localStorage.getItem('isApiavailable'))) {
        const payload = {
          user_id: userState?.user?.user_id || null,
          task: "get_full_history",
          precursor_id: id,
        }
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify(payload))
        } else {
          console.error('WebSocket is not open')
        }
      }
      else {
        console.log("API不可用")
      }
    } catch (error) {
      console.error('请求失败:', error)
      ws.close();
    }
  }
  ws.onmessage = (event) => {
    const originMessages = JSON.parse(event.data).history;
    const newMessages = originMessages.map(obj => {
      const newObj = {};

      for (const key in obj) {
        if (obj.hasOwnProperty(key)) { // 确保只遍历对象自身的属性
          if (key === 'role') {
            newObj['sender'] = obj[key]; // 替换 "role" 为 "sender"
          } else {
            newObj[key] = obj[key]; // 复制其他键值对
          }
        }
      }

      return newObj;
    });
    console.log(newMessages);
    isOldchat.value = JSON.parse(event.data).isOldchat;
    conversation.value.splice(1, conversation.value.length, ...newMessages);
    ws.close();
    getHistoryPreview(); // 关闭历史记录
  }
}

// 格式化历史记录内容以及时间
const formatPreview = (msg) => {
  return msg.length > 15 ? msg.slice(0, 15) + '...' : msg;
};
const formatTime = (timestamp) => {
  const date = new Date(timestamp.replace(/-/g, '/'));
  date.setHours(date.getHours() + 8); // 修正时区

  const now = new Date();
  const pad = (n) => n.toString().padStart(2, '0');

  const isToday = date.toDateString() === now.toDateString();
  const isThisYear = date.getFullYear() === now.getFullYear();

  if (isToday) {
    return `${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
  } else if (isThisYear) {
    return `${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
  } else {
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
  }
};

// 新建对话
const newConversation = () => {
  if (!data.displayEverything) {
    // 展开对话框
    changeDisplay();
  }
  if (data.displayHistory) {
    // 收起历史记录
    getHistoryPreview();
  }
  conversation.value = [conversation.value[0]];
  isOldchat.value = 0;
};

// 标签颜色映射函数
const getColorByLabel = (label) => {
  const colorMap = {
    Topic: '#FF6B6B',
    "专题": '#FF6B6B',
    FirstLevelBranch: '#4ECDC4',
    "一级分支": '#4ECDC4',
    SecondLevelBranch: '#45B7D1',
    "二级分支": '#45B7D1',
    ThirdLevelBranch: '#96CEB4',
    "三级分支": '#96CEB4',
    FourthLevelBranch: '#FFEEAD',
    "四级分支": '#FFEEAD',
    FifthLevelBranch: '#FFD3B6',
    "五级分支": '#FFD3B6',
    Supplement: '#C3B1E1',
    "补充": '#C3B1E1',
  };
  return colorMap[label] || '#C0C0C0';
}

// 渲染知识图谱
const renderKnowledgeGraph = async (cypher) => {
  const driver = neo4j.driver(
      "bolt://localhost:7687",
      neo4j.auth.basic("neo4j", "123456789")
  );
  const session = driver.session();

  try {
    let query;
    if (cypher) { query = cypher; }
    else { query = neo4jQuery["earthAndMap"]; }
    // 查询路径数据
    const result = await session.run(query);

    const nodes = new Map();
    const edges = new Map();

    result.records.forEach(record => {
      const path = record.get('path');

      path.segments.forEach(segment => {
        // 处理起始节点
        const startNode = segment.start;
        nodes.set(startNode.identity.toString(), {
          id: startNode.identity.toString(),
          label: startNode.properties.name || startNode.properties.名称 || "未命名节点",
          properties: startNode.properties,
          labels: startNode.labels
        });

        // 处理关系
        const relationship = segment.relationship;
        if (nonsenseType.includes(relationship.type)) {
          relationship.type = '关联';
        }
        edges.set(relationship.identity.toString(), {
          id: relationship.identity.toString(),
          from: startNode.identity.toString(),
          to: segment.end.identity.toString(),
          label: relationship.type,
          properties: relationship.properties
        });

        // 处理结束节点
        const endNode = segment.end;
        nodes.set(endNode.identity.toString(), {
          id: endNode.identity.toString(),
          label: endNode.properties.name || endNode.properties.名称 || "未命名节点",
          properties: endNode.properties,
          labels: endNode.labels
        });
      });
    });

    // 转换可视化数据格式
    const networkData = {
      nodes: Array.from(nodes.values()).map(node => ({
        id: node.id,
        label: node.label,
        title: `
          Labels: ${node.labels.join(', ')}
          Properties: ${JSON.stringify(node.properties, null, 2)}
        `,
        color: getColorByLabel(node.labels[0]),
        font: { color: '#fff' }
      })),
      edges: Array.from(edges.values()).map(edge => ({
        id: edge.id,
        from: edge.from,
        to: edge.to,
        label: edge.label,
        arrows: 'to',
        title: `Type: ${edge.label}\nProperties: ${JSON.stringify(edge.properties)}`
      }))
    };

    // 可视化配置
    const options = {
      nodes: {
        shape: 'box',
        margin: 10,
        size: 30,
        font: {
          size: 14,
          face: 'Microsoft YaHei'
        }
      },
      edges: {
        width: 2,
        smooth: {
          type: 'cubicBezier'
        }
      },
      physics: {
        stabilization: true,
        barnesHut: {
          gravitationalConstant: -2000
        }
      },
      interaction: {
        hover: true
      }
    };

    // 渲染图谱
    const container = document.getElementById('graph-container');
    const network = new Network(container, networkData, options);
    let count = 0;

    // 左移知识图谱，使得位置合适
    network.on("stabilized", function () {
      if (count !== 0) return;
      const deviation = 0;
      const offsetX = window.innerWidth * deviation;
      const currentPos = network.getViewPosition();
      network.moveTo({
        position: {
          x: currentPos.x + offsetX,
          y: currentPos.y
        },
        scale: network.getScale()
      });
      count++;
    });

    // 点击节点显示名称
    network.on("click", function (params) {
      if (params.nodes.length > 0 && isActive.value) {
        const nodeId = params.nodes[0];
        const node = nodes.get(nodeId);

        if (!data.displayEverything) {
          if (data.displayHistory) {
            data.displayHistory = false;
            gsap.set('.LLM-wrapper',{left: "0"});
          }
          gsap.timeline()
              .set('.tag-container',{display: 'flex',flexWrap:'wrap',overflow:'hidden'})
              .set(['.outputArea','.LLM-background'],{display:'block'})
              // .to('.graph-container',{left:"10%",width:"80%"})
              .to(['.outputArea','.inputArea','.bookmark'],{left: "+=28%"},"<")
              .to('.LLM-background',{left:"0"},"<")
              .to(['.tag-container'],{left:"1%"},"<")
              .set(['.submit-btn','.stop-btn'],{display:'block'})
          data.displayEverything = true;
        } else {
          gsap.timeline()
              .set('.tag-container',{display: 'flex',flexWrap:'wrap',overflow:'hidden'})
              .to(['.tag-container'],{left:"1%"},"<")
        }

        const obj = {'input':node.label};
        const exists = inputBoxes.value.some(item => JSON.stringify(item) === JSON.stringify(obj));
        if (!exists && inputBoxes.value.length <= 5) {
          inputBoxes.value.push({'input':node.label});
        }
        getInputAreaTop();
      }
    });

  } catch (error) {
    console.error('Neo4j查询错误:', error);
  } finally {
    await session.close();
    await driver.close();
  }
}
onMounted(() => {
  // 加载监听器
  window.addEventListener('resize', updatePosition);

  // 页面轮播图动画
  gsap.timeline({repeat:-1})
      .to('.image1',{opacity:1,scale:1,duration:3,ease:'none'})
      .to('.image1',{opacity:0,scale:0.75,duration:3,ease:'none'})
      .to('.image2',{opacity:1,scale:1,duration:3,ease:'none'})
      .to('.image2',{opacity:0,scale:0.75,duration:3,ease:'none'})
      .to('.image3',{opacity:1,scale:1,duration:3,ease:'none'})
      .to('.image3',{opacity:0,scale:0.75,duration:3,ease:'none'})

  setTimeout(() => {
    playPromptAudio('greeting');
  },2000)

  // 加载 Live2D
  loadLive2D();

  // // 展示模型动画
  // ScrollTrigger.create({
  //   trigger:'.section2',
  //   start:'top-=400 top',
  //   end:'+=200',
  //   scrub:true,
  //   animation:
  //       gsap.timeline()
  //           .to('.section1',{y:'-=100',opacity:0})
  //           .from('.section2',{y:'+=100',opacity:0},"<")
  // });

  // 执行渲染
  renderKnowledgeGraph();
});


// 组件卸载时销毁 WebGL 资源，停止对话
onUnmounted(() => {
  if (app.value) {
    app.value.destroy(true);
    app.value = null;
    model.value = null;
  }
  window.removeEventListener('resize', updatePosition);
  stopLLMGeneration();
});

// 自动滚动
const scrollToBottom = () => {
  const container = document.querySelector('.outputArea');
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
}

// 在消息更新后调用
watch(() => conversation.value, () => {
  nextTick(() => {
    if (autoScroll.value) {
      scrollToBottom()
    }
  });
}, { deep: true })

// 自动调整行高
watch(() => data.textInput, () => {
  nextTick(() => {
    // 添加 requestAnimationFrame 确保浏览器完成布局
    requestAnimationFrame(() => {
      getInputAreaTop();
    });
  });
}, { deep: true });

// 添加滚动监听
watch(() => data.displayEverything, () => {
  nextTick(() => {
    if (data.displayEverything) {
      outputAreaRef.value?.addEventListener('scroll', handleScroll);
    } else {
      outputAreaRef.value?.removeEventListener('scroll', handleScroll);
    }
  })
})

// 添加图谱请求监听
watch(() => currentIndex.value, async (val) => {
  const key = Object.keys(neo4jQuery)[val]
  const cypher = neo4jQuery[key]
  await renderKnowledgeGraph(cypher);
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&display=swap');

/* 标签展示框 */
.tag-container {
  position: fixed;
  bottom: 11%;
  left: -27%;
  width: 23%;
  gap: 8px;
  z-index: 12;
}
/* 移除滚动条 */
.tag-container::-webkit-scrollbar {
  display: none;
}

/* 展开/隐藏对话框 */
.bookmark {
  position: fixed;
  top: 10.5%;
  left: 0;
  width: 40px;
  height: 40px;
  background-color: #aac6b6;
  box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
  color: white;
  font-size: 24px;
  text-align: center;
  line-height: 40px;
  cursor: pointer;
  border-radius: 0 8px 8px 0;
  z-index: 10;
  pointer-events: auto;
}
.bookmark:hover {
  background-color: #98b2a4; /* hover 时稍微变深 */
}
.bookmark2 {
  top: calc(10.5vh + 45px);
}
.bookmark3 {
  top: calc(10.5vh + 90px);
}

/* 输入输出区域 */
.LLM-input-output {
  position: fixed;
  top: 0;
  left: 0;
  width: 28%;
  height: 100%;
  z-index: 11;
  pointer-events: none;
}

/* 输入输出背景 */
.LLM-background {
  position: fixed;
  top: 0;
  left: -28%;
  width: 28%;
  height: 100%;
  display: none;
  background-color: #e2f0ec;
  box-shadow: 0 -2px 7px rgba(0, 0, 0, 0.2);
}

/* 输入输出蒙层 */
.LLM-wrapper {
  position: fixed;
  left: 0;
  top: 0;
  width: 28%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  z-index: 100;
  opacity: 0;
  display: none;
  pointer-events: auto;
}

/* 用户输入框 */
:deep(.el-textarea__inner) {
  border-radius: 12px !important;
  line-height: 1.8 !important;
  padding-bottom: 30px;
}
.inputArea {
  position: fixed;
  bottom: 2%;
  left: -27%;
  width: 26%;
  font-size: 16px;
  border-radius: 50px !important;
  z-index: 11;
  /* display: none;
  opacity: 0; */
  pointer-events: auto;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
}
:deep(.el-textarea__inner) {
  padding: 10px 25px 35px 15px; /* 调整这个值来控制文字与边框的间距 */
}

/* 输入按钮 */
.submit-btn,.stop-btn {
  position: fixed;
  bottom: 3%;
  left: 24%;
  width: 30px;
  height: 30px;
  border-radius: 100%;
  margin: 0;
  padding: 7px 0;
  justify-content: center;
  align-items: center;
  font-size: 18px;
  z-index: 12;
  display: none;
  pointer-events: auto;
}
/* 终止按钮 */
.stop-btn {
  display: block;
  opacity: 1;
}

/* 空输入提示 */
.warning-alert {
  position: fixed;
  top: 9%;
  right: 25%;
  width: 24%;
  transform: translateX(-50%);
  border-radius: 20px;
  opacity: 0;
  pointer-events: none;
  z-index: 15;
}

/* 历史记录 */
.historyDisplay {
  position: fixed;
  top: 0;
  left: -28%;
  width: 23%;
  height: 100vh;
  padding-top: 10vh;
  background-color: #f9f9f9;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  overflow-y: auto;
  z-index: 1000;
  border-right: 1px solid #ddd;
  display: none;
  pointer-events: auto;
}
/* 大标题 */
.historyDisplay h3 {
  font-size: 1.3rem;
  font-weight: bold;
  padding: 0 20px;
  margin-bottom: 1rem;
  color: #2c3e50;
}
/* 小标题 */
.historyDisplay h4 {
  font-size: 1rem;
  margin: 1rem 20px 0.5rem;
  color: #34495e;
  border-bottom: 1px solid #ccc;
  padding-bottom: 4px;
}
/* 正文 */
.history-item {
  padding: 7px 10px;
  margin: 4px 10px;
  cursor: pointer;
  transition: background-color 0.2s ease;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #2d2d2d;
  border-radius: 10px;
}
/* 悬停 */
.history-item:hover {
  background-color: #ececec;
}
/* 选中 */
.history-item.active {
  background-color: #d8d8d8;
}
/* 时间戳 */
.timestamp {
  font-size: 0.8rem;
  color: #999;
  margin-left: 10px;
  white-space: nowrap;
}

/* 美化滚动条 */
.historyDisplay::-webkit-scrollbar {
  width: 8px;
  height: unset;
}
.historyDisplay::-webkit-scrollbar-thumb {
  background-color: #e3e3e3;
  border-radius: 10px;
  border: 4px solid rgba(0, 0, 0, 0);
  background-clip: unset;
  box-shadow: unset;
  transition: background 0.3s ease;
}
.historyDisplay::-webkit-scrollbar-track {
  background-color: transparent;
  border-radius: unset;
  box-shadow: unset;
}
.historyDisplay::-webkit-scrollbar-thumb:hover {
  background-color: #d1d1d1;
}
.outputArea::-webkit-scrollbar {
  width: 8px;
}
.outputArea::-webkit-scrollbar-thumb {
  box-shadow: unset;
  background-clip: unset;
}

/* 无历史记录 */
.no-history {
  text-align: center;
  margin-top: 20vh;
  color: #999;
  font-size: 14px;
}
.no-history-icon {
  font-size: 36px;
  display: block;
  margin-bottom: 0.5rem;
}
.no-history-text {
  font-size: 16px;
  color: #666;
}

/* LLM输出框 */
.outputArea {
  position: fixed;
  top: 10%;
  left: -28%;
  width: calc(28% - 30px);
  height: calc(65vh - 15px);
  color: #0d0f1a;
  padding: 0 15px 15vh 15px;
  font-size: 16px;
  overflow-y: auto;
  overflow-x: hidden;
  line-height: 1.8;
  z-index: 11;
  display: none;
  background-color: #e2f0ec;
  pointer-events: auto;
}

/* 概要输出 */
.summary-output {
  position: fixed;
  top: 35%;
  right: 12%;
  z-index: 103;
  letter-spacing: 1px;
  background: linear-gradient(135deg, #fffdf3, #ffebcd); /* 柔和渐变背景 */
  color: #4b3f3f;
  font-family: 'ZCOOL KuaiLe', sans-serif;
  font-size: 18px;
  padding: 14px 22px;
  border-radius: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  max-width: 300px;
  word-wrap: break-word;
  animation: fadeInUp 0.5s ease-out;
  transition: all 0.3s ease-in-out;
}

/* 气泡底部的小圆点模拟云朵 */
.summary-output::before,
.summary-output::after {
  content: "";
  position: absolute;
  bottom: -10px; /* 让装饰元素位于文本框下方 */
  background: #ffebcd;
  border-radius: 50%;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

/* 小圆 */
.summary-output::before {
  width: 18px;
  height: 18px;
  right: 2%; /* 控制偏移 */
  bottom: -50px;
}

/* 大圆 */
.summary-output::after {
  width: 25px;
  height: 25px;
  right: 20px; /* 控制偏移 */
  bottom: -30px;
}

/* Live2D */
canvas {
  position: fixed;
  top: 40%;
  right: -35%;
  border: none;
  z-index: 100;
}

/* 公共容器 */
.container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

/* 第一屏 */
.section1 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  z-index: 5;
  overflow-x: hidden;
}

/* 轮播图图片 */
.image1,.image2,.image3 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  scale: 1.25;
  z-index: 1;
  object-fit: cover;
}

/* 首页大标题 */
.section1-title {
  position: absolute;
  top: 35%;
  left: 50%;
  font-size: 64px;
  font-weight: bold;
  text-align: center;
  transform: translate(-50%, -50%);
  color: #33aaeb; /* 深蓝青色，增强对白色背景的对比度 */
  text-shadow: 0 0 8px rgba(29, 168, 202, 0.6),
  0 0 16px rgba(31, 139, 166, 0.4); /* 适度光晕，减少眩光感 */
  z-index: 10;
}

/* 首页副标题 */
.section1-subtitle {
  font-size: 18px;
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #d6f5ff;
  background: rgba(0, 0, 0, 0.5);
  padding: 10px 20px;
  border-radius: 6px;
  border: 1px solid rgba(0, 255, 255, 0.6);
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
  z-index: 10;
}

/* 第二屏 */
.section2 {
  position: absolute;
  top: 100vh;
  left: 0;
  height: 100vh;
}

/* 切换模式按钮 */
.switch-mode-container {
  position: absolute;
  top: 15%;
  right: 5.5%;
  z-index: 2;
}
.wrapper {
  scale: 1.5;
}
.switch-words {
  position: absolute;
  top: 11%;
  right: 4.6%;
  z-index: 3;
  font-weight: 600;
  font-size: 18px;
  color: #333333;
  letter-spacing: 1px;
}

/* 切换图谱按钮 */
.graph-changer {
  position: absolute;
  top: 8%;
  right: calc(50% - 135px);
  z-index: 1;
}

/* 知识图谱 */
.graph-container {
  width: 80%;
  height: 90%;
  position: absolute;
  top: 10%;
  left: 10%;
}
</style>