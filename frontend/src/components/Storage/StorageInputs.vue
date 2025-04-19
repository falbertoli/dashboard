<template>
  <div class="storage-container">
    <!-- Hydrogen Demand Panel - Always visible -->
    <section class="info-panel demand-panel">
      <div class="panel-header">
        <i class="fas fa-flask"></i>
        <h3>Hydrogen Demand</h3>
        <div class="info-tooltip" title="Total hydrogen volume required based on demand calculations">
          <i class="fas fa-info-circle"></i>
        </div>
      </div>

      <div v-if="totalH2Volume > 0" class="panel-content">
        <div class="info-card primary">
          <div class="info-label">Total Hydrogen Demand for 11 days</div>
          <div class="info-value">{{ $formatCompactNumber(totalH2Volume) }} ft³</div>
        </div>
      </div>

      <div v-else class="warning-message">
        <i class="fas fa-exclamation-triangle"></i>
        <span>No hydrogen demand data available. Please calculate demand in the Hydrogen section first.</span>
      </div>
    </section>

    <div v-if="totalH2Volume > 0" class="tabbed-content">
      <!-- Tab Navigation -->
      <div class="tab-navigation">
        <button :class="['tab-button', { active: activeTab === 'specs' }]" @click="activeTab = 'specs'">
          <i class="fas fa-cogs"></i>
          <span>Specifications</span>
        </button>
        <button :class="['tab-button', { active: activeTab === 'capacity' }]" @click="activeTab = 'capacity'">
          <i class="fas fa-database"></i>
          <span>Capacity</span>
        </button>
        <button :class="['tab-button', { active: activeTab === 'overview' }]" @click="activeTab = 'overview'">
          <i class="fas fa-chart-pie"></i>
          <span>Overview</span>
        </button>
      </div>

      <!-- Tab Content -->
      <div class="tab-content">
        <!-- Overview Tab -->
        <div v-if="activeTab === 'overview'" class="tab-pane">
          <div class="panel-grid">
            <!-- Recommended Tanks Panel -->
            <section class="info-panel recommendation-panel">
              <div class="panel-header">
                <i class="fas fa-calculator"></i>
                <h3>Recommended Storage</h3>
              </div>

              <div class="panel-content">
                <div class="recommended-value">
                  <span class="value">{{ recommendedTankCount }}</span>
                  <span class="unit">tanks</span>
                </div>

                <div class="calculation-details" v-if="rawTankCount > 0">
                  Raw calculation: {{ $formatNumber(rawTankCount) }} tanks
                </div>
              </div>
            </section>

            <!-- Tank Fill Level Panel -->
            <section class="info-panel fill-panel" v-if="lastTankFillPercentage > 0">
              <div class="panel-header">
                <i class="fas fa-fill-drip"></i>
                <h3>Last Tank Fill Level</h3>
              </div>

              <div class="panel-content">
                <div class="fill-gauge">
                  <div class="fill-indicator" :style="{ width: `${Math.min(lastTankFillPercentage, 100)}%` }"></div>
                </div>
                <div class="fill-percentage">{{ $formatNumber(lastTankFillPercentage) }}%</div>
              </div>
            </section>
          </div>
        </div>

        <!-- Specifications Tab -->
        <div v-if="activeTab === 'specs'" class="tab-pane">
          <!-- Tank Specifications Panel -->
          <section class="info-panel specs-panel">
            <div class="panel-header">
              <i class="fas fa-database"></i>
              <h3>Tank Specifications</h3>
              <div class="info-tooltip" title="Physical dimensions and characteristics of storage tanks">
                <i class="fas fa-info-circle"></i>
              </div>
            </div>

            <div class="specs-grid">
              <div class="spec-card">
                <div class="spec-icon"><i class="fas fa-circle"></i></div>
                <div class="spec-content">
                  <div class="spec-label">Tank Diameter</div>
                  <div class="spec-value">{{ tankDiameter }} ft</div>
                </div>
              </div>

              <div class="spec-card">
                <div class="spec-icon"><i class="fas fa-arrows-alt-h"></i></div>
                <div class="spec-content">
                  <div class="spec-label">Tank Length</div>
                  <div class="spec-value">{{ tankLength }} ft</div>
                </div>
              </div>

              <div class="spec-card">
                <div class="spec-icon"><i class="fas fa-snowflake"></i></div>
                <div class="spec-content">
                  <div class="spec-label">Insulation Volume</div>
                  <div class="spec-value">{{ $formatNumber(insulationVolume) }} ft³</div>
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- Capacity Tab -->
        <div v-if="activeTab === 'capacity'" class="tab-pane">
          <!-- Storage Capacity Summary -->
          <section class="info-panel summary-panel">
            <div class="panel-header">
              <i class="fas fa-chart-bar"></i>
              <h3>Storage Summary</h3>
              <div class="info-tooltip" title="Storage capacity and supply duration metrics">
                <i class="fas fa-info-circle"></i>
              </div>
            </div>

            <div class="panel-content">
              <div class="summary-grid">
                <div class="summary-item">
                  <div class="summary-label">Usable Volume per Tank</div>
                  <div class="summary-value">{{ $formatNumber(usableVolumePerTank) }} ft³</div>
                </div>

                <div class="summary-item">
                  <div class="summary-label">Days of Supply</div>
                  <div class="summary-value">11 days</div>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useStorageStore } from '@/store/storageStore'
import { ref } from 'vue'

const store = useStorageStore()
const {
  recommendedTankCount,
  usableVolumePerTank,
  totalH2Volume,
  rawTankCount,
  lastTankFillPercentage,
  tankDiameter,
  tankLength,
  insulationVolume,
  results
} = storeToRefs(store)

