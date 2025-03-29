<!-- File: frontend/src/components/Storage/StorageCostBreakdownChart.vue -->

<template>
  <DoughnutChart :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  construction: Number,
  insulation: Number
})

const chartData = computed(() => ({
  labels: ['Construction', 'Insulation'],
  datasets: [{
    data: [props.construction, props.insulation],
    backgroundColor: ['#64ffda', '#2979ff'],
    borderWidth: 0
  }]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        boxWidth: 12,
        padding: 20
      }
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          return ` ${context.label}: $${context.raw.toLocaleString()}`
        }
      }
    }
  },
  cutout: '75%'
}
</script>