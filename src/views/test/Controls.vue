<template>
  <div class="controls">
    <div class="control-group">
      <label>太阳高度角: {{ state.elevation.toFixed(1) }}°</label>
      <input
          type="range"
          v-model.number="state.elevation"
          min="-90"
          max="90"
          step="0.1"
      >
    </div>

    <div class="control-group">
      <label>太阳方位角: {{ state.azimuth.toFixed(1) }}°</label>
      <input
          type="range"
          v-model.number="state.azimuth"
          min="-180"
          max="180"
          step="0.1"
      >
    </div>

    <div class="control-group">
      <label>大气浑浊度: {{ state.turbidity.toFixed(1) }}</label>
      <input
          type="range"
          v-model.number="state.turbidity"
          min="0"
          max="20"
          step="0.1"
      >
    </div>

    <div class="control-group">
      <label>曝光强度: {{ state.exposure.toFixed(2) }}</label>
      <input
          type="range"
          v-model.number="state.exposure"
          min="0.1"
          max="1"
          step="0.01"
      >
    </div>
  </div>
</template>

<script setup>
import { inject } from 'vue';

const state = inject('skyState', () => ({
  turbidity: 10,
  rayleigh: 3,
  mieCoefficient: 0.005,
  mieDirectionalG: 0.7,
  elevation: 2,
  azimuth: 180,
  exposure: 0.5
}));
</script>

<style scoped>
.controls {
  position: fixed;
  top: 20px;
  left: 20px;
  background: rgba(0, 0, 0, 0.7);
  padding: 15px;
  border-radius: 8px;
  color: white;
  font-family: Arial, sans-serif;
}

.control-group {
  margin: 10px 0;
}

label {
  display: block;
  margin-bottom: 5px;
  font-size: 0.9em;
}

input[type="range"] {
  width: 200px;
}
</style>