<template>
  <div class="vanta-container" ref="vantaSection"></div>
  <div class="page1"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const vantaEffect = ref(null);
const vantaSection = ref(null);

const setVanta = () => {
  if (window.VANTA) {
    vantaEffect.value = VANTA.GLOBE({
      el: vantaSection.value,
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      color: 0xd1174f,
      size: 1.0,
      backgroundColor: 0x251444,
    });
  }
};

onMounted(() => {
  setVanta();

});

onBeforeUnmount(() => {
  if (vantaEffect.value) {
    vantaEffect.value.destroy();
  }
});

</script>

<style scoped>

.vanta-container {
  width: 100%;
  height: 100vh; /* 或其他合适的高度 */
  position: absolute; /* 改为绝对定位 */
  top: 0;
  left: 0;
  z-index: 1; /* 确保 Vanta.js 在底层 */
  pointer-events: none; /* 禁用 Vanta.js 的鼠标事件 */
}

.page1 {
  width: 100%;
  height: 100vh;

}
</style>