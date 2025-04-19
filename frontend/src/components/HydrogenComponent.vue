<!-- File: frontend/src/components/HydrogenComponent.vue -->

<template>
  <div class="hydrogen-dashboard">

    <!-- Flight Attendant Tooltip Component -->
    <div class="flight-attendant-tooltip" v-if="showTooltip">
      <div class="attendant">
        <div class="attendant-head"></div>
        <div class="attendant-body"></div>
      </div>
      <div class="speech-bubble">
        <p>{{ tooltipMessage }}</p>
        <button class="close-tooltip" @click="hideTooltip">×</button>
      </div>
    </div>
    <div class="dashboard-header">
      <div class="header-left">
        <h2><i class="fas fa-plane-departure animated-hover"></i> <span class="airport-transition-hub-text">Transition
            Hub
          </span> </h2>
        <div class="boarding-pass">
          <span class="boarding-text">GREEN FLIGHT</span>
          <span class="flight-number">H2-2025</span>
        </div>
      </div>
      <div class="airport-status">
        <span class="status-dot"></span>
        <span class="status-text">{{ statusMessage || 'Transition In Progress' }}</span>
        <button class="help-button"
          @click="showTooltipMessage('Welcome to the Hydrogen Airport Transition Hub! Adjust the parameters to see how hydrogen can transform airport operations.')">
          <i class="fas fa-info-circle"></i>
        </button>
      </div>
    </div>

    <!-- Input Parameters Section -->
    <div class="parameters-section">
      <h3>
        <i class="fas fa-clipboard-check"></i> Flight Parameters
        <div class="luggage-tag"
          @click="showTooltipMessage('Set these parameters to calculate hydrogen demand for your airport.')">
          <span class="tag-hole"></span>
          <span class="tag-text">HELP</span>
        </div>
      </h3>

      <!-- Fleet Percentage Input -->
      <div class="form-group">
        <div class="input-with-help">
          <Slider label="Fleet Percentage:" id="fleet-percentage" :min="0" :max="100" :step="1"
            v-model="fleetPercentage" unit="%" />
          <div class="help-icon"
            @click="showTooltipMessage('Adjust the percentage of fleet to transition to hydrogen power.')">
            <i class="fas fa-tags"></i>
          </div>
        </div>
      </div>

      <!-- Year Selection with Help Icon -->
      <div class="form-group">
        <div class="input-with-help">
          <Dropdown label="Select End Year:" id="year-selection" :options="yearOptions" v-model="year" />
          <div class="help-icon"
            @click="showTooltipMessage('Select the target year for your hydrogen transition plan.')">
            <i class="fas fa-tags"></i>
          </div>
        </div>
      </div>

      <!-- GSE Selection with Help Icon -->
      <div class="form-group">
        <div class="input-with-help">
          <CheckboxGroup :options="gseOptionsFormatted" v-model="gseList" />
          <div class="help-icon"
            @click="showTooltipMessage('Select which ground vehicles to transition to hydrogen power.')">
            <i class="fas fa-tags"></i>
          </div>
        </div>
      </div>
    </div>

    <!-- Results Section -->
    <div class="results-container">
      <!-- Tabs -->
      <div class="tabs">
        <button :class="['tab-button', { active: activeTab === 'demand' }]" @click="activeTab = 'demand'">
          <i class="fas fa-chart-line"></i> Demand Details
        </button>
        <button :class="['tab-button', { active: activeTab === 'chart' }]" @click="activeTab = 'chart'">
          <i class="fas fa-chart-bar"></i> Charts
        </button>
      </div>

      <!-- Demand Details Tab -->
      <div v-show="activeTab === 'demand'" class="demand-grid">
        <!-- Aircraft Hydrogen Demand -->
        <div v-if="aircraftH2Demand" class="demand-section">
          <h3><i class="fas fa-plane"></i> Aircraft Hydrogen Demand</h3>
          <div class="metric-card">
            <div class="metric">
              <span class="metric-label">Daily Demand:</span>
              <span class="metric-value">{{ $formatNumberDecimals(aircraftH2Demand.daily_h2_demand_ft3) }} ft3</span>
            </div>
            <div class="metric">
              <span class="metric-label">Projected Fuel Weight:</span>
              <span class="metric-value">{{ $formatCompactNumber(aircraftH2Demand.projected_fuel_weight_lb) }} lb</span>
            </div>
          </div>
        </div>

        <!-- GSE Hydrogen Demand -->
        <div v-if="gseH2Demand" class="demand-section">
          <h3><i class="fas fa-truck"></i> Ground Vehicles Hydrogen Demand</h3>
          <div class="metric-card">
            <div class="metric">
              <span class="metric-label">Daily Demand:</span>
              <span class="metric-value">{{ $formatNumberDecimals(gseH2Demand.daily_h2_demand_ft3) }}
                ft3</span>
            </div>
            <div class="metric">
              <span class="metric-label">Total Diesel Used:</span>
              <span class="metric-value">{{ $formatNumber(gseH2Demand.total_diesel_used_lb) }} lb</span>
            </div>
            <div class="metric">
              <span class="metric-label">Total Gasoline Used:</span>
              <span class="metric-value">{{ $formatNumber(gseH2Demand.total_gasoline_used_lb) }} lb</span>
            </div>
          </div>
        </div>

        <!-- Total Hydrogen Demand -->
        <div v-if="gseH2Demand && store.totalH2Demand" class="demand-section total-demand span-full">
          <h3><i class="fas fa-tachometer-alt"></i> Total Hydrogen Demand</h3>
          <div class="metric-card highlight">
            <div class="metric">
              <span class="metric-label">Daily Demand:</span>
              <span class="metric-value">{{ $formatNumberDecimals(store.totalH2Demand) }} ft3</span>
            </div>
          </div>
        </div>
        <!-- Inside demand-grid, before the closing div -->
        <div class="runway-animation">
          <div class="takeoff-runway">
            <div class="runway-lights"></div>
          </div>
          <div class="airplane" :class="{ 'takeoff': calculateTakeoffStatus }">
            <div class="airplane-body"></div>
            <div class="airplane-tail"></div>
            <div class="airplane-wing"></div>
            <div class="hydrogen-trail">
              <span class="h2-molecule">H₂</span>
              <span class="h2-molecule">H₂</span>
              <span class="h2-molecule">H₂</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Tab -->
      <div v-show="activeTab === 'chart'" class="chart-tab">
        <div class="floating-bubbles">
          <div class="bubble-container">
            <div class="h2-bubble bubble-1">H₂</div>
            <div class="h2-bubble bubble-2">H₂</div>
            <div class="h2-bubble bubble-3">H₂</div>
            <div class="h2-bubble bubble-4">H₂</div>
            <div class="h2-bubble bubble-5">H₂</div>
          </div>
        </div>
        <div class="charts-container">
          <div class="chart-wrapper">
            <h3><i class="fas fa-chart-bar"></i> Hydrogen Demand (Log Scale)</h3>
            <p class="chart-explanation">Logarithmic scale comparison showing the vast difference between aircraft and
              ground vehicles hydrogen demands</p>
            <div class="chart-container">
              <ChartComponent chart-id="hydrogen-demand-log" chart-type="bar" :chart-data="hydrogenDemandData"
                :chart-options="hydrogenDemandLogOptions" />
            </div>
          </div>
          <div class="chart-wrapper">
            <h3><i class="fas fa-chart-pie"></i> Demand Distribution (%)</h3>
            <p class="chart-explanation">Proportional distribution of hydrogen demand between aircraft and ground
              vehicles</p>
            <div class="chart-container">
              <ChartComponent chart-id="hydrogen-demand-pie" chart-type="doughnut" :chart-data="hydrogenDemandPieData"
                :chart-options="hydrogenDemandPieOptions" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error-container">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup>
