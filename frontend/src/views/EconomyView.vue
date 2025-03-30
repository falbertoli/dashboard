<!-- File: frontend/src/views/EconomyView.vue -->

<template>
  <div class="economy-view">
    <h1>Economic Impact Analysis</h1>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-placeholder">
      <p>Generating charts, please wait...</p>
    </div>

    <!-- Error State -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- No Data State -->
    <div v-if="!isLoading && !error && (!results || Object.keys(results).length === 0)">
      <p class="no-data-message">No economic impact data available. Please adjust your inputs or try again later.</p>
    </div>

    <!-- Results Display -->
    <div v-if="results && Object.keys(results).length > 0">
      <h2>Revenue Drop vs Year</h2>
      <ChartComponent v-for="(data, rate) in results" :key="rate" :chartId="'chart-' + rate" chartType="line"
        :chartData="formatChartData(data, rate)" :chartOptions="chartOptions" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useEconomicsStore } from "@/store/economicsStore";
import { useHydrogenStore } from "@/store/hydrogenStore";
import { storeToRefs } from 'pinia'
import ChartComponent from "@/components/ChartComponent.vue";

export default {
  components: { ChartComponent },
  setup() {
    const economicsStore = useEconomicsStore();
    const hydrogenStore = useHydrogenStore();

    const { results, isLoading, error } = storeToRefs(economicsStore);

    const fetchData = async () => {
      const currentYear = new Date().getFullYear();

      const params = {
        totalH2Demand: hydrogenStore.totalH2Demand || 0,
        fleetPercentage: hydrogenStore.fleetPercentage || 0.1,
        startYear: currentYear,
        endYear: hydrogenStore.year || 2040,
        growthRate: 0.02,
        extraTurnTime: 30,
        turnTimeDecreaseRates: [0, 1, 2, 3, 4, 5],
      };

      console.log("API Parameters for Economic Impact:", params);

      await economicsStore.fetchEconomicImpact(params);
    };

    onMounted(() => {
      fetchData();
    });

    const formatChartData = (data, rate) => {
      if (!data || data.length === 0) {
        console.warn(`No data available for rate ${rate}.`);
        return {
          labels: [],
          datasets: [],
        };
      }

      return {
        labels: data.map((d) => d.Year),
        datasets: [
          {
            label: `${rate} min/year Reduction`,
            data: data.map((d) => d["Pct Drop"] || 0),
            borderColor: "rgba(75, 192, 192, 1)",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
          },
        ],
      };
    };

    const chartOptions = {
      responsive: true,
      plugins: {
        legend: { position: "top" },
      },
      scales: {
        x: { title: { display: true, text: "Year" } },
        y: { title: { display: true, text: "% Revenue Drop" } },
      },
    };

    return {
      results,
      isLoading,
      error,
      fetchEconomicImpact: economicsStore.fetchEconomicImpact,
      formatChartData,
      chartOptions,
    };
  },
};
</script>

<style scoped>
.economy-view {
  padding: 20px;
}

.error {
  color: red;
  font-weight: bold;
  text-align: center;
  margin: 20px 0;
}

.loading-message {
  color: blue;
  font-style: italic;
}

.loading-placeholder {
  color: gray;
  text-align: center;
  font-style: italic;
}

.no-data-message {
  color: gray;
  text-align: center;
  font-size: 1.2em;
}
</style>