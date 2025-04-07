<!-- File: frontend/src/components/HydrogenComponent.vue -->

<template>
  <div>
    <h2>Hydrogen Demand Estimation</h2>
    <!-- Fleet Percentage Input -->
    <div class="input-section">
      <Slider label="Fleet Percentage:" id="fleet-percentage" :min="0" :max="100" :step="1" v-model="fleetPercentage" />
    </div>

    <!-- Year Selection -->
    <div class="input-section">
      <Dropdown label="Select Year:" id="year-selection" :options="yearOptions" v-model="year" />
    </div>

    <!-- GSE Selection -->
    <div class="input-section">
      <CheckboxGroup label="GSE to Transition:" :options="gseOptionsFormatted" v-model="gseList" />
    </div>

    <!-- Aircraft Hydrogen Demand -->
    <div v-if="aircraftH2Demand" class="demand-section">
      <h3>Aircraft Hydrogen Demand</h3>
      <p>Daily Demand (ft³): {{ aircraftH2Demand.daily_h2_demand_ft3?.toFixed(2) ?? 'N/A' }}</p>
      <p>Projected Fuel Weight (lb): {{ aircraftH2Demand.projected_fuel_weight_lb?.toFixed(2) ?? 'N/A' }}</p>
    </div>

    <!-- GSE Hydrogen Demand -->
    <div v-if="gseH2Demand" class="demand-section">
      <h3>GSE Hydrogen Demand</h3>
      <p>Daily Demand (ft³): {{ gseH2Demand.daily_h2_demand_ft3?.toFixed(2) ?? 'N/A' }}</p>
      <p>Total Diesel Used (lb): {{ gseH2Demand.total_diesel_used_lb?.toFixed(2) ?? 'N/A' }}</p>
      <p>Total Gasoline Used (lb): {{ gseH2Demand.total_gasoline_used_lb?.toFixed(2) ?? 'N/A' }}</p>
    </div>
    <ChartComponent chart-id="hydrogen-demand-chart" chart-type="bar" :chart-data="hydrogenDemandData"
      :chart-options="hydrogenDemandOptions" />

    <!-- Total Hydrogen Demand -->
    <div class="demand-section">
      <h3>Total Hydrogen Demand</h3>
      <p>Daily Demand (ft³): {{ store.totalH2Demand }}</p>
    </div>

    <!-- Error Message -->
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
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
.input-section {
  margin-bottom: 20px;
}

.demand-section {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  color: #ddd;
}

.demand-section p {
  margin: 5px 0;
  color: #aaa;
}

.error {
  color: #ff6384;
  font-weight: 600;
  margin-top: 10px;
}

.chart-container {
  margin-top: 20px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
}
</style>