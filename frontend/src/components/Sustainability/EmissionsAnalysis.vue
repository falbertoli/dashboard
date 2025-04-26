<!-- File: frontend/src/components/Sustainability/EmissionsAnalysis.vue -->

<template>
  <div class="emissions-analysis">
    <h2>Emissions Analysis</h2>

    <!-- Alert shown when no hydrogen data is available -->
    <div v-if="!hydrogenStore.aircraftH2Demand || !hydrogenStore.gseH2Demand" class="alert info">
      <i class="fas fa-info-circle"></i>
      <span>Please configure hydrogen demand in the Hydrogen section first.</span>
    </div>

    <!-- Loading state -->
    <div v-else-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>Calculating emissions impact...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-message">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ error }}</p>
    </div>

    <!-- No results state with hydrogen demand info -->
    <div v-else-if="!emissionsResults" class="no-results">
      <!-- Hydrogen Demand Information -->
      <div class="hydrogen-demand-info">
        <h3><i class="fas fa-atom"></i> Hydrogen Demand</h3>
        <div class="info-row total-demand">
          <span>Total Daily Hydrogen Demand:</span>
          <strong>{{ $formatCompactNumber(hydrogenStore.totalH2Demand) }} ft³</strong>
        </div>
        <div class="breakdown-container">
          <div class="breakdown-item">
            <div class="icon-wrapper">
              <i class="fas fa-plane"></i>
            </div>
            <div class="content">
              <span>Aircraft</span>
              <strong>{{ $formatCompactNumber(hydrogenStore.aircraftH2Demand.daily_h2_demand_ft3) }} ft³</strong>
            </div>
          </div>
          <div class="breakdown-item">
            <div class="icon-wrapper">
              <i class="fas fa-truck"></i>
            </div>
            <div class="content">
              <span>Ground Vehicles</span>
              <strong>{{ $formatNumber(hydrogenStore.gseH2Demand.daily_h2_demand_ft3) }} ft³</strong>
            </div>
          </div>
        </div>
      </div>

      <p>Click the button below to calculate the emissions impact of hydrogen adoption.</p>
      <button class="primary-button" @click="calculateEmissions">
        <i class="fas fa-calculator"></i> Calculate Emissions
      </button>
    </div>

    <!-- Results container with hydrogen demand pill -->
    <div v-else class="results-container">
      <!-- Hydrogen demand summary pill -->
      <div class="hydrogen-demand-summary">
        <div class="info-pill">
          <div class="pill-item">
            <i class="fas fa-atom pulse-icon"></i>
            <span class="hydrogen-demand-summary-span">Daily H₂ Demand: <strong>{{
              $formatCompactNumber(hydrogenStore.totalH2Demand) }}
                ft³</strong></span>
          </div>
          <div class="divider"></div>
          <div class="pill-item">
            <i class="fas fa-plane-departure"></i>
            <span class="hydrogen-demand-summary-span">Fleet Adoption: <strong>{{
              $formatNumber(parseFloat(hydrogenStore.fleetPercentage)) }}%</strong></span>
          </div>
          <div class="divider"></div>
          <div class="pill-item">
            <i class="fa-solid fa-calendar-days"></i>
            <span class="hydrogen-demand-summary-span">End Year: <strong>{{
              hydrogenStore.year }}</strong></span>
          </div>
        </div>
      </div>

      <div class="reduction-percentage-card">
        <div class="percentage-value">{{ emissionsReductionPercentage.toFixed(1) }}%</div>
        <div class="percentage-label">Emissions Reduction</div>
        <div class="percentage-description">
          Through hydrogen adoption, your operations would reduce CO₂ emissions by
          {{ emissionsReductionPercentage.toFixed(1) }}% compared to conventional operations.
        </div>
      </div>

      <!-- Summary Cards -->
      <div class="summary-grid">
        <div class="summary-card reduction">
          <div class="card-icon">
            <i class="fas fa-leaf"></i>
          </div>
          <div class="card-content">
            <div class="card-title">CO₂ Emissions Reduction</div>
            <div class="card-value">{{ $formatCompactNumber(emissionsReduction) }} metric tons</div>
            <div class="card-percentage">{{ emissionsReductionPercentage.toFixed(1) }}% reduction</div>
          </div>
        </div>

        <div class="summary-card conventional">
          <div class="card-icon">
            <i class="fas fa-plane"></i>
          </div>
          <div class="card-content">
            <div class="card-title">Conventional Operations</div>
            <div class="card-value">{{ $formatCompactNumber(totalJetAEmissions) }} metric tons CO₂</div>
            <div class="card-percentage">Baseline scenario</div>
          </div>
        </div>

        <div class="summary-card hydrogen">
          <div class="card-icon">
            <i class="fas fa-atom"></i>
          </div>
          <div class="card-content">
            <div class="card-title">Hybrid Operations</div>
            <div class="card-value">{{ $formatCompactNumber(totalHydrogenEmissions) }} metric tons CO₂</div>
            <div class="card-percentage">
              <span style="color:rgba(231, 76, 60, 0.5);font-weight:rgba(231, 76, 60, 0.5);">Jet A: {{
                $formatCompactNumber(emissionsResults.jetA_co2) }}</span> +
              <span style="color:rgba(52, 152, 219, 0.8);font-weight:rgba(52, 152, 219, 0.8);">H₂: {{
                $formatNumber(emissionsResults.H2_co2, 0) }}</span>
              metric tons CO₂
            </div>
          </div>
        </div>
      </div>

      <div class="charts-container">
        <!-- Emissions Comparison Chart -->
        <div class="chart-section">
          <h3>Emissions Comparison</h3>
          <ChartComponent chart-id="emissions-comparison-chart" chart-type="bar"
            :chart-data="emissionsComparisonChartData" :chart-options="emissionsComparisonChartOptions" />
        </div>

        <!-- Emissions Reduction Chart -->
        <div class="chart-section">
          <h3>Emissions Reduction Impact</h3>
          <ChartComponent chart-id="emissions-reduction-chart" chart-type="doughnut"
            :chart-data="emissionsReductionChartData" :chart-options="emissionsReductionChartOptions" />
        </div>
      </div>

      <!-- Environmental Equivalents -->
      <div class="equivalents-section">
        <h3>Environmental Impact Equivalents</h3>

        <!-- New container to separate conventional vs reduction metrics -->
        <div class="equivalents-container">
          <!-- Reduction Metrics -->
          <div class="equivalents-comparison">
            <h4>Emissions Reduction Impact</h4>
            <div class="equivalents-grid">
              <div class="equivalent-card reduction">
                <div class="equivalent-icon">
                  <i class="fas fa-tree"></i>
                </div>
                <div class="equivalent-content">
                  <div class="equivalent-title">Carbon Sequestration Equivalent</div>
                  <div class="equivalent-value">{{ $formatCompactNumber(carbonOffsetEquivalent) }} trees</div>
                  <div class="equivalent-description">Number of trees needed to absorb the same amount of CO₂ over one
                    year</div>
                </div>
              </div>

              <div class="equivalent-card reduction">
                <div class="equivalent-icon">
                  <i class="fas fa-car"></i>
                </div>
                <div class="equivalent-content">
                  <div class="equivalent-title">Vehicle Emissions Equivalent</div>
                  <div class="equivalent-value">{{ $formatCompactNumber(vehicleEquivalent) }} cars</div>
                  <div class="equivalent-description">Number of cars taken off the road for one year</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Conventional Metrics -->
          <div class="equivalents-comparison conventional">
            <h4>Conventional Operations Impact</h4>
            <div class="equivalents-grid">
              <div class="equivalent-card conventional">
                <div class="equivalent-icon">
                  <i class="fas fa-tree"></i>
                </div>
                <div class="equivalent-content">
                  <div class="equivalent-title">Conventional Operations Tree Equivalent</div>
                  <div class="equivalent-value">{{ $formatCompactNumber(conventionalTreeEquivalent) }} trees</div>
                  <div class="equivalent-description">Number of trees needed to absorb conventional operations CO₂ over
                    one year</div>
                </div>
              </div>
              <div class="equivalent-card conventional">
                <div class="equivalent-icon">
                  <i class="fas fa-car"></i>
                </div>
                <div class="equivalent-content">
                  <div class="equivalent-title">Vehicle Emissions Equivalent</div>
                  <div class="equivalent-value">{{ $formatCompactNumber(conventionalVehicleEquivalent) }} cars</div>
                  <div class="equivalent-description">Number of cars that would emit the same CO₂ as conventional
                    operations over one year</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Emissions Breakdown -->
      <div class="breakdown-section">
        <h3>Emissions Breakdown</h3>
        <div class="table-container">
          <div class="table-header">
            <div class="header-cell">Source</div>
            <div class="header-cell">Emissions (metric tons CO₂)</div>
            <div class="header-cell">Percentage</div>
          </div>

          <div class="table-row">
            <div class="row-cell">Jet A (Conventional)</div>
            <div class="row-cell">{{ $formatCompactNumber(emissionsResults.just_jetA_co2) }}</div>
            <div class="row-cell">100%</div>
          </div>

          <div class="table-row">
            <div class="row-cell">Jet A (Hybrid)</div>
            <div class="row-cell">{{ $formatCompactNumber(emissionsResults.jetA_co2) }}</div>
            <div class="row-cell">{{ ((emissionsResults.jetA_co2 / emissionsResults.just_jetA_co2) * 100).toFixed(1) }}%
            </div>
          </div>

          <div class="table-row">
            <div class="row-cell">Hydrogen</div>
            <div class="row-cell">{{ $formatCompactNumber(emissionsResults.H2_co2, 0) }}</div>
            <div class="row-cell">{{ ((emissionsResults.H2_co2 / emissionsResults.just_jetA_co2) * 100).toFixed(1)
            }}%
            </div>
          </div>

          <div class="table-row total">
            <div class="row-cell">Total Reduction</div>
            <div class="row-cell">{{ $formatCompactNumber(emissionsReduction) }}</div>
            <div class="row-cell">{{ emissionsReductionPercentage.toFixed(1) }}%</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { useHydrogenStore } from '@/store/hydrogenStore';
