<template>
    <Scene @onSceneLoad="onSceneLoad" />
    <LoadingProgress v-if="isLoading" :progress="progress" class="loading-progress" />
</template>

<script setup>
import { ref } from 'vue';
import Scene from "@/objects/Scene.vue";
import LoadingProgress from "@/components/LoadingProgress.vue";


// 通过 ref 获取 loading 屏幕的 DOM 引用
const loading = ref(null);
const isLoading = ref(true);
const progress = ref(0);

// 定义 onSceneLoad 方法
const onSceneLoad = () => {
    // loading.value.style.display = 'none'; // 隐藏 loading 屏幕
    isLoading.value = false;
};
</script>

<style scoped lang="scss">
.loading-screen {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 2;
    width: 100%;
    height: 100%;
    background-color: var(--dark);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 16px;
    font-weight: bold;

    .planet {
        width: 80px;
        height: 80px;
        overflow: hidden;
        border-radius: 50%;
        background-color: #3009e0;
        position: relative;
        box-shadow: inset -20px 0px 12px 0px #05014d;

        .cloud {
            border-radius: var(--radius);
            background-color: rgb(208, 208, 208);
            width: 30px;
            height: 10px;
            position: absolute;
            transform: translateY(-100px);
        }

        .cloud:nth-child(1) {
            top: 3px;
            animation: cloud 1500ms linear 100ms infinite;
        }

        .cloud:nth-child(2) {
            top: 28px;
            animation: cloud 1700ms linear 50ms infinite;
        }

        .cloud:nth-child(3) {
            top: 58px;
            animation: cloud 1800ms linear 200ms infinite;
        }
    }
}

@keyframes cloud {
    0% {
        transform: translateX(-50px);
    }

    100% {
        transform: translateX(90px);
    }
}

.loading-progress {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1000;
    transition: opacity 0.5s ease-out;
}

.loading-progress {
    --progress-color: #42b883;
    --jump-animation: jump 0.8s infinite alternate;
}

@keyframes jump {
    0% {
        transform: translateY(0);
    }

    100% {
        transform: translateY(-20px);
    }
}
</style>