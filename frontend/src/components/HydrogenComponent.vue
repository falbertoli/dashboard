<!-- File: frontend/src/components/HydrigenComponent.vue -->
<template>
  <div>
    <h2>Hydrogen Demand Estimation</h2>

    <!-- Fleet Percentage Input -->
    <label>Fleet Percentage: {{ fleetPercentage }}%</label>
    <input type="range" v-model="fleetPercentage" min="0" max="100" step="1" @change="updateFleet">

    <!-- Year Selection -->
    <label>Select Year</label>
    <select v-model.number="year" @change="updateYear">
      <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
    </select>


    <!-- GSE Selection -->
    <label>GSE to Transition</label>
    <div v-if="gseOptions.length">
      <div v-for="item in gseOptions" :key="item">
        <input type="checkbox" :value="item" v-model="gseList" />
        {{ item }}
      </div>
    </div>
    <p v-else>Loading GSE options...</p>


    <!-- Aircraft Hydrogen Demand -->
    <div v-if="aircraftH2Demand">
      <h3>Aircraft Hydrogen Demand</h3>
      <p>Daily Demand (ft³): {{ aircraftH2Demand.daily_h2_demand_ft3.toFixed(2) }}</p>
      <p>Projected Fuel Weight (lb): {{ aircraftH2Demand.projected_fuel_weight_lb.toFixed(2) }}</p>
    </div>

    <!-- GSE Hydrogen Demand -->
    <div v-if="gseH2Demand">
      <h3>GSE Hydrogen Demand</h3>
      <p>Daily Demand (ft³): {{ gseH2Demand.daily_h2_demand_ft3.toFixed(2) }}</p>
      <p>Total Diesel Used (lb): {{ gseH2Demand.total_diesel_used_lb.toFixed(2) }}</p>
      <p>Total Gasoline Used (lb): {{ gseH2Demand.total_gasoline_used_lb.toFixed(2) }}</p>
    </div>

    <!-- Error Message -->
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from "vue";
import { useHydrogenStore } from "../store/hydrogenStore";
import { fetchGseOptions } from "../utils/api.js";

const store = useHydrogenStore();
const fleetPercentage = computed(() => store.fleetPercentage);
const year = computed(() => store.year);
const aircraftH2Demand = computed(() => store.aircraftH2Demand);
const gseH2Demand = computed(() => store.gseH2Demand);
const gseOptions = ref([]); // Store the fetched GSE options
const gseList = ref([]); // ✅ Use `ref` instead of computed
const errorMessage = ref("");

const years = ref(Array.from({ length: 2050 - 2023 + 1 }, (_, i) => i + 2023));

// Watch for changes in `gseList` and update store
watch(gseList, (newGseList) => {
  store.setGseList(newGseList);
});

// Update fleet percentage
async function updateFleet(event) {
  try {
    await store.setFleetPercentage(event.target.value);
  } catch (error) {
    errorMessage.value = "Failed to fetch aircraft hydrogen demand.";
  }
}

// Update selected year
async function updateYear(event) {
  try {
    const selectedYear = parseInt(event.target.value, 10); // ✅ Ensure it's an integer
    await store.setYear(selectedYear);
  } catch (error) {
    errorMessage.value = "Failed to fetch data for the selected year.";
  }
}

onMounted(async () => {
  try {
    console.log("🚀 Fetching GSE options...");
    const response = await fetchGseOptions();
    console.log("✅ GSE Options Loaded:", response);

    gseOptions.value = response.data; // ✅ Ensure correct data assignment
    gseList.value = store.gseList; // Sync initial selected items
    await store.loadAircraftH2Demand();
    await store.loadGSEH2Demand();
  } catch (error) {
    console.error("❌ Error loading HydrogenComponent:", error);
    errorMessage.value = "Error loading data. Please check backend connection.";
  }
});
</script>


<style scoped>
input[type="range"] {
  width: 100%;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>
