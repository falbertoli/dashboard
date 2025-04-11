<!-- File: frontend/src/components/Storage/StorageVisualization.vue -->

<template>
  <div class="storage-visualization">
    <div class="visualization-header">
      <h4>Storage Tank Visualization</h4>
      <div class="tank-stats">
        <div class="stat-item">
          <span class="stat-label">Total Tanks:</span>
          <span class="stat-value">{{ count }}</span>
        </div>
        <div class="stat-item" v-if="lastTankFill !== undefined">
          <span class="stat-label">Last Tank Fill:</span>
          <span class="stat-value">{{ $formatNumber(lastTankFill) }}%</span>
        </div>
      </div>
    </div>

    <div class="visualization-controls">
      <div class="view-options">
        <span class="view-label">Display Mode:</span>
        <div class="view-selector">
          <button @click="viewMode = 'grid'" :class="{ active: viewMode === 'grid' }" title="Grid View">
            <i class="fas fa-th"></i>
          </button>
          <button @click="viewMode = 'compact'" :class="{ active: viewMode === 'compact' }" title="Compact View">
            <i class="fas fa-bars"></i>
          </button>
        </div>
      </div>

      <div class="pagination" v-if="viewMode === 'grid' && totalPages > 1">
        <button @click="currentPage = 1" :disabled="currentPage === 1" class="page-btn">
          <i class="fas fa-angle-double-left"></i>
        </button>
        <button @click="currentPage = Math.max(1, currentPage - 1)" :disabled="currentPage === 1" class="page-btn">
          <i class="fas fa-chevron-left"></i>
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button @click="currentPage = Math.min(totalPages, currentPage + 1)" :disabled="currentPage === totalPages"
          class="page-btn">
          <i class="fas fa-chevron-right"></i>
        </button>
        <button @click="currentPage = totalPages" :disabled="currentPage === totalPages" class="page-btn">
          <i class="fas fa-angle-double-right"></i>
        </button>
      </div>
    </div>

    <!-- Grid View -->
    <div v-if="viewMode === 'grid'" class="tank-grid">
      <div v-for="i in displayedTanks" :key="i" class="tank"
        :class="{ 'last-tank': i === count && lastTankFill !== undefined }" :style="{
          width: `${diameter * 3}px`,
          height: `${length * 1.5}px`
        }" @mouseenter="showTooltip(i)" @mouseleave="hideTooltip">
        <div v-if="i === count && lastTankFill !== undefined" class="fill-level"
          :style="{ height: `${lastTankFill}%` }"></div>
        <div class="tank-label">Tank {{ i }}</div>
      </div>
    </div>

    <!-- Compact View -->
    <div v-else class="tank-compact-view">
      <div class="tanks-row">
        <div v-for="i in count" :key="i" class="tank-indicator" :class="{
          'last-tank-indicator': i === count && lastTankFill !== undefined,
          'filled-indicator': i < count
        }" @mouseenter="showTooltip(i)" @mouseleave="hideTooltip">
          <div v-if="i === count && lastTankFill !== undefined" class="indicator-fill"
            :style="{ height: `${lastTankFill}%` }"></div>
        </div>
      </div>
      <div class="tank-labels">
        <span>1</span>
        <span>{{ Math.floor(count / 2) }}</span>
        <span>{{ count }}</span>
      </div>
    </div>

    <!-- Tooltip -->
    <div v-if="tooltipVisible" class="tank-tooltip" :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }">
      <div class="tooltip-header">Tank {{ tooltipTankIndex }}</div>
      <div class="tooltip-content">
        <div class="tooltip-row">
          <span class="tooltip-label">Diameter:</span>
          <span class="tooltip-value">{{ diameter }} ft</span>
        </div>
        <div class="tooltip-row">
          <span class="tooltip-label">Length:</span>
          <span class="tooltip-value">{{ length }} ft</span>
        </div>
        <div class="tooltip-row">
          <span class="tooltip-label">Usable Volume:</span>
          <span class="tooltip-value">{{ formatNumber(usableVolumePerTank) }} ft³</span>
        </div>
        <div class="tooltip-row" v-if="tooltipTankIndex === count && lastTankFill !== undefined">
          <span class="tooltip-label">Fill Level:</span>
          <span class="tooltip-value partial-fill">{{ lastTankFill.toFixed(2) }}%</span>
        </div>
        <div class="tooltip-row" v-else>
          <span class="tooltip-label">Fill Level:</span>
          <span class="tooltip-value">100%</span>
        </div>
      </div>
    </div>

    <div class="legend">
      <div class="legend-item">
        <div class="legend-color full-tank"></div>
        <span>Full Tank</span>
      </div>
      <div class="legend-item" v-if="lastTankFill !== undefined">
        <div class="legend-color partial-tank"></div>
        <span>Partially Filled Tank ({{ lastTankFill.toFixed(2) }}%)</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  diameter: {
    type: Number,
    required: true
  },
  length: {
    type: Number,
    required: true
  },
  count: {
    type: Number,
    required: true
  },
  lastTankFill: {
    type: Number,
    default: undefined
  },
  usableVolumePerTank: {
    type: Number,
    required: true
  }
});

// View mode: grid or compact
const viewMode = ref('grid');
const currentPage = ref(1);
const tanksPerPage = 12;

