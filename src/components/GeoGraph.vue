<template>
  <section>
    <!--  加载背景  -->
    <Loading title=".section1-title" subtitle=".section1-subtitle"></Loading>
  </section>
  <section>
    <!--  固定对话内容  -->
    <div>
      <!--  Live2D -->
      <canvas ref="canvas" class="live2Dmodel" @click="changeDisplay"></canvas>
      <!--  便捷标签 -->
      <div class="convenient-tags-container">
        <el-button class="zoom-outputArea-btn" @click="changeOutputArea">
          <el-icon v-if="!data.changeArea"><ZoomIn /></el-icon>
          <el-icon v-else><ZoomOut /></el-icon>
        </el-button>
        <el-button class="refresh-outputArea-btn" @click="refreshPosition"
                   @mouseenter="animateTooltip('show')"
                   @mouseleave="animateTooltip('hide')">
          <el-icon><Refresh /></el-icon>
        </el-button>
        <div class="gsap-tooltip">重置输出框</div>
      </div>
      <!--   输入和输出   -->
      <div class="LLM-input-output">
        <el-alert title="请注意，输入不能为空" type="error" center show-icon class="warning-alert" :closable="false"/>
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
                placeholder="您可以在这里输入您想和小助教对话的内容！"
                class="inputArea"
                @keydown="handleKeydown"
                id="textInputArea"
            />
            <el-button v-if="!isGenerating" type="primary" @click="handleChatWithLocalLLM" class="submit-btn" :disabled="data.isDisabled">
              <el-icon  ><Top /></el-icon>
            </el-button>
            <el-button v-else type="primary" @click="handleStopLLMGeneration" class="stop-btn">
              <el-icon  ><Close /></el-icon>
            </el-button>
          </div>
        </div>
        <!--  输出区域  -->
        <div class="outputArea" ref="outputAreaRef">
          <ChatMessages
              :messages="conversation"
              :user-config="{
                name: `${userState.user? userState.user.username : '用户'}`,
                bgColor: '#d3e0d1',
                textColor: '#fffdf3'
              }"
              :llm-config="{
                name: 'AI助教',
                bgColor: '#f7f2eb',
                textColor: '#fffdf3',
                errorColor: '#ff4444'
              }"
              :show-llm-cursor="isGenerating"
          />
        </div>
      </div>
    </div>
  </section>
  <!--  首页背景图及标题 -->
  <section>
    <div class="container section1">
      <img src="@/assets/Full-Graph-test-1.png" alt="万象图谱" loading="lazy" class="image1">
      <img src="@/assets/Full-Graph-test-2.jpg" alt="万象图谱" loading="lazy" class="image2">
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
      <div class="switch-mode-container wrapper"><SwitchButton v-model="isActive"/></div>
      <div id="graph-container" style="width: 100%; height: 90%; border: 1px solid #ddd;position: absolute;top: 10%;"></div>
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
gsap.registerPlugin(ScrollTrigger,Draggable);

window.PIXI = PIXI;

const data = reactive({
  textInput:"",
  changeArea:false,
  displayEverything:false,
  isDisabled:false,
  nodeInfo:[],
})

// live2D
const canvas = ref(null); // live2D 载体
const app = ref(null); // live2D 应用
const model = ref(null); // live2D 模型

// LLM对话
const showCursor = ref(false); // 控制光标
const isGenerating = ref(false); // 控制加载状态
const conversation = ref([  { sender: 'llm', content: '您好呀，我是您的专属AI助教，请问有什么可以帮到您？' },]); // 对话记录
const streamingMessageRef = ref(null); // 当前流式消息的引用
let controller = new AbortController();  // 用于控制请求
let reader = null;  // 读取流

// 其他内容
const inputBoxes = ref([]); // 标签盒
const isActive = ref(true); // 切换便捷模式
const autoScroll = ref(true);
const outputAreaRef = ref(null);

// 封装 Live2D 加载逻辑
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
    // "https://cdn.jsdelivr.net/gh/guansss/pixi-live2d-display/test/assets/haru/haru_greeter_t03.model3.json"
    // "/haru/haru_greeter_t03.model3.json"
    // "/maolili/mailili.model3.json"
    // "/ariu/ariu.model3.json"
    // "/IceGIrl Live2D/IceGirl.model3.json"
    model.value = await Live2DModel.from("/haru/haru_greeter_t03.model3.json");
    app.value.stage.addChild(model.value);

    // 调整模型大小
    model.value.scale.set(0.2);
    model.value.x = -60;

    console.log("Live2D 模型加载成功");
  } catch (error) {
    console.error("加载失败", error);
  }
}

// 更新live2D位置
const updatePosition = () => {
  model.value.x = -0.05 * window.innerWidth;
};

// 历史记录
const chatHistory = ref([
  { role: "system", content: "你是一位经验丰富的高中地理老师，你的学生目前遇到了一些地理问题，你需要耐心地帮助他解决问题，并通俗易懂地讲解。记住，你只能用中文思考和回答。如果他输入的是其他方面的问题，也请像个老师一样耐心教导他。" }
]);

