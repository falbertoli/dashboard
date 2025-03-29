<!-- File: frontend/src/components/ChartComponent.vue -->

<template>
  <div class="chart-container">
    <canvas :id="chartId" ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import Chart from 'chart.js/auto';

export default {
  name: 'ChartComponent',
  props: {
    chartId: {
      type: String,
      required: true,
    },
    chartType: {
      type: String,
      default: 'bar',
    },
    chartData: {
      type: Object,
      required: true,
    },
    chartOptions: {
      type: Object,
      default: () => ({}),
    },
  },
  setup(props) {
    const chartCanvas = ref(null);
    let chartInstance = null;

    const createChart = () => {
      const ctx = chartCanvas.value.getContext('2d');
      chartInstance = new Chart(ctx, {
        type: props.chartType,
        data: props.chartData,
        options: props.chartOptions,
      });
    };

    const destroyChart = () => {
      if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
      }
    };

    watch(
      () => [props.chartType, props.chartData, props.chartOptions],
      () => {
        destroyChart();
        createChart();
      },
      { deep: true }
    );

    onMounted(() => {
      createChart();
    });

    onUnmounted(() => {
      destroyChart();
    });

    return { chartCanvas };
  },
};
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 300px;
  /* Adjust as needed */
}
</style>