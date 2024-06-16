<script setup lang="ts">
  import {Marker} from "../../schemas/latLong.ts";
  import {ref, watch} from "vue";

  interface Props {
    marker: Marker | null
  };

  const props = defineProps<Props>();
  console.log(props.marker)
  
  const stringifyDate = (date: Date): string => {
    return date.toISOString().split('T')[0] + ' ' + date.toISOString().split('T')[1].split('.')[0]
  }

  const series = ref([{
    name: "Values",
    data: props.marker?.velocities.reverse().map(dp => ({ x: stringifyDate(dp.date), y: dp.value })) ?? []
  }]);

  console.log(series.value)

  watch(() => props.marker, (newMarker) => {
    if (newMarker) {
      series.value = [
        {
          name: "Values",
          data: newMarker.velocities.reverse().map(dp => ({
            x: stringifyDate(dp.date),
            y: dp.value
          }))
        }
      ];
    }
  }, { immediate: true });

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
      text: 'Average vehicles` speed for every hour',
      align: 'center',
      style: {
        fontSize: '18px',
        fontWeight: 'bold'
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
    xaxis: {
      type: 'datetime',
        labels: {
          format: 'dd MMM yyyy HH:mm:ss'
        }
    },
    yaxis: {
      title: {
        text: 'Speed (km/h)'
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
  <div class="bg-gray-50 pl-4 pr-4 pt-1">
    <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>