import { useSustainabilityStore } from '@/store/sustainabilityStore';
import ChartComponent from '@/components/ChartComponent.vue';
import { getCurrentInstance } from 'vue';

const instance = getCurrentInstance();
const { $formatNumber, $formatCompactNumber } = instance.appContext.config.globalProperties;

const hydrogenStore = useHydrogenStore();
const sustainabilityStore = useSustainabilityStore();

const {
  emissionsResults,
  isLoading,
  error,
  totalJetAEmissions,
  totalHydrogenEmissions,
  emissionsReduction,
  emissionsReductionPercentage,
  carbonOffsetEquivalent,
  conventionalTreeEquivalent,
  conventionalVehicleEquivalent,
  vehicleEquivalent
} = storeToRefs(sustainabilityStore);

// Calculate emissions when requested
const calculateEmissions = () => {
  sustainabilityStore.calculateEmissions();
};

// Emissions Comparison Chart Data
const emissionsComparisonChartData = computed(() => {
  if (!emissionsResults.value) return { labels: [], datasets: [] };

  return {
    labels: ['Conventional Operations', 'Hydrogen Operations'],
    datasets: [
      {
        label: 'Jet A Emissions Conventional',
        data: [emissionsResults.value.just_jetA_co2, 0],
        backgroundColor: ['rgba(231, 76, 60, 0.8)'], // Updated to match our red
        borderColor: ['rgba(231, 76, 60, 1)'],
        borderWidth: 1
      },
      {
        label: 'Jet A Emissions Hybrid',
        data: [0, emissionsResults.value.jetA_co2],
        backgroundColor: ['rgba(231, 76, 60, 0.5)'], // Lighter red for remaining Jet A
        borderColor: ['rgba(231, 76, 60, 0.8)'],
        borderWidth: 1
      },
      {
        label: 'Hydrogen Emissions',
        data: [0, emissionsResults.value.H2_co2],
        backgroundColor: 'rgba(52, 152, 219, 0.8)', // Updated blue for hydrogen
        borderColor: 'rgba(52, 152, 219, 1)',
        borderWidth: 1
      }
    ]
  };
});

