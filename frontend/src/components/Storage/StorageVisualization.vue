<!-- File: frontend/src/components/Storage/StorageVisualization.vue -->

<template>
  <div class="storage-visualization">
    <div class="tank-grid">
      <div v-for="i in Math.min(count, 12)" :key="i" class="tank" :style="{
        width: `${diameter * 3}px`,
        height: `${length * 1.5}px`
      }">
        <div class="tank-label">Tank {{ i }}</div>
      </div>
      <div v-if="count > 12" class="more-tanks">
        +{{ count - 12 }} more tanks
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  diameter: {
    type: Number,
    required: true
  },
  length: {
    type: Number,
    required: true
  },
  count: {
    type: Number,
    required: true
  }
});
</script>

<style scoped>
.storage-visualization {
  padding: 1rem;
}

.tank-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.tank {
  background-color: rgba(100, 255, 218, 0.2);
  border: 2px solid #64ffda;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
  min-height: 40px;
}

.tank-label {
  color: #64ffda;
  font-size: 0.8rem;
}

.more-tanks {
  display: flex;
  align-items: center;
  color: #64ffda;
  font-weight: 600;
}
</style>