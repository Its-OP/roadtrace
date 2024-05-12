<script setup lang="ts">
  import {ref} from "vue";
  import {DataPoint} from "../schemas/latLong.ts";

  const dataPoints = ref<DataPoint[]>([
        { date: new Date('2024-04-30'), value: 110 },
        { date: new Date('2024-04-29'), value: 99 },
        { date: new Date('2024-04-28'), value: 133 },
        { date: new Date('2024-04-27'), value: 80 },
        { date: new Date('2024-04-26'), value: 124 },
        { date: new Date('2024-04-25'), value: 101 },
        { date: new Date('2024-04-24'), value: 70 },
        { date: new Date('2024-04-23'), value: 122 },
        { date: new Date('2024-04-22'), value: 112 },
        { date: new Date('2024-04-21'), value: 171 },
        { date: new Date('2024-04-20'), value: 71 },
        { date: new Date('2024-04-19'), value: 88 },
        { date: new Date('2024-04-18'), value: 131 },
        { date: new Date('2024-04-17'), value: 85 },
        { date: new Date('2024-04-16'), value: 100 },
        { date: new Date('2024-04-15'), value: 60 },
        { date: new Date('2024-04-14'), value: 53 },
        { date: new Date('2024-04-13'), value: 128 },
        { date: new Date('2024-04-12'), value: 104 },
        { date: new Date('2024-04-11'), value: 104 },
        { date: new Date('2024-04-10'), value: 139 },
        { date: new Date('2024-04-09'), value: 104 },
        { date: new Date('2024-04-08'), value: 147 },
        { date: new Date('2024-04-07'), value: 175 },
        { date: new Date('2024-04-06'), value: 112 },
        { date: new Date('2024-04-05'), value: 112 },
        { date: new Date('2024-04-04'), value: 173 },
        { date: new Date('2024-04-03'), value: 143 },
        { date: new Date('2024-04-02'), value: 115 },
        { date: new Date('2024-04-01'), value: 137 }
      ]
  );

  const series = [{
    name: "Values",
    data: dataPoints.value.map(dp => ({ x: dp.date.toISOString().split('T')[0], y: dp.value }))
  }];

  const chartOptions = {
    chart: {
      type: 'line',
      height: 'auto',
      toolbar: {
        show: true,
        offsetX: 0,
        offsetY: 0,
        tools: {
          download: false,
          selection: true,
          zoom: false,
          zoomin: true,
          zoomout: true,
          pan: false,
          reset: true
        }
      }
    },
    title: {
      text: 'Vehicles count over the month',
      align: 'center',
      style: {
        fontSize: '18px',
        fontWeight: 'bold'
      }
    },
    xaxis: {
      type: 'datetime',
      min: new Date('2024-04-01').getTime(),  // Set to the minimum date of your data
      max: new Date('2024-04-30').getTime()
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
  <div class="bg-gray-50 pl-4 pr-4 pt-1">
    <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>