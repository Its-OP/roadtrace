<script setup lang="ts">
  import {ref} from "vue";
  import {DataPoint} from "../schemas/schemas.ts";

  const dataPoints = ref<DataPoint[]>([
    { date: new Date('2024-04-30'), value: 150 },
    { date: new Date('2024-04-29'), value: 85 },
    { date: new Date('2024-04-28'), value: 80 },
    { date: new Date('2024-04-27'), value: 108 },
    { date: new Date('2024-04-26'), value: 114 },
    { date: new Date('2024-04-25'), value: 138 },
    { date: new Date('2024-04-24'), value: 107 }
  ]);

  const dataIsSufficient = () => dataPoints.value.length >= 5;

  const series = [{
    name: "Values",
    data: dataIsSufficient() ? dataPoints.value.map(dp => ({ x: dp.date.toISOString().split('T')[0], y: dp.value })) : []
  }];
  
  const chartOptions = {
    chart: {
      type: 'line',
      height: 'auto',
      toolbar: {
        show: false,
        offsetX: 0,
        offsetY: 0,
        tools: {
          download: false,
          selection: false,
          zoom: false,
          zoomin: false,
          zoomout: false,
          pan: false,
          reset: false
        }
      },
    },
    noData: {
      text: 'Insufficient data to display the chart',
      align: 'center',
      verticalAlign: 'middle',
      offsetX: 0,
      offsetY: 0,
      style: {
        fontSize: '16px',
      }
    },
    title: {
      text: 'Vehicles count over the week',
      align: 'center',
      style: {
        fontSize: '18px',
        fontWeight: 'bold'
      }
    },
    xaxis: {
      type: 'datetime'
    },
    yaxis: {
      title: {
        text: 'Vehicles Spotted'
      }
    },
    tooltip: {
      x: {
        format: 'dd MMM yyyy'
      }
    }
  };
</script>

<template>
  <div class="bg-white rounded-lg shadow-md pl-4 pr-4 pt-4">
    <apexchart type="line" height="320" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>