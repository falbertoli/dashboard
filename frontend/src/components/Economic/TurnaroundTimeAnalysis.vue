<!-- File: frontend/src/components/Economic/TurnaroundTimeAnalysis.vue -->

<template>
  <!-- Alert shown when no hydrogen data is available -->
  <div
    v-if="!hydrogenStore.aircraftH2Demand || !hydrogenStore.gseH2Demand"
    class="alert info"
  >
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
    <p>
      No hydrogen demand data available. Please calculate hydrogen demand first.
    </p>
    <router-link to="/hydrogen" class="btn primary">
      <i class="fas fa-arrow-right"></i> Go to Hydrogen Demand
    </router-link>
  </div>

  <div v-else>
    <!-- Add description section -->
    <div class="explanation-section">
      <h2><i class="fas fa-info-circle"></i> About Turnaround Time Analysis</h2>

      <div class="explanation-tabs">
        <button
          v-for="(tab, index) in explanationTabs"
          :key="index"
          :class="[
            'explanation-tab',
            { active: activeExplanationTab === index },
          ]"
          @click="activeExplanationTab = index"
        >
          <i :class="tab.icon"></i>
          {{ tab.title }}
          <span class="tab-indicator"></span>
        </button>
      </div>

      <div class="explanation-content">
        <!-- Time Impact Tab -->
        <div v-show="activeExplanationTab === 0" class="explanation-panel">
          <div class="explanation-item">
            <div class="item-header">
              <i class="fas fa-clock"></i>
              <h3>Extra Turnaround Time</h3>
            </div>
            <div class="item-content">
              <p>
                The additional time (in minutes) required for hydrogen aircraft
                refueling compared to conventional jet fuel. This represents the
                initial technology maturity level in the start year.
              </p>
              <div class="visual-indicators">
                <div
                  class="visual-indicator"
                  title="Starting impact on operations"
                >
                  <i class="fas fa-level-up-alt"></i>
                  <span>Initial Impact: Higher Turnaround Time</span>
                  <div class="indicator-graphic">
                    <div class="bar-container">
                      <div class="bar high"></div>
                      <span class="label">Start</span>
                    </div>
                  </div>
                </div>
                <div
                  class="visual-indicator"
                  title="Technology improvement over time"
                >
                  <i class="fas fa-chart-line"></i>
                  <span>Gradual Improvement</span>
                  <div class="indicator-graphic">
                    <div class="trend-line">
                      <div class="point start"></div>
                      <div class="line"></div>
                      <div class="point end"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="explanation-item">
            <div class="item-header">
              <i class="fas fa-chart-line"></i>
              <h3>Annual Reduction Rate</h3>
            </div>
            <p>
              Measured in minutes per operation annually (annual min/ops), this
              rate represents how quickly refueling technology improves. For
              example, a rate of 3 annual min/ops means the extra turnaround
              time decreases by 3 minutes per operation each year as efficiency
              improves.
            </p>
          </div>
        </div>

        <!-- Financial Impact Tab -->
        <div v-show="activeExplanationTab === 1" class="explanation-panel">
          <div class="explanation-item">
            <h3><i class="fas fa-percent"></i> Revenue Impact</h3>
            <p>
              Shows the percentage decrease in revenue due to longer turnaround
              times. This is calculated based on reduced daily flight capacity
              and fleet percentage ({{ hydrogenStore.fleetPercentage }}%).
            </p>
          </div>
          <div class="explanation-item">
            <h3>
              <i class="fas fa-dollar-sign"></i> Equivalent Subsidy Requirements
            </h3>
            <p>
              The required subsidy ($/gallon) to offset revenue losses. Based on
              hydrogen demand ({{ $formatNumber(hydrogenStore.totalH2Demand) }}
              ft³/day) and revenue impact.
            </p>
          </div>
        </div>

        <!-- Key Metrics Tab -->
        <div v-show="activeExplanationTab === 2" class="explanation-panel">
          <div class="metrics-grid">
            <div class="metric-item">
              <h4><i class="fas fa-star"></i> Peak Subsidy</h4>
              <p>
                Maximum required subsidy equivalent needed per gallon of
                hydrogen fuel during the transition period
              </p>
            </div>
            <div class="metric-item">
              <h4><i class="fas fa-chart-line"></i> Min Revenue Impact</h4>
              <p>
                Smallest percentage drop in revenue across the analysis period
              </p>
            </div>
            <div class="metric-item">
              <h4><i class="fas fa-coins"></i> Cumulative Cost</h4>
              <p>
                Total revenue loss in millions of dollars through
                {{ hydrogenStore.year }}
              </p>
            </div>
            <div class="metric-item">
              <h4><i class="fas fa-percentage"></i> Cost Recovery</h4>
              <p>Percentage of revenue loss offset by subsidies equivalent</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add assumptions section -->
    <div class="assumptions-section">
      <h2><i class="fas fa-clipboard-check"></i> Model Assumptions</h2>
      <div class="assumptions-tabs">
        <button
          v-for="(tab, index) in assumptionTabs"
          :key="index"
          :class="['assumption-tab', { active: activeAssumptionTab === index }]"
          @click="activeAssumptionTab = index"
        >
          <i :class="tab.icon"></i>
          {{ tab.title }}
        </button>
      </div>

      <div class="assumptions-content">
        <div v-show="activeAssumptionTab === 0" class="assumption-list">
          <div class="assumption-item">
            <i class="fas fa-check-circle"></i>
            <span>Only extra turnaround time impact on revenue considered</span>
          </div>
          <div class="assumption-item">
            <i class="fas fa-check-circle"></i>
            <span>Total utilization is scalable</span>
          </div>
          <div class="assumption-item">
            <i class="fas fa-check-circle"></i>
            <span>Revenue is Scalable</span>
          </div>
          <div class="assumption-item">
            <i class="fas fa-check-circle"></i>
            <span
              >Extra turnaround from the destination airport considered</span
            >
          </div>
        </div>

        <div v-show="activeAssumptionTab === 1" class="assumption-list">
          <div class="assumption-item">
            <i class="fas fa-check-circle"></i>
            <span
              >Average Extra Turnaround Time for all hydrogen powered
              aircrafts</span
            >
          </div>
          <div class="assumption-item">
            <i class="fas fa-check-circle"></i>
            <span
              >Required subsidies equivalent to compensate only for the
              turnaround time impact</span
            >
          </div>
        </div>

        <div v-show="activeAssumptionTab === 2" class="assumption-list">
          <div class="assumption-item">
            <i class="fas fa-check-circle"></i>
            <span>Fixed Subsidy Equivalent Rate</span>
          </div>
          <div class="assumption-item">
            <i class="fas fa-check-circle"></i>
            <span>No maximum credit limit</span>
          </div>
          <div class="assumption-item">
            <i class="fas fa-check-circle"></i>
            <span
              >Annual reduction in turnaround time per flight until Jet A
              aircraft levels</span
            >
          </div>
        </div>
      </div>
    </div>

    <!-- Add auto-recalculate option here -->
    <div class="auto-recalculate-option">
      <label class="toggle-switch">
        <input
          type="checkbox"
          v-model="economicsStore.autoRecalculate"
          @change="handleAutoRecalculateChange"
        />
        <span class="toggle-slider"></span>
      </label>
      <span class="toggle-label"
        >Auto-recalculate when hydrogen data changes</span
      >
    </div>

    <!-- Always show calculation parameters -->
    <div class="calculation-params">
      <h3><i class="fas fa-cog"></i> Calculation Parameters</h3>
      <div class="params-grid">
        <div class="param-item">
          <span class="param-label">Fleet Percentage:</span>
          <span class="param-value"
            >{{ $formatNumber(hydrogenStore.fleetPercentage) }}%</span
          >
          <span class="param-note">(from Hydrogen Demand)</span>
        </div>
        <div class="param-item">
          <span class="param-label">Growth Rate:</span>
          <span class="param-value">{{ $formatNumber(2.0) }}%</span>
          <span class="param-note">(fixed)</span>
        </div>
        <div class="param-item">
          <span class="param-label">Initial Extra Turn Time:</span>
          <span class="param-value">{{ extraTurnTime }} minutes</span>
          <span class="param-note">(user input)</span>
        </div>
        <div class="param-item">
          <span class="param-label">Years:</span>
          <span class="param-value"
            >{{ economicsStore.startYear }} - {{ hydrogenStore.year }}</span
          >
        </div>
      </div>
    </div>

    <div class="data-consistency-indicator" v-if="economicsStore.results">
      <div
        class="calculation-timestamp"
        v-if="economicsStore.results && economicsStore.lastCalculationTime"
      >
        <i class="fas fa-clock"></i>
        <span
          >Last calculated:
          {{ formatTimestamp(economicsStore.lastCalculationTime) }}</span
        >
      </div>
      <div
        class="indicator"
        :class="{
          consistent: isDataConsistent,
          inconsistent: !isDataConsistent,
        }"
      >
        <i
          :class="
            isDataConsistent
              ? 'fas fa-check-circle'
              : 'fas fa-exclamation-triangle'
          "
        ></i>
        <span
          >Data {{ isDataConsistent ? "is consistent" : "has changed" }}</span
        >
      </div>
      <button
        v-if="!isDataConsistent"
        @click="calculateEconomicImpact"
        class="btn warning"
      >
        <i class="fas fa-sync"></i> Recalculate
      </button>
    </div>

    <div class="parameters-description" v-if="!economicsStore.results">
      <p>
        <strong>Economic Model Parameters:</strong> This model calculates the
        economic impact of hydrogen adoption based on the hydrogen demand you
        calculated. The key variable is the extra turnaround time required for
        hydrogen aircraft and how quickly this time decreases as the technology
        matures.
      </p>
      <p>
        <strong>Fixed Parameters:</strong> Fleet percentage ({{
          hydrogenStore.fleetPercentage
        }}%), projection year ({{ hydrogenStore.year }}), and growth rate (2%)
        are derived from your hydrogen demand calculation.
      </p>
    </div>

    <div class="parameters-section" v-if="!economicsStore.results">
      <h2><i class="fas fa-sliders-h"></i> Turnaround Time Parameters</h2>

      <div class="form-group">
        <div class="extraTurnTime-container">
          <div class="extraTurnTime">
            <label for="extraTurnTime">Initial Extra Turnaround Time:</label>
            <input
              type="number"
              id="extraTurnTime"
              v-model.number="extraTurnTime"
              min="0"
              max="60"
            />
            <span>minutes</span>
          </div>
        </div>
        <small
          >Additional turnaround time required for hydrogen aircraft compared to
          conventional aircraft</small
        >
      </div>

      <div class="scenario-config">
        <h3>
          <i class="fas fa-layer-group"></i> Turnaround Time Reduction Scenarios
        </h3>
        <p>
          Define different annual reduction rates (minutes/year) as hydrogen
          refueling technology matures:
        </p>

        <div class="scenarios-grid">
          <div
            v-for="(rate, index) in turnTimeDecreaseRates"
            :key="index"
            class="scenario-input"
          >
            <label :for="`scenario${index}`">Scenario {{ index + 1 }}:</label>
            <input
              :id="`scenario${index}`"
              type="number"
              v-model.number="turnTimeDecreaseRates[index]"
              min="0"
              max="10"
              step="1"
            />
            <span>annual min/ops</span>
            <button
              v-if="index > 0"
              @click="removeScenario(index)"
              class="btn remove"
              title="Remove scenario"
            >
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
        <button
          @click="calculateEconomicImpact"
          class="btn primary"
          :disabled="!isFormValid"
        >
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
          <div
            v-for="scenario in economicsStore.scenarioComparison"
            :key="scenario.rate"
            class="comparison-card"
            :class="{ selected: selectedScenario === scenario.rate }"
            @click="selectScenario(scenario.rate)"
          >
            <h3>
              <i class="fas fa-tachometer-alt"></i> {{ scenario.rate }} annual
              improvements min/ops
            </h3>
            <div class="card-metrics">
              <div class="metric">
                <span class="metric-label"
                  ><i class="fas fa-dollar-sign"></i> Max Subsidy
                  Equivalent</span
                >
                <span class="metric-value">{{ scenario.maxTaxCredit }}</span>
              </div>
              <div class="metric">
                <span class="metric-label"
                  ><i class="fas fa-chart-line"></i> Min Revenue Drop</span
                >
                <span class="metric-value">{{ scenario.maxRevenueDrop }}</span>
              </div>
              <div class="metric">
                <span class="metric-label"
                  ><i class="fas fa-money-bill-wave"></i> Final Subsidy
                  Equivalent</span
                >
                <span class="metric-value">{{
                  scenario.finalYearTaxCredit
                }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Selected Scenario Summary -->
      <section class="scenario-summary">
        <h2>
          <i class="fas fa-chart-pie"></i> {{ selectedScenario }} annual min/ops
          Scenario Summary
        </h2>
        <div class="summary-metrics">
          <div class="metric-card">
            <h3><i class="fas fa-dollar-sign"></i> Peak Subsidy Equivalent</h3>
            <p class="metric-value">
              ${{ $formatNumber(getMaxTaxCredit(selectedScenario), 2) }}/gal
            </p>
            <p class="metric-year">
              in {{ getTaxCreditPeakYear(selectedScenario) }}
            </p>
          </div>
          <div class="metric-card">
            <h3><i class="fas fa-chart-line"></i> Min Revenue Impact</h3>
            <p class="metric-value">
              {{ $formatNumber(getMaxRevenueDrop(selectedScenario), 2) }}%
            </p>
            <p class="metric-year">
              in {{ getRevenueDropPeakYear(selectedScenario) }}
            </p>
          </div>
          <div class="metric-card">
            <h3><i class="fas fa-coins"></i> Cumulative Cost</h3>
            <p class="metric-value">
              ${{ $formatNumber(getCumulativeCost(selectedScenario)) }}M
            </p>
            <p class="metric-year">through {{ hydrogenStore.year }}</p>
          </div>
        </div>
      </section>

      <!-- Tabs for different data views -->
      <div class="data-tabs">
        <button
          v-for="tab in dataTabs"
          :key="tab.id"
          :class="['tab-button', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          <i :class="tab.icon"></i>
          <span>{{ tab.label }}</span>
        </button>
      </div>

      <!-- Detailed Results Table -->
      <section v-if="activeTab === 'details'" class="details-section">
        <h2>
          <i class="fas fa-table"></i> Detailed Results for
          {{ selectedScenario }} annual min/ops Scenario
        </h2>
        <div class="table-container details-table">
          <div class="table-header">
            <div class="header-cell">
              <i class="fas fa-calendar-alt"></i> Year
            </div>
            <div class="header-cell">
              <i class="fas fa-chart-line"></i> Growth Factor
            </div>
            <div class="header-cell">
              <i class="fas fa-clock"></i> Turn Time (min)
            </div>
            <div class="header-cell">
              <i class="fas fa-plane"></i> H2 Flights (%)
            </div>
            <div class="header-cell">
              <i class="fas fa-dollar-sign"></i> Baseline Revenue ($M)
            </div>
            <div class="header-cell">
              <i class="fas fa-hydrogen"></i> H2 Revenue ($M)
            </div>
            <div class="header-cell">
              <i class="fas fa-chart-area"></i> Revenue Drop (%)
            </div>
          </div>

          <div
            v-for="item in selectedScenarioData"
            :key="item.Year"
            class="table-row"
          >
            <div class="row-cell">{{ item.Year }}</div>
            <div class="row-cell">
              {{ $formatNumber(item.Growth_Factor, 2) }}
            </div>
            <div class="row-cell">{{ $formatNumber(item.Turn_Time_min) }}</div>
            <div class="row-cell">
              {{ $formatNumber(item.Fraction_Flights_H2 * 100) }}%
            </div>
            <div class="row-cell">
              ${{ $formatNumber(item.Baseline_Revenue_M, 2) }}M
            </div>
            <div class="row-cell">
              ${{ $formatNumber(item.Hydrogen_Revenue_M, 2) }}M
            </div>
            <div class="row-cell">{{ $formatNumber(item.Pct_Drop, 2) }}%</div>
          </div>
        </div>
      </section>

      <!-- Subsidies Equivalent Table -->
      <section v-if="activeTab === 'taxCredits'" class="taxCredits-section">
        <h2>
          <i class="fas fa-receipt"></i> Required equivalent subsidies for
          {{ selectedScenario }} annual min/ops Scenario
        </h2>
        <div class="table-container taxCredits-table">
          <div class="table-header">
            <div class="header-cell">
              <i class="fas fa-calendar-alt"></i> Year
            </div>
            <div class="header-cell">
              <i class="fas fa-arrow-down"></i> Revenue Loss ($M)
            </div>
            <div class="header-cell">
              <i class="fas fa-gas-pump"></i> H2 Volume (gal)
            </div>
            <div class="header-cell">
              <i class="fas fa-file-invoice-dollar"></i> Required subsidy cost
              recovery ($/gal)
            </div>
            <!-- <div class="header-cell"><i class="fas fa-hand-holding-usd"></i> Total Subsidy ($M)</div> -->
            <!-- <div class="header-cell"><i class="fas fa-percentage"></i> Cost Recovery (%)</div> -->
          </div>

          <div
            v-for="item in selectedScenarioData"
            :key="item.Year"
            class="table-row"
          >
            <div class="row-cell">{{ item.Year }}</div>
            <div class="row-cell">
              ${{ $formatNumber(item.Revenue_Drop_M || 0, 2) }}M
            </div>
            <div class="row-cell">
              {{
                formatH2Volume(
                  $formatCompactNumber(item.H2_Demand_annual_gal) || 0
                )
              }}
            </div>
            <div class="row-cell">
              ${{ $formatNumber(item.Req_Tax_Credit_per_gal || 0, 2) }}
            </div>
            <!-- <div class="row-cell">${{ $formatNumber(calculateTotalSubsidy(item)) }}M</div> -->
            <!-- <div class="row-cell">{{ $formatNumber(calculateCostRecovery(item)) }}%</div> -->
          </div>

          <div class="table-row total">
            <div class="row-cell">
              <i class="fas fa-calculator"></i> Average
            </div>
            <div class="row-cell">
              ${{ $formatNumber(calculateAverageRevenueLoss(), 2) }}M
            </div>
            <div class="row-cell">
              {{
                formatH2Volume($formatCompactNumber(calculateAverageH2Volume()))
              }}
            </div>
            <div class="row-cell">
              ${{ $formatNumber(calculateAverageTaxCredit(), 2) }}
            </div>
            <!-- <div class="row-cell">${{ $formatNumber(calculateTotalSubsidies()) }}M</div>
            <div class="row-cell">{{ $formatNumber(calculateAverageCostRecovery()) }}%</div> -->
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
          <p class="chart-description">
            Shows how revenue decreases over time for different turnaround time
            improvement rates. Higher reduction rates lead to lower revenue
            impact.
          </p>
          <ChartComponent
            chartId="revenueDropChart"
            chartType="line"
            :chartData="revenueDropChartData"
            :chartOptions="revenueChartOptions"
          />
        </div>

        <!-- Subsidy Equivalent Chart -->
        <div class="chart-wrapper">
          <h3>
            <i class="fas fa-file-invoice-dollar"></i> Subsidies Equivalent by
            Scenario
          </h3>
          <p class="chart-description">
            Required subsidy equivalent per gallon of hydrogen over time.
            Credits decrease as refueling efficiency improves.
          </p>
          <ChartComponent
            chartId="taxCreditChart"
            chartType="line"
            :chartData="taxCreditChartData"
            :chartOptions="taxCreditChartOptions"
          />
        </div>

        <!-- Cumulative Cost Chart -->
        <div class="chart-wrapper">
          <h3><i class="fas fa-coins"></i> Cumulative Cost Comparison</h3>
          <p class="chart-description">
            Total revenue loss through {{ hydrogenStore.year }} for each
            scenario. Shows the long-term financial impact of different
            improvement rates.
          </p>
          <ChartComponent
            chartId="cumulativeCostChart"
            chartType="bar"
            :chartData="cumulativeCostChartData"
            :chartOptions="cumulativeCostChartOptions"
          />
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from "vue";
import { useEconomicsStore } from "@/store/economicsStore";
import { useHydrogenStore } from "@/store/hydrogenStore";
import { useNotificationStore } from "@/store/notificationStore";
import ChartComponent from "@/components/ChartComponent.vue";

export default {
  name: "EconomicImpactView",

  components: {
    ChartComponent,
  },

  setup() {
    const economicsStore = useEconomicsStore();
    const hydrogenStore = useHydrogenStore();
    const notificationStore = useNotificationStore();
    const selectedScenario = ref(3); // Default to 3 annual min/ops reduction
    const activeTab = ref("details"); // Default active tab

    // Only allow user to modify turnaround time parameters
    const extraTurnTime = ref(30); // 30 minutes default
    const turnTimeDecreaseRates = ref([0, 1, 2, 3, 4, 5]); // Default scenarios

    // Form validation
    const isFormValid = computed(() => {
      return (
        extraTurnTime.value >= 0 &&
        turnTimeDecreaseRates.value.length > 0 &&
        turnTimeDecreaseRates.value.every((rate) => rate >= 0)
      );
    });

    // Function to notify user
    const notifyUser = (message, type = "info") => {
      notificationStore.addNotification(message, type);
    };

    // Format timestamp function
    const formatTimestamp = (timestamp) => {
      if (!timestamp) return "Never";

      const date = new Date(timestamp);
      return new Intl.DateTimeFormat("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }).format(date);
    };

    // Add handler for toggle change
    const handleAutoRecalculateChange = (event) => {
      economicsStore.setAutoRecalculate(event.target.checked);
    };

    // Add/remove scenario functions
    const addScenario = () => {
      // Add a new scenario with the next integer value or 0
      const nextValue =
        turnTimeDecreaseRates.value.length > 0
          ? Math.max(...turnTimeDecreaseRates.value) + 1
          : 0;
      turnTimeDecreaseRates.value.push(Math.min(nextValue, 10)); // Cap at 10 annual min/ops
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
      if (!economicsStore.results || !economicsStore.results.scenarios)
        return [];
      return economicsStore.results.scenarios[selectedScenario.value] || [];
    });

    // Helper functions for scenario summary
    const getMaxTaxCredit = (rate) => {
      if (!economicsStore.results || !economicsStore.results.scenarios)
        return "0.00";
      const data = economicsStore.results.scenarios[rate] || [];
      if (data.length === 0) return "0.00";

      const maxCredit = Math.max(
        ...data.map((item) => item.Req_Tax_Credit_per_gal || 0)
      );
      return maxCredit;
    };

    const getTaxCreditPeakYear = (rate) => {
      if (!economicsStore.results || !economicsStore.results.scenarios)
        return "";
      const data = economicsStore.results.scenarios[rate] || [];
      if (data.length === 0) return "";

      const maxCredit = Math.max(
        ...data.map((item) => item.Req_Tax_Credit_per_gal || 0)
      );
      const peakItem = data.find(
        (item) => (item.Req_Tax_Credit_per_gal || 0) === maxCredit
      );
      return peakItem ? peakItem.Year : "";
    };

    const getMaxRevenueDrop = (rate) => {
      if (!economicsStore.results || !economicsStore.results.scenarios)
        return "0.00";
      const data = economicsStore.results.scenarios[rate] || [];
      if (data.length === 0) return "0.00";

      const maxDrop = Math.max(...data.map((item) => item.Pct_Drop || 0));
      return maxDrop;
    };

    const getRevenueDropPeakYear = (rate) => {
      if (!economicsStore.results || !economicsStore.results.scenarios)
        return "";
      const data = economicsStore.results.scenarios[rate] || [];
      if (data.length === 0) return "";

      const maxDrop = Math.max(...data.map((item) => item.Pct_Drop || 0));
      const peakItem = data.find((item) => (item.Pct_Drop || 0) === maxDrop);
      return peakItem ? peakItem.Year : "";
    };

    const getCumulativeCost = (rate) => {
      if (!economicsStore.results || !economicsStore.results.scenarios)
        return "0.00";
      const data = economicsStore.results.scenarios[rate] || [];
      if (data.length === 0) return "0.00";

      const totalCost = data.reduce((sum, item) => {
        const revenueLoss =
          (item.Baseline_Revenue_M || 0) - (item.Hydrogen_Revenue_M || 0);
        return sum + revenueLoss;
      }, 0);
      return totalCost;
    };

    // Helper functions for subsidy equivalent summary calculations
    const calculateAverageRevenueLoss = () => {
      if (
        !selectedScenarioData.value ||
        selectedScenarioData.value.length === 0
      )
        return 0;
      const total = selectedScenarioData.value.reduce(
        (sum, item) => sum + (item.Revenue_Drop_M || 0),
        0
      );
      return total / selectedScenarioData.value.length;
    };

    const calculateAverageH2Volume = () => {
      if (
        !selectedScenarioData.value ||
        selectedScenarioData.value.length === 0
      )
        return 0;
      const total = selectedScenarioData.value.reduce(
        (sum, item) => sum + (item.H2_Demand_annual_gal || 0),
        0
      );
      return total / selectedScenarioData.value.length;
    };

    const calculateTotalH2Volume = () => {
      if (
        !selectedScenarioData.value ||
        selectedScenarioData.value.length === 0
      )
        return 0;
      return selectedScenarioData.value.reduce(
        (sum, item) => sum + (item.H2_Demand_annual_gal || 0),
        0
      );
    };

    const calculateAverageTaxCredit = () => {
      if (
        !selectedScenarioData.value ||
        selectedScenarioData.value.length === 0
      )
        return 0;
      const total = selectedScenarioData.value.reduce(
        (sum, item) => sum + (item.Req_Tax_Credit_per_gal || 0),
        0
      );
      return total / selectedScenarioData.value.length;
    };

    const calculateTotalSubsidies = () => {
      if (
        !selectedScenarioData.value ||
        selectedScenarioData.value.length === 0
      )
        return 0;
      return selectedScenarioData.value.reduce(
        (sum, item) => sum + calculateTotalSubsidy(item),
        0
      );
    };

    const calculateAverageCostRecovery = () => {
      if (
        !selectedScenarioData.value ||
        selectedScenarioData.value.length === 0
      )
        return 0;

      const validItems = selectedScenarioData.value.filter(
        (item) => (item.Revenue_Drop_M || 0) > 0
      );
      if (validItems.length === 0) return 0;

      const total = validItems.reduce(
        (sum, item) => sum + calculateCostRecovery(item),
        0
      );
      return total / validItems.length;
    };

    // Helper functions for subsidy equivalent table
    const calculateRevenueLoss = (item) => {
      return (item.Baseline_Revenue_M || 0) - (item.Hydrogen_Revenue_M || 0);
    };

    const formatH2Volume = (volume) => {
      if (!volume) return "0";
      if (volume >= 1000000) {
        return `${volume / 1000000}M gal`;
      } else if (volume >= 1000) {
        return `${volume / 1000}K gal`;
      }
      return `${volume} gal`;
    };

    const calculateTotalSubsidy = (item) => {
      return (
        ((item.Req_Tax_Credit_per_gal || 0) *
          (item.H2_Demand_annual_gal || 0)) /
        1000000
      ); // Convert to millions
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
        const csvData = economicsStore.exportScenarioData(
          selectedScenario.value
        );
        const blob = new Blob([csvData], { type: "text/csv" });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.setAttribute("hidden", "");
        a.setAttribute("href", url);
        a.setAttribute(
          "download",
          `scenario_${selectedScenario.value}_min_per_year.csv`
        );
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } catch (error) {
        console.error("Error exporting data:", error);
        alert("Failed to export data: " + error.message);
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
        finalH2Year: hydrogenStore.year,
      });

      // Store calculation timestamp
      economicsStore.lastCalculationTime = new Date();
    };

    // Function to get colors for different rates
    const getColorForRate = (rate, alpha = 1) => {
      const colors = [
        `rgba(255, 107, 107, ${alpha})`, // 0 annual min/ops
        `rgba(77, 166, 255, ${alpha})`, // 1 annual min/ops
        `rgba(255, 230, 66, ${alpha})`, // 2 annual min/ops
        `rgba(75, 222, 172, ${alpha})`, // 3 annual min/ops
        `rgba(188, 140, 255, ${alpha})`, // 4 annual min/ops
        `rgba(255, 170, 66, ${alpha})`, // 5 annual min/ops
      ];
      return colors[rate] || `rgba(200, 200, 200, ${alpha})`;
    };

    // Revenue Drop Chart Data
    const revenueDropChartData = computed(() => {
      if (!economicsStore.results || !economicsStore.results.scenarios)
        return { labels: [], datasets: [] };

      const scenarios = economicsStore.results.scenarios;
      const firstScenario = Object.values(scenarios)[0];
      const labels = firstScenario.map((item) => item.Year);

      const datasets = Object.entries(scenarios).map(([rate, data]) => ({
        label: `${rate} annual min/ops reduction`,
        data: data.map((item) => item.Pct_Drop),
        borderColor: getColorForRate(parseInt(rate)),
        backgroundColor: getColorForRate(parseInt(rate), 0.2),
        borderWidth: parseInt(rate) === selectedScenario.value ? 3 : 1,
        pointBackgroundColor: getColorForRate(parseInt(rate)),
        pointBorderColor: "#000000", // Dark border around points
        pointRadius: 5, // Slightly larger points
        pointHoverRadius: 7,
        tension: 0.1, // Slight curve for better visibility
      }));

      return { labels, datasets };
    });

    // Subsidy Equivalent Chart Data
    const taxCreditChartData = computed(() => {
      if (!economicsStore.results || !economicsStore.results.scenarios)
        return { labels: [], datasets: [] };

      const scenarios = economicsStore.results.scenarios;
      const firstScenario = Object.values(scenarios)[0];
      const labels = firstScenario.map((item) => item.Year);

      const datasets = Object.entries(scenarios).map(([rate, data]) => {
        return {
          label: `${rate} annual min/ops reduction`,
          data: data.map((item) => item.Req_Tax_Credit_per_gal || 0),
          borderColor: getColorForRate(parseInt(rate)),
          backgroundColor: getColorForRate(parseInt(rate), 0.2),
          borderWidth: parseInt(rate) === selectedScenario.value ? 3 : 1,
          pointBackgroundColor: getColorForRate(parseInt(rate)),
          pointBorderColor: "#000000",
          pointRadius: 5,
          pointHoverRadius: 7,
          tension: 0.1,
        };
      });

      return { labels, datasets };
    });

    // Cumulative Cost Chart Data
    const cumulativeCostChartData = computed(() => {
      if (!economicsStore.results || !economicsStore.results.scenarios)
        return { labels: [], datasets: [] };

      const scenarios = economicsStore.results.scenarios;
      const labels = Object.keys(scenarios).map(
        (rate) => `${rate} annual min/ops`
      );

      const cumulativeCosts = Object.entries(scenarios).map(([rate, data]) => {
        return data.reduce((sum, item) => {
          const revenueLoss =
            (item.Baseline_Revenue_M || 0) - (item.Hydrogen_Revenue_M || 0);
          return sum + revenueLoss;
        }, 0);
      });

      const datasets = [
        {
          label: "Cumulative Cost ($M)",
          data: cumulativeCosts,
          backgroundColor: Object.keys(scenarios).map((rate) =>
            getColorForRate(parseInt(rate), 0.8)
          ),
          borderColor: Object.keys(scenarios).map((rate) =>
            getColorForRate(parseInt(rate))
          ),
          borderWidth: 2,
        },
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
          text: "Revenue Drop vs. Year for Different Turn-Time Reduction Rates",
          color: "#ffffff", // White text for title on dark background
          font: {
            weight: "bold",
            size: 16,
          },
        },
        legend: {
          labels: {
            color: "#ffffff", // White text for legend on dark background
            font: {
              weight: "medium",
              size: 12,
            },
            boxWidth: 15, // Smaller legend box for better readability
            padding: 15, // More spacing between legend items
            usePointStyle: true, // Use point style instead of rectangles
            pointStyle: "circle", // Circle points for better visibility
          },
        },
        tooltip: {
          backgroundColor: "rgba(255, 255, 255, 0.9)", // Light background for tooltip on dark theme
          titleColor: "#000000", // Black text for tooltip title
          bodyColor: "#000000", // Black text for tooltip body
          borderColor: "#888888",
          borderWidth: 1,
          callbacks: {
            label: (context) =>
              `${context.dataset.label}: ${context.raw.toFixed(2)}%`,
          },
        },
      },
      scales: {
        y: {
          title: {
            display: true,
            text: "% Revenue Drop",
            color: "#ffffff", // White text for y-axis title
            font: {
              weight: "bold",
            },
          },
          ticks: {
            color: "#cccccc", // Light gray text for y-axis ticks
            font: {
              weight: "medium",
            },
          },
          grid: {
            color: "rgba(255, 255, 255, 0.1)", // Subtle light grid lines
          },
        },
        x: {
          title: {
            display: true,
            text: "Year",
            color: "#ffffff", // White text for x-axis title
            font: {
              weight: "bold",
            },
          },
          ticks: {
            color: "#cccccc", // Light gray text for x-axis ticks
            font: {
              weight: "medium",
            },
          },
          grid: {
            color: "rgba(255, 255, 255, 0.1)", // Subtle light grid lines
          },
        },
      },
    };

    const taxCreditChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        title: {
          display: true,
          text: "Subsidies Equivalent vs. Year for Different Turn-Time Reduction Rates",
          color: "#ffffff", // White text for title
          font: {
            weight: "bold",
            size: 16,
          },
        },
        legend: {
          labels: {
            color: "#ffffff", // White text for legend
            font: {
              weight: "medium",
              size: 12,
            },
            boxWidth: 15,
            padding: 15,
            usePointStyle: true,
            pointStyle: "circle",
          },
        },
        tooltip: {
          backgroundColor: "rgba(255, 255, 255, 0.9)",
          titleColor: "#000000",
          bodyColor: "#000000",
          borderColor: "#888888",
          borderWidth: 1,
          callbacks: {
            label: (context) =>
              `${context.dataset.label}: $${context.raw.toFixed(2)}/gal`,
          },
        },
      },
      scales: {
        y: {
          title: {
            display: true,
            text: "Subsidy Equivalent ($/gal)",
            color: "#ffffff",
            font: {
              weight: "bold",
            },
          },
          ticks: {
            color: "#cccccc",
            font: {
              weight: "medium",
            },
          },
          grid: {
            color: "rgba(255, 255, 255, 0.1)",
          },
        },
        x: {
          title: {
            display: true,
            text: "Year",
            color: "#ffffff",
            font: {
              weight: "bold",
            },
          },
          ticks: {
            color: "#cccccc",
            font: {
              weight: "medium",
            },
          },
          grid: {
            color: "rgba(255, 255, 255, 0.1)",
          },
        },
      },
    };

    const cumulativeCostChartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        title: {
          display: true,
          text: "Cumulative Cost by Scenario",
          color: "#ffffff",
          font: {
            weight: "bold",
            size: 16,
          },
        },
        tooltip: {
          backgroundColor: "rgba(255, 255, 255, 0.9)",
          titleColor: "#000000",
          bodyColor: "#000000",
          borderColor: "#888888",
          borderWidth: 1,
          callbacks: {
            label: (context) => `${context.label}: $${context.raw.toFixed(2)}M`,
          },
        },
      },
      scales: {
        y: {
          title: {
            display: true,
            text: "Cumulative Cost ($M)",
            color: "#ffffff",
            font: {
              weight: "bold",
            },
          },
          beginAtZero: true,
          ticks: {
            color: "#cccccc",
            font: {
              weight: "medium",
            },
          },
          grid: {
            color: "rgba(255, 255, 255, 0.1)",
          },
        },
        x: {
          ticks: {
            color: "#cccccc",
            font: {
              weight: "medium",
            },
          },
          grid: {
            color: "rgba(255, 255, 255, 0.1)",
          },
        },
      },
    };

    // Watch for changes in hydrogen demand data
    watch(
      [
        () => hydrogenStore.totalH2Demand,
        () => hydrogenStore.fleetPercentage,
        () => hydrogenStore.year,
      ],
      async (
        [newH2Demand, newFleetPercentage, newYear],
        [oldH2Demand, oldFleetPercentage, oldYear]
      ) => {
        // Only trigger if auto-recalculate is enabled
        if (economicsStore.autoRecalculate) {
          // Check if any value actually changed
          if (
            newH2Demand !== oldH2Demand ||
            newFleetPercentage !== oldFleetPercentage ||
            newYear !== oldYear
          ) {
            console.log("Auto-recalculating due to hydrogen data change");
            // Make sure we have valid parameters before calculating
            if (isFormValid.value) {
              await calculateEconomicImpact();
              notifyUser("Economic calculations automatically updated", "info");
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
        const currentTotalH2Demand = parseFloat(
          hydrogenStore.totalH2Demand || 0
        );
        const currentFleetPercentage =
          hydrogenStore.fleetPercentage / 100 || 0.1;
        const currentYear = hydrogenStore.year || 2036;

        // Check if current hydrogen data matches the data used for economic calculations
        if (
          currentTotalH2Demand !== economicsStore.lastParams.totalH2Demand ||
          currentFleetPercentage !==
            economicsStore.lastParams.fleetPercentage ||
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
        notifyUser(
          "Hydrogen parameters have changed. Please recalculate economic impact.",
          "warning"
        );
      }
    });

    // Add these new reactive references
    const activeAssumptionTab = ref(0);

    const assumptionTabs = [
      { title: "Operational", icon: "fas fa-plane" },
      { title: "Technical", icon: "fas fa-cogs" },
      { title: "Financial", icon: "fas fa-dollar-sign" },
    ];

    const activeExplanationTab = ref(0);
    const explanationTabs = [
      { title: "Time Impact", icon: "fas fa-clock" },
      { title: "Financial Impact", icon: "fas fa-dollar-sign" },
      { title: "Key Metrics", icon: "fas fa-chart-bar" },
    ];

    const dataTabs = [
      { id: "details", label: "Yearly Details", icon: "fas fa-table" },
      {
        id: "taxCredits",
        label: "Subsidies Equivalent",
        icon: "fas fa-receipt",
      },
      { id: "charts", label: "Charts", icon: "fas fa-chart-bar" },
    ];

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
      calculateAverageH2Volume,
      calculateAverageTaxCredit,
      calculateTotalSubsidies,
      calculateAverageCostRecovery,
      handleAutoRecalculateChange,
      formatTimestamp,
      activeAssumptionTab,
      assumptionTabs,
      activeExplanationTab,
      explanationTabs,
      dataTabs,
    };
  },
};
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
  padding: 6px;
  margin-left: auto;
  background-color: rgba(255, 99, 132, 0.1);
  border: 1px solid rgba(255, 99, 132, 0.3);
  color: #ff6384;
  border-radius: 4px;
  transition: all 0.2s ease;
  position: absolute;
  /* Change to absolute positioning */
  right: 15px;
  /* Position it on the right with some padding */
  top: 50%;
  /* Center vertically */
  transform: translateY(-50%);
  /* Adjust for perfect centering */
}

