<!-- File: frontend/src/views/EconomicImpactView.vue -->

<template>
  <div class="economic-impact-view">
    <h1>Economic Impact Analysis</h1>

    <div v-if="economicsStore.isLoading" class="loading-container">
      <p>Loading economic data...</p>
    </div>

    <div v-else-if="economicsStore.error" class="error-container">
      <p>{{ economicsStore.error }}</p>
    </div>

    <div v-else-if="!economicsStore.results" class="no-data-container">
      <p>No economic data available. Please calculate hydrogen demand first.</p>
      <button @click="calculateEconomicImpact" class="btn primary">Calculate Economic Impact</button>
    </div>

    <div class="form-group">
      <label for="fleetPercentage">
        Hydrogen Fleet Percentage (%)
        <span class="info-icon" title="This percentage remains constant throughout the projection period">ⓘ</span>
      </label>
      <input type="number" id="fleetPercentage" v-model.number="fleetPercentage" min="0" max="100" step="1" />
    </div>

    <div class="parameters-description" v-if="!economicsStore.results">
      <p>
        <strong>Economic Model Parameters:</strong> This model calculates the economic impact of hydrogen adoption
        with a constant fleet percentage over time. The key variable across scenarios is how quickly the
        extra turnaround time decreases each year.
      </p>
      <p>
        <strong>Growth Model:</strong> A simple compound growth rate is applied to demand, revenue, and utilization
        each year, consistent with the approach used in the hydrogen demand model.
      </p>
    </div>

    <div class="parameters-section" v-if="!economicsStore.results">
      <h2>Economic Projection Parameters</h2>
      <div class="form-grid">
        <div class="form-group">
          <label for="fleetPercentage">
            Hydrogen Fleet Percentage (%)
            <span class="info-icon" title="This percentage remains constant throughout the projection period">ⓘ</span>
          </label>
          <input type="number" id="fleetPercentage" v-model.number="fleetPercentage" min="0" max="100" step="1" />
        </div>

        <div class="form-group">
          <label for="startYear">Start Year:</label>
          <input type="number" id="startYear" v-model.number="startYear" min="2023" max="2050" />
        </div>

        <div class="form-group">
          <label for="endYear">End Year:</label>
          <input type="number" id="endYear" v-model.number="endYear" min="2023" max="2050" />
          <small>Must be after start year</small>
        </div>

        <div class="form-group">
          <label for="growthRate">
            Annual Compound Growth Rate (%)
            <span class="info-icon"
              title="Simple compound growth rate applied to demand, revenue, and utilization each year">ⓘ</span>
          </label>
          <input type="number" id="growthRate" v-model.number="growthRate" min="0" max="10" step="0.1" />
          <small>Default value (2%) matches the demand model assumptions</small>
        </div>

        <div class="form-group">
          <label for="extraTurnTime">Initial Extra Turn Time (minutes):</label>
          <input type="number" id="extraTurnTime" v-model.number="extraTurnTime" min="0" max="60" />
        </div>
      </div>

      <div class="scenario-config">
        <h3>Turnaround Time Reduction Scenarios</h3>
        <p>Define different annual reduction rates (minutes/year) for turnaround time:</p>

        <div class="scenarios-grid">
          <div v-for="(rate, index) in turnTimeDecreaseRates" :key="index" class="scenario-input">
            <label :for="`scenario${index}`">Scenario {{ index + 1 }}:</label>
            <input :id="`scenario${index}`" type="number" v-model.number="turnTimeDecreaseRates[index]" min="0" max="10"
              step="1" />
            <span>min/year</span>
            <button v-if="index > 0" @click="removeScenario(index)" class="btn remove" title="Remove scenario">
              ✕
            </button>
          </div>
        </div>

        <div class="scenario-actions">
          <button @click="addScenario" class="btn secondary">Add Scenario</button>
        </div>
      </div>

      <div class="form-actions">
        <button @click="calculateEconomicImpact" class="btn primary" :disabled="!isFormValid">
          Calculate Economic Impact
        </button>
      </div>
    </div>

    <div v-else class="results-container">
      <!-- Summary Cards -->
      <section class="summary-section">
        <h2>Scenario Comparison</h2>
        <div class="summary-cards">
          <div v-for="(metrics, rate) in economicsStore.scenarioSummary" :key="rate" class="summary-card"
            :class="{ 'selected': selectedScenario === parseInt(rate) }" @click="selectScenario(parseInt(rate))">
            <h3>{{ rate }} min/year reduction</h3>
            <div class="metrics">
              <div class="metric">
                <span class="label">Max Tax Credit:</span>
                <span class="value">${{ metrics.max_tax_credit.toFixed(2) }}/gal</span>
              </div>
              <div class="metric">
                <span class="label">Max Revenue Drop:</span>
                <span class="value">{{ metrics.max_revenue_drop_pct.toFixed(2) }}%</span>
              </div>
              <div class="metric">
                <span class="label">Final Year Tax Credit:</span>
                <span class="value">${{ metrics.final_year_tax_credit.toFixed(2) }}/gal</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div v-if="economicsStore.results" class="recalculate-container">
        <button @click="resetCalculation" class="btn secondary">Adjust Parameters</button>
      </div>

      <!-- calculation parameters section here -->
      <div class="calculation-params">
        <p>
          <strong>Calculation Parameters:</strong>
          Fleet Percentage: {{ fleetPercentage }}%,
          Growth Rate: {{ growthRate }}%/year,
          Initial Turn Time: {{ extraTurnTime }} minutes,
          Years: {{ startYear }} - {{ endYear }}
        </p>
      </div>


      <!-- Charts Section -->
      <section class="charts-section">
        <h2>Economic Impact Visualization</h2>

        <!-- Revenue Drop Chart -->
        <div class="chart-wrapper">
          <h3>Revenue Drop by Scenario</h3>
          <ChartComponent chartId="revenueDropChart" chartType="line" :chartData="revenueDropChartData"
            :chartOptions="revenueChartOptions" />
        </div>

        <!-- Tax Credit Chart -->
        <div class="chart-wrapper">
          <h3>Required Tax Credit by Scenario</h3>
          <ChartComponent chartId="taxCreditChart" chartType="line" :chartData="taxCreditChartData"
            :chartOptions="taxCreditChartOptions" />
        </div>

        <!-- Revenue Comparison Chart -->
        <div class="chart-wrapper">
          <h3>Revenue Comparison for {{ selectedScenario }} min/year Scenario</h3>
          <ChartComponent chartId="revenueComparisonChart" chartType="bar" :chartData="revenueComparisonChartData"
            :chartOptions="revenueComparisonOptions" />
        </div>
      </section>

      <!-- Detailed Results Table -->
      <section class="details-section">
        <h2>Detailed Results for {{ selectedScenario }} min/year Scenario</h2>
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Year</th>
                <th>Growth Factor</th> <!-- New column -->
                <th>Turn Time (min)</th>
                <th>H2 Flights (%)</th>
                <th>Baseline Revenue ($M)</th>
                <th>H2 Revenue ($M)</th>
                <th>Revenue Drop (%)</th>
                <th>Tax Credit ($/gal)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in selectedScenarioData" :key="item.Year">
                <td>{{ item.Year }}</td>
                <td>{{ item.Growth_Factor.toFixed(3) }}</td> <!-- New column -->
                <td>{{ item.Turn_Time_min }}</td>
                <td>{{ (item.Fraction_Flights_H2 * 100).toFixed(1) }}%</td>
                <td>${{ item.Baseline_Revenue_M.toFixed(2) }}M</td>
                <td>${{ item.Hydrogen_Revenue_M.toFixed(2) }}M</td>
                <td>{{ item.Pct_Drop.toFixed(2) }}%</td>
                <td>${{ item.Req_Tax_Credit_per_gal.toFixed(2) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
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

    // Form inputs with defaults
    const startYear = ref(new Date().getFullYear());
    const endYear = ref(hydrogenStore.year || 2036);
    const growthRate = ref(2.0); // 2% default, displayed as percentage
    const extraTurnTime = ref(30); // 30 minutes default
    const fleetPercentage = ref(hydrogenStore.fleetPercentage || 10); // Default to 10%
    const turnTimeDecreaseRates = ref([0, 1, 2, 3, 4, 5]); // Default scenarios

    // Form validation
    const isFormValid = computed(() => {
      return startYear.value < endYear.value &&
        growthRate.value >= 0 &&
        extraTurnTime.value >= 0 &&
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

    // Tax Credit Chart Data
    const taxCreditChartData = computed(() => {
      if (!economicsStore.results || !economicsStore.results.scenarios) return { labels: [], datasets: [] };

      const scenarios = economicsStore.results.scenarios;
      const firstScenario = Object.values(scenarios)[0];
      const labels = firstScenario.map(item => item.Year);

      const datasets = Object.entries(scenarios).map(([rate, data]) => ({
        label: `${rate} min/year reduction`,
        data: data.map(item => item.Req_Tax_Credit_per_gal),
        borderColor: getColorForRate(parseInt(rate)),
        backgroundColor: getColorForRate(parseInt(rate), 0.2),
        borderWidth: parseInt(rate) === selectedScenario.value ? 3 : 1,
      }));

      return { labels, datasets };
    });

    // Revenue Comparison Chart Data
    const revenueComparisonChartData = computed(() => {
      if (!selectedScenarioData.value.length) return { labels: [], datasets: [] };

      const labels = selectedScenarioData.value.map(item => item.Year);

      const datasets = [
        {
          label: 'Baseline Revenue',
          data: selectedScenarioData.value.map(item => item.Baseline_Revenue_M),
          backgroundColor: 'rgba(75, 192, 192, 0.5)',
        },
        {
          label: 'Hydrogen Revenue',
          data: selectedScenarioData.value.map(item => item.Hydrogen_Revenue_M),
          backgroundColor: 'rgba(255, 159, 64, 0.5)',
        }
      ];

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

    const taxCreditChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: 'Required Tax Credit vs. Year for Different Turn-Time Reduction Rates'
        },
        tooltip: {
          callbacks: {
            label: (context) => `${context.dataset.label}: $${context.raw.toFixed(2)}/gal`
          }
        }
      },
      scales: {
        y: {
          title: {
            display: true,
            text: 'Required Tax Credit ($/gal)'
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

    const revenueComparisonOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: 'Revenue Comparison for Selected Scenario'
        },
        tooltip: {
          callbacks: {
            label: (context) => `${context.dataset.label}: $${context.raw.toFixed(2)}M`
          }
        }
      },
      scales: {
        y: {
          title: {
            display: true,
            text: 'Revenue (Millions $)'
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

    // Enhanced calculation function with user parameters
    const calculateEconomicImpact = async () => {
      if (!isFormValid.value) return;

      await economicsStore.fetchEconomicImpact({
        startYear: startYear.value,
        endYear: endYear.value,
        growthRate: growthRate.value / 100, // Convert from percentage to decimal
        extraTurnTime: extraTurnTime.value,
        turnTimeDecreaseRates: turnTimeDecreaseRates.value,
        fleetPercentage: fleetPercentage.value / 100 // Convert from percentage to decimal
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
      taxCreditChartData,
      revenueComparisonChartData,
      revenueChartOptions,
      taxCreditChartOptions,
      revenueComparisonOptions,
      selectScenario,
      calculateEconomicImpact,
      // Add the new properties
      startYear,
      endYear,
      growthRate,
      extraTurnTime,
      fleetPercentage, // Add this
      turnTimeDecreaseRates,
      isFormValid,
      addScenario,
      removeScenario,
      resetCalculation
    };
  }
}
</script>

<style scoped>
.economic-impact-view {
  padding: 1rem;
}

h1,
h2,
h3 {
  color: #333;
  margin-bottom: 1rem;
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
  background-color: #f5f5f5;
}

.error-container {
  background-color: #ffeeee;
  color: #cc0000;
}

.no-data-container {
  background-color: #f5f5f5;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.btn.primary {
  background-color: #4caf50;
  color: white;
}

.summary-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

.summary-card {
  flex: 1;
  min-width: 200px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f9f9f9;
  cursor: pointer;
  transition: all 0.2s ease;
}

.summary-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.summary-card.selected {
  border-color: #4caf50;
  background-color: #e8f5e9;
}

.metric {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.chart-wrapper {
  height: 400px;
  margin-bottom: 2rem;
  padding: 1rem;
  border: 1px solid #eee;
  border-radius: 4px;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 2rem;
}

.data-table th,
.data-table td {
  border: 1px solid #ddd;
  padding: 0.5rem;
  text-align: right;
}

.data-table th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.data-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.data-table tr:hover {
  background-color: #f0f0f0;
}

.parameters-section {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
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
}

.form-group input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
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
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
}

.btn.remove {
  background-color: #f8d7da;
  color: #721c24;
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
}

.btn.secondary {
  background-color: #e9ecef;
  color: #495057;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.form-actions {
  margin-top: 1.5rem;
  text-align: center;
}

.recalculate-container {
  text-align: right;
  margin-bottom: 1rem;
}

.info-icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  line-height: 16px;
  text-align: center;
  border-radius: 50%;
  background-color: #6c757d;
  color: white;
  font-size: 12px;
  margin-left: 4px;
  cursor: help;
}

.calculation-params {
  background-color: #f0f8ff;
  /* Light blue background */
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
  border-left: 4px solid #4caf50;
  /* Green left border */
}

.calculation-params p {
  margin: 0;
  font-size: 0.9rem;
}
</style>