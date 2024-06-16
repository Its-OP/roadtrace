<script setup lang="ts">
  import {Marker} from "../../schemas/latLong.ts";
  import {ref, watch} from "vue";

  interface Props {
    marker: Marker | null
  };

  const props = defineProps<Props>();

  const series = ref([{
    name: "Values",
    data: props.marker?.numbers.slice(0, 7).map(dp => ({ x: dp.date.toISOString().split('T')[0], y: dp.value })) ?? []
  }]);

  watch(() => props.marker, (newMarker) => {
    if (newMarker) {
      series.value = [
        {
          name: "Values",
          data: newMarker.numbers.slice(0, 7).map(dp => ({
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
  <div class="bg-gray-50 pl-4 pr-4 pt-1">
    <apexchart type="line" height="350" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>