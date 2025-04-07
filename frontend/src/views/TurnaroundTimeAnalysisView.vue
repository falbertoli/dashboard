<!-- File: frontend/src/views/TurnaroundTimeAnalysis.vue -->

<template>
  <div class="page-view">
    <div class="page-header">
      <h1>Turnaround Time Analysis</h1>
      <p class="description">
        Analyze the turnaround time for aircraft and ground support equipment (GSE) based on fleet
        size and operational parameters.
      </p>
    </div>

    <div class="sustainability-content">
      <div class="card">
        <TurnaroundTimeAnalysis />
      </div>
    </div>
  </div>
</template>

<script setup>
import TurnaroundTimeAnalysis from '@/components/Economic/TurnaroundTimeAnalysis.vue';
</script>