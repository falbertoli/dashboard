<!-- File: frontend/src/views/SustainabilityView.vue -->

<template>
  <div class="page-view">
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