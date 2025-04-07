<!-- File: frontend/src/components/HydrogenComponent.vue -->

<template>
  <div>
    <h2><i class="fas fa-atom"></i> Hydrogen Demand Estimation</h2>

    <!-- Input Parameters Section -->
    <div class="parameters-section">
      <h3><i class="fas fa-sliders-h"></i> Input Parameters</h3>

      <!-- Fleet Percentage Input -->
      <div class="form-group">
        <Slider label="Fleet Percentage:" id="fleet-percentage" :min="0" :max="100" :step="1"
          v-model="fleetPercentage" />
      </div>

      <!-- Year Selection -->
      <div class="form-group">
        <Dropdown label="Select Year:" id="year-selection" :options="yearOptions" v-model="year" />
      </div>

      <!-- GSE Selection -->
      <div class="form-group">
        <CheckboxGroup label="GSE to Transition:" :options="gseOptionsFormatted" v-model="gseList" />
      </div>
    </div>

    <!-- Results Section -->
    <div class="results-container">
      <!-- Aircraft Hydrogen Demand -->
      <div v-if="aircraftH2Demand" class="demand-section">
        <h3><i class="fas fa-plane"></i> Aircraft Hydrogen Demand</h3>
        <div class="metric-card">
          <div class="metric">
            <span class="metric-label">Daily Demand:</span>
            <span class="metric-value">{{ $formatNumber(aircraftH2Demand.daily_h2_demand_ft3) }} ft³</span>
          </div>
          <div class="metric">
            <span class="metric-label">Projected Fuel Weight:</span>
            <span class="metric-value">{{ $formatNumber(aircraftH2Demand.projected_fuel_weight_lb) }} lb</span>
          </div>
        </div>
      </div>

      <!-- GSE Hydrogen Demand -->
      <div v-if="gseH2Demand" class="demand-section">
        <h3><i class="fas fa-truck"></i> GSE Hydrogen Demand</h3>
        <div class="metric-card">
          <div class="metric">
            <span class="metric-label">Daily Demand:</span>
            <span class="metric-value">{{ $formatNumber(gseH2Demand.daily_h2_demand_ft3) }} ft³</span>
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

      <!-- Chart Section -->
      <div class="chart-wrapper">
        <h3><i class="fas fa-chart-bar"></i> Hydrogen Demand Distribution</h3>
        <ChartComponent chart-id="hydrogen-demand-chart" chart-type="bar" :chart-data="hydrogenDemandData"
          :chart-options="hydrogenDemandOptions" />
      </div>

      <!-- Total Hydrogen Demand -->
      <div class="demand-section total-demand">
        <h3><i class="fas fa-tachometer-alt"></i> Total Hydrogen Demand</h3>
        <div class="metric-card highlight">
          <div class="metric">
            <span class="metric-label">Daily Demand:</span>
            <span class="metric-value">{{ $formatNumber(store.totalH2Demand) }} ft³</span>
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

//Chart Data
const hydrogenDemandData = computed(() => {
  return {
    labels: ['Aircraft', 'GSE'],
    datasets: [{
      label: 'Daily Hydrogen Demand (ft³)',
      data: [
        store.aircraftH2Demand?.daily_h2_demand_ft3 || 0,
        store.gseH2Demand?.daily_h2_demand_ft3 || 0
      ],
      backgroundColor: [
        'rgba(54, 162, 235, 0.8)',
        'rgba(255, 99, 132, 0.8)'
      ],
      borderColor: [
        'rgba(54, 162, 235, 1)',
        'rgba(255, 99, 132, 1)'
      ],
      borderWidth: 1
    }]
  };
});

//Chart Options
const hydrogenDemandOptions = computed(() => ({
  scales: {
    y: {
      beginAtZero: true
    }
  }
}))

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

/* Results Container */
.results-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
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
  height: 400px;
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
}
</style>