// Emissions Comparison Chart Options
const emissionsComparisonChartOptions = computed(() => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#ddd'
        }
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            return `${context.dataset.label}: ${$formatCompactNumber(context.raw)} metric tons CO₂`;
          },
          footer: function (tooltipItems) {
            let sum = 0;
            tooltipItems.forEach(item => {
              sum += item.raw;
            });
            return `Total: ${$formatCompactNumber(sum)} metric tons CO₂`;
          }
        }
      }
    },
    scales: {
      x: {
        ticks: {
          color: '#ddd'
        },
        grid: {
          display: false
        },
        stacked: true
      },
      y: {
        beginAtZero: true,
        stacked: true,
        title: {
          display: true,
          text: 'CO₂ Emissions (metric tons)',
          color: '#ddd'
        },
        ticks: {
          color: '#aaa',
          callback: function (value) {
            return $formatCompactNumber(value);
          }
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        }
      }
    }
  };
});

// Emissions Reduction Chart Data
const emissionsReductionChartData = computed(() => {
  if (!emissionsResults.value) return { labels: [], datasets: [] };

  return {
    labels: ['Emissions Reduced', 'Remaining Emissions'],
    datasets: [{
      data: [
        emissionsReduction.value,
        totalHydrogenEmissions.value
      ],
      backgroundColor: [
        'rgba(46, 204, 113, 0.8)', // Updated teal for emissions reduced
        'rgba(231, 76, 60, 0.5)'  // Updated red for remaining emissions
      ],
      borderColor: [
        'rgba(46, 204, 113, 1)',
        'rgba(231, 76, 60, 0.8)'
      ],
      borderWidth: 1
    }]
  };
});