// 向本地LLM发送流式请求
const chatWithLLM = async () => {
  isGenerating.value = true; // 进入生成状态
  showCursor.value = true; // 显示光标

  // 创建新的控制器
  controller = new AbortController();
  const signal = controller.signal;

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
    conversation.value.push({ // 同时添加到对话列表
      sender: 'user',
      content: userContent
    });
    // 创建并添加流式消息占位符
    const streamMessage = {
      sender: 'llm',
      content: '',
      isStreaming: true
    };
    conversation.value.push(streamMessage);
    streamingMessageRef.value = streamMessage; // 保存当前流式消息引用
    try {
      const response = await fetch("http://localhost:8040/proxy/chat/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "deepseek-r1-distill-llama-8b", // phi-4 deepseek-r1-distill-llama-8b deepseek-r1-distill-qwen-14b
          messages: chatHistory.value,
          temperature: 0.6,
          max_tokens: 4096,
          stream: true, // 启用流式返回
        }),
        signal,// 绑定信号
      });

      if (!response.ok || !response.body) throw new Error("LLM 请求失败");

      // 获取可读流
      reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");


      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        // 先解码成字符串
        const chunk = decoder.decode(value, { stream: true });
        if (chunk === "[DONE]") {
          console.log("流式结束");
          break; // 停止流式读取
        }
        streamingMessageRef.value.content += chunk;

        // // 解析 JSON，提取内容
        // const lines = chunk.split("\n"); // API 可能返回多行
        // for (const line of lines) {
        //   if (line.trim().startsWith("data:")) {
        //     try {
        //       const json = JSON.parse(line.replace("data: ", ""));
        //       if (json.choices && json.choices[0].delta.content) {
        //         // 实时更新流式消息内容
        //         streamingMessageRef.value.content += json.choices[0].delta.content;
        //       }
        //     } catch (err) {
        //       console.error("解析错误:", err);
        //     }
        //   }
        // }
      }
      // 生成完成后，把 LLM 的回复也加入历史记录
      chatHistory.value.push({ role: "assistant", content: streamingMessageRef.value.content});
      console.log(chatHistory.value);
    } catch (error) {
      if (error.name === 'AbortError') {
        console.log('请求中止');
        // 移除未完成的流式消息
        const index = conversation.value.indexOf(streamingMessageRef.value);
        if (index > -1) conversation.value.splice(index, 1);
      } else {
        console.error('请求失败:', error);
        // 标记错误状态
        streamingMessageRef.value.error = true;
        streamingMessageRef.value.content += '\n[生成中断]';
      }
    } finally {
      isGenerating.value = false; // 结束生成状态
      showCursor.value = false; // 隐藏光标
      streamingMessageRef.value = null;

      // 恢复按钮状态
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
  }
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
const handleChatWithLocalLLM = () => {
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
      handleChatWithLocalLLM();
    }
  } else if (e.key === "Escape" && isGenerating.value) {
    handleStopLLMGeneration();
  }
}

// 放大输出结果
const changeOutputArea = () => {
  if (!data.changeArea) {
    gsap.timeline()
        .to('.outputArea',{top:'10%',height:'55%'})
    data.changeArea = true;
  } else {
    gsap.timeline()
        .to('.outputArea',{top:'20%',height:'30%'})
    data.changeArea = false;
  }
}

// 显示/隐藏输入/输出/提交按钮
const changeDisplay = () => {
  if (data.displayEverything) {
    gsap.timeline()
        .to(['.outputArea','.inputArea','.submit-btn','.tag-container','.stop-btn'],{opacity:0,ease:'power2.out'})
        .set(['.outputArea','.inputArea','.submit-btn','.tag-container','.stop-btn'],{display:'none'})
    data.displayEverything = false;
  } else {
    gsap.set(['.outputArea','.inputArea','.submit-btn','.stop-btn'],{display:'block'});
    gsap.set('.tag-container',{display:'flex',flexWrap:'wrap',overflow:'hidden'})
    gsap.to(['.outputArea','.inputArea','.submit-btn','.tag-container','.stop-btn'],{opacity:1,ease:'power2.in'});
    data.displayEverything = true;
  }
}