console.log(usableVolumePerTank.value, 'usableVolumePerTank')

// Tab management
const activeTab = ref('overview')
</script>

<style scoped>
/* Main Container */
.storage-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 100%;
  font-family: 'Inter', sans-serif;
}

/* Common Panel Styling */
.info-panel {
  border-radius: 8px;
  background-color: rgba(30, 41, 59, 0.5);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  margin-bottom: 1rem;
}

.info-panel:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background-color: rgba(30, 41, 59, 0.8);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.panel-header i {
  font-size: 1rem;
}

.panel-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #f0f0f0;
}

.panel-content {
  padding: 1rem;
}

/* Hydrogen Demand Panel */
.demand-panel .panel-header i {
  color: #36a2eb;
}

.demand-panel {
  border-left: 3px solid #36a2eb;
}

.info-card {
  padding: 1rem;
  border-radius: 6px;
  background-color: rgba(255, 255, 255, 0.05);
}

.info-card.primary {
  border-left: 3px solid #36a2eb;
}

.info-label {
  color: #aaa;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.info-value {
  color: #36a2eb;
  font-size: 1.25rem;
  font-weight: 600;
}

.warning-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  color: #ff9f43;
}

.warning-message i {
  font-size: 1.1rem;
}

/* Tab System */
.tabbed-content {
  margin-top: 0.5rem;
}

.tab-navigation {
  display: flex;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 1rem;
  overflow-x: auto;
  scrollbar-width: thin;
}

.tab-button {
  background: none;
  border: none;
  padding: 0.75rem 1.25rem;
  color: #aaa;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 2px solid transparent;
  white-space: nowrap;
}

.tab-button:hover {
  color: #ddd;
  background-color: rgba(255, 255, 255, 0.05);
}

.tab-button.active {
  color: #64ffda;
  border-bottom: 2px solid #64ffda;
}

.tab-content {
  padding: 0.5rem;
}

.tab-pane {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(5px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.panel-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 768px) {
  .panel-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Recommended Tanks Panel */
.recommendation-panel {
  border-left: 3px solid #64ffda;
}

.recommendation-panel .panel-header i {
  color: #64ffda;
}

.recommended-value {
  text-align: center;
  margin-bottom: 0.75rem;
}

.recommended-value .value {
  font-size: 2rem;
  font-weight: 700;
  color: #64ffda;
  line-height: 1;
}

.recommended-value .unit {
  font-size: 0.875rem;
  color: #aaa;
  margin-left: 0.25rem;
}

.tooltip-container {
  display: flex;
  justify-content: center;
  margin-bottom: 0.75rem;
  position: relative;
}

.tooltip-container i {
  color: #64ffda;
  cursor: help;
}

.tooltip-text {
  visibility: hidden;
  width: 220px;
  background-color: #1a1e24;
  color: #ddd;
  text-align: center;
  border-radius: 4px;
  padding: 0.5rem;
  position: absolute;
  z-index: 10;
  bottom: 125%;
  left: 50%;
  margin-left: -110px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 0.75rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.tooltip-container:hover .tooltip-text {
  visibility: visible;
  opacity: 1;
}

.calculation-details {
  text-align: center;
  color: #aaa;
  font-size: 0.75rem;
  font-style: italic;
}

/* Tank Fill Panel */
.fill-panel {
  border-left: 3px solid #ff9f43;
}

.fill-panel .panel-header i {
  color: #ff9f43;
}

.fill-gauge {
  height: 12px;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.fill-indicator {
  height: 100%;
  background: linear-gradient(90deg, #ff9f43, #ff7f50);
  border-radius: 6px;
  transition: width 0.5s ease-out;
}

.fill-percentage {
  text-align: right;
  color: #ff9f43;
  font-weight: 600;
  font-size: 1rem;
}

/* Tank Specifications Panel */
.specs-panel {
  border-left: 3px solid #64ffda;
}

.specs-panel .panel-header i {
  color: #64ffda;
}

.specs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 0.75rem;
  padding: 1rem;
}

.spec-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: transform 0.2s ease;
  border: 1px solid rgba(100, 255, 218, 0.1);
}

.spec-card:hover {
  transform: translateY(-1px);
  border-color: rgba(100, 255, 218, 0.3);
}

.spec-icon {
  color: rgba(100, 255, 218, 0.3);
  font-size: 1.25rem;
}

.spec-content {
  flex: 1;
}

.spec-label {
  color: #a0aec0;
  font-size: 0.75rem;
  margin-bottom: 0.25rem;
}

.spec-value {
  color: #64ffda;
  font-size: 1.1rem;
  font-weight: 600;
}

/* Summary Panel */
.summary-panel {
  border-left: 3px solid #a3a3ff;
}

.summary-panel .panel-header i {
  color: #a3a3ff;
}

.summary-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 0.75rem;
}

@media (min-width: 768px) {
  .summary-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
}

.summary-label {
  color: #aaa;
  font-size: 0.875rem;
}

.summary-value {
  color: #a3a3ff;
  font-weight: 600;
  font-size: 1rem;
}

/* Responsive Adjustments */
@media (max-width: 576px) {
  .tab-button {
    padding: 0.5rem 0.75rem;
  }

  .tab-button i {
    margin-right: 0;
  }

  .tab-button span {
    display: none;
  }

  .summary-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }
}

/* Tooltip Styling */
.info-tooltip {
  margin-left: 0.5rem;
  color: #aaa;
  cursor: help;
}

.info-tooltip:hover {
  color: #64ffda;
}
</style>