<!-- frontend>src>views>HydrogenView.vue -->
<template>
  <div class="page-view">
    <div class="page-header">
      <h1>Hydrogen Demand Analysis</h1>
      <p class="description">
        Analyze the hydrogen demand for aircraft and ground vehicles based on fleet
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

<style>
/****** Width Reactive Enhancements for HydrogenView ******/

/* Base container styling */
.page-view {
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 20px;
  box-sizing: border-box;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 2rem;
  color: #64ffda;
  margin-bottom: 10px;
}

.description {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.7);
  max-width: 800px;
  line-height: 1.5;
}

.hydrogen-content {
  width: 100%;
}

.card {
  background: rgba(22, 28, 36, 0.7);
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(100, 255, 218, 0.1);
  transition: all 0.3s ease;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .page-header h1 {
    font-size: 1.8rem;
  }

  .description {
    font-size: 1rem;
  }

  .card {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .page-view {
    padding: 0 10px;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }

  .card {
    padding: 15px;
    border-radius: 8px;
  }
}

@media (min-width: 1400px) {
  .card {
    padding: 40px;
  }
}
</style>