// Emissions Reduction Chart Options
const emissionsReductionChartOptions = computed(() => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '60%',
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#ddd'
        }
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            const value = context.raw;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(1);
            return `${context.label}: ${$formatCompactNumber(value)} metric tons (${percentage}%)`;
          }
        }
      }
    }
  };
});
</script>

<style scoped>
/* =========================
   Color Variables & Root
   ========================= */
:root {
  /* Primary semantic colors */
  --color-reduction: #2ecc71;
  /* Brighter teal for reductions */
  --color-conventional: #e74c3c;
  /* Clear red for conventional emissions */
  --color-hydrogen: #3498db;
  /* Bright blue for hydrogen */

  /* Background variations */
  --bg-reduction: rgba(46, 204, 113, 0.1);
  --bg-conventional: rgba(231, 76, 60, 0.1);
  --bg-hydrogen: rgba(52, 152, 219, 0.1);

  /* Border variations */
  --border-reduction: rgba(46, 204, 113, 0.8);
  --border-conventional: rgba(231, 76, 60, 0.8);
  --border-hydrogen: rgba(52, 152, 219, 0.8);

  /* UI colors */
  --text-primary: #fff;
  --text-secondary: #ddd;
  --text-tertiary: #aaa;
  --bg-card: rgba(255, 255, 255, 0.07);
  --bg-surface: rgba(255, 255, 255, 0.05);
  --border-subtle: rgba(255, 255, 255, 0.1);
}

/* =========================
   Global & Utility Styles
   ========================= */
.emissions-analysis {
  margin-bottom: 30px;
  color: var(--text-secondary);
}

/* =========================
   Headings
   ========================= */
h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: var(--color-reduction);
  font-size: 1.5rem;
  font-weight: 600;
}

h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: var(--text-secondary);
  font-size: 1.1rem;
  border-bottom: 1px solid var(--border-subtle);
  padding-bottom: 0.5rem;
}

h4 {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-bottom: 15px;
  font-weight: 500;
}

/* =========================
   Alerts & Feedback Messages
   ========================= */
