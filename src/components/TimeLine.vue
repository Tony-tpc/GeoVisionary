<template>
    <!-- <div>
        {{ props.yearArr }}
    </div> -->
    <div :class="props.bgcolor == 'light' ? 'TimeLine2-light' : 'TimeLine2-dark'">
        <div class="LeftBox">
            <el-slider v-model="value" :show-tooltip="false" :min="minValue" :max="maxValue" :marks="marks"
                @change="handleTimeLineChange" />
        </div>
        <div class="RightBox">
            <el-tooltip class="box-item" effect="light" content="上一个" placement="top">
                <el-icon :color="props.bgcolor == 'light' ? '#4a0987' : 'white'" size="30px" @click="handleSub">
                    <DArrowLeft />
                </el-icon>
            </el-tooltip>

            <el-tooltip class="box-item" effect="light" content="播放/暂停" placement="top">
                <el-icon :color="props.bgcolor == 'light' ? '#4a0987' : 'white'" size="30px" v-if="playSwitch"
                    @click="handlePlay">
                    <VideoPause />
                </el-icon>
                <el-icon :color="props.bgcolor == 'light' ? '#4a0987' : 'white'" size="30px" v-if="!playSwitch"
                    @click="handlePlay">
                    <VideoPlay />
                </el-icon>
            </el-tooltip>

            <el-tooltip class="box-item" effect="light" content="下一个" placement="top">
                <el-icon :color="props.bgcolor == 'light' ? '#4a0987' : 'white'" size="30px" @click="handleAdd">
                    <DArrowRight />
                </el-icon>
            </el-tooltip>
        </div>
    </div>
</template>

<script setup>
// vue
import {
    ref,
    watch,
    computed,
    onBeforeMount,
    onMounted,
    onBeforeUpdate,
    onUpdated,
} from "vue";
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { VideoPlay, VideoPause, DArrowLeft, DArrowRight } from '@element-plus/icons-vue'
// 宏
// 父组件传参 nowValue-当前选中或自动播放时的当前时间 yearArr-所有年份数组
// const props = defineProps(["bgcolor", "nowValue", "yearArr", 'second']);
const props = defineProps({
    bgcolor: {
        type: String,
        default: "dark",
    },
    nowValue: {
        type: String,
        default: '',
    },
    yearArr: {
        type: Array,
        default: () => [],
    },
    second: {
        type: Number,
        default: 0.1,
    },
    hourArr: {
        type: Array,
        default: () => [0, 0],
    }
});

// 派发事件 改变当前值-nowValue
const emits = defineEmits(["handleNowValueChange"]);

// 变量
// 自动播放 定时器
let timer = null;
// 一页几条
let pageSize = ref(5);
// 当前页数
let pageCode = ref(1);

// 当前值
let value = ref(0);

let minValue = ref(0);

let maxValue = ref(120);

// 刻度
const marks = ref({
    // 0: '2000-5',
    // 25: '2000-6',
    // 50: '2000-7',
    // 75: '2000-8',
    // 100: '2000-9',
    // 100: '2000-10',
});

// 播放控制 开关 默认关闭
let playSwitch = ref(false);

// 子组件 时间数组
let timeArr = ref([]);

let hourArr = ref([0, 0])
// 函数
// 时间线发生变化
const handleTimeLineChange = (val) => {
    hourArr = calculate(value)
    emits("handleNowValueChange", hourArr);  // 触发事件，并传递 val 参数
};

// 时间计算
const calculate = (value) => {
    // let rettime = ref([0, 0])// hour minute
    // rettime.value[0] = Math.floor(value.value / 5);
    // rettime.value[1] = Math.floor(value.value) % 5 * 24;
    return value.value / maxValue.value
}

// 播放控制
const handlePlay = () => {
    playSwitch.value = !playSwitch.value;
};

