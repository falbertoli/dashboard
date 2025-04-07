<!-- File: frontend/src/components/Economic/TurnaroundTimeAnalysis.vue -->

<template>
  <!-- Alert shown when no hydrogen data is available -->
  <div v-if="!hydrogenStore.aircraftH2Demand || !hydrogenStore.gseH2Demand" class="alert info">
    <i class="fas fa-info-circle"></i>
    <span>Please configure hydrogen demand in the Hydrogen section first.</span>
  </div>

  <!-- Loading indicator -->
  <div v-else-if="economicsStore.isLoading" class="loading-container">
    <div class="spinner"></div>
    <p>Loading economic data...</p>
  </div>

  <!-- Error message -->
  <div v-else-if="economicsStore.error" class="error-container">
    <i class="fas fa-exclamation-triangle"></i>
    <p>{{ economicsStore.error }}</p>
  </div>

  <!-- No data message -->
  <div v-else-if="!hydrogenStore.totalH2Demand" class="no-data-container">
    <i class="fas fa-info-circle"></i>
    <p>No hydrogen demand data available. Please calculate hydrogen demand first.</p>
    <router-link to="/hydrogen" class="btn primary">
      <i class="fas fa-arrow-right"></i> Go to Hydrogen Demand
    </router-link>
  </div>

  <div v-else>
    <div class="data-consistency-indicator" v-if="economicsStore.results">
      <div class="calculation-timestamp" v-if="economicsStore.results && economicsStore.lastCalculationTime">
        <i class="fas fa-clock"></i>
        <span>Last calculated: {{ formatTimestamp(economicsStore.lastCalculationTime) }}</span>
      </div>
      <div class="indicator" :class="{ 'consistent': isDataConsistent, 'inconsistent': !isDataConsistent }">
        <i :class="isDataConsistent ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle'"></i>
        <span>Data {{ isDataConsistent ? 'is consistent' : 'has changed' }}</span>
      </div>
      <button v-if="!isDataConsistent" @click="calculateEconomicImpact" class="btn warning">
        <i class="fas fa-sync"></i> Recalculate
      </button>
    </div>

    <!-- Add auto-recalculate option here -->
    <div class="auto-recalculate-option">
      <label class="toggle-switch">
        <input type="checkbox" v-model="economicsStore.autoRecalculate" @change="handleAutoRecalculateChange">
        <span class="toggle-slider"></span>
      </label>
      <span class="toggle-label">Auto-recalculate when hydrogen data changes</span>
    </div>

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
      <h2><i class="fas fa-sliders-h"></i> Turnaround Time Parameters</h2>

      <div class="form-group">
        <label for="extraTurnTime"><i class="fas fa-clock"></i> Initial Extra Turnaround Time for H₂ Aircraft
          (minutes):</label>
        <input type="number" id="extraTurnTime" v-model.number="extraTurnTime" min="0" max="60" />
        <small>Additional turnaround time required for hydrogen aircraft compared to conventional aircraft</small>
      </div>

      <div class="scenario-config">
        <h3><i class="fas fa-layer-group"></i> Turnaround Time Reduction Scenarios</h3>
        <p>Define different annual reduction rates (minutes/year) as hydrogen refueling technology matures:</p>

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

    <!-- Results section -->
    <div class="results-container" v-else>
      <!-- Recalculate button with icon -->
      <div class="recalculate-container">
        <button @click="resetCalculation" class="btn secondary">
          <i class="fas fa-undo"></i> Adjust Parameters
        </button>
        <button @click="exportCurrentScenario" class="btn secondary">
          <i class="fas fa-download"></i> Export Data
        </button>
      </div>

      <!-- Scenario Comparison Dashboard -->
      <section class="scenario-comparison">
        <h2><i class="fas fa-balance-scale"></i> Scenario Comparison</h2>
        <div class="comparison-cards">
          <div v-for="scenario in economicsStore.scenarioComparison" :key="scenario.rate" class="comparison-card"
            :class="{ 'selected': selectedScenario === scenario.rate }" @click="selectScenario(scenario.rate)">
            <h3><i class="fas fa-tachometer-alt"></i> {{ scenario.rate }} min/year</h3>
            <div class="card-metrics">
              <div class="metric">
                <span class="metric-label"><i class="fas fa-dollar-sign"></i> Max Tax Credit</span>
                <span class="metric-value">{{ scenario.maxTaxCredit }}</span>
              </div>
              <div class="metric">
                <span class="metric-label"><i class="fas fa-chart-line"></i> Max Revenue Drop</span>
                <span class="metric-value">{{ scenario.maxRevenueDrop }}</span>
              </div>
              <div class="metric">
                <span class="metric-label"><i class="fas fa-money-bill-wave"></i> Final Tax Credit</span>
                <span class="metric-value">{{ scenario.finalYearTaxCredit }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Calculation Parameters Section -->
      <div class="calculation-params">
        <p>
          <i class="fas fa-cog"></i> <strong>Calculation Parameters:</strong>
          Fleet Percentage: {{ hydrogenStore.fleetPercentage }}% (from Hydrogen Demand),
          Growth Rate: 2.0% per year (fixed),
          Initial Turn Time: {{ extraTurnTime }} minutes (user input),
          Years: {{ economicsStore.startYear }} - {{ hydrogenStore.year }}
        </p>
      </div>

      <!-- Selected Scenario Summary -->
      <section class="scenario-summary">
        <h2><i class="fas fa-chart-pie"></i> {{ selectedScenario }} min/year Scenario Summary</h2>
        <div class="summary-metrics">
          <div class="metric-card">
            <h3><i class="fas fa-dollar-sign"></i> Peak Tax Credit</h3>
            <p class="metric-value">${{ getMaxTaxCredit(selectedScenario) }}/gal</p>
            <p class="metric-year">in {{ getTaxCreditPeakYear(selectedScenario) }}</p>
          </div>
          <div class="metric-card">
            <h3><i class="fas fa-chart-line"></i> Peak Revenue Impact</h3>
            <p class="metric-value">{{ getMaxRevenueDrop(selectedScenario) }}%</p>
            <p class="metric-year">in {{ getRevenueDropPeakYear(selectedScenario) }}</p>
          </div>
          <div class="metric-card">
            <h3><i class="fas fa-coins"></i> Cumulative Cost</h3>
            <p class="metric-value">${{ getCumulativeCost(selectedScenario) }}M</p>
            <p class="metric-year">through {{ hydrogenStore.year }}</p>
          </div>
        </div>
      </section>

      <!-- Tabs for different data views -->
      <div class="data-tabs">
        <button class="tab-button" :class="{ active: activeTab === 'details' }" @click="activeTab = 'details'">
          <i class="fas fa-table"></i> Yearly Details
        </button>
        <button class="tab-button" :class="{ active: activeTab === 'taxCredits' }" @click="activeTab = 'taxCredits'">
          <i class="fas fa-receipt"></i> Tax Credits
        </button>
        <button class="tab-button" :class="{ active: activeTab === 'charts' }" @click="activeTab = 'charts'">
          <i class="fas fa-chart-bar"></i> Charts
        </button>
      </div>

      <!-- Detailed Results Table -->
      <section v-if="activeTab === 'details'" class="details-section">
        <h2><i class="fas fa-table"></i> Detailed Results for {{ selectedScenario }} min/year Scenario</h2>
        <div class="table-container details-table">
          <div class="table-header">
            <div class="header-cell"><i class="fas fa-calendar-alt"></i> Year</div>
            <div class="header-cell"><i class="fas fa-chart-line"></i> Growth Factor</div>
            <div class="header-cell"><i class="fas fa-clock"></i> Turn Time (min)</div>
            <div class="header-cell"><i class="fas fa-plane"></i> H2 Flights (%)</div>
            <div class="header-cell"><i class="fas fa-dollar-sign"></i> Baseline Revenue ($M)</div>
            <div class="header-cell"><i class="fas fa-hydrogen"></i> H2 Revenue ($M)</div>
            <div class="header-cell"><i class="fas fa-chart-area"></i> Revenue Drop (%)</div>
          </div>

          <div v-for="item in selectedScenarioData" :key="item.Year" class="table-row">
            <div class="row-cell">{{ item.Year }}</div>
            <div class="row-cell">{{ item.Growth_Factor.toFixed(3) }}</div>
            <div class="row-cell">{{ item.Turn_Time_min }}</div>
            <div class="row-cell">{{ (item.Fraction_Flights_H2 * 100).toFixed(1) }}%</div>
            <div class="row-cell">${{ item.Baseline_Revenue_M.toFixed(2) }}M</div>
            <div class="row-cell">${{ item.Hydrogen_Revenue_M.toFixed(2) }}M</div>
            <div class="row-cell">{{ item.Pct_Drop.toFixed(2) }}%</div>
          </div>
        </div>
      </section>

      <!-- Tax Credits Table -->
      <section v-if="activeTab === 'taxCredits'" class="taxCredits-section">
        <h2><i class="fas fa-receipt"></i> Tax Credits for {{ selectedScenario }} min/year Scenario</h2>
        <div class="table-container taxCredits-table">
          <div class="table-header">
            <div class="header-cell"><i class="fas fa-calendar-alt"></i> Year</div>
            <div class="header-cell"><i class="fas fa-arrow-down"></i> Revenue Loss ($M)</div>
            <div class="header-cell"><i class="fas fa-gas-pump"></i> H2 Volume (gal)</div>
            <div class="header-cell"><i class="fas fa-file-invoice-dollar"></i> Tax Credit ($/gal)</div>
            <div class="header-cell"><i class="fas fa-hand-holding-usd"></i> Total Subsidy ($M)</div>
            <div class="header-cell"><i class="fas fa-percentage"></i> Cost Recovery (%)</div>
          </div>

          <div v-for="item in selectedScenarioData" :key="item.Year" class="table-row">
            <div class="row-cell">{{ item.Year }}</div>
            <div class="row-cell">${{ item.Revenue_Drop_M ? item.Revenue_Drop_M.toFixed(2) : '0.00' }}M</div>
            <div class="row-cell">{{ formatH2Volume(item.H2_Demand_annual_gal || 0) }}</div>
            <div class="row-cell">${{ item.Req_Tax_Credit_per_gal ? item.Req_Tax_Credit_per_gal.toFixed(2) : '0.00' }}
            </div>
            <div class="row-cell">${{ calculateTotalSubsidy(item).toFixed(2) }}M</div>
            <div class="row-cell">{{ calculateCostRecovery(item).toFixed(1) }}%</div>
          </div>

          <div class="table-row total">
            <div class="row-cell"><i class="fas fa-calculator"></i> Average</div>
            <div class="row-cell">${{ calculateAverageRevenueLoss().toFixed(2) }}M</div>
            <div class="row-cell">{{ formatH2Volume(calculateTotalH2Volume()) }}</div>
            <div class="row-cell">${{ calculateAverageTaxCredit().toFixed(2) }}</div>
            <div class="row-cell">${{ calculateTotalSubsidies().toFixed(2) }}M</div>
            <div class="row-cell">{{ calculateAverageCostRecovery().toFixed(1) }}%</div>
          </div>
        </div>
      </section>

      <!-- Charts Section -->
      <!-- Charts Section with icons -->
      <section v-if="activeTab === 'charts'" class="charts-section">
        <h2><i class="fas fa-chart-bar"></i> Economic Impact Visualization</h2>

        <!-- Revenue Drop Chart -->
        <div class="chart-wrapper">
          <h3><i class="fas fa-chart-line"></i> Revenue Drop by Scenario</h3>
          <ChartComponent chartId="revenueDropChart" chartType="line" :chartData="revenueDropChartData"
            :chartOptions="revenueChartOptions" />
        </div>

        <!-- Tax Credit Chart -->
        <div class="chart-wrapper">
          <h3><i class="fas fa-file-invoice-dollar"></i> Tax Credits by Scenario</h3>
          <ChartComponent chartId="taxCreditChart" chartType="line" :chartData="taxCreditChartData"
            :chartOptions="taxCreditChartOptions" />
        </div>

        <!-- Cumulative Cost Chart -->
        <div class="chart-wrapper">
          <h3><i class="fas fa-coins"></i> Cumulative Cost Comparison</h3>
          <ChartComponent chartId="cumulativeCostChart" chartType="bar" :chartData="cumulativeCostChartData"
            :chartOptions="cumulativeCostChartOptions" />
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useEconomicsStore } from '@/store/economicsStore';
import { useHydrogenStore } from '@/store/hydrogenStore';
import { useNotificationStore } from '@/store/notificationStore';
import ChartComponent from '@/components/ChartComponent.vue';

