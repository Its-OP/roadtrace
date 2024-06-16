<script setup lang="ts">
  import {computed, ref, watch} from "vue";
  import {Marker} from "../schemas/latLong.ts";
  import MarkerInfo from "./MarkerInfo.vue";
  import VelocityRealTimeChart from "./velocity/VelocityRealTimeChart.vue";
  import CountRealTimeChart from "./count/CountRealTimeChart.vue";
  import CountWeeklyChart from "./count/CountWeeklyChart.vue";
  import CountMonthlyChart from "./count/CountMonthlyChart.vue";
  import VelocityDailyChart from "./velocity/VelocityDailyChart.vue";
  
  interface Props {
    marker: Marker | null,
    onDelete: {
      type: Function,
      required: true
    },
    onUpdate: {
      type: Function,
      required: true
    },
  };
  
  const props = defineProps<Props>();
  const selectedMarker = computed(() => props.marker);

  const markerInfo = ref<Marker | null>(props.marker);

  watch(selectedMarker, (newMarker) => {
    markerInfo.value = newMarker;
    // Any additional handling for marker updates
  });
  
  const selectedChart = ref('week');
  const selectedOption = ref('count');
  
</script>

<template>
  <div class="w-full h-full z-[1] bg-slate-500 p-2 overflow-y-auto overflow-x-hidden scrollbar-track-black custom-scrollbar">
    <div id="camera-info" class="bg-white rounded-lg max-w-full w-full pt-1.5">
      <h1 class="font-charts text-xl text-center font-bold">Camera's Details</h1>
      <MarkerInfo :marker="markerInfo" :onDelete="onDelete" :onUpdate="onUpdate"/>
    </div>
    <div id="charts" class="bg-white rounded-lg max-w-full w-full flex flex-col justify-center mt-3 pt-1.5 pb-1.5">
      <h1 class="font-charts text-xl text-center font-bold">Camera's Data</h1>
      <v-btn-toggle v-model="selectedOption" mandatory rounded="0" class="mt-3 flex justify-stretch max-w-full w-full">
        <v-btn value="count" class="h-12 flex-1">Count</v-btn>
        <v-btn value="velocity" class="h-12 flex-1">Velocity</v-btn>
      </v-btn-toggle>
      <div v-show="selectedOption === 'count'">
        <div class="max-w-full w-full mt-1">
          <CountRealTimeChart :marker="markerInfo" />
        </div>
        <v-btn-toggle v-model="selectedChart" mandatory rounded="0" class="mt-3 flex justify-stretch max-w-full w-full">
          <v-btn value="week" class="h-12 flex-1">Week</v-btn>
          <v-btn value="month" class="h-12 flex-1">Month</v-btn>
        </v-btn-toggle>
        <div class="max-w-full w-full mt-3">
          <CountWeeklyChart v-show="selectedChart === 'week'" :marker="markerInfo" />
          <CountMonthlyChart v-show="selectedChart === 'month'" :marker="markerInfo" />
        </div>
      </div>
      <div v-show="selectedOption === 'velocity'">
        <div class="max-w-full w-full mt-1">
          <VelocityRealTimeChart :marker="markerInfo" />
        </div>
        <VelocityDailyChart :marker="markerInfo" />
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