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
          <strong>{{ formatNumber(parseFloat(hydrogenStore.totalH2Demand)) }} ft³</strong>
        </div>
        <div class="breakdown-container">
          <div class="breakdown-item">
            <div class="icon-wrapper">
              <i class="fas fa-plane"></i>
            </div>
            <div class="content">
              <span>Aircraft</span>
              <strong>{{ formatNumber(hydrogenStore.aircraftH2Demand.daily_h2_demand_ft3) }} ft³</strong>
            </div>
          </div>
          <div class="breakdown-item">
            <div class="icon-wrapper">
              <i class="fas fa-truck"></i>
            </div>
            <div class="content">
              <span>Ground Vehicles</span>
              <strong>{{ formatNumber(hydrogenStore.gseH2Demand.daily_h2_demand_ft3) }} ft³</strong>
            </div>
          </div>
        </div>
      </div>

      <p>Click the button below to calculate the emissions impact of hydrogen adoption.</p>
      <button class="calculate-btn" @click="calculateEmissions">
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
              formatNumber(parseFloat(hydrogenStore.totalH2Demand)) }}
                ft³</strong></span>
          </div>
          <div class="divider"></div>
          <div class="pill-item">
            <i class="fas fa-plane-departure"></i>
            <span class="hydrogen-demand-summary-span">Fleet Adoption: <strong>{{
              formatNumber(parseFloat(hydrogenStore.fleetPercentage)) }}%</strong></span>
          </div>
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
            <div class="card-value">{{ formatNumber(emissionsReduction) }} metric tons</div>
            <div class="card-percentage">{{ emissionsReductionPercentage.toFixed(1) }}% reduction</div>
          </div>
        </div>

        <div class="summary-card conventional">
          <div class="card-icon">
            <i class="fas fa-plane"></i>
          </div>
          <div class="card-content">
            <div class="card-title">Conventional Operations</div>
            <div class="card-value">{{ formatNumber(totalJetAEmissions) }} metric tons CO₂</div>
            <div class="card-percentage">Baseline scenario</div>
          </div>
        </div>

        <div class="summary-card hydrogen">
          <div class="card-icon">
            <i class="fas fa-atom"></i>
          </div>
          <div class="card-content">
            <div class="card-title">Hybrid Operations</div>
            <div class="card-value">{{ formatNumber(totalHydrogenEmissions) }} metric tons CO₂</div>
            <div class="card-percentage">Hydrogen transition scenario</div>
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
        <div class="equivalents-grid">
          <div class="equivalent-card">
            <div class="equivalent-icon">
              <i class="fas fa-tree"></i>
            </div>
            <div class="equivalent-content">
              <div class="equivalent-title">Carbon Sequestration Equivalent</div>
              <div class="equivalent-value">{{ formatNumber(carbonOffsetEquivalent) }} trees</div>
              <div class="equivalent-description">Number of trees needed to absorb the same amount of CO₂ over one year
              </div>
            </div>
          </div>

          <div class="equivalent-card">
            <div class="equivalent-icon">
              <i class="fas fa-car"></i>
            </div>
            <div class="equivalent-content">
              <div class="equivalent-title">Vehicle Emissions Equivalent</div>
              <div class="equivalent-value">{{ formatNumber(vehicleEquivalent) }} cars</div>
              <div class="equivalent-description">Number of cars taken off the road for one year</div>
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
            <div class="row-cell">{{ formatNumber(emissionsResults.just_jetA_co2) }}</div>
            <div class="row-cell">100%</div>
          </div>

          <div class="table-row">
            <div class="row-cell">Jet A (Hybrid)</div>
            <div class="row-cell">{{ formatNumber(emissionsResults.jetA_co2) }}</div>
            <div class="row-cell">{{ ((emissionsResults.jetA_co2 / emissionsResults.just_jetA_co2) * 100).toFixed(1) }}%
            </div>
          </div>

          <div class="table-row">
            <div class="row-cell">Hydrogen</div>
            <div class="row-cell">{{ formatNumber(emissionsResults.H2_co2) }}</div>
            <div class="row-cell">{{ ((emissionsResults.H2_co2 / emissionsResults.just_jetA_co2) * 100).toFixed(1)
            }}%
            </div>
          </div>

          <div class="table-row total">
            <div class="row-cell">Total Reduction</div>
            <div class="row-cell">{{ formatNumber(emissionsReduction) }}</div>
            <div class="row-cell">{{ emissionsReductionPercentage.toFixed(1) }}%</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useHydrogenStore } from '@/store/hydrogenStore';
import { useSustainabilityStore } from '@/store/sustainabilityStore';
import ChartComponent from '@/components/ChartComponent.vue';

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
  vehicleEquivalent
} = storeToRefs(sustainabilityStore);

// Format number with commas
const formatNumber = (value) => {
  return new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 2
  }).format(value || 0);
};

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
        backgroundColor: ['rgba(255, 99, 132, 0.8)',],
        borderColor: ['rgba(255, 99, 132, 1)',],
        borderWidth: 1
      },
      {
        label: 'Jet A Emissions Hybrid',
        data: [0, emissionsResults.value.jetA_co2],
        backgroundColor: ['rgba(255, 255, 80, 0.8)'],
        borderColor: ['rgba(54, 162, 235, 1)'],
        borderWidth: 3
      },
      {
        label: 'Hydrogen Emissions',
        data: [0, emissionsResults.value.H2_co2],
        backgroundColor: 'rgba(10, 255, 10, 0.8)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 3
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
            return `${context.dataset.label}: ${formatNumber(context.raw)} metric tons CO₂`;
          },
          footer: function (tooltipItems) {
            let sum = 0;
            tooltipItems.forEach(item => {
              sum += item.raw;
            });
            return `Total: ${formatNumber(sum)} metric tons CO₂`;
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
          color: '#aaa'
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
        'rgba(76, 175, 80, 0.8)',
        'rgba(54, 162, 235, 0.8)'
      ],
      borderColor: [
        'rgba(76, 175, 80, 1)',
        'rgba(54, 162, 235, 1)'
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
            return `${context.label}: ${formatNumber(value)} metric tons (${percentage}%)`;
          }
        }
      }
    }
  };
});
</script>

