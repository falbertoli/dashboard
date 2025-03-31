<!-- File: frontend/src/views/EconomicImpactView.vue -->

<template>
  <div class="economic-impact-view">
    <h1>Economic Impact Analysis</h1>

    <!-- Alert shown when no hydrogen data is available -->
    <div v-if="!hydrogenStore.aircraftH2Demand || !hydrogenStore.gseH2Demand" class="alert info">
      <i class="fas fa-info-circle"></i>
      <span>Please configure hydrogen demand in the Hydrogen section first.</span>
    </div>

    <div v-else-if="economicsStore.isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading economic data...</p>
    </div>

    <div v-else-if="economicsStore.error" class="error-container">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ economicsStore.error }}</p>
    </div>

    <div v-else-if="!hydrogenStore.totalH2Demand" class="no-data-container">
      <i class="fas fa-info-circle"></i>
      <p>No hydrogen demand data available. Please calculate hydrogen demand first.</p>
      <router-link to="/hydrogen" class="btn primary">
        <i class="fas fa-arrow-right"></i> Go to Hydrogen Demand
      </router-link>
    </div>

    <div v-else>
      <div class="parameters-description" v-if="!economicsStore.results">
        <p>
          <strong>Economic Model Parameters:</strong> This model calculates the economic impact of hydrogen adoption
          based on the hydrogen demand you calculated. The key variable is the extra turnaround time required for
          hydrogen aircraft and how quickly this time decreases as the technology matures.
        </p>
        <p>
          <strong>Fixed Parameters:</strong> Fleet percentage ({{ hydrogenStore.fleetPercentage }}%),
          projection year ({{ hydrogenStore.year }}), and growth rate (2%) are derived from your hydrogen demand
          calculation.
        </p>
      </div>

      <div class="parameters-section" v-if="!economicsStore.results">
        <h2>Turnaround Time Parameters</h2>

        <div class="form-group">
          <label for="extraTurnTime">Initial Extra Turnaround Time for H₂ Aircraft (minutes):</label>
          <input type="number" id="extraTurnTime" v-model.number="extraTurnTime" min="0" max="60" />
          <small>Additional turnaround time required for hydrogen aircraft compared to conventional aircraft</small>
        </div>

        <div class="scenario-config">
          <h3>Turnaround Time Reduction Scenarios</h3>
          <p>Define different annual reduction rates (minutes/year) as hydrogen refueling technology matures:</p>

          <div class="scenarios-grid">
            <div v-for="(rate, index) in turnTimeDecreaseRates" :key="index" class="scenario-input">
              <label :for="`scenario${index}`">Scenario {{ index + 1 }}:</label>
              <input :id="`scenario${index}`" type="number" v-model.number="turnTimeDecreaseRates[index]" min="0"
                max="10" step="1" />
              <span>min/year</span>
              <button v-if="index > 0" @click="removeScenario(index)" class="btn remove" title="Remove scenario">
                ✕
              </button>
            </div>
          </div>

          <div class="scenario-actions">
            <button @click="addScenario" class="btn secondary">
              <i class="fas fa-plus"></i> Add Scenario
            </button>
          </div>
        </div>

        <div class="form-actions">
          <button @click="calculateEconomicImpact" class="btn primary" :disabled="!isFormValid">
            <i class="fas fa-calculator"></i> Calculate Economic Impact
          </button>
        </div>
      </div>

      <div class="results-container" v-else>
        <div v-if="economicsStore.results" class="recalculate-container">
          <button @click="resetCalculation" class="btn secondary">
            <i class="fas fa-adjust"></i> Adjust Turnaround Parameters
          </button>
        </div>

        <!-- Calculation Parameters Section -->
        <div class="calculation-params">
          <p>
            <strong>Calculation Parameters:</strong>
            Fleet Percentage: {{ hydrogenStore.fleetPercentage }}% (from Hydrogen Demand),
            Growth Rate: 2.0% per year (fixed),
            Initial Turn Time: {{ extraTurnTime }} minutes (user input),
            Years: {{ currentYear }} - {{ hydrogenStore.year }}
          </p>
        </div>

        <!-- Dropdown for Scenario Selection -->
        <div class="scenario-selection">
          <label for="scenarioSelect">Select Scenario:</label>
          <select id="scenarioSelect" v-model="selectedScenario">
            <option v-for="rate in turnTimeDecreaseRates" :key="rate" :value="rate">{{ rate }} min/year reduction
            </option>
          </select>
        </div>

        <!-- Detailed Results Table -->
        <section class="details-section">
          <h2>Detailed Results for {{ selectedScenario }} min/year Scenario</h2>
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Year</th>
                  <th>Growth Factor</th>
                  <th>Turn Time (min)</th>
                  <th>H2 Flights (%)</th>
                  <th>Baseline Revenue ($M)</th>
                  <th>H2 Revenue ($M)</th>
                  <th>Revenue Drop (%)</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in selectedScenarioData" :key="item.Year">
                  <td>{{ item.Year }}</td>
                  <td>{{ item.Growth_Factor.toFixed(3) }}</td>
                  <td>{{ item.Turn_Time_min }}</td>
                  <td>{{ (item.Fraction_Flights_H2 * 100).toFixed(1) }}%</td>
                  <td>${{ item.Baseline_Revenue_M.toFixed(2) }}M</td>
                  <td>${{ item.Hydrogen_Revenue_M.toFixed(2) }}M</td>
                  <td>{{ item.Pct_Drop.toFixed(2) }}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Charts Section -->
        <section class="charts-section">
          <h2>Economic Impact Visualization</h2>

          <!-- Revenue Drop Chart -->
          <div class="chart-wrapper">
            <h3>Revenue Drop by Scenario</h3>
            <ChartComponent chartId="revenueDropChart" chartType="line" :chartData="revenueDropChartData"
              :chartOptions="revenueChartOptions" />
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useEconomicsStore } from '@/store/economicsStore';
import { useHydrogenStore } from '@/store/hydrogenStore';
import ChartComponent from '@/components/ChartComponent.vue';

