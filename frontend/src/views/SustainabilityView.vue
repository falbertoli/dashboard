<!-- File: frontend/src/views/SustainabilityView.vue -->

<template>
  <div class="sustainability-view">
    <div class="page-header">
      <h1>Sustainability Analysis</h1>
      <p class="description">
        Analyze the environmental impact of hydrogen adoption, including emissions reductions
        and equivalent carbon offset metrics.
      </p>
    </div>

    <div class="sustainability-content">
      <div class="card">
        <EmissionsAnalysis />
      </div>
    </div>
  </div>
</template>

<script setup>
import EmissionsAnalysis from '@/components/Sustainability/EmissionsAnalysis.vue';
</script>

<style scoped>
.sustainability-view {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 2.2rem;
  color: #282C34;
  margin-bottom: 10px;
}

.description {
  color: #aaa;
  max-width: 800px;
  line-height: 1.5;
}

.card {
  background-color: #282c34;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>