// 页面减
const handleSub = () => {
    if (value.value > minValue.value) {
        // value.value -= 25;
        var now = Math.ceil(value.value / 30)
        value.value = (now + 4 - 1) % 4 * 30
        hourArr = calculate(value)
        emits(
            "handleNowValueChange",
            hourArr
        );
    } else {
        value.value = maxValue.value;
        hourArr = calculate(value)
        emits(
            "handleNowValueChange",
            hourArr
        );
    }
};

// 页面加
const handleAdd = () => {
    if (value.value < maxValue.value) {
        value.value += 30;
        value.value = Math.floor(value.value / 30) * 30
        hourArr = calculate(value)
        emits(
            "handleNowValueChange",
            hourArr
        );
    } else {
        value.value = 0;
        hourArr = calculate(value)
        emits(
            "handleNowValueChange",
            hourArr
        );
    }
};

// 初始监听 为 timeArr赋值
watch(
    () => props.yearArr,
    (newVal, oldVal) => {
        timeArr.value = Array.from(newVal).slice(
            (pageCode.value - 1) * pageSize.value,
            pageCode.value * pageSize.value
        );
    }
);

// 监听 timeArr 改变 为marks赋值 且 计算最值
watch(
    timeArr,
    (newVal, oldVal) => {
        let obj = {};

        timeArr.value.forEach((item, index) => {
            obj[index * 30] = item;
        });


        marks.value = obj;

        maxValue.value = (timeArr.value.length - 1) * 30;
    },
    { deep: true }
);

// 监听 播放开关
watch(playSwitch, (newVal, oldVal) => {
    if (newVal) {
        timer = setInterval(() => {
            if (value.value < maxValue.value) {
                value.value += 0.1;
                hourArr = calculate(value)
                emits(
                    "handleNowValueChange",
                    hourArr
                );
            } else {
                value.value = 0;
                hourArr = calculate(value)
                emits(
                    "handleNowValueChange",
                    hourArr
                );
            }
        }, props.second);
    } else {
        if (timer) {
            clearInterval(timer);
        }
    }
});

// 生命周期
onBeforeUpdate(() => {
    // console.log(props.nowValue, props.yearArr, props.bgcolor, props.second);
});
</script>

<style lang="scss" scoped>
.TimeLine2-light {
    user-select: none;

    width: 100%;
    height: 70%;

    border: 2px solid slateblue;
    border-radius: 10px;

    background-color: rgba(255, 255, 255, 0.5);

    backdrop-filter: blur(10px);

    display: flex;
    justify-content: space-between;
    align-items: center;

    .LeftBox {
        width: 80%;
        height: 100;

        padding: 0px 30px;

        :deep() .el-slider__runway {
            // height: px;
            background-color: #cccccc88;
        }

        :deep() .el-slider__button {
            width: 10px;
            height: 10px;
            background-color: transparent;
            border: none;
        }

        :deep() .el-slider__stop {
            width: 1px;
            height: 6px;
            background-color: #4a0987;
            z-index: 999;
            display: block;
        }

        :deep() .el-slider__marks-text {
            color: #4a0987;
        }
    }

    .RightBox {
        width: 20%;
        height: 100;

        display: flex;
        justify-content: space-around;
        align-items: center;
    }
}

.TimeLine2-dark {
    user-select: none;

    width: 100%;
    height: 100%;

    border: 2px solid white;
    border-radius: 10px;

    background-color: rgba(41, 5, 75, .5);

    backdrop-filter: blur(10px);

    display: flex;
    justify-content: space-between;
    align-items: center;

    .LeftBox {
        width: 80%;
        height: 20;

        padding: 0px 30px;

        :deep() .el-slider__runway {
            // height: 10px;
            background-color: #fff3;
        }

        :deep() .el-slider__button {
            width: 10px;
            height: 10px;
            background-color: transparent;
            border: none;
        }

        :deep() .el-slider__stop {
            width: 1px;
            height: 12px;
            background-color: white;
            z-index: 999;
            display: block;
        }

        :deep() .el-slider__marks-text {
            color: white;
        }
    }

    .RightBox {
        width: 20%;
        height: 20;

        display: flex;
        justify-content: space-around;
        align-items: center;
    }
}
</style>