import Slider from '../components/Slider.vue';
import Dropdown from '../components/Dropdown.vue';
import CheckboxGroup from '../components/CheckboxGroup.vue';
import ChartComponent from '../components/ChartComponent.vue';
import { computed, ref, onMounted, watch, onUnmounted } from "vue";
import { useHydrogenStore } from "../store/hydrogenStore";
import { fetchGseOptions } from "../utils/api.js";
import { getCurrentInstance } from 'vue';

const instance = getCurrentInstance();
const { $formatNumber, $formatCompactNumber, $formatNumberDecimals } = instance.appContext.config.globalProperties;

const store = useHydrogenStore();
const fleetPercentage = computed({
  get: () => store.fleetPercentage,
  set: (value) => {
    console.log(`HydrogenComponent: Setting fleetPercentage in store to ${value}`);
    store.setFleetPercentage(value);
  }
});
const year = computed({
  get: () => store.year,
  set: (value) => {
    console.log(`HydrogenComponent: Setting year in store to ${value}`);
    store.setYear(value);
  }
});
const aircraftH2Demand = computed(() => store.aircraftH2Demand);
const gseH2Demand = computed(() => store.gseH2Demand);

const gseOptions = ref([]); // Store the fetched GSE options
const gseList = computed({
  get: () => store.gseList,
  set: (value) => {
    console.log(`HydrogenComponent: Setting gseList in store to ${value}`);
    store.setGseList(value);
  }
});
const errorMessage = ref("");

