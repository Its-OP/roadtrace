<script setup lang="ts">
  import MonthlyChart from "./MonthlyChart.vue";
  import WeeklyChart from "./WeeklyChart.vue";
  import RealTimeChart from "./RealTimeChart.vue";
  import {computed, ref, watch} from "vue";
  import {Marker} from "../schemas/latLong.ts";
  import MarkerInfo from "./MarkerInfo.vue";
  
  interface Props {
    marker: Marker | null
  };
  
  const props = defineProps<Props>();
  const selectedMarker = computed(() => props.marker);

  const markerInfo = ref<Marker | null>(props.marker);

  watch(selectedMarker, (newMarker) => {
    markerInfo.value = newMarker;
    // Any additional handling for marker updates
  });
  const selectedChart = ref('week');
  
</script>

<template>
  <div class="w-full h-full z-[1] bg-slate-500 p-2 overflow-y-auto overflow-x-hidden scrollbar-track-black custom-scrollbar">
    <div id="camera-info" class="bg-white rounded-lg max-w-full w-full pt-1.5">
      <h1 class="font-charts text-xl text-center font-bold">Camera's Details</h1>
      <MarkerInfo :marker="markerInfo" />
    </div>
    <div id="charts" class="bg-white rounded-lg max-w-full w-full flex flex-col justify-center mt-3 pt-1.5 pb-1.5">
      <h1 class="font-charts text-xl text-center font-bold">Camera's Data</h1>
      <div class="max-w-full w-full mt-1">
        <RealTimeChart />
      </div>
      <v-btn-toggle v-model="selectedChart" mandatory rounded="0" class="mt-3 flex justify-stretch max-w-full w-full">
        <v-btn value="week" class="h-12 flex-1">Week</v-btn>
        <v-btn value="month" class="h-12 flex-1">Month</v-btn>
      </v-btn-toggle>
      <div class="max-w-full w-full mt-3">
        <WeeklyChart v-show="selectedChart === 'week'" />
        <MonthlyChart v-show="selectedChart === 'month'" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 12px;
  background-color: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #888;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background-color: #f1f1f1;
}

.custom-scrollbar {
  direction: rtl;
}

.custom-scrollbar > * {
  direction: ltr;
}
</style>