<style scoped>
/* =========================
   Global & Utility Styles
   ========================= */
.emissions-analysis {
  margin-bottom: 30px;
}

/* =========================
   Headings
   ========================= */
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

/* =========================
   Alerts & Feedback Messages
   ========================= */
.error-message {
  border-left: 4px solid #e74c3c;
  color: #e74c3c;
  background-color: rgba(255, 99, 132, 0.1);
  padding: 15px;
  border-radius: 6px;
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

.no-results {
  color: #aaa;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 20px;
  border-radius: 8px;
  text-align: center;
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
.calculate-btn {
  margin-top: 15px;
  padding: 10px 20px;
  background-color: #64ffda;
  color: #1a1e24;
  border: none;
  border-radius: 4px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.calculate-btn:hover {
  background-color: #73ffde;
  transform: translateY(-2px);
}

.calculate-btn i {
  font-size: 1rem;
}

/* =========================
   Hydrogen Demand Info
   ========================= */
.hydrogen-demand-info {
  background: linear-gradient(145deg, rgba(54, 162, 235, 0.1), rgba(100, 255, 218, 0.1));
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 25px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.hydrogen-demand-info h3 {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #64ffda;
  margin-bottom: 20px;
  font-size: 1.2rem;
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
  color: #64ffda;
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
  background: rgba(100, 255, 218, 0.1);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-wrapper i {
  color: #64ffda;
  font-size: 1.1rem;
}

.breakdown-item .content {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.breakdown-item span {
  color: #aaa;
  font-size: 0.9rem;
}

.breakdown-item strong {
  color: #fff;
  font-size: 1.1rem;
}

@media (max-width: 600px) {
  .breakdown-container {
    grid-template-columns: 1fr;
  }
}

/* =========================
   Hydrogen Demand Summary Pill
   ========================= */
.hydrogen-demand-summary-span {
  padding-left: 10px;
}

/* =========================
   Results & Summary Cards
   ========================= */
.results-container {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.summary-card {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 15px;
}

.summary-card.reduction {
  background-color: rgba(76, 175, 80, 0.1);
  border-left: 4px solid #4caf50;
}

.summary-card.conventional {
  background-color: rgba(255, 99, 132, 0.1);
  border-left: 4px solid #ff6384;
}

.summary-card.hydrogen {
  background-color: rgba(54, 162, 235, 0.1);
  border-left: 4px solid #36a2eb;
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
  background-color: rgba(76, 175, 80, 0.2);
  color: #4caf50;
}

.summary-card.conventional .card-icon {
  background-color: rgba(255, 99, 132, 0.2);
  color: #ff6384;
}

.summary-card.hydrogen .card-icon {
  background-color: rgba(54, 162, 235, 0.2);
  color: #36a2eb;
}

.card-content {
  flex: 1;
}

.card-title {
  color: #aaa;
  font-size: 0.9rem;
  margin-bottom: 5px;
}

.card-value {
  color: #fff;
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 5px;
}

.summary-card.reduction .card-value {
  color: #4caf50;
}

.summary-card.conventional .card-value {
  color: #ff6384;
}

.summary-card.hydrogen .card-value {
  color: #36a2eb;
}

.card-percentage {
  color: #aaa;
  font-size: 0.9rem;
}

/* =========================
   Chart Section
   ========================= */
.chart-section,
.equivalents-section,
.breakdown-section {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
}

.chart-container {
  height: 300px;
  position: relative;
}

/* =========================
   Equivalents Grid & Cards
   ========================= */
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
}

.equivalent-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: rgba(100, 255, 218, 0.1);
  color: #64ffda;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
}

.equivalent-content {
  flex: 1;
}

.equivalent-title {
  color: #ddd;
  font-size: 1rem;
  margin-bottom: 5px;
}

.equivalent-value {
  color: #64ffda;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 5px;
}

.equivalent-description {
  color: #aaa;
  font-size: 0.8rem;
}

/* =========================
   Table
   ========================= */
.table-container {
  width: 100%;
  border-collapse: collapse;
}

.table-header {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  background-color: rgba(255, 255, 255, 0.05);
  padding: 12px 15px;
  border-radius: 6px 6px 0 0;
  font-weight: 600;
  color: #ddd;
}

.table-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
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
   Charts Container & Responsive Layout
   ========================= */
.charts-container {
  display: flex;
  gap: 20px;
  margin-bottom: 25px;
}

.chart-section {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
  flex: 1;
  min-width: 0;
  /* Prevents flex items from overflowing */
}

/* =========================
   Responsive Adjustments
   ========================= */
@media (max-width: 1024px) {
  .charts-container {
    flex-direction: column;
  }
}

@media (max-width: 768px) {

  .summary-grid,
  .equivalents-grid {
    grid-template-columns: 1fr;
  }

  .table-header,
  .table-row {
    grid-template-columns: 2fr 1fr 1fr;
  }
}
</style>