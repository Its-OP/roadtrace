<script setup lang="ts">
import {ref, onUnmounted, watch, onMounted} from 'vue';
import {DataPoint, Marker} from '../../schemas/latLong.ts';

interface Props {
  marker: Marker | null
};

const props = defineProps<Props>();
const intervalId = ref(0);

const getDataPoints = () => [
  { date: new Date(new Date().getTime() - 2000), value: generateRandomValue(110, 120) },
  { date: new Date(new Date().getTime() - 1000), value: generateRandomValue(110, 120) },
  { date: new Date(new Date().getTime()), value: generateRandomValue(110, 120) },
];

// Helper function to generate random values between min and max
function generateRandomValue(min: number, max: number): number {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

const dataPoints = ref<DataPoint[]>([]);

const dataIsSufficient = () => dataPoints.value.length >= 5;

const series = ref([{
  name: "Values",
  data: []
}]);

const runFillSeries = () => {
  console.log(props.marker);
  intervalId.value = setInterval(() => {
    if (!props.marker?.code || !props.marker?.source) {
      return;
    }
    
    const newValue = generateRandomValue(110, 120);
    dataPoints.value.push({ date: new Date(), value: newValue });

    if (dataPoints.value.length > 20) {
      dataPoints.value.shift(); // Remove the first element if length exceeds 20
    }

    series.value[0].data = dataIsSufficient()
        ? dataPoints.value.map(dp => ({
            x: dp.date.toISOString().split('T')[0] + ' ' + dp.date.toTimeString().split(' ')[0],
            y: dp.value
          }))
        : [];
  }, 1000);
}

watch(() => props.marker, (newMarker) => {
  if (newMarker) {
    clearInterval(intervalId.value);
    series.value[0].data = [];
    dataPoints.value = getDataPoints();
    runFillSeries();
  }
}, { immediate: true });

onUnmounted(() => {
  clearInterval(intervalId.value);
});

const chartOptions = {
  chart: {
    type: 'line',
    height: 'auto',
    animations: {
      enabled: false,
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
    text: 'Average vehicles` speed per second',
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
      text: 'Speed (km/h)'
    }
  },
  tooltip: {
    x: {
      format: 'HH:mm:ss'
    }
  }
};
</script>

<template>
  <div class="bg-gray-50 pl-4 pr-4 pt-1">
    <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>
