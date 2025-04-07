<template>
  <div class="page-view">
    <div class="page-header">
      <h1>Hydrogen Demand Analysis</h1>
      <p class="description">
        Analyze the hydrogen demand for aircraft and ground support equipment (GSE) based on fleet
        size and operational parameters.
      </p>
    </div>

    <div class="hydrogen-content">
      <div class="card">
        <HydrogenComponent />
      </div>
    </div>
  </div>
</template>

<script setup>
import HydrogenComponent from '../components/HydrogenComponent.vue';
</script>