export default {
  name: 'EconomicImpactView',

  components: {
    ChartComponent
  },

  setup() {
    const economicsStore = useEconomicsStore();
    const hydrogenStore = useHydrogenStore();
    const selectedScenario = ref(3); // Default to 3 min/year reduction
    const currentYear = ref(new Date().getFullYear());

    // Only allow user to modify turnaround time parameters
    const extraTurnTime = ref(30); // 30 minutes default
    const turnTimeDecreaseRates = ref([0, 1, 2, 3, 4, 5]); // Default scenarios

    // Form validation
    const isFormValid = computed(() => {
      return extraTurnTime.value >= 0 &&
        turnTimeDecreaseRates.value.length > 0 &&
        turnTimeDecreaseRates.value.every(rate => rate >= 0);
    });

    // Add/remove scenario functions
    const addScenario = () => {
      // Add a new scenario with the next integer value or 0
      const nextValue = turnTimeDecreaseRates.value.length > 0
        ? Math.max(...turnTimeDecreaseRates.value) + 1
        : 0;
      turnTimeDecreaseRates.value.push(Math.min(nextValue, 10)); // Cap at 10 min/year
    };

    const removeScenario = (index) => {
      turnTimeDecreaseRates.value.splice(index, 1);
    };

    // Reset calculation to adjust parameters
    const resetCalculation = () => {
      economicsStore.results = null;
    };

    // Get the selected scenario data
    const selectedScenarioData = computed(() => {
      if (!economicsStore.results || !economicsStore.results.scenarios) return [];
      return economicsStore.results.scenarios[selectedScenario.value] || [];
    });

    // Revenue Drop Chart Data
    const revenueDropChartData = computed(() => {
      if (!economicsStore.results || !economicsStore.results.scenarios) return { labels: [], datasets: [] };

      const scenarios = economicsStore.results.scenarios;
      const firstScenario = Object.values(scenarios)[0];
      const labels = firstScenario.map(item => item.Year);

      const datasets = Object.entries(scenarios).map(([rate, data]) => ({
        label: `${rate} min/year reduction`,
        data: data.map(item => item.Pct_Drop),
        borderColor: getColorForRate(parseInt(rate)),
        backgroundColor: getColorForRate(parseInt(rate), 0.2),
        borderWidth: parseInt(rate) === selectedScenario.value ? 3 : 1,
      }));

      return { labels, datasets };
    });

    // Chart Options
    const revenueChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: 'Revenue Drop vs. Year for Different Turn-Time Reduction Rates'
        },
        tooltip: {
          callbacks: {
            label: (context) => `${context.dataset.label}: ${context.raw.toFixed(2)}%`
          }
        }
      },
      scales: {
        y: {
          title: {
            display: true,
            text: '% Revenue Drop'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Year'
          }
        }
      }
    };

    // Function to select a scenario
    const selectScenario = (rate) => {
      selectedScenario.value = rate;
    };

    // Simplified calculation function with only turnaround parameters
    const calculateEconomicImpact = async () => {
      if (!isFormValid.value) return;

      await economicsStore.fetchEconomicImpact({
        extraTurnTime: extraTurnTime.value,
        turnTimeDecreaseRates: turnTimeDecreaseRates.value,
        // Use hydrogen store values for other parameters
        fleetPercentage: hydrogenStore.fleetPercentage / 100, // Convert from percentage to decimal
        startYear: currentYear.value,
        endYear: hydrogenStore.year,
        finalH2Year: hydrogenStore.year
      });
    };

    // Function to get colors for different rates
    const getColorForRate = (rate, alpha = 1) => {
      const colors = [
        `rgba(255, 99, 132, ${alpha})`,   // 0 min/year
        `rgba(54, 162, 235, ${alpha})`,   // 1 min/year
        `rgba(255, 206, 86, ${alpha})`,   // 2 min/year
        `rgba(75, 192, 192, ${alpha})`,   // 3 min/year
        `rgba(153, 102, 255, ${alpha})`,  // 4 min/year
        `rgba(255, 159, 64, ${alpha})`    // 5 min/year
      ];
      return colors[rate] || `rgba(0, 0, 0, ${alpha})`;
    };

    // Load data when component mounts
    onMounted(async () => {
      if (hydrogenStore.totalH2Demand && !economicsStore.results) {
        // Don't auto-calculate on mount anymore, let user set parameters first
        // await calculateEconomicImpact();
      }
    });

    return {
      economicsStore,
      hydrogenStore,
      selectedScenario,
      selectedScenarioData,
      revenueDropChartData,
      revenueChartOptions,
      selectScenario,
      calculateEconomicImpact,
      // Only turnaround time parameters
      extraTurnTime,
      turnTimeDecreaseRates,
      // Other required properties
      currentYear,
      isFormValid,
      addScenario,
      removeScenario,
      resetCalculation
    };
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