const years = ref(Array.from({ length: 2050 - 2023 + 1 }, (_, i) => i + 2023));

// Format years array for Dropdown component
const yearOptions = computed(() => {
  return years.value.map(year => ({ value: year, text: String(year) }));
});

// Format gseOptions for CheckboxGroup component
const gseOptionsFormatted = computed(() => {
  return gseOptions.value.map(gse => ({ value: gse, text: gse }));
});

// Chart Data
const hydrogenDemandData = computed(() => {
  return {
    labels: ['Aircraft', 'Ground Vehicles'],
    datasets: [{
      label: 'Daily Hydrogen Demand (ft³)',
      data: [
        store.aircraftH2Demand?.daily_h2_demand_ft3 || 0,
        store.gseH2Demand?.daily_h2_demand_ft3 || 0
      ],
      backgroundColor: [
        'rgba(100, 255, 218, 0.7)',
        'rgba(255, 99, 132, 0.7)'
      ],
      borderColor: [
        'rgba(100, 255, 218, 1)',
        'rgba(255, 99, 132, 1)'
      ],
      borderWidth: 2,
      borderRadius: 5,
    }]
  };
});

const hydrogenDemandPieData = computed(() => {
  const aircraftDemand = store.aircraftH2Demand?.daily_h2_demand_ft3 || 0;
  const gseDemand = store.gseH2Demand?.daily_h2_demand_ft3 || 0;
  const total = aircraftDemand + gseDemand;

  return {
    labels: ['Aircraft', 'Ground Vehicles'],
    datasets: [{
      data: [aircraftDemand, gseDemand],
      backgroundColor: [
        'rgba(100, 255, 218, 0.7)',
        'rgba(255, 99, 132, 0.7)'
      ],
      borderColor: [
        'rgba(100, 255, 218, 1)',
        'rgba(255, 99, 132, 1)'
      ],
      borderWidth: 2,
    }]
  };
});

// Chart Options
const hydrogenDemandLogOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#64ffda',
      bodyColor: '#fff',
      callbacks: {
        label: (context) => `${$formatCompactNumber(context.raw.toFixed(0)).toLocaleString()} ft³`
      }
    }
  },
  scales: {
    y: {
      type: 'logarithmic',
      grid: {
        color: 'rgba(255, 255, 255, 0.1)'
      },
      ticks: {
        color: '#aaa',
        callback: (value) => $formatCompactNumber(value).toLocaleString() + ' ft³'
      }
    },
    x: {
      grid: { display: false },
      ticks: { color: '#aaa' }
    }
  }
}));

const hydrogenDemandPieOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: '#aaa', // Changed to match the log chart color
        font: {
          size: 12,
          color: '#64ffda'
        },
        padding: 20,
        generateLabels: (chart) => {
          const data = chart.data;
          const total = data.datasets[0].data.reduce((a, b) => a + b, 0);
          return data.labels.map((label, i) => ({
            text: `${label} (${((data.datasets[0].data[i] / total) * 100).toFixed(0)}%)`,
            fillStyle: data.datasets[0].backgroundColor[i],
            strokeStyle: data.datasets[0].borderColor[i],
            fontColor: '#aaa',
            lineWidth: 1,
            hidden: false,
          }));
        }
      }
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleColor: '#64ffda',
      bodyColor: '#fff',
      callbacks: {
        label: (context) => {
          const value = context.raw;
          const total = context.dataset.data.reduce((a, b) => a + b, 0);
          const percentage = ((value / total) * 100).toFixed(0);
          return [
            `Demand: ${$formatCompactNumber(value.toFixed(0))} ft³`,
            `Percentage: ${percentage}%`
          ];
        }
      }
    }
  }
}));

