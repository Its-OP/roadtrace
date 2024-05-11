<script setup lang="ts">
import { ref, onUnmounted } from 'vue';
import { DataPoint } from '../schemas/schemas.ts';

// Helper function to generate random values between min and max
function generateRandomValue(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

const startDate = new Date('2024-04-30T00:00:00');

const dataPoints = ref<DataPoint[]>([
  { date: new Date(startDate.getTime()), value: generateRandomValue(5, 15) },
  { date: new Date(startDate.getTime() + 1000), value: generateRandomValue(5, 15) },
  { date: new Date(startDate.getTime() + 2000), value: generateRandomValue(5, 15) },
]);

const dataIsSufficient = () => dataPoints.value.length >= 5;

const series = ref([{
  name: "Values",
  data: dataIsSufficient()
    ? dataPoints.value.map(dp => ({ x: dp.date.toISOString().split('T')[0] + ' ' + dp.date.toTimeString().split(' ')[0], y: dp.value }))
    : []
}]);

const intervalId = setInterval(() => {
  const newValue = generateRandomValue(5, 15);
  const lastDate = new Date(dataPoints.value.at(-1).date.getTime() + 1000); // Increment last date by 1 second
  dataPoints.value.push({ date: lastDate, value: newValue });

  if (dataPoints.value.length > 20) {
    dataPoints.value.shift(); // Remove the first element if length exceeds 20
  }

  series.value[0].data = dataPoints.value.map(dp => ({
    x: dp.date.toISOString().split('T')[0] + ' ' + dp.date.toTimeString().split(' ')[0],
    y: dp.value
  }));
}, 1000);

onUnmounted(() => {
  clearInterval(intervalId);
});

const chartOptions = {
  chart: {
    type: 'line',
    height: 'auto',
    animations: {
      enabled: true,
      easing: 'linear',
      dynamicAnimation: {
        speed: 100
      }
    },
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
    text: 'Vehicles count per second',
    align: 'center',
    style: {
      fontSize: '18px',
      fontWeight: 'bold'
    }
  },
  xaxis: {
    type: 'datetime',
    labels: {
      format: 'HH:mm:ss'
    }
  },
  yaxis: {
    title: {
      text: 'Vehicles Spotted'
    }
  },
  tooltip: {
    x: {
      format: 'dd MMM yyyy HH:mm:ss'
    }
  }
};
</script>

<template>
  <div class="bg-white rounded-lg shadow-md pl-4 pr-4 pt-4">
    <apexchart type="line" height="320" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>
