<!-- File: frontend/src/components/Storage/StorageResults.vue -->

<template>
  <div class="storage-results">
    <h2>Storage Analysis Results</h2>
    <p class="results-description">Detailed analysis of storage requirements, including tank configuration, costs, and
      spatial considerations.</p>

    <div v-if="!results" class="no-results">
      <p>No results available. Please calculate storage requirements first.</p>
    </div>

    <div v-else class="results-content">
      <!-- Summary Section -->
      <div class="summary-section">
        <h3>Summary</h3>
        <p class="section-description">Key metrics for the storage system configuration and requirements.</p>
        <div class="summary-grid">
          <div class="summary-item" title="Total ground area required for all storage tanks">
            <div class="summary-label">Total Storage Area</div>
            <div class="summary-value">{{ $formatCompactNumber(results.footprint_total) }} ft²</div>
            <div class="metric-description">Ground area required for tank installation</div>
          </div>
          <div class="summary-item" title="Total cost of storage infrastructure including construction and tanks">
            <div class="summary-label">Total Tank Infrastructure Cost</div>
            <div class="summary-value">${{ $formatCompactNumber(results.total_infrastructure_cost) }}</div>
            <div class="metric-description">Combined costs for construction and tanks</div>
          </div>
          <div class="summary-item" title="Recommended number of storage tanks">
            <div class="summary-label">Number of Tanks</div>
            <div class="summary-value">{{ recommendedTankCount }}</div>
            <div class="summary-detail" v-if="rawTankCount > 0">
              Raw: {{ rawTankCount.toFixed(2) }}
            </div>
            <div class="metric-description">Total tanks needed for storage requirements</div>
          </div>
          <div class="summary-item" title="Total volume that can be stored across all tanks">
            <div class="summary-label">Total Storage Capacity</div>
            <div class="summary-value">{{ $formatCompactNumber(usableVolumePerTank * recommendedTankCount) }} ft³</div>
            <div class="metric-description">Maximum hydrogen volume that can be stored</div>
          </div>
        </div>
      </div>

      <!-- Tank Utilization Section -->
      <div class="utilization-section" v-if="lastTankFillPercentage > 0">
        <h3>Storage Utilization</h3>
        <p class="section-description">Analysis of storage capacity usage and efficiency metrics.</p>
        <div class="utilization-info">
          <div class="utilization-detail" title="Total volume of hydrogen that needs to be stored">
            <div class="detail-label">Total Hydrogen Volume:</div>
            <div class="detail-value">{{ $formatCompactNumber(totalH2Volume) }} ft³</div>
            <div class="metric-description">Required storage volume based on demand</div>
          </div>
          <div class="utilization-detail" title="Percentage of the last tank's capacity being used">
            <div class="detail-label">Last Tank Fill Level:</div>
            <div class="detail-value">{{ $formatNumber(lastTankFillPercentage) }}%</div>
            <div class="metric-description">Utilization of the final storage tank</div>
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
        <h3>Tank Cost Breakdown</h3>
        <p class="section-description">Detailed breakdown of infrastructure costs including construction and tank
          expenses.</p>
        <div class="cost-grid">
          <div class="cost-item" title="Total cost for site preparation and construction">
            <div class="cost-label">Tank Construction Cost</div>
            <div class="cost-value">${{ $formatCompactNumber(results.construction_cost) }}</div>
            <div class="cost-percentage">{{ formatPercentage(results.construction_cost /
              results.total_infrastructure_cost * 100) }}</div>
            <div class="metric-description">Site preparation and building expenses</div>
          </div>
          <div class="cost-item" title="Total cost for tank materials and installation">
            <div class="cost-label">Tank Cost</div>
            <div class="cost-value">${{ $formatCompactNumber(results.insulation_cost) }}</div>
            <div class="cost-percentage">{{ formatPercentage(results.insulation_cost / results.total_infrastructure_cost
              * 100) }}</div>
            <div class="metric-description">Storage tank materials and installation</div>
          </div>
        </div>
        <div class="cost-total" title="Total combined cost for the entire storage system">
          <div class="cost-label">Total Tank Cost</div>
          <div class="cost-value">${{ $formatCompactNumber(results.total_infrastructure_cost) }}</div>
          <div class="metric-description">Combined infrastructure and equipment costs</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
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

.metric-description {
  color: #666;
  font-size: 0.8rem;
  margin-top: 0.25rem;
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

.cost-total .metric-description {
  color: #666;
  font-size: 0.8rem;
  margin-top: 0.5rem;
  font-style: italic;
  text-align: right;
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

.utilization-detail .metric-description {
  color: #666;
  font-size: 0.8rem;
  margin-top: 0.25rem;
  font-style: italic;
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

.results-description {
  color: #aaa;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
  line-height: 1.5;
}

.section-description {
  color: #888;
  font-size: 0.85rem;
  margin: -0.5rem 0 1rem 0;
}
</style>