const activeTab = ref('demand');

watch(fleetPercentage, (newFleetPercentage) => {
  console.log('Setting fleetPercentage in store:', newFleetPercentage);
  store.setFleetPercentage(newFleetPercentage);
});

watch(year, (newYear) => {
  store.setYear(newYear);
});

onMounted(async () => {
  try {
    console.log("🚀 Fetching GSE options...");
    const response = await fetchGseOptions();
    console.log("✅ GSE Options Loaded:", response);

    gseOptions.value = response.data; // ✅ Ensure correct data assignment
    await store.loadAircraftH2Demand();
    await store.loadGSEH2Demand();
  } catch (error) {
    console.error("❌ Error loading HydrogenComponent:", error);
    errorMessage.value = "Error loading data. Please check backend connection.";
  }
});

// Tooltip state management
const showTooltip = ref(false);
const tooltipMessage = ref('');
const tooltipTimeout = ref(null);

// Helper methods for tooltips
// Helper methods for tooltips with improved behavior
function showTooltipMessage(message) {
  // Clear any existing timeout
  if (tooltipTimeout.value) {
    clearTimeout(tooltipTimeout.value);
  }

  tooltipMessage.value = message;
  showTooltip.value = true;

  // Auto-hide tooltip after 8 seconds
  tooltipTimeout.value = setTimeout(() => {
    hideTooltipWithAnimation();
  }, 8000);
}

function hideTooltipWithAnimation() {
  const tooltipElement = document.querySelector('.flight-attendant-tooltip');
  if (tooltipElement) {
    tooltipElement.style.opacity = '0';
    tooltipElement.style.transform = 'translateY(20px) scale(0.95)';

    setTimeout(() => {
      showTooltip.value = false;
      if (tooltipElement) {
        tooltipElement.style.opacity = '';
        tooltipElement.style.transform = '';
      }
    }, 300);
  } else {
    showTooltip.value = false;
  }
}

function hideTooltip() {
  hideTooltipWithAnimation();
  if (tooltipTimeout.value) {
    clearTimeout(tooltipTimeout.value);
  }
}

// Status message based on fleet percentage
const statusMessage = computed(() => {
  if (fleetPercentage.value === 0) return 'Ready for Hydrogen Transition';
  if (fleetPercentage.value < 25) return 'Initial Transition Phase';
  if (fleetPercentage.value < 50) return 'Transition In Progress';
  if (fleetPercentage.value < 75) return 'Advanced Transition';
  if (fleetPercentage.value === 100) return 'Complete Transition';
  return 'Near-Complete Transition';
});

// For airplane animation
const calculateTakeoffStatus = computed(() => {
  return fleetPercentage.value > 30;
});

// Show a welcome tooltip when component is mounted
onMounted(async () => {
  try {
    console.log("🚀 Fetching GSE options...");
    const response = await fetchGseOptions();
    console.log("✅ GSE Options Loaded:", response);

    gseOptions.value = response.data;
    await store.loadAircraftH2Demand();
    await store.loadGSEH2Demand();

    // Show welcome tooltip after a short delay
    setTimeout(() => {
      showTooltipMessage('Welcome to the Hydrogen Airport Transition Hub! Adjust the parameters to see how hydrogen can transform your airport operations.');
    }, 1000);
  } catch (error) {
    console.error("❌ Error loading HydrogenComponent:", error);
    errorMessage.value = "Error loading data. Please check backend connection.";
  }
});

// Clean up timeout when component is unmounted
onUnmounted(() => {
  if (tooltipTimeout.value) {
    clearTimeout(tooltipTimeout.value);
  }
});
</script>

<style scoped>
/* Global & Utility Styles */
h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #64ffda;
  font-size: 1.5rem;
  font-weight: 600;
}

.airport-transition-hub-text {
  padding-left: 10px;
}

h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #ddd;
  font-size: 1.1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

/* Form Elements */
.parameters-section {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 25px;
}

.form-group {
  margin-bottom: 20px;
}

.gse-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.gse-actions {
  display: flex;
  gap: 8px;
}

.action-button {
  background-color: rgba(255, 255, 255, 0.05);
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  color: #aaa;
  cursor: pointer;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}