export default {
  name: 'EconomicImpactView',

  components: {
    ChartComponent
  },

  setup() {
    const economicsStore = useEconomicsStore();
    const hydrogenStore = useHydrogenStore();
    const notificationStore = useNotificationStore();
    const selectedScenario = ref(3); // Default to 3 min/year reduction
    const activeTab = ref('details'); // Default active tab

    // Only allow user to modify turnaround time parameters
    const extraTurnTime = ref(30); // 30 minutes default
    const turnTimeDecreaseRates = ref([0, 1, 2, 3, 4, 5]); // Default scenarios

    // Form validation
    const isFormValid = computed(() => {
      return extraTurnTime.value >= 0 &&
        turnTimeDecreaseRates.value.length > 0 &&
        turnTimeDecreaseRates.value.every(rate => rate >= 0);
    });

    // Function to notify user
    const notifyUser = (message, type = 'info') => {
      notificationStore.addNotification(message, type);
    };

    // Format timestamp function
    const formatTimestamp = (timestamp) => {
      if (!timestamp) return 'Never';

      const date = new Date(timestamp);
      return new Intl.DateTimeFormat('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      }).format(date);
    };

    // Add handler for toggle change
    const handleAutoRecalculateChange = (event) => {
      economicsStore.setAutoRecalculate(event.target.checked);
    };

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
      economicsStore.resetResults();
    };

    // Get the selected scenario data
    const selectedScenarioData = computed(() => {
      if (!economicsStore.results || !economicsStore.results.scenarios) return [];
      return economicsStore.results.scenarios[selectedScenario.value] || [];
    });

    // Helper functions for scenario summary
    const getMaxTaxCredit = (rate) => {
      if (!economicsStore.results || !economicsStore.results.scenarios) return '0.00';
      const data = economicsStore.results.scenarios[rate] || [];
      if (data.length === 0) return '0.00';

      const maxCredit = Math.max(...data.map(item => item.Req_Tax_Credit_per_gal || 0));
      return maxCredit.toFixed(2);
    };

    const getTaxCreditPeakYear = (rate) => {
      if (!economicsStore.results || !economicsStore.results.scenarios) return '';
      const data = economicsStore.results.scenarios[rate] || [];
      if (data.length === 0) return '';

      const maxCredit = Math.max(...data.map(item => item.Req_Tax_Credit_per_gal || 0));
      const peakItem = data.find(item => (item.Req_Tax_Credit_per_gal || 0) === maxCredit);
      return peakItem ? peakItem.Year : '';
    };

    const getMaxRevenueDrop = (rate) => {
      if (!economicsStore.results || !economicsStore.results.scenarios) return '0.00';
      const data = economicsStore.results.scenarios[rate] || [];
      if (data.length === 0) return '0.00';

      const maxDrop = Math.max(...data.map(item => item.Pct_Drop || 0));
      return maxDrop.toFixed(2);
    };

    const getRevenueDropPeakYear = (rate) => {
      if (!economicsStore.results || !economicsStore.results.scenarios) return '';
      const data = economicsStore.results.scenarios[rate] || [];
      if (data.length === 0) return '';

      const maxDrop = Math.max(...data.map(item => item.Pct_Drop || 0));
      const peakItem = data.find(item => (item.Pct_Drop || 0) === maxDrop);
      return peakItem ? peakItem.Year : '';
    };

    const getCumulativeCost = (rate) => {
      if (!economicsStore.results || !economicsStore.results.scenarios) return '0.00';
      const data = economicsStore.results.scenarios[rate] || [];
      if (data.length === 0) return '0.00';

      const totalCost = data.reduce((sum, item) => {
        const revenueLoss = (item.Baseline_Revenue_M || 0) - (item.Hydrogen_Revenue_M || 0);
        return sum + revenueLoss;
      }, 0);
      return totalCost.toFixed(2);
    };

    // Helper functions for tax credit summary calculations
    const calculateAverageRevenueLoss = () => {
      if (!selectedScenarioData.value || selectedScenarioData.value.length === 0) return 0;
      const total = selectedScenarioData.value.reduce((sum, item) => sum + (item.Revenue_Drop_M || 0), 0);
      return total / selectedScenarioData.value.length;
    };

    const calculateTotalH2Volume = () => {
      if (!selectedScenarioData.value || selectedScenarioData.value.length === 0) return 0;
      return selectedScenarioData.value.reduce((sum, item) => sum + (item.H2_Demand_annual_gal || 0), 0);
    };

    const calculateAverageTaxCredit = () => {
      if (!selectedScenarioData.value || selectedScenarioData.value.length === 0) return 0;
      const total = selectedScenarioData.value.reduce((sum, item) => sum + (item.Req_Tax_Credit_per_gal || 0), 0);
      return total / selectedScenarioData.value.length;
    };

    const calculateTotalSubsidies = () => {
      if (!selectedScenarioData.value || selectedScenarioData.value.length === 0) return 0;
      return selectedScenarioData.value.reduce((sum, item) => sum + calculateTotalSubsidy(item), 0);
    };

    const calculateAverageCostRecovery = () => {
      if (!selectedScenarioData.value || selectedScenarioData.value.length === 0) return 0;

      const validItems = selectedScenarioData.value.filter(item => (item.Revenue_Drop_M || 0) > 0);
      if (validItems.length === 0) return 0;

      const total = validItems.reduce((sum, item) => sum + calculateCostRecovery(item), 0);
      return total / validItems.length;
    };

    // Helper functions for tax credit table
    const calculateRevenueLoss = (item) => {
      return (item.Baseline_Revenue_M || 0) - (item.Hydrogen_Revenue_M || 0);
    };

    const formatH2Volume = (volume) => {
      if (!volume) return '0';
      if (volume >= 1000000) {
        return `${(volume / 1000000).toFixed(2)}M gal`;
      } else if (volume >= 1000) {
        return `${(volume / 1000).toFixed(2)}K gal`;
      }
      return `${volume.toFixed(2)} gal`;
    };

    const calculateTotalSubsidy = (item) => {
      return (item.Req_Tax_Credit_per_gal || 0) * (item.H2_Demand_annual_gal || 0) / 1000000; // Convert to millions
    };

    const calculateCostRecovery = (item) => {
      const revenueLoss = item.Revenue_Drop_M || 0;
      if (revenueLoss <= 0) return 0;

      const subsidy = calculateTotalSubsidy(item);
      return (subsidy / revenueLoss) * 100;
    };

    // Function to select a scenario
    const selectScenario = (rate) => {
      selectedScenario.value = rate;
    };

    // Export current scenario data
    const exportCurrentScenario = () => {
      try {
        const csvData = economicsStore.exportScenarioData(selectedScenario.value);
        const blob = new Blob([csvData], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.setAttribute('hidden', '');
        a.setAttribute('href', url);
        a.setAttribute('download', `scenario_${selectedScenario.value}_min_per_year.csv`);
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } catch (error) {
        console.error('Error exporting data:', error);
        alert('Failed to export data: ' + error.message);
      }
    };

    // Simplified calculation function with only turnaround parameters
    const calculateEconomicImpact = async () => {
      if (!isFormValid.value) return;

      await economicsStore.fetchEconomicImpact({
        extraTurnTime: extraTurnTime.value,
        turnTimeDecreaseRates: turnTimeDecreaseRates.value,
        // Use hydrogen store values for other parameters
        fleetPercentage: hydrogenStore.fleetPercentage / 100, // Convert from percentage to decimal
        startYear: economicsStore.startYear,
        endYear: hydrogenStore.year,
        finalH2Year: hydrogenStore.year
      });

      // Store calculation timestamp
      economicsStore.lastCalculationTime = new Date();
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

      const datasets = Object.entries(scenarios).map(([rate, data]) => {
        return {
          label: `${rate} min/year reduction`,
          data: data.map(item => item.Req_Tax_Credit_per_gal || 0),
          borderColor: getColorForRate(parseInt(rate)),
          backgroundColor: getColorForRate(parseInt(rate), 0.2),
          borderWidth: parseInt(rate) === selectedScenario.value ? 3 : 1,
        };
      });

      return { labels, datasets };
    });

    // Cumulative Cost Chart Data
    const cumulativeCostChartData = computed(() => {
      if (!economicsStore.results || !economicsStore.results.scenarios) return { labels: [], datasets: [] };

      const scenarios = economicsStore.results.scenarios;
      const labels = Object.keys(scenarios).map(rate => `${rate} min/year`);

      const cumulativeCosts = Object.entries(scenarios).map(([rate, data]) => {
        return data.reduce((sum, item) => {
          const revenueLoss = (item.Baseline_Revenue_M || 0) - (item.Hydrogen_Revenue_M || 0);
          return sum + revenueLoss;
        }, 0);
      });

      const datasets = [{
        label: 'Cumulative Cost ($M)',
        data: cumulativeCosts,
        backgroundColor: Object.keys(scenarios).map(rate => getColorForRate(parseInt(rate), 0.7)),
        borderColor: Object.keys(scenarios).map(rate => getColorForRate(parseInt(rate))),
        borderWidth: 1
      }];

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
          text: 'Tax Credits vs. Year for Different Turn-Time Reduction Rates'
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
            text: 'Tax Credit ($/gal)'
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

    const cumulativeCostChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: 'Cumulative Cost by Scenario'
        },
        tooltip: {
          callbacks: {
            label: (context) => `${context.label}: $${context.raw.toFixed(2)}M`
          }
        }
      },
      scales: {
        y: {
          title: {
            display: true,
            text: 'Cumulative Cost ($M)'
          },
          beginAtZero: true
        }
      }
    };

    // Watch for changes in hydrogen demand data
    watch(
      [
        () => hydrogenStore.totalH2Demand,
        () => hydrogenStore.fleetPercentage,
        () => hydrogenStore.year,
      ],
      async ([newH2Demand, newFleetPercentage, newYear], [oldH2Demand, oldFleetPercentage, oldYear]) => {
        // Only trigger if auto-recalculate is enabled
        if (economicsStore.autoRecalculate) {
          // Check if any value actually changed
          if (newH2Demand !== oldH2Demand ||
            newFleetPercentage !== oldFleetPercentage ||
            newYear !== oldYear) {
            console.log('Auto-recalculating due to hydrogen data change');
            // Make sure we have valid parameters before calculating
            if (isFormValid.value) {
              await calculateEconomicImpact();
              notifyUser('Economic calculations automatically updated', 'info');
            }
          }
        }
      },
      { deep: true, immediate: true } // Add immediate: true to run on component mount
    );

    // Check for data consistency on component mount
    onMounted(() => {
      // If economic results exist but are based on different hydrogen data
      if (economicsStore.results && economicsStore.lastParams) {
        const currentTotalH2Demand = parseFloat(hydrogenStore.totalH2Demand || 0);
        const currentFleetPercentage = hydrogenStore.fleetPercentage / 100 || 0.1;
        const currentYear = hydrogenStore.year || 2036;

        // Check if current hydrogen data matches the data used for economic calculations
        if (
          currentTotalH2Demand !== economicsStore.lastParams.totalH2Demand ||
          currentFleetPercentage !== economicsStore.lastParams.fleetPercentage ||
          currentYear !== economicsStore.lastParams.endYear
        ) {
          // Reset economic calculations if data is inconsistent
          economicsStore.resetResults();
          // Optional: Show notification to user
          // notifyUser('Hydrogen parameters have changed. Please recalculate economic impact.');
        }
      }
    });

    // Check if data is consistent
    const isDataConsistent = computed(() => {
      if (!economicsStore.results || !economicsStore.lastParams) return true;

      const currentTotalH2Demand = parseFloat(hydrogenStore.totalH2Demand || 0);
      const currentFleetPercentage = hydrogenStore.fleetPercentage / 100 || 0.1;
      const currentYear = hydrogenStore.year || 2036;

      return (
        currentTotalH2Demand === economicsStore.lastParams.totalH2Demand &&
        currentFleetPercentage === economicsStore.lastParams.fleetPercentage &&
        currentYear === economicsStore.lastParams.endYear
      );
    });

    // Watch for data consistency changes
    watch(isDataConsistent, (newValue) => {
      if (!newValue) {
        notifyUser('Hydrogen parameters have changed. Please recalculate economic impact.', 'warning');
      }
    });

    return {
      economicsStore,
      hydrogenStore,
      notifyUser,
      isDataConsistent,
      selectedScenario,
      selectedScenarioData,
      activeTab,
      revenueDropChartData,
      taxCreditChartData,
      cumulativeCostChartData,
      revenueChartOptions,
      taxCreditChartOptions,
      cumulativeCostChartOptions,
      selectScenario,
      calculateEconomicImpact,
      // Only turnaround time parameters
      extraTurnTime,
      turnTimeDecreaseRates,
      // Other required properties
      isFormValid,
      addScenario,
      removeScenario,
      resetCalculation,
      exportCurrentScenario,
      // Helper functions
      getMaxTaxCredit,
      getTaxCreditPeakYear,
      getMaxRevenueDrop,
      getRevenueDropPeakYear,
      getCumulativeCost,
      calculateRevenueLoss,
      formatH2Volume,
      calculateTotalSubsidy,
      calculateCostRecovery,
      calculateAverageRevenueLoss,
      calculateTotalH2Volume,
      calculateAverageTaxCredit,
      calculateTotalSubsidies,
      calculateAverageCostRecovery,
      handleAutoRecalculateChange,
      formatTimestamp
    };
  }
}
</script>