.btn.remove:hover {
  background-color: rgba(255, 99, 132, 0.2);
  border-color: #ff6384;
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

.extraTurnTime-container {
  margin-bottom: 15px;
}

.extraTurnTime {
  display: flex;
  align-items: center;
  gap: 12px;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 15px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.extraTurnTime:hover {
  background-color: rgba(255, 255, 255, 0.08);
  border-color: rgba(100, 255, 218, 0.3);
}

.extraTurnTime label {
  color: #aaa;
  font-size: 0.9rem;
  min-width: 200px;
}

.extraTurnTime input {
  width: 70px;
  padding: 8px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: #64ffda;
  font-size: 1rem;
  text-align: center;
  transition: all 0.2s ease;
}

.extraTurnTime input:focus {
  outline: none;
  border-color: #64ffda;
  background-color: rgba(100, 255, 218, 0.1);
}

.extraTurnTime span {
  color: #aaa;
  font-size: 0.9rem;
}

/* =========================
   Scenario Configuration
   ========================= */
.scenario-config {
  margin-top: 25px;
}

.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.scenario-input {
  display: flex;
  align-items: center;
  gap: 12px;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 15px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.2s ease;
  position: relative;
  /* For absolute positioning of the remove button */
  overflow: hidden;
  /* Ensure content stays within */
  flex-wrap: wrap;
  /* Allow wrapping for smaller screens */
}

.scenario-input:hover {
  background-color: rgba(255, 255, 255, 0.08);
  border-color: rgba(100, 255, 218, 0.3);
}

.scenario-input label {
  color: #aaa;
  font-size: 0.9rem;
  min-width: 90px;
}

.scenario-input input {
  width: 70px;
  padding: 8px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  color: #64ffda;
  font-size: 1rem;
  text-align: center;
  transition: all 0.2s ease;
}

.scenario-input input:focus {
  outline: none;
  border-color: #64ffda;
  background-color: rgba(100, 255, 218, 0.1);
}

.scenario-input span {
  color: #aaa;
  font-size: 0.9rem;
}

.scenario-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.scenario-config h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #64ffda;
  margin-bottom: 15px;
}

.scenario-config p {
  color: #aaa;
  font-size: 0.9rem;
  margin-bottom: 20px;
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
  min-width: 300px;
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
  gap: 2px;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 4px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.tab-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  background: none;
  border: none;
  color: #aaa;
  cursor: pointer;
  font-size: 0.95rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.tab-button:hover {
  color: #ddd;
  background-color: rgba(255, 255, 255, 0.05);
}

.tab-button.active {
  background-color: rgba(100, 255, 218, 0.1);
  color: #64ffda;
}

.tab-button i {
  font-size: 0.9rem;
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
  grid-template-columns: 0.7fr 1fr 1.2fr 2fr;
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

.row-cell {
  padding-left: 2.5em;
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

.chart-description {
  color: #aaa;
  font-size: 0.9rem;
  text-align: center;
  margin: -15px 0 20px 0;
  font-style: italic;
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

  .assumptions-tabs {
    flex-direction: column;
    gap: 4px;
  }

  .assumption-tab {
    justify-content: flex-start;
  }

  .data-tabs {
    flex-direction: column;
    gap: 4px;
  }

  .tab-button {
    justify-content: flex-start;
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

.table-header .header-cell {
  color: #64ffda;
  opacity: 0.8;
}

i {
  color: #64ffda;
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
  transition: 0.4s;
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
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: rgba(100, 255, 218, 0.2);
}

input:checked + .toggle-slider:before {
  transform: translateX(26px);
}

.toggle-label {
  font-size: 0.9rem;
  color: #aaa;
}

/* =========================
   Calculation Parameters
   ========================= */
.calculation-params {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  color: #ddd;
}

.calculation-params h3 {
  margin: 0 0 15px 0;
  color: #64ffda;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 8px;
}

.params-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
}

.param-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.param-label {
  color: #aaa;
  font-size: 0.9rem;
}

.param-value {
  color: #64ffda;
  font-weight: 600;
  font-size: 1.1rem;
}

.param-note {
  color: #aaa;
  font-size: 0.8rem;
  font-style: italic;
}

/* Add these new styles */
.assumptions-section {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 25px;
}

.assumptions-tabs {
  display: flex;
  gap: 2px;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 4px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.assumption-tab {
  flex: 1;
  padding: 10px 20px;
  background: none;
  border: none;
  color: #aaa;
  cursor: pointer;
  font-size: 0.9rem;
  border-radius: 4px;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.assumption-tab:hover {
  color: #ddd;
  background-color: rgba(255, 255, 255, 0.05);
}

.assumption-tab.active {
  background-color: rgba(100, 255, 218, 0.1);
  color: #64ffda;
}

.assumptions-content {
  background-color: rgba(255, 255, 255, 0.03);
  border-radius: 6px;
  padding: 20px;
}

.assumption-list {
  display: grid;
  gap: 15px;
}

.assumption-item {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #ddd;
  font-size: 0.95rem;
}

.assumption-item i {
  color: #64ffda;
  font-size: 0.9rem;
}

/* Update the data-tabs styling */
.data-tabs {
  display: flex;
  gap: 2px;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 4px;
  border-radius: 6px;
  margin-bottom: 20px;
}

.tab-button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  background: none;
  border: none;
  color: #aaa;
  cursor: pointer;
  font-size: 0.95rem;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.tab-button:hover {
  color: #ddd;
  background-color: rgba(255, 255, 255, 0.05);
}

.tab-button.active {
  background-color: rgba(100, 255, 218, 0.1);
  color: #64ffda;
}

.tab-button i {
  font-size: 0.9rem;
}

/* Add responsive styles */
@media (max-width: 768px) {
  .assumptions-tabs {
    flex-direction: column;
    gap: 4px;
  }

  .assumption-tab {
    justify-content: flex-start;
  }

  .data-tabs {
    flex-direction: column;
    gap: 4px;
  }

  .tab-button {
    justify-content: flex-start;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }
}

.explanation-section {
  background: linear-gradient(
    145deg,
    rgba(255, 255, 255, 0.07) 0%,
    rgba(255, 255, 255, 0.03) 100%
  );
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.explanation-tabs {
  display: flex;
  gap: 4px;
  background: rgba(255, 255, 255, 0.03);
  padding: 5px;
  border-radius: 8px;
  position: relative;
  margin-bottom: 25px;
}

.explanation-tab {
  flex: 1;
  padding: 12px 24px;
  background: transparent;
  border: none;
  color: #aaa;
  cursor: pointer;
  font-size: 0.95rem;
  border-radius: 6px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.explanation-tab:hover {
  color: #fff;
  background: rgba(100, 255, 218, 0.05);
}

.explanation-tab.active {
  color: #64ffda;
  background: rgba(100, 255, 218, 0.1);
}

.tab-indicator {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 2px;
  width: 100%;
  background: transparent;
  transition: transform 0.3s ease;
}

.explanation-tab.active .tab-indicator {
  background: #64ffda;
  transform: scaleX(1);
}

.explanation-content {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
  padding: 25px;
  transition: all 0.3s ease;
}

.explanation-item {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  transition: all 0.3s ease;
  border: 1px solid rgba(100, 255, 218, 0.1);
}

.explanation-item:hover {
  transform: translateY(-2px);
  border-color: rgba(100, 255, 218, 0.2);
  box-shadow: 0 4px 12px rgba(100, 255, 218, 0.1);
}

.item-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 15px;
}

/* .item-header i {
  color: #64ffda;
  font-size: 1.2rem;
  background: rgba(100, 255, 218, 0.1);
  padding: 8px;
  border-radius: 50%;
} */

.item-header h3 {
  margin: 0;
  color: #fff;
  font-size: 1.1rem;
  border: none;
  padding: 0;
}

.item-content {
  color: #aaa;
  font-size: 0.95rem;
  line-height: 1.6;
}

.visual-indicators {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-top: 15px;
}

.visual-indicator {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  color: #64ffda;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.visual-indicator:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateX(5px);
}

.indicator-graphic {
  margin-left: auto;
  padding-left: 15px;
  min-width: 100px;
}

/* Bar Graph Styling */
.bar-container {
  position: relative;
  height: 30px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.bar {
  width: 100%;
  background: rgba(100, 255, 218, 0.2);
  border-radius: 4px;
  transition: height 0.3s ease;
}

.bar.high {
  height: 20px;
}

.label {
  font-size: 0.8rem;
  color: #aaa;
  margin-top: 4px;
}

/* Trend Line Styling */
.trend-line {
  position: relative;
  height: 30px;
  width: 100%;
}

.line {
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background: #64ffda;
  transform: rotate(-15deg);
}

.point {
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #64ffda;
}

.point.start {
  top: 5px;
  left: 0;
}

.point.end {
  bottom: 5px;
  right: 0;
}

/* Animation for trend line */
@keyframes drawLine {
  from {
    transform: scaleX(0);
  }

  to {
    transform: scaleX(1);
  }
}

.line {
  transform-origin: left;
  animation: drawLine 1.5s ease-out forwards;
}

/* Tooltip styling */
.visual-indicator[title] {
  position: relative;
  cursor: help;
}

.visual-indicator[title]:hover::after {
  content: attr(title);
  position: absolute;
  bottom: 100%;
  left: 50%;
  transform: translateX(-50%);
  padding: 6px 10px;
  background: rgba(0, 0, 0, 0.8);
  color: #fff;
  font-size: 0.8rem;
  border-radius: 4px;
  white-space: nowrap;
  z-index: 10;
}

@media (max-width: 768px) {
  .visual-indicator {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .indicator-graphic {
    width: 100%;
    margin-left: 0;
    padding-left: 0;
    margin-top: 10px;
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .explanation-tabs {
    flex-direction: column;
  }

  .explanation-tab {
    justify-content: flex-start;
  }

  .item-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

/****** Width Reactive Enhancements ******/

.page-view {
  width: 100%;
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 20px;
  box-sizing: border-box;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 2rem;
  color: #64ffda;
  margin-bottom: 10px;
}

.description {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.7);
  max-width: 800px;
  line-height: 1.5;
}

.sustainability-content {
  width: 100%;
}

.card {
  background: rgba(22, 28, 36, 0.7);
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(100, 255, 218, 0.1);
  transition: all 0.3s ease;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .page-header h1 {
    font-size: 1.8rem;
  }

  .description {
    font-size: 1rem;
  }

  .card {
    padding: 20px;
  }
}

@media (max-width: 480px) {
  .page-view {
    padding: 0 10px;
  }

  .page-header h1 {
    font-size: 1.5rem;
  }

  .card {
    padding: 15px;
    border-radius: 8px;
  }
}

@media (min-width: 1400px) {
  .card {
    padding: 40px;
  }
}

/****** Width Reactive Enhancements for Scenario Buttons ******/

@media (min-width: 3600px) {
  .scenario-input {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .btn.remove {
    font-size: 1.1rem;
    padding: 6px 10px;
  }

  /* Optional: show label */
  .btn.remove::after {
    content: "";
    font-size: 0.9rem;
    color: #ddd;
  }
}
</style>
