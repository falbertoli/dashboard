<!-- File: frontend/src/components/Storage/StorageInputs.vue -->

<template>
  <div class="storage-inputs">
    <!-- Add Hydrogen Demand Information at the top -->
    <div class="hydrogen-demand-info">
      <h3>Hydrogen Demand</h3>
      <div class="info-row" v-if="totalH2Volume > 0">
        <span>Total Daily Hydrogen Demand:</span>
        <strong>{{ totalH2Volume.toFixed(2) }} ft³</strong>
      </div>
      <div class="info-alert" v-else>
        <i class="fas fa-exclamation-triangle"></i>
        <span>No hydrogen demand data available. Please calculate demand in the Hydrogen section first.</span>
      </div>
    </div>

    <div v-if="totalH2Volume > 0">
      <div class="auto-calculated-field">
        <div class="field-label">
          <span>Recommended Number of Tanks</span>
          <div class="tooltip">
            <i class="fas fa-info-circle"></i>
            <span class="tooltip-text">Automatically calculated based on hydrogen demand and tank dimensions</span>
          </div>
        </div>
        <div class="field-value">{{ recommendedTankCount }}</div>
        <div class="field-detail" v-if="rawTankCount > 0">
          <span>Raw calculation: {{ rawTankCount.toFixed(2) }} tanks</span>
        </div>
      </div>

      <!-- Add Last Tank Fill Information -->
      <div class="tank-fill-info" v-if="lastTankFillPercentage > 0">
        <div class="fill-label">Last Tank Fill Level:</div>
        <div class="fill-bar">
          <div class="fill-progress" :style="{ width: `${Math.min(lastTankFillPercentage, 100)}%` }"></div>
        </div>
        <div class="fill-percentage">{{ lastTankFillPercentage.toFixed(2) }}%</div>
      </div>

      <div class="calculated-value">
        <span>Usable Volume per Tank:</span>
        <strong>{{ usableVolumePerTank.toFixed(2) }} ft³</strong>
      </div>

      <div class="calculated-value">
        <span>Total Storage Capacity:</span>
        <strong>{{ (usableVolumePerTank * recommendedTankCount).toFixed(2) }} ft³</strong>
      </div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useStorageStore } from '@/store/storageStore'

const store = useStorageStore()
const {
  recommendedTankCount,
  usableVolumePerTank,
  totalH2Volume,
  rawTankCount,
  lastTankFillPercentage
} = storeToRefs(store)
</script>

<style scoped>
.storage-inputs {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* New styles for hydrogen demand info */
.hydrogen-demand-info {
  background-color: rgba(54, 162, 235, 0.1);
  border-radius: 6px;
  padding: 1rem;
  border-left: 3px solid #36a2eb;
}

.hydrogen-demand-info h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #ddd;
  font-size: 1.1rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-row span {
  color: #aaa;
}

.info-row strong {
  color: #36a2eb;
  font-size: 1.1rem;
}

.info-alert {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #ff9f43;
}

.info-alert i {
  font-size: 1.1rem;
}

.auto-calculated-field {
  background-color: rgba(100, 255, 218, 0.1);
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 6px;
  border-left: 3px solid #64ffda;
}

.field-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #aaa;
  margin-bottom: 5px;
}

.field-detail {
  margin-top: 8px;
  font-size: 0.85rem;
  color: #aaa;
  font-style: italic;
}

.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip i {
  color: #64ffda;
  font-size: 0.9rem;
  cursor: help;
}

.tooltip-text {
  visibility: hidden;
  width: 250px;
  background-color: #1a1e24;
  color: #ddd;
  text-align: center;
  border-radius: 6px;
  padding: 8px;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  margin-left: -125px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 0.8rem;
}

.tooltip:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}

.field-value {
  font-size: 1.2rem;
  font-weight: 600;
  color: #64ffda;
}

/* Tank Fill Styles */
.tank-fill-info {
  background-color: rgba(255, 159, 67, 0.1);
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 6px;
  border-left: 3px solid #ff9f43;
}

.fill-label {
  color: #aaa;
  margin-bottom: 8px;
}

.fill-bar {
  height: 12px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 8px;
}

.fill-progress {
  height: 100%;
  background-color: #ff9f43;
  border-radius: 6px;
  transition: width 0.3s ease;
}

.fill-percentage {
  text-align: right;
  color: #ff9f43;
  font-weight: 600;
}

.calculated-value {
  background-color: rgba(255, 255, 255, 0.05);
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.calculated-value span {
  color: #aaa;
}

.calculated-value strong {
  color: #64ffda;
  font-size: 1.1rem;
}
</style>