<!-- File: frontend/src/components/HydrogenComponent.vue -->

<template>
  <div>
    <h2><i class="fas fa-atom"></i> Hydrogen Demand Estimation</h2>

    <!-- Input Parameters Section -->
    <div class="parameters-section">
      <h3><i class="fas fa-sliders-h"></i> Input Parameters</h3>

      <!-- Fleet Percentage Input -->
      <div class="form-group">
        <Slider label="Fleet Percentage:" id="fleet-percentage" :min="0" :max="100" :step="1" v-model="fleetPercentage"
          unit="%" />
      </div>

      <!-- Year Selection -->
      <div class="form-group">
        <Dropdown label="Select Year:" id="year-selection" :options="yearOptions" v-model="year" />
      </div>

      <!-- GSE Selection -->
      <div class="form-group">
        <div class="gse-header">
          <label>Ground vehicles to Transition:</label>
          <div class="gse-actions">
            <button class="action-button" @click="selectAllGse">
              <i class="fas fa-check-square"></i> Select All
            </button>
            <button class="action-button" @click="deselectAllGse">
              <i class="fas fa-square"></i> Deselect All
            </button>
          </div>
        </div>
        <CheckboxGroup :options="gseOptionsFormatted" v-model="gseList" />
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
      </div>

      <!-- Charts Tab -->
      <div v-show="activeTab === 'chart'" class="chart-tab">
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
import { computed, ref, onMounted, watch } from "vue";
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

const selectAllGse = () => {
  gseList.value = [...gseOptions.value];
};

const deselectAllGse = () => {
  gseList.value = [];
};

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
</style>