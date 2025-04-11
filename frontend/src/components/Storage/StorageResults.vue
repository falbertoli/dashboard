<!-- File: frontend/src/components/Storage/StorageResults.vue -->

<template>
  <div class="storage-results">
    <h2>Storage Analysis Results</h2>

    <div v-if="!results" class="no-results">
      <p>No results available. Please calculate storage requirements first.</p>
    </div>

    <div v-else class="results-content">
      <!-- Summary Section -->
      <div class="summary-section">
        <h3>Summary</h3>
        <div class="summary-grid">
          <div class="summary-item">
            <div class="summary-label">Total Storage Area</div>
            <div class="summary-value">{{ $formatArea(results.footprint_total) }}</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Total Infrastructure Cost</div>
            <div class="summary-value">${{ $formatNumber(results.total_infrastructure_cost) }}</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Number of Tanks</div>
            <div class="summary-value">{{ recommendedTankCount }}</div>
            <div class="summary-detail" v-if="rawTankCount > 0">
              Raw: {{ rawTankCount.toFixed(2) }}
            </div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Total Storage Capacity</div>
            <div class="summary-value">{{ formatNumber(usableVolumePerTank * recommendedTankCount) }} ft³</div>
          </div>
        </div>
      </div>

      <!-- Tank Utilization Section -->
      <div class="utilization-section" v-if="lastTankFillPercentage > 0">
        <h3>Storage Utilization</h3>
        <div class="utilization-info">
          <div class="utilization-detail">
            <div class="detail-label">Total Hydrogen Volume:</div>
            <div class="detail-value">{{ formatNumber(totalH2Volume) }} ft³</div>
          </div>
          <div class="utilization-detail">
            <div class="detail-label">Last Tank Fill Level:</div>
            <div class="detail-value">{{ lastTankFillPercentage.toFixed(2) }}%</div>
          </div>
          <div class="utilization-detail">
            <div class="detail-label">Storage Efficiency:</div>
            <div class="detail-value">{{ formatPercentage((totalH2Volume / (usableVolumePerTank * recommendedTankCount))
              * 100) }}</div>
          </div>
          <div class="utilization-chart">
            <div class="chart-label">Tank Fill Visualization:</div>
            <div class="tanks-container">
              <div v-for="i in recommendedTankCount" :key="i" class="tank-indicator" :class="{
                'full-tank': i < recommendedTankCount,
                'partial-tank': i === recommendedTankCount
              }">
                <div v-if="i === recommendedTankCount" class="tank-fill"
                  :style="{ height: `${lastTankFillPercentage}%` }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cost Breakdown Section -->
      <div class="cost-section">
        <h3>Cost Breakdown</h3>
        <div class="cost-grid">
          <div class="cost-item">
            <div class="cost-label">Construction Cost</div>
            <div class="cost-value">${{ $formatNumber(results.construction_cost) }}</div>
            <div class="cost-percentage">{{ formatPercentage(results.construction_cost /
              results.total_infrastructure_cost * 100) }}</div>
          </div>
          <div class="cost-item">
            <div class="cost-label">Tank Cost</div>
            <div class="cost-value">${{ $formatNumber(results.insulation_cost) }}</div>
            <div class="cost-percentage">{{ formatPercentage(results.insulation_cost / results.total_infrastructure_cost
              * 100) }}</div>
          </div>
        </div>
        <div class="cost-total">
          <div class="cost-label">Total Cost</div>
          <div class="cost-value">${{ $formatNumber(results.total_infrastructure_cost) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useStorageStore } from '@/store/storageStore'

const store = useStorageStore()
const {
  results,
  tankDiameter,
  tankLength,
  recommendedTankCount,
  usableVolumePerTank,
  totalH2Volume,
  rawTankCount,
  lastTankFillPercentage
} = storeToRefs(store)

// Format number with commas
const formatNumber = (value) => {
  return new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 2
  }).format(value || 0);
}

// Format percentage
const formatPercentage = (value) => {
  return new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 1,
    minimumFractionDigits: 1
  }).format(value || 0) + '%';
}
</script>

<style scoped>
.storage-results {
  padding: 1rem 0;
}

h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #fff;
}

h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #ddd;
  font-size: 1.1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

.no-results {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  color: #aaa;
}

.results-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.summary-section,
.cost-section,
.tank-section,
.utilization-section {
  background-color: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  padding: 1.5rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.summary-item {
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
}

.summary-label {
  color: #aaa;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.summary-value {
  color: #64ffda;
  font-size: 1.2rem;
  font-weight: 600;
}

.summary-detail {
  color: #aaa;
  font-size: 0.8rem;
  margin-top: 0.5rem;
  font-style: italic;
}

.cost-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.cost-item {
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
}

.cost-label {
  color: #aaa;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.cost-value {
  color: #64ffda;
  font-size: 1.2rem;
  font-weight: 600;
}

.cost-percentage {
  color: #ddd;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.cost-total {
  padding: 1rem;
  background-color: rgba(100, 255, 218, 0.1);
  border-radius: 6px;
  border-left: 3px solid #64ffda;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cost-total .cost-label {
  font-weight: 600;
  color: #ddd;
  font-size: 1rem;
}

.cost-total .cost-value {
  font-size: 1.4rem;
}

.specs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.spec-item {
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
}

.spec-label {
  color: #aaa;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.spec-value {
  color: #ddd;
  font-size: 1.1rem;
}

/* Utilization Section Styles */
.utilization-info {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.utilization-detail {
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
}

.detail-label {
  color: #aaa;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.detail-value {
  color: #ff9f43;
  font-size: 1.1rem;
  font-weight: 600;
}

.utilization-chart {
  grid-column: 1 / -1;
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  margin-top: 1rem;
}

.chart-label {
  color: #aaa;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.tanks-container {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 8px;
}

.tank-indicator {
  width: 30px;
  height: 100px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.full-tank {
  background-color: rgba(100, 255, 218, 0.3);
  border: 1px solid #64ffda;
}

.partial-tank {
  border: 1px solid #ff9f43;
}

.tank-fill {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: rgba(255, 159, 67, 0.6);
  transition: height 0.3s ease;
}
</style>