// Tooltip state
const tooltipVisible = ref(false);
const tooltipX = ref(0);
const tooltipY = ref(0);
const tooltipTankIndex = ref(0);

// Calculate total pages
const totalPages = computed(() => {
  return Math.ceil(props.count / tanksPerPage);
});

// Calculate which tanks to display based on pagination
const displayedTanks = computed(() => {
  const start = (currentPage.value - 1) * tanksPerPage + 1;
  const end = Math.min(start + tanksPerPage - 1, props.count);
  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
});

// Show tooltip with tank information
const showTooltip = (tankIndex) => {
  tooltipTankIndex.value = tankIndex;
  tooltipVisible.value = true;

  // Get mouse position from event (simplified version)
  const updatePosition = (e) => {
    tooltipX.value = e.clientX + 10;
    tooltipY.value = e.clientY + 10;
  };

  document.addEventListener('mousemove', updatePosition);
  setTimeout(() => {
    document.removeEventListener('mousemove', updatePosition);
  }, 100);
};

// Hide tooltip
const hideTooltip = () => {
  tooltipVisible.value = false;
};

// Format number with commas
const formatNumber = (value) => {
  return new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 2
  }).format(value || 0);
};
</script>

<style scoped>
.storage-visualization {
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  /* margin-top: 1.5rem; */
  position: relative;
}

.visualization-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.visualization-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.view-options {
  display: flex;
  align-items: center;
  gap: 0.2rem;
}

.view-label {
  color: #aaa;
  font-size: 0.9rem;
}

.view-selector {
  display: flex;
  gap: 0.5rem;
}

.view-selector button {
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: #aaa;
  cursor: pointer;
  padding: 0.5rem;
  transition: all 0.2s;
}

.view-selector button.active {
  background-color: rgba(100, 255, 218, 0.1);
  border-color: #64ffda;
  color: #64ffda;
}

.pagination {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-btn {
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: #aaa;
  cursor: pointer;
  padding: 0.5rem;
  transition: all 0.2s;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #ddd;
  font-size: 0.9rem;
}

h4 {
  margin: 0;
  color: #ddd;
  font-size: 1.1rem;
}

.tank-stats {
  display: flex;
  gap: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-label {
  color: #aaa;
  font-size: 0.9rem;
}

.stat-value {
  color: #64ffda;
  font-weight: 600;
}

.tank-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
  justify-content: center;
}

.tank {
  background-color: rgba(100, 255, 218, 0.2);
  border: 2px solid #64ffda;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
  min-height: 40px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;
}

.tank:hover {
  transform: scale(1.05);
  z-index: 5;
}

.last-tank {
  border: 2px solid #ff9f43;
  background-color: rgba(255, 159, 67, 0.1);
}

.fill-level {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: rgba(255, 159, 67, 0.4);
  z-index: 1;
}

.tank-label {
  color: #64ffda;
  font-size: 0.8rem;
  position: relative;
  z-index: 2;
}

.last-tank .tank-label {
  color: #ff9f43;
}

/* Compact view styles */
.tank-compact-view {
  margin-bottom: 1.5rem;
}

.tanks-row {
  display: flex;
  height: 50px;
  border-radius: 4px;
  overflow: hidden;
  background-color: rgba(255, 255, 255, 0.05);
  margin-bottom: 0.5rem;
}

.tank-indicator {
  flex: 1;
  height: 100%;
  position: relative;
  cursor: pointer;
  transition: transform 0.2s;
  position: relative;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
}

.tank-indicator:last-child {
  border-right: none;
}

.tank-indicator:hover {
  transform: scaleY(1.1);
  z-index: 2;
}

.filled-indicator {
  background-color: rgba(100, 255, 218, 0.3);
}

.last-tank-indicator {
  background-color: transparent;
}

.indicator-fill {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background-color: rgba(255, 159, 67, 0.5);
}

.tank-labels {
  display: flex;
  justify-content: space-between;
  color: #aaa;
  font-size: 0.8rem;
  padding: 0 0.5rem;
}

/* Tooltip styles */
.tank-tooltip {
  position: fixed;
  background-color: #1a1e24;
  border: 1px solid rgba(100, 255, 218, 0.3);
  border-radius: 6px;
  padding: 0.75rem;
  z-index: 100;
  min-width: 200px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  pointer-events: none;
}

.tooltip-header {
  font-weight: 600;
  color: #64ffda;
  margin-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

.tooltip-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.tooltip-row {
  display: flex;
  justify-content: space-between;
}

.tooltip-label {
  color: #aaa;
  font-size: 0.9rem;
}

.tooltip-value {
  color: #ddd;
  font-weight: 600;
}

.tooltip-value.partial-fill {
  color: #ff9f43;
}

.legend {
  display: flex;
  gap: 1.5rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #aaa;
  font-size: 0.9rem;
}

.legend-color {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.full-tank {
  background-color: rgba(100, 255, 218, 0.2);
  border: 2px solid #64ffda;
}

.partial-tank {
  background-color: rgba(255, 159, 67, 0.1);
  border: 2px solid #ff9f43;
}

@media (max-width: 768px) {
  .visualization-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .tank-stats {
    width: 100%;
    justify-content: space-between;
  }

  .visualization-controls {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .pagination {
    width: 100%;
    justify-content: center;
  }

  .tank {
    min-width: 50px;
    min-height: 30px;
  }
}
</style>