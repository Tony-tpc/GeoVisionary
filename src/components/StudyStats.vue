<script setup>
import { ref, onMounted } from "vue";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart, LineChart, BarChart, RadarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  VisualMapComponent,
  GridComponent,
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { provide } from "vue";
import { userState } from "@/store/userStore.js";
/**
 * @typedef {"topic_proficiency" | "active_time_distribution"
 *  | "study_frequency_last_7_days" | "content_click_rate"} Behaviors
 */

// 配置 echarts 组件
use([
  CanvasRenderer,
  PieChart,
  LineChart,
  BarChart,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  VisualMapComponent,
  GridComponent,
]);

provide(THEME_KEY, "light");

// 域名
const domain = 'http://localhost:8040/';
// 知识点掌握度数据
const knowledgeData = ref({});
const knowledgeOption = ref({});
// 活跃时间分布数据
const activeTimeData = ref([]);
const activeTimeOption = ref({});
const activeTimeConfig = {
  morning: "早上",
  afternoon: "下午",
  evening: "晚上",
};
// 内容点击偏好数据
const clickPreferenceData = ref([]);
const clickPreferenceOption = ref({});
const clickPreferenceConfig = {
  text: "图文",
  video: "视频",
};
// 近 7 天学习情况数据
const studyFrequencyOption = ref({});
const studyFrequencyDataList = ref([]); // 存储日期
const studyFrequencyValueList = ref([]); // 存储学习次数

/**
 * 用户学习行为请求
 * @param behaviorType {Behaviors}
 * @returns {Object}
 */
const behaviorRequest = async (behaviorType) => {
  const url = domain + "api/get-learning-behavior/";
  const response = await fetch(url, {
    method: "POST",
    body: JSON.stringify({
      user: userState.user,
      behavior_type: behaviorType,
    }),
    headers: {
      "Content-Type": "application/json",
    }
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data)
  }
  return data;
}

// 知识点掌握度请求（雷达图）
const knowledgeRequest = async () => {
  const data = await behaviorRequest("topic_proficiency")

  // 存储原始数据
  knowledgeData.value = data;

  // 创建完整名称映射：简称 -> 全名
  const nameMap = {};

  // 创建雷达图 indicator 和 value
  const indicators = [];
  const values = [];

  for (const [fullName, val] of Object.entries(data)) {
    let shortName = fullName.split("：")[1].slice(0, 5);
    if (fullName.split("：")[1].length > 5) {
      shortName += "...";
    }
    nameMap[shortName] = fullName.split("：")[1];  // 只保留冒号后内容
    indicators.push({
      name: shortName,
      max: 100,
    });
    values.push(val * 100);
  }

  // 更新雷达图配置
  knowledgeOption.value = {
    title: {
      text: "知识点掌握度",
      left: "center",
    },
    tooltip: {
      trigger: "item",
      formatter: (params) => {
        const items = params.value.map((v, i) => {
          const short = indicators[i].name;
          const full = nameMap[short];
          return `${full}：${v.toFixed(1)}%`;
        }).join("<br>");
        return `<strong>${params.name}</strong><br>${items}`;
      },
    },
    radar: {
      indicator: indicators,
      radius: 90,
    },
    series: [
      {
        name: "掌握度",
        type: "radar",
        data: [
          {
            value: values,
            name: userState.user.username,
          },
        ],
      },
    ],
  };
}

// 活跃时间请求（环形图）
const activeTimeRequest = async () => {
  const data = await behaviorRequest("active_time_distribution");
  // 将对象转变为数组，并设置指定键值，符合 echarts 渲染逻辑
  for (const [name, val] of Object.entries(data)) {
    activeTimeData.value.push({
      value: val * 100,
      name: activeTimeConfig[name],
    })
  }

  activeTimeOption.value = {
    title: {
      text: "活跃时间分布",
      left: "center",
    },
    tooltip: {
      trigger: "item",
      valueFormatter: (value) => {
        return `${value.toFixed(1)}%`;
      },
    },
    legend: {
      bottom: 0,
    },
    series: [
      {
        name: "活跃时间",
        type: "pie",
        radius: ["40%", "70%"],
        avoidLabelOverlap: false,
        data: activeTimeData.value,
      },
    ],
  };
}

// 点击偏好请求（普通饼图）
const clickPreferenceRequest = async () => {
  const data = await behaviorRequest("content_click_rate");
  // 将对象转变为数组，并设置指定键值，符合 echarts 渲染逻辑
  for (const [name, val] of Object.entries(data)) {
    clickPreferenceData.value.push({
      value: val * 100,
      name: clickPreferenceConfig[name],
    })
  }

  clickPreferenceOption.value = {
    title: {
      text: "内容点击偏好",
      left: "center",
    },
    tooltip: {
      trigger: "item",
      valueFormatter: (value) => {
        return `${value.toFixed(1)}%`;
      },
    },
    legend: {
      bottom: 0,
    },
    series: [
      {
        name: "点击偏好",
        type: "pie",
        radius: "60%",
        data: clickPreferenceData.value,
      },
    ],
  };
}

// 学习情况请求（折线图）
const studyFrequencyRequest = async () => {
  const data = await behaviorRequest("study_frequency_last_7_days");
  let max = 0;
  // 将原本的对象转变为日期和值数组，并设置最大值
  for (const [name, val] of Object.entries(data)) {
    studyFrequencyDataList.value.push(name);
    studyFrequencyValueList.value.push(val);
    if (val > max) {
      max = val;
    }
  }

  studyFrequencyOption.value = {  // 改用 ref 包装
    visualMap: {
      show: false,
      type: 'continuous',
      seriesIndex: 0,
      min: 0,
      max: max,
    },
    title: {
      text: '近 7 天学习情况',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: studyFrequencyDataList,
    },
    yAxis: {},
    series: [
      {
        type: 'line',
        showSymbol: false,
        data: studyFrequencyValueList,
      }
    ]
  };
}

onMounted(() => {
  knowledgeRequest();
  activeTimeRequest();
  clickPreferenceRequest();
  studyFrequencyRequest();
})
</script>

<template>
  <div class="parent-container" style="margin-bottom: 2rem">
    <v-chart class="chart" :option="knowledgeOption" autoresize/>
    <v-chart class="chart" :option="activeTimeOption" autoresize/>
    <v-chart class="chart" :option="clickPreferenceOption" autoresize/>
  </div>
  <div class="parent-container">
    <v-chart class="line-chart" :option="studyFrequencyOption" autoresize/>
  </div>
</template>

<style scoped>
.parent-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
}
.chart {
  height: 300px;
  width: 330px;
}
.line-chart {
  width: 100%;
  height: 300px;
}
</style>