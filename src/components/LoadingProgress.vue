<template>
    <transition name="fade">
        <div v-if="isLoading" class="loading-container">
            <div class="progress-bar">
                <div class="progress" :style="{ width: progress + '%' }"></div>
            </div>
            <div class="jumping-blocks">
                <div v-for="(block, index) in blocks" :key="index" class="block" :style="blockStyle(index)"></div>
            </div>
        </div>
    </transition>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
    progress: {
        type: Number,
        default: 0
    }
})

const isLoading = ref(true)
const blocks = Array(5).fill(null)

const blockStyle = (index) => ({
    animationDelay: `${index * 0.2}s`,
    transform: `scale(${0.8 + (props.progress / 100 * 0.4)})`
})

// 暴露方法供父组件调用
defineExpose({
    complete: () => {
        isLoading.value = false
    }
})
</script>

<style scoped>
.loading-container {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 9999;
}

.progress-bar {
    width: 300px;
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 40px;
}

.progress {
    height: 100%;
    background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
    transition: width 0.3s ease;
}

.jumping-blocks {
    display: flex;
    justify-content: center;
    gap: 15px;
}

.block {
    width: 20px;
    height: 20px;
    background: #4facfe;
    border-radius: 4px;
    animation: jump 0.6s ease-in-out infinite;
}

@keyframes jump {

    0%,
    100% {
        transform: translateY(0) scale(1);
    }

    50% {
        transform: translateY(-20px) scale(1.2);
    }
}

.fade-leave-active {
    transition: opacity 1s ease;
}

.fade-leave-to {
    opacity: 0;
}
</style>