// 复原输出框
const refreshPosition = () => {
  gsap.set('.outputArea',{y:'0',x:'0', width: '50%', height: '30%'})
  gsap.timeline()
      .to('.outputArea',{top:'20%',height:'30%'})
  data.changeArea = false;
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

// GSAP控制
function animateTooltip(action) {
  const tooltip = document.querySelector('.gsap-tooltip');

  if(action === 'show') {
    gsap.to(tooltip, {
      opacity: 1,
      duration: 0.3,
      onUpdate: () => {
        // 实时跟随鼠标
        const mouseX = event.clientX + 15;
        const mouseY = event.clientY + 15;
        gsap.set(tooltip, { x: mouseX, y: mouseY });
      }
    });
  } else {
    gsap.to(tooltip, { opacity: 0, duration: 0.2 });
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

  // 拖动动画
  Draggable.create(".outputArea",{
    bounds:'.LLM-input-output',
    inertia:true,
    edgeResistance: 1,
    onDragEnd: function () {
      console.log('当前位置：',this.x,this.y);
    }
  });

  // 加载 Live2D
  loadLive2D();

  // 展示模型动画
  ScrollTrigger.create({
    trigger:'.section2',
    start:'top-=400 top',
    end:'+=200',
    scrub:true,
    animation:
        gsap.timeline()
            .to('.section1',{y:'-=100',opacity:0})
            .from('.section2',{y:'+=100',opacity:0},"<")
  });

  // 渲染知识图谱
  async function renderKnowledgeGraph() {
    const driver = neo4j.driver(
        "bolt://localhost:7687",
        neo4j.auth.basic("neo4j", "123456789")
    );
    const session = driver.session();

    try {
      // 查询路径数据
      const result = await session.run(`
      MATCH path=(n)-[r]->(m)
      RETURN path
      LIMIT 25`);

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

      // 点击节点显示名称
      network.on("click", function (params) {
        if (params.nodes.length > 0 && isActive.value) {
          const nodeId = params.nodes[0];
          const node = nodes.get(nodeId);
          gsap.set(['.outputArea','.inputArea','.submit-btn','.stop-btn'],{display:'block'});
          gsap.set('.tag-container',{display: 'flex',flexWrap:'wrap',overflow:'hidden'});
          gsap.to(['.outputArea','.inputArea','.submit-btn','.tag-container','.stop-btn'],{opacity:1,ease:'power2.in'});
          data.displayEverything = true;
          const obj = {'input':node.label};
          const exists = inputBoxes.value.some(item => JSON.stringify(item) === JSON.stringify(obj));
          if (!exists) {
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

  // 标签颜色映射函数
  function getColorByLabel(label) {
    const colorMap = {
      Topic: '#FF6B6B',
      FirstLevelBranch: '#4ECDC4',
      SecondLevelBranch: '#45B7D1',
      ThirdLevelBranch: '#96CEB4',
      FourthLevelBranch: '#FFEEAD'
    };
    return colorMap[label] || '#C0C0C0';
  }

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
</script>

<style scoped>
/* 标签展示框 */
.tag-container {
  position: fixed;
  bottom: 11%;
  left: 25%;
  width: 52%;
  gap: 8px;
  opacity: 0;
  display: none;
  pointer-events: none;
  z-index: 11;
}
/* 移除滚动条 */
.tag-container::-webkit-scrollbar {
  display: none;
}

/* 输入输出区域 */
.LLM-input-output {
  position: fixed;
  top: -20%;
  left: -50%;
  width: 195%;
  height: 140%;
  z-index: 11;
  pointer-events: none;
}

/* 用户输入框 */
:deep(.el-textarea__inner) {
  border-radius: 12px !important;
  line-height: 1.8 !important;
  padding-bottom: 30px;
}
.inputArea {
  position: fixed;
  bottom: 8%;
  left: 25%;
  width: 52%;
  font-size: 16px;
  border-radius: 50px !important;
  z-index: 11;
  display: none;
  opacity: 0;
  pointer-events: auto;
}
:deep(.el-textarea__inner) {
  padding: 10px 25px 35px 15px; /* 调整这个值来控制文字与边框的间距 */
}

/* 输入按钮 */
.submit-btn,.stop-btn {
  position: fixed;
  bottom: 9%;
  right: 24%;
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
  opacity: 0;
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

/* LLM输出框 */
.outputArea {
  position: fixed;
  top: 20%;
  left: 25%;
  width: 50%;
  height: 30%;
  color: #0d0f1a;
  border: 1px solid #0d0f1a;
  border-radius: 30px;
  padding: 15px;
  font-size: 16px;
  overflow-y: auto;
  overflow-x: hidden;
  line-height: 1.8;
  z-index: 11;
  display: none;
  opacity: 0;
  background-color: rgba(0,0,0,.8);
  pointer-events: auto;
}

/* 悬停提示文字 */
.gsap-tooltip {
  position: fixed;
  background: rgba(0,0,0,0.8);
  color: white;
  padding: 8px 12px;
  border-radius: 4px;
  pointer-events: none;
  opacity: 0;
  rotate: -90deg;
}

/* Live2D */
canvas {
  position: fixed;
  top: 40%;
  right: -35%;
  border: none;
  z-index: 100;
}

/* 便捷标签容器 */
.convenient-tags-container {
  position: fixed;
  bottom: 21%;
  right: 10%;
  z-index: 101;
  width: 150px;
  height: 35px;
  border-radius: 30px;
  rotate: 90deg;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #0d0f1a;
}

/* 便捷标签 */
.zoom-outputArea-btn,.refresh-outputArea-btn {
  padding: 6px;
  height: 30px;
  width: 30px;
  border-radius: 100%;
  justify-content: center;
  align-items: center;
  top: 21%;
  rotate: -90deg;
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
.image1,.image2 {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  scale: 1.25;
  z-index: 1;
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
  right: -2%;
  z-index: 2;
}
.wrapper {
  transform: scale(0.5);
  transform-origin: 0 0;
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

</style>