.error-message {
  border-left: 4px solid var(--color-conventional);
  color: var(--color-conventional);
  background-color: var(--bg-conventional);
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.alert {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 25px;
}

.alert i {
  margin-right: 10px;
  font-size: 1.2rem;
  color: var(--color-hydrogen);
}

.no-results {
  color: var(--text-tertiary);
  background-color: var(--bg-surface);
  padding: 25px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* =========================
   Loading & Spinner
   ========================= */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: var(--color-reduction);
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top: 4px solid var(--color-reduction);
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
.primary-button {
  margin-top: 20px;
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.calculate-btn:hover {
  background-color: rgba(0, 196, 167, 0.9);
  transform: translateY(-2px);
  box-shadow: 0 6px 10px rgba(0, 0, 0, 0.15);
}

.calculate-btn:active {
  transform: translateY(0);
}

.calculate-btn i {
  font-size: 1rem;
}

/* =========================
   Hydrogen Demand Info
   ========================= */
.hydrogen-demand-info {
  background: rgba(100, 255, 218, 0.1);
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 25px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.hydrogen-demand-info h3 {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--color-hydrogen);
  margin-bottom: 20px;
  font-size: 1.2rem;
  border-bottom: none;
}

.hydrogen-demand-info h3 i {
  font-size: 1.1rem;
}

.info-row.total-demand {
  background: rgba(255, 255, 255, 0.05);
  padding: 15px;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.info-row.total-demand strong {
  color: var(--color-hydrogen);
  font-size: 1.2rem;
}

.breakdown-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.breakdown-item {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  padding: 15px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.breakdown-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.icon-wrapper {
  background: var(--bg-hydrogen);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-wrapper i {
  color: var(--color-hydrogen);
  font-size: 1.1rem;
}

.breakdown-item .content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.breakdown-item span {
  color: var(--text-tertiary);
  font-size: 0.9rem;
}

.breakdown-item strong {
  color: var(--text-primary);
  font-size: 1.1rem;
}

/* =========================
   Hydrogen Demand Summary Pill
   ========================= */
.hydrogen-demand-summary {
  margin-bottom: 16px;
}

.info-pill {
  background: linear-gradient(145deg, rgba(100, 255, 218, 0.5), rgba(100, 255, 218, 0.05));
  background: rgba(100, 255, 218, 0.7);
  border-radius: 50px;
  padding: 12px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  /* background-color: #64ffda;
  border-color: #64ffda; */
}

.info-pill .pill-item {
  display: flex;
  align-items: center;
}

.hydrogen-demand-summary-span {
  padding-left: 10px;
  color: var(--text-secondary);
}

.hydrogen-demand-summary-span strong {
  color: var(--color-hydrogen);
}

.divider {
  width: 1px;
  height: 24px;
  background-color: rgba(255, 255, 255, 0.2);
  margin: 0 12px;
}

/* =========================
   Results & Summary Cards
   ========================= */
.results-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
  animation: fadeIn 0.6s ease-out;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  margin-bottom: 30px;
}

.summary-card {
  background-color: var(--bg-surface);
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s;
}

.summary-card:hover {
  transform: translateY(-3px);
}

.summary-card.reduction {
  background-color: var(--bg-reduction);
  border-left: 4px solid var(--color-reduction);
}

.summary-card.conventional {
  background-color: var(--bg-conventional);
  border-left: 4px solid var(--color-conventional);
}

.summary-card.hydrogen {
  background-color: var(--bg-hydrogen);
  border-left: 4px solid var(--color-hydrogen);
}

.card-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.summary-card.reduction .card-icon {
  background-color: rgba(46, 204, 113, 0.5);
  color: var(--color-reduction);
}

.summary-card.conventional .card-icon {
  background-color: rgba(231, 76, 60, 0.2);
  color: var(--color-conventional);
}

.summary-card.hydrogen .card-icon {
  background-color: rgba(52, 152, 219, 0.2);
  color: var(--color-hydrogen);
}

.card-content {
  flex: 1;
}

.card-title {
  color: var(--text-tertiary);
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.card-value {
  color: var(--text-primary);
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 5px;
}

.summary-card.reduction .card-value {
  color: var(--color-reduction);
}

.summary-card.conventional .card-value {
  color: var(--color-conventional);
}

.summary-card.hydrogen .card-value {
  color: var(--color-hydrogen);
}

.card-percentage {
  color: var(--text-tertiary);
  font-size: 0.9rem;
}

/* =========================
   Chart Section
   ========================= */
.charts-container {
  display: flex;
  gap: 24px;
  margin-bottom: 30px;
}

.chart-section {
  background-color: var(--bg-card);
  border-radius: 12px;
  padding: 24px;
  flex: 1;
  min-width: 0;
  /* Prevents flex items from overflowing */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.chart-container {
  height: 300px;
  position: relative;
}

/* =========================
   Equivalents Grid & Cards
   ========================= */
.equivalents-section {
  background-color: var(--bg-card);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 30px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.equivalents-container {
  display: flex;
  gap: 24px;
  margin-top: 20px;
}

.equivalents-comparison {
  background-color: var(--bg-reduction);
  border-radius: 12px;
  padding: 22px;
  flex: 1;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.equivalents-comparison.conventional {
  background-color: var(--bg-conventional);
}

.equivalents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.equivalent-card {
  background-color: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 15px;
  transition: transform 0.2s;
}

.equivalent-card:hover {
  transform: translateY(-2px);
}

.equivalent-card.reduction {
  border-left: 4px solid var(--color-reduction);
}

.equivalent-card.conventional {
  border-left: 4px solid var(--color-conventional);
}

.equivalent-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.equivalent-card.reduction .equivalent-icon {
  background-color: rgba(46, 204, 113, 0.5);
  color: var(--color-reduction);
}

.equivalent-card.conventional .equivalent-icon {
  background-color: rgba(231, 76, 60, 0.15);
  color: var(--color-conventional);
}

.equivalent-content {
  flex: 1;
}

.equivalent-title {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-bottom: 5px;
}

.equivalent-value {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 5px;
}

.equivalent-card.reduction .equivalent-value {
  color: var(--color-reduction);
}

.equivalent-card.conventional .equivalent-value {
  color: var(--color-conventional);
}

.equivalent-description {
  color: var(--text-tertiary);
  font-size: 0.8rem;
}

/* =========================
   Reduction Percentage Card
   ========================= */
.reduction-percentage-card {
  background: linear-gradient(145deg, rgba(46, 204, 113, 0.5), rgba(46, 204, 113, 0.3));
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 28px;
  text-align: center;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  border-left: 6px solid var(--color-reduction);
}

.percentage-value {
  font-size: 3.5rem;
  font-weight: 700;
  color: var(--color-reduction);
  margin-bottom: 10px;
  animation: fadeInUp 0.6s ease-out;
}

.percentage-label {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 10px;
  font-weight: 500;
}

.percentage-description {
  color: var(--text-tertiary);
  font-size: 0.95rem;
  line-height: 1.5;
  max-width: 600px;
  margin: 0 auto;
}

/* =========================
   Table Styles
   ========================= */
.breakdown-section {
  background-color: var(--bg-card);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.table-container {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  margin-top: 15px;
}

.table-header {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  background-color: rgba(255, 255, 255, 0.08);
  padding: 14px 16px;
  font-weight: 600;
  color: var(--text-primary);
}

.table-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  padding: 14px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  color: var(--text-tertiary);
}

.table-row:last-child {
  border-bottom: none;
}

.table-row.total {
  background-color: var(--bg-reduction);
  color: var(--color-reduction);
  font-weight: 600;
}

.header-cell,
.row-cell {
  padding: 0 10px;
}

/* =========================
   Animations
   ========================= */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

.pulse-icon {
  animation: pulse 2s infinite;
  color: var(--color-hydrogen);
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }

  50% {
    transform: scale(1.15);
    opacity: 0.8;
  }

  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* =========================
   Responsive Adjustments
   ========================= */
@media (max-width: 1024px) {
  .charts-container {
    flex-direction: column;
    gap: 28px;
  }

  .chart-section {
    min-height: 350px;
  }

  .equivalents-container {
    flex-direction: column;
  }
}

@media (max-width: 768px) {

  .summary-grid,
  .equivalents-grid {
    grid-template-columns: 1fr;
    gap: 18px;
  }

  .breakdown-container {
    grid-template-columns: 1fr;
  }

  .reduction-percentage-card {
    padding: 24px;
  }

  .percentage-value {
    font-size: 2.8rem;
  }

  .charts-container {
    gap: 24px;
  }

  .hydrogen-demand-info {
    padding: 20px;
  }

  .info-pill {
    flex-direction: column;
    border-radius: 12px;
    padding: 16px;
  }

  .divider {
    width: 80%;
    height: 1px;
    margin: 10px 0;
  }
}

@media (max-width: 600px) {
  h2 {
    font-size: 1.3rem;
  }

  h3 {
    font-size: 1rem;
  }

  .table-header,
  .table-row {
    grid-template-columns: 1.5fr 0.75fr 0.75fr;
    font-size: 0.9rem;
    padding: 12px;
  }

  .header-cell,
  .row-cell {
    padding: 0 6px;
  }

  .card-value {
    font-size: 1.2rem;
  }

  .equivalent-value {
    font-size: 1.1rem;
  }

  .percentage-description {
    font-size: 0.85rem;
  }
}
</style>