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
              <button class="primary-button" @click="calculateStorage" :disabled="!hydrogenStore.totalH2Demand">
                <i class="fas fa-calculator"></i> Calculate
              </button>
              <button class="secondary-button" @click="resetStorage" :disabled="!hydrogenStore.totalH2Demand">
                <i class="fas fa-undo"></i> Reset
              </button>
            </div>
          </div>

          <div v-if="storageStore.results && storageStore.totalH2Volume > 0" class="card visualization-card">
            <StorageVisualization :diameter="storageStore.tankDiameter" :length="storageStore.tankLength"
              :count="storageStore.recommendedTankCount" :lastTankFill="storageStore.lastTankFillPercentage"
              :usableVolumePerTank="storageStore.usableVolumePerTank" />
          </div>
        </div>

        <!-- Right column: Results -->
        <div class="results-column">
          <div v-if="isLoading" class="loading-message">
            <div class="spinner"></div>
            <p>Calculating storage requirements...</p>
          </div>

          <div v-else-if="storageStore.results" class="card">
            <div class="data-consistency-indicator">
              <div class="calculation-timestamp" v-if="storageStore.lastCalculationTime">
                <i class="fas fa-clock"></i>
                <span>Last calculated: {{ formatTimestamp(storageStore.lastCalculationTime) }}</span>
              </div>
              <div class="indicator" :class="{ 'consistent': isDataConsistent, 'inconsistent': !isDataConsistent }">
                <i :class="isDataConsistent ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle'"></i>
                <span>Data {{ isDataConsistent ? 'is consistent' : 'has changed' }}</span>
              </div>
            </div>
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
import { computed, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useHydrogenStore } from '@/store/hydrogenStore';
import { useStorageStore } from '@/store/storageStore';
import StorageInputs from '@/components/Storage/StorageInputs.vue';
import StorageResults from '@/components/Storage/StorageResults.vue';
import StorageVisualization from '@/components/Storage/StorageVisualization.vue';

const hydrogenStore = useHydrogenStore();
const storageStore = useStorageStore();
const { isLoading } = storeToRefs(storageStore);

// Calculate storage requirements
const calculateStorage = () => {
  storageStore.calculateRequirements();
  storageStore.lastCalculationTime = new Date();
};

// Reset storage calculations
const resetStorage = () => {
  storageStore.reset();
};

// Format timestamp helper
const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'Never';
  const date = new Date(timestamp);
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
};

// Check if data is consistent
const isDataConsistent = computed(() => {
  if (!storageStore.results || !storageStore.lastParams) return true;

  const currentTotalH2Demand = parseFloat(hydrogenStore.totalH2Demand || 0);
  return currentTotalH2Demand === storageStore.lastParams.totalH2Demand;
});

// Check for data consistency on component mount
onMounted(() => {
  if (storageStore.results && storageStore.lastParams) {
    const currentTotalH2Demand = parseFloat(hydrogenStore.totalH2Demand || 0);
    if (currentTotalH2Demand !== storageStore.lastParams.totalH2Demand) {
      storageStore.reset();
    }
  }
});
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
  color: #64ffda;
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

.visualization-card {
  margin-top: 35px;
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
  position: relative;
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

.loading-message {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
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

.data-consistency-indicator {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  padding: 12px 15px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: #ddd;
}

.calculation-timestamp {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  color: #aaa;
  margin-right: auto;
}

.calculation-timestamp i {
  color: #64ffda;
  margin-right: 8px;
}

.indicator {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.9rem;
  background-color: rgba(255, 255, 255, 0.03);
}

.indicator i {
  margin-right: 8px;
}

.indicator.consistent {
  color: #64ffda;
}

.indicator.consistent i {
  color: #64ffda;
}

.indicator.inconsistent {
  color: #ff9800;
}

.indicator.inconsistent i {
  color: #ff9800;
}

/* Responsive adjustments */
@media (max-width: 1024px) {
  .storage-grid {
    grid-template-columns: 1fr;
  }
}
</style>