.economic-impact-view {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
  font-family: 'Roboto', sans-serif;
  color: #e0e0e0;
  background-color: #1a1e24;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

h1,
h2,
h3 {
  color: #64ffda;
  margin-bottom: 1rem;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

.loading-container,
.error-container,
.no-data-container {
  padding: 2rem;
  text-align: center;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}

.loading-container {
  background-color: #333;
  color: #64ffda;
}

.error-container {
  background-color: rgba(255, 255, 255, 0.05);
  border-left: 4px solid #e74c3c;
  color: #e74c3c;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 10px;
}

.no-data-container {
  background-color: rgba(255, 255, 255, 0.05);
  color: #aaa;
  display: flex;
  align-items: center;
  gap: 10px;
}

.alert.info {
  background-color: rgba(54, 162, 235, 0.1);
  border-left: 4px solid rgba(54, 162, 235, 0.8);
  color: #ddd;
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 25px;
}

.alert i {
  margin-right: 10px;
  font-size: 1.2rem;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn.primary {
  background-color: #64ffda;
  color: #1a1e24;
}

.btn.primary:hover {
  background-color: #73ffde;
}

.btn.secondary {
  background-color: #333;
  color: #64ffda;
}

.btn.secondary:hover {
  background-color: #444;
}

.chart-wrapper {
  height: 400px;
  margin-bottom: 2rem;
  padding: 1rem;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.05);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.table-container {
  overflow-x: auto;
  margin-bottom: 2rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
  color: #e0e0e0;
}

.data-table th,
.data-table td {
  border: 1px solid #444;
  padding: 0.5rem;
  text-align: right;
}

.data-table th {
  background-color: rgba(255, 255, 255, 0.05);
  font-weight: bold;
  color: #64ffda;
}

.data-table tr:nth-child(even) {
  background-color: rgba(255, 255, 255, 0.03);
}

.data-table tr:hover {
  background-color: #444;
}

.parameters-section {
  background-color: rgba(255, 255, 255, 0.05);
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #64ffda;
}

.form-group input {
  padding: 0.5rem;
  border: 1px solid #444;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.form-group input:focus {
  border-color: #64ffda;
  outline: none;
}

.form-group small {
  font-size: 0.8rem;
  color: #666;
  margin-top: 0.25rem;
}

.scenario-config {
  margin-bottom: 1.5rem;
}

.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.scenario-input {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.scenario-input input {
  width: 60px;
  padding: 0.5rem;
  border: 1px solid #444;
  border-radius: 4px;
  text-align: center;
  transition: border-color 0.2s ease;
}

.scenario-input input:focus {
  border-color: #64ffda;
  outline: none;
}

.btn.remove {
  background-color: #ff5252;
  color: #fff;
  border: none;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 10px;
  padding: 0;
  transition: background-color 0.2s ease;
}

.btn.remove:hover {
  background-color: #ff1744;
}

.form-actions {
  margin-top: 1.5rem;
  text-align: center;
}

.recalculate-container {
  text-align: right;
  margin-bottom: 1rem;
}

.calculation-params {
  background-color: rgba(255, 255, 255, 0.05);
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  border-left: 4px solid #64ffda;
  font-size: 0.9rem;
  color: #e0e0e0;
}

.calculation-params p {
  margin: 0;
}

.results-container {
  margin-top: 2rem;
}

.charts-section {
  margin-bottom: 2rem;
}

.details-section {
  margin-bottom: 2rem;
}

.scenario-selection {
  margin-bottom: 1.5rem;
}

.scenario-selection label {
  font-weight: bold;
  color: #64ffda;
}

.scenario-selection select {
  padding: 0.5rem;
  border: 1px solid #444;
  border-radius: 4px;
  background-color: #333;
  color: #e0e0e0;
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.scenario-selection select:focus {
  border-color: #64ffda;
  outline: none;
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top: 4px solid #64ffda;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .chart-wrapper {
    height: 300px;
  }

  .data-table th,
  .data-table td {
    padding: 0.25rem;
    font-size: 0.9rem;
  }
}
</style>