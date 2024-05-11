<script setup lang="ts">
  import MonthlyChart from "./MonthlyChart.vue";
  import WeeklyChart from "./WeeklyChart.vue";
  import {ref} from "vue";

  const selectedChart = ref('week');
</script>

<template>
  <div class="h-full w-full z-[1] bg-slate-500 p-2 flex flex-col items-center">
    <div class="flex-1"> <!-- Content that might be above the chart -->
      <!-- Other sidebar content goes here -->
    </div>
    <v-btn-toggle v-model="selectedChart" mandatory rounded>
      <v-btn value="week">Week</v-btn>
      <v-btn value="month">Month</v-btn>
    </v-btn-toggle>
    <div class="max-w-full w-full mt-3">
<!--      <RealTimeChart v-if="selectedChart === 'week'" />-->
      <WeeklyChart v-if="selectedChart === 'week'" />
      <MonthlyChart v-else-if="selectedChart === 'month'" />
    </div>
  </div>
</template>

<style scoped>

</style>