.action-button:hover {
  background-color: rgba(100, 255, 218, 0.1);
  color: #64ffda;
}

.action-button i {
  font-size: 0.8rem;
}

/* Results Container */
.results-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

/* Tabs Styling */
.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.tab-button {
  background-color: rgba(255, 255, 255, 0.05);
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  color: #aaa;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tab-button.active {
  background-color: rgba(100, 255, 218, 0.1);
  color: #64ffda;
}

.tab-button i {
  margin-right: 8px;
}

/* Demand Grid Layout */
.demand-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.span-full {
  grid-column: 1 / -1;
}

/* Chart Tab */
.chart-tab {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
}

.charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.chart-wrapper {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  min-height: 450px;
}

.chart-wrapper:hover {
  background-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.chart-explanation {
  color: #aaa;
  font-size: 0.9rem;
  margin: 0 0 15px 0;
  font-style: italic;
}

.chart-container {
  flex: 1;
  min-height: 350px;
}

/* Demand Sections */
.demand-section {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
}

.metric-card {
  background-color: rgba(255, 255, 255, 0.03);
  border-radius: 6px;
  padding: 15px;
}

.metric {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.metric:last-child {
  margin-bottom: 0;
}

.metric-label {
  color: #aaa;
  font-size: 0.9rem;
}

.metric-value {
  color: #64ffda;
  font-weight: 600;
}

/* Total Demand Highlight */
.total-demand .metric-card.highlight {
  background-color: rgba(100, 255, 218, 0.1);
  border-left: 4px solid #64ffda;
}

/* Chart Styles */
.chart-wrapper {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  min-height: 450px;
}

.chart-wrapper:hover {
  background-color: rgba(255, 255, 255, 0.08);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.chart-explanation {
  color: #aaa;
  font-size: 0.9rem;
  margin: 0 0 15px 0;
  font-style: italic;
}

.chart-container {
  flex: 1;
  min-height: 350px;
}

/* Error Container */
.error-container {
  border-left: 4px solid #e74c3c;
  color: #e74c3c;
  background-color: rgba(255, 99, 132, 0.1);
  padding: 15px;
  border-radius: 6px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Icon Styling */
h2 i,
h3 i {
  margin-right: 8px;
  width: 16px;
  text-align: center;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .metric {
    flex-direction: column;
    gap: 5px;
  }

  .metric-value {
    text-align: right;
  }

  .demand-grid {
    grid-template-columns: 1fr;
  }

  .charts-container {
    grid-template-columns: 1fr;
  }
}

/****** Width Reactive Enhancements ******/

/* Base container responsiveness */
div {
  max-width: 100%;
}

/* More responsive form elements */
.parameters-section {
  display: flex;
  flex-direction: column;
  width: 100%;
  box-sizing: border-box;
}

/* Improved responsive tabs */
@media (max-width: 500px) {
  .tabs {
    flex-direction: column;
    width: 100%;
  }

  .tab-button {
    width: 100%;
    text-align: center;
  }
}

/* Enhanced charts responsiveness */
.chart-wrapper {
  width: 100%;
  box-sizing: border-box;
}

/* Better responsive demand grid for medium screens */
@media (min-width: 769px) and (max-width: 1100px) {
  .charts-container {
    grid-template-columns: 1fr;
  }

  .chart-wrapper {
    min-height: 400px;
  }

  .chart-container {
    min-height: 300px;
  }
}

/* Small screen adjustments */
@media (max-width: 480px) {
  .gse-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .gse-actions {
    width: 100%;
    justify-content: space-between;
  }

  .action-button {
    flex: 1;
    justify-content: center;
  }

  .chart-wrapper {
    padding: 15px;
    min-height: 350px;
  }

  .chart-container {
    min-height: 250px;
  }
}

/* Large screen improvements */
@media (min-width: 1400px) {
  .demand-grid {
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  }

  .charts-container {
    gap: 30px;
  }

  .chart-wrapper {
    min-height: 500px;
  }

  .chart-container {
    min-height: 400px;
  }
}

.hydrogen-dashboard {
  background-color: #1a1d24;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  border: 1px solid #333;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid rgba(100, 255, 218, 0.2);
}

.animated-spin {
  display: inline-block;
  animation: spin 8s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.airport-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 12px;
  height: 12px;
  background-color: #64ffda;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

.status-text {
  font-size: 0.9rem;
  color: #64ffda;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(100, 255, 218, 0.7);
  }

  70% {
    box-shadow: 0 0 0 10px rgba(100, 255, 218, 0);
  }

  100% {
    box-shadow: 0 0 0 0 rgba(100, 255, 218, 0);
  }
}

/* Enhanced tabs styling */
.tabs {
  border-radius: 8px;
  overflow: hidden;
  background-color: rgba(0, 0, 0, 0.2);
  padding: 3px;
}

.tab-button {
  border-radius: 6px;
  padding: 12px 20px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.tab-button i {
  transition: transform 0.3s ease;
}

.tab-button:hover i {
  transform: translateY(-2px);
}

.tab-button.active {
  background: linear-gradient(135deg, rgba(100, 255, 218, 0.15), rgba(100, 255, 218, 0.05));
  box-shadow: 0 4px 12px rgba(100, 255, 218, 0.1);
}

/* Enhanced dashboard header */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid rgba(100, 255, 218, 0.2);
  background-color: rgba(18, 21, 30, 0.8);
  border-radius: 10px;
  padding: 15px 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.header-left {
  display: flex;
  flex-direction: column;
}

.animated-hover {
  transition: transform 0.3s ease;
}

.animated-hover:hover {
  transform: translateY(-2px) rotate(-10deg);
}

.boarding-pass {
  background: linear-gradient(135deg, #64ffda, #43c6ac);
  color: #12151e;
  padding: 2px 10px;
  border-radius: 5px;
  font-size: 0.7rem;
  font-weight: bold;
  display: inline-flex;
  gap: 5px;
  align-items: center;
  margin-top: 5px;
  position: relative;
  width: fit-content;
  box-shadow: 0 0 10px rgba(100, 255, 218, 0.5);
}

.boarding-pass::before {
  content: "";
  position: absolute;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background-color: #12151e;
  top: 50%;
  left: -7px;
  transform: translateY(-50%);
}

.boarding-text {
  letter-spacing: 1px;
}

.flight-number {
  background-color: rgba(0, 0, 0, 0.2);
  padding: 1px 5px;
  border-radius: 3px;
}

/* Help button and tooltip */
.help-button {
  background: none;
  border: none;
  color: #64ffda;
  cursor: pointer;
  margin-left: 10px;
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.help-button:hover {
  transform: scale(1.2);
}

/* Improved Flight Attendant Tooltip */
.flight-attendant-tooltip {
  position: fixed;
  bottom: 30px;
  right: 30px;
  display: flex;
  align-items: flex-end;
  z-index: 1000;
  animation: slideIn 0.5s ease;
  max-width: 350px;
  /* Control maximum width */
  transform-origin: bottom right;
  filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.3));
  transition: all 0.3s ease;
}

.flight-attendant-tooltip:hover {
  transform: scale(1.03);
}

@keyframes slideIn {
  from {
    transform: translateY(50px) scale(0.9);
    opacity: 0;
  }

  to {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}

.attendant {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  margin-right: -5px;
  /* Slight overlap with speech bubble */
  z-index: 2;
}

.attendant-head {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ffcebf, #f5b39e);
  position: relative;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.attendant-head::before,
.attendant-head::after {
  content: "";
  position: absolute;
  background-color: #333;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  top: 10px;
}

.attendant-head::before {
  left: 7px;
}

.attendant-head::after {
  right: 7px;
}

.attendant-body {
  width: 36px;
  height: 45px;
  background: linear-gradient(180deg, #64ffda, #43c6ac);
  border-radius: 10px 10px 0 0;
  position: relative;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.2);
}

.attendant-body::after {
  content: "";
  position: absolute;
  width: 18px;
  height: 9px;
  background-color: #fff;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  border-radius: 5px;
}

.speech-bubble {
  max-width: 280px;
  padding: 16px;
  background-color: rgba(30, 35, 45, 0.95);
  border-radius: 16px;
  border: 2px solid rgba(100, 255, 218, 0.3);
  margin-left: 10px;
  position: relative;
  color: #e6e6e6;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3),
    inset 0 0 20px rgba(100, 255, 218, 0.05);
  z-index: 1;
}

.speech-bubble::before {
  content: "";
  position: absolute;
  left: -10px;
  bottom: 20px;
  width: 0;
  height: 0;
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
  border-right: 10px solid rgba(100, 255, 218, 0.3);
  z-index: 0;
}

.speech-bubble::after {
  content: "";
  position: absolute;
  left: -7px;
  bottom: 22px;
  width: 0;
  height: 0;
  border-top: 8px solid transparent;
  border-bottom: 8px solid transparent;
  border-right: 8px solid rgba(30, 35, 45, 0.95);
  z-index: 1;
}

.speech-bubble p {
  margin: 0 0 10px 0;
  font-size: 0.95rem;
  line-height: 1.5;
  color: #fff;
}

.close-tooltip {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(100, 255, 218, 0.1);
  border: 1px solid rgba(100, 255, 218, 0.3);
  border-radius: 50%;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64ffda;
  cursor: pointer;
  font-size: 0.75rem;
  transition: all 0.2s ease;
}

.close-tooltip:hover {
  background: rgba(100, 255, 218, 0.2);
  transform: rotate(90deg);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .flight-attendant-tooltip {
    bottom: 15px;
    right: 15px;
    max-width: 85%;
  }

  .attendant-head {
    width: 24px;
    height: 24px;
  }

  .attendant-body {
    width: 32px;
    height: 40px;
  }

  .speech-bubble {
    padding: 12px;
    font-size: 0.9rem;
  }
}

/* Improved Slider to use more horizontal space */
.form-group {
  margin-bottom: 20px;
  width: 100%;
}

.input-with-help {
  display: flex;
  align-items: center;
  width: 100%;
}

/* Make slider take full width minus the help icon width */
.input-with-help> :first-child {
  flex: 1;
  width: calc(100% - 40px);
}

.help-icon {
  flex: 0 0 30px;
  margin-left: 10px;
}

/* Ensure the slider container itself uses all available width */
:deep(.slider-container) {
  width: 100%;
}

:deep(.slider-input) {
  width: 100%;
}

/* Luggage Tag Help Icons */
.luggage-tag {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(135deg, #64ffda, #43c6ac);
  padding: 2px 10px 2px 20px;
  border-radius: 0 15px 15px 0;
  margin-left: 15px;
  position: relative;
  cursor: pointer;
  font-size: 0.7rem;
  color: #12151e;
  font-weight: bold;
  box-shadow: 0 3px 10px rgba(100, 255, 218, 0.3);
  transition: transform 0.3s ease;
}

.luggage-tag:hover {
  transform: scale(1.1);
}

.tag-hole {
  position: absolute;
  left: 7px;
  top: 50%;
  transform: translateY(-50%);
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #12151e;
}

.tag-text {
  letter-spacing: 1px;
}

.input-with-help {
  display: flex;
  align-items: center;
  gap: 10px;
}

.help-icon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(100, 255, 218, 0.1), rgba(100, 255, 218, 0.05));
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: 1px solid rgba(100, 255, 218, 0.3);
  color: #64ffda;
  transition: all 0.3s ease;
}

.help-icon:hover {
  transform: rotate(15deg);
  background: rgba(100, 255, 218, 0.2);
}

/* Runway Animation */
.runway-animation {
  grid-column: 1 / -1;
  height: 120px;
  position: relative;
  margin-top: 30px;
  overflow: hidden;
  background-color: rgba(18, 21, 30, 0.8);
  border-radius: 10px;
}

.takeoff-runway {
  position: absolute;
  bottom: 20px;
  left: 0;
  width: 100%;
  height: 30px;
  background-color: #2c3040;
  z-index: 1;
}

.runway-lights {
  position: absolute;
  top: 50%;
  left: 0;
  width: 100%;
  height: 2px;
  background: repeating-linear-gradient(90deg, #64ffda, #64ffda 20px, transparent 20px, transparent 40px);
  transform: translateY(-50%);
  animation: runwayLights 1s infinite linear;
}

@keyframes runwayLights {
  from {
    background-position: 0 0;
  }

  to {
    background-position: 40px 0;
  }
}

.airplane {
  position: absolute;
  bottom: 35px;
  left: 10%;
  z-index: 2;
  transform: translateX(0);
  transition: all 2s cubic-bezier(0.42, 0, 0.58, 1);
}

.airplane.takeoff {
  transform: translateX(300px) translateY(-30px) rotate(-10deg);
}

.airplane-body {
  width: 60px;
  height: 20px;
  background-color: #fff;
  border-radius: 20px 5px 5px 20px;
  position: relative;
}

.airplane-wing {
  position: absolute;
  width: 40px;
  height: 8px;
  background-color: #64ffda;
  border-radius: 0 10px 0 0;
  top: -8px;
  left: 15px;
}

.airplane-tail {
  position: absolute;
  width: 15px;
  height: 15px;
  background-color: #64ffda;
  transform: rotate(45deg);
  top: -15px;
  right: 5px;
}

.hydrogen-trail {
  position: absolute;
  left: -20px;
  top: 5px;
  display: flex;
}

.h2-molecule {
  opacity: 0;
  color: #64ffda;
  font-size: 0.8rem;
  font-weight: bold;
  margin-right: 5px;
  animation: trail 2s infinite;
}

.h2-molecule:nth-child(2) {
  animation-delay: 0.4s;
}

.h2-molecule:nth-child(3) {
  animation-delay: 0.8s;
}

@keyframes trail {
  0% {
    opacity: 0;
    transform: translateX(0);
  }

  10% {
    opacity: 1;
  }

  90% {
    opacity: 1;
  }

  100% {
    opacity: 0;
    transform: translateX(-30px);
  }
}

/* Floating Hydrogen Bubbles */
.floating-bubbles {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  overflow: hidden;
}

.bubble-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.h2-bubble {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(100, 255, 218, 0.1);
  border: 1px solid rgba(100, 255, 218, 0.3);
  border-radius: 50%;
  color: #64ffda;
  font-weight: bold;
  animation: float 15s infinite;
  box-shadow: 0 0 15px rgba(100, 255, 218, 0.2);
}

.bubble-1 {
  width: 40px;
  height: 40px;
  bottom: 10%;
  left: 10%;
  font-size: 0.9rem;
  animation-delay: 0s;
}

.bubble-2 {
  width: 30px;
  height: 30px;
  bottom: 20%;
  left: 30%;
  font-size: 0.7rem;
  animation-delay: 3s;
}

.bubble-3 {
  width: 50px;
  height: 50px;
  bottom: 5%;
  left: 50%;
  font-size: 1rem;
  animation-delay: 6s;
}

.bubble-4 {
  width: 35px;
  height: 35px;
  bottom: 15%;
  left: 70%;
  font-size: 0.8rem;
  animation-delay: 9s;
}

.bubble-5 {
  width: 25px;
  height: 25px;
  bottom: 25%;
  left: 85%;
  font-size: 0.6rem;
  animation-delay: 12s;
}

@keyframes float {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 0;
  }

  10% {
    opacity: 1;
  }

  90% {
    opacity: 1;
  }

  100% {
    transform: translateY(-500px) rotate(360deg);
    opacity: 0;
  }
}

/* Enhanced chart tabs */
.chart-tab {
  position: relative;
}

.chart-wrapper {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(100, 255, 218, 0.1);
}

.chart-wrapper:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(100, 255, 218, 0.1);
}

/* Enhanced results container */
.results-container {
  border-radius: 10px;
  overflow: hidden;
  background-color: rgba(18, 21, 30, 0.5);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  padding: 20px;
  position: relative;
}

/* Enhanced parameters section */
.parameters-section {
  background: linear-gradient(to right, rgba(18, 21, 30, 0.9), rgba(28, 35, 45, 0.9));
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  border-left: 4px solid #64ffda;
}

.parameters-section h3 {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Make both sections look like boarding gate monitors */
.demand-section {
  border: 2px solid rgba(100, 255, 218, 0.2);
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(18, 21, 30, 0.8), rgba(28, 35, 45, 0.8));
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.demand-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 5px;
  background: linear-gradient(90deg, #64ffda, transparent);
  opacity: 0.7;
}

.demand-section h3 {
  padding-left: 10px;
  margin-top: 10px;
}

.metric-card {
  background-color: rgba(255, 255, 255, 0.05);
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3);
}

/* Responsive media queries */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .airport-status {
    align-self: flex-start;
  }

  .help-icon {
    display: none;
  }

  .luggage-tag {
    display: none;
  }

  .flight-attendant-tooltip {
    bottom: 10px;
    right: 10px;
    max-width: 80%;
  }

  .speech-bubble {
    max-width: 200px;
    padding: 10px;
  }
}
</style>