<style scoped>
/* =========================
   Global & Utility Styles
   ========================= */
.economic-impact-view {
  margin-bottom: 30px;
  color: #ddd;
}

/* =========================
   Headings
   ========================= */
h1,
h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #64ffda;
  font-size: 1.5rem;
  font-weight: 600;
}

h1 {
  font-size: 1.8rem;
  margin-bottom: 25px;
}

h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #ddd;
  font-size: 1.1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 0.5rem;
}

/* =========================
   Alerts & Feedback Messages
   ========================= */
.error-container {
  border-left: 4px solid #e74c3c;
  color: #e74c3c;
  background-color: rgba(255, 99, 132, 0.1);
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.alert {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 6px;
  margin-bottom: 25px;
}

.alert.info {
  background-color: rgba(54, 162, 235, 0.1);
  border-left: 4px solid rgba(54, 162, 235, 0.8);
  color: #ddd;
}

.alert i {
  margin-right: 10px;
  font-size: 1.2rem;
}

.no-data-container {
  color: #aaa;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 20px;
}

/* =========================
   Loading & Spinner
   ========================= */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #64ffda;
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

/* =========================
   Button Styles
   ========================= */
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn.primary {
  background-color: #64ffda;
  color: #1a1e24;
}

.btn.secondary {
  background-color: rgba(255, 255, 255, 0.1);
  color: #ddd;
}

.btn:hover {
  transform: translateY(-2px);
}

.btn.primary:hover {
  background-color: #73ffde;
}

.btn.secondary:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

.btn.remove {
  background-color: transparent;
  color: #ff6384;
  padding: 5px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn.warning {
  background-color: rgba(255, 152, 0, 0.1);
  border: 1px solid #ff9800;
  color: #ff9800;
}

.btn.warning:hover {
  background-color: rgba(255, 152, 0, 0.2);
}

/* =========================
   Form Elements
   ========================= */
.parameters-section {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 25px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #ddd;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: #fff;
}

.form-group small {
  display: block;
  margin-top: 5px;
  color: #aaa;
  font-size: 0.85rem;
}

.form-actions {
  margin-top: 25px;
}

/* =========================
   Scenario Configuration
   ========================= */
.scenario-config {
  margin-top: 25px;
}

.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.scenario-input {
  display: flex;
  align-items: center;
  gap: 10px;
  background-color: rgba(255, 255, 255, 0.03);
  padding: 12px;
  border-radius: 6px;
}

.scenario-input input {
  width: 60px;
  padding: 6px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: #fff;
  text-align: center;
}

.scenario-actions {
  margin-top: 15px;
}

/* =========================
   Results Container
   ========================= */
.results-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.recalculate-container {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.calculation-params {
  background-color: rgba(255, 255, 255, 0.03);
  border-radius: 6px;
  padding: 15px;
  margin-bottom: 20px;
  color: #aaa;
  font-size: 0.9rem;
}

/* =========================
   Scenario Comparison
   ========================= */
.scenario-comparison {
  margin-bottom: 30px;
}

.comparison-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.comparison-card {
  flex: 1;
  min-width: 200px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.2s;
}

.comparison-card:hover {
  transform: translateY(-3px);
  background-color: rgba(255, 255, 255, 0.08);
}

.comparison-card.selected {
  background-color: rgba(100, 255, 218, 0.1);
  border-left: 4px solid #64ffda;
}

.comparison-card h3 {
  margin: 0 0 10px 0;
  color: #ddd;
  font-size: 1.1rem;
  border-bottom: none;
  padding-bottom: 0;
}

.card-metrics {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.metric {
  display: flex;
  justify-content: space-between;
}

.metric-label {
  color: #aaa;
  font-size: 0.9rem;
}

.metric-value {
  color: #64ffda;
  font-weight: 600;
}

/* =========================
   Scenario Summary
   ========================= */
.scenario-summary {
  margin-bottom: 30px;
}

.summary-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.metric-card {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
}

.metric-card h3 {
  margin: 0 0 15px 0;
  color: #aaa;
  font-size: 1rem;
  border-bottom: none;
  padding-bottom: 0;
}

.metric-card .metric-value {
  color: #64ffda;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 5px;
}

.metric-card .metric-year {
  color: #aaa;
  font-size: 0.85rem;
}

/* =========================
   Tabs
   ========================= */
.data-tabs {
  display: flex;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 20px;
}

.tab-button {
  padding: 10px 20px;
  background: none;
  border: none;
  color: #aaa;
  cursor: pointer;
  font-size: 1rem;
  position: relative;
  transition: color 0.2s;
}

.tab-button:hover {
  color: #ddd;
}

.tab-button.active {
  color: #64ffda;
}

.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: #64ffda;
}

/* =========================
   Table
   ========================= */
.table-container {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 25px;
}

.taxCredits-section .table-header,
.taxCredits-section .table-row {
  display: grid;
  grid-template-columns: 0.7fr 1fr 1.2fr 1fr 1fr 1fr;
}

.details-section .table-header,
.details-section .table-row {
  display: grid;
  grid-template-columns: 0.7fr 1fr 1fr 1fr 1.2fr 1.2fr 1fr;
}

.table-header {
  background-color: rgba(255, 255, 255, 0.05);
  padding: 12px 15px;
  border-radius: 6px 6px 0 0;
  font-weight: 600;
  color: #ddd;
}

.table-row {
  padding: 12px 15px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: #aaa;
}

.table-row:last-child {
  border-bottom: none;
}

.table-row.total {
  background-color: rgba(100, 255, 218, 0.05);
  color: #64ffda;
  font-weight: 600;
  border-radius: 0 0 6px 6px;
}

.header-cell,
.row-cell {
  padding: 0 10px;
}

/* =========================
   Charts
   ========================= */
.charts-section {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.chart-wrapper {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
  height: 400px;
}

.chart-wrapper h3 {
  text-align: center;
  margin-bottom: 20px;
}

/* =========================
   Responsive Adjustments
   ========================= */
@media (max-width: 1024px) {
  .summary-metrics {
    grid-template-columns: 1fr 1fr;
  }

  .comparison-cards {
    flex-direction: column;
  }

  .comparison-card {
    min-width: 100%;
  }
}

@media (max-width: 768px) {
  .summary-metrics {
    grid-template-columns: 1fr;
  }

  .taxCredits-section .table-header,
  .taxCredits-section .table-row {
    grid-template-columns: 1fr 1fr 1fr;
  }

  .details-section .table-header,
  .details-section .table-row {
    grid-template-columns: 1fr 1fr 1fr;
  }

  .table-container {
    overflow-x: auto;
  }
}

/* Icon styling */
.header-cell i,
h2 i,
h3 i,
.btn i,
.metric-label i,
.card-icon i {
  margin-right: 8px;
  width: 16px;
  text-align: center;
}

.table-header .header-cell i {
  color: #64ffda;
  opacity: 0.8;
}

h2 i {
  color: #64ffda;
}

h3 i {
  color: #ddd;
}

.metric-card h3 i {
  color: #64ffda;
  background-color: rgba(100, 255, 218, 0.1);
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
}

.table-row.total i {
  color: #64ffda;
}

/* Fix for FontAwesome hydrogen icon which might not exist */
.fas.fa-hydrogen:before {
  content: "\f12b";
  /* Use atom icon as fallback */
}

.data-consistency-indicator {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  padding: 12px 15px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: #ddd;
}

.calculation-timestamp {
  display: flex;
  align-items: center;
  font-size: 0.9rem;
  color: #aaa;
  margin-right: auto;
}

.calculation-timestamp i {
  color: #64ffda;
  margin-right: 8px;
}

.indicator {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.9rem;
  background-color: rgba(255, 255, 255, 0.03);
}

.indicator i {
  margin-right: 8px;
}

.indicator.consistent {
  color: #64ffda;
}

.indicator.consistent i {
  color: #64ffda;
}

.indicator.inconsistent {
  color: #ff9800;
}

.indicator.inconsistent i {
  color: #ff9800;
}

/* =========================
   Auto-recalculate Option
   ========================= */
.auto-recalculate-option {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 12px 15px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: #ddd;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
  margin-right: 10px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.1);
  transition: .4s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: #64ffda;
  transition: .4s;
  border-radius: 50%;
}

input:checked+.toggle-slider {
  background-color: rgba(100, 255, 218, 0.2);
}

input:checked+.toggle-slider:before {
  transform: translateX(26px);
}

.toggle-label {
  font-size: 0.9rem;
  color: #aaa;
}
</style>