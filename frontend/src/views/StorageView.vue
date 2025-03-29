<!-- File: frontend/src/views/StorageView.vue -->

<template>
  <div class="storage-view">
    <div class="page-header">
      <h1>Hydrogen Storage Analysis</h1>
      <p class="description">
        Design and analyze hydrogen storage infrastructure based on calculated hydrogen demand.
        The number of tanks is automatically calculated based on demand and tank dimensions.
      </p>
    </div>

    <div v-if="!hydrogenStore.totalH2Demand" class="alert info">
      <i class="fas fa-info-circle"></i>
      <span>Please configure hydrogen demand in the Hydrogen section first.</span>
    </div>

    <div v-else class="storage-content">
      <div class="storage-grid">
        <!-- Left column: Configuration -->
        <div class="config-column">
          <div class="card">
            <h2>Storage Configuration</h2>
            <StorageInputs />

            <div class="actions">
              <button class="primary-button" @click="calculateStorage" :disabled="isLoading">
                <i class="fas fa-calculator"></i> Calculate
              </button>
              <button class="secondary-button" @click="resetStorage" :disabled="isLoading">
                <i class="fas fa-undo"></i> Reset
              </button>
            </div>
          </div>
        </div>

        <!-- Right column: Results -->
        <div class="results-column">
          <div v-if="isLoading" class="loading-overlay">
            <div class="spinner"></div>
            <p>Calculating storage requirements...</p>
          </div>

          <div v-else-if="storageStore.results" class="card">
            <StorageResults />
          </div>

          <div v-else class="card placeholder-card">
            <div class="placeholder-content">
              <i class="fas fa-database"></i>
              <p>Configure specifications and click "Calculate" to see results.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import { useHydrogenStore } from '@/store/hydrogenStore';
import { useStorageStore } from '@/store/storageStore';
import StorageInputs from '@/components/Storage/StorageInputs.vue';
import StorageResults from '@/components/Storage/StorageResults.vue';

const hydrogenStore = useHydrogenStore();
const storageStore = useStorageStore();
const { isLoading } = storeToRefs(storageStore);

// Calculate storage requirements
const calculateStorage = () => {
  storageStore.calculateRequirements();
};

// Reset storage calculations
const resetStorage = () => {
  storageStore.reset();
};
</script>

<style scoped>
.storage-view {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 2.2rem;
  color: #fff;
  margin-bottom: 10px;
}

.description {
  color: #aaa;
  max-width: 800px;
  line-height: 1.5;
}

.alert {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 25px;
}

.alert.info {
  background-color: rgba(54, 162, 235, 0.1);
  border-left: 4px solid rgba(54, 162, 235, 0.8);
  color: #ddd;
}

.alert i {
  margin-right: 10px;
  font-size: 1.2rem;
}

.storage-grid {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 25px;
  margin-bottom: 25px;
}

.card {
  background-color: #282c34;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.card h2 {
  font-size: 1.3rem;
  color: #eee;
  margin-top: 0;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.primary-button,
.secondary-button {
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.primary-button {
  background-color: #64ffda;
  color: #1a1e24;
  font-weight: 600;
}

.primary-button:hover:not(:disabled) {
  background-color: #73ffde;
  transform: translateY(-2px);
}

.secondary-button {
  background-color: transparent;
  border: 1px solid #64ffda;
  color: #64ffda;
}

.secondary-button:hover:not(:disabled) {
  background-color: rgba(100, 255, 218, 0.1);
}

.primary-button:disabled,
.secondary-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.placeholder-card {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px;
}

.placeholder-content {
  text-align: center;
  color: #aaa;
}

.placeholder-content i {
  font-size: 3rem;
  margin-bottom: 15px;
  color: rgba(100, 255, 218, 0.3);
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(40, 44, 52, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  z-index: 10;
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top: 4px solid #64ffda;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .storage-grid {
    grid-template-columns: 1fr;
  }
}

/* Add Font Awesome for icons */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');
</style>