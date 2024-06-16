<script setup lang="ts">
  import {Marker} from "../../schemas/latLong.ts";
  import {ref, watch} from "vue";

  interface Props {
    marker: Marker | null
  };

  const props = defineProps<Props>();

  const series = ref([{
    name: "Values",
    data: props.marker?.numbers.map(dp => ({ x: dp.date.toISOString().split('T')[0], y: dp.value })) ?? []
  }]);

  watch(() => props.marker, (newMarker) => {
    if (newMarker) {
      series.value = [
        {
          name: "Values",
          data: newMarker.numbers.map(dp => ({
            x: dp.date.toISOString().split('T')[0],
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
      text: 'Vehicles count over the month',
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
  <div class="bg-gray-50 pl-4 pr-4 pt-1">
    <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>