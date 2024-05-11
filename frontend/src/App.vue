<script setup lang="ts">
import MainView from "./views/MainView.vue";
</script>

<template>
  <MainView />
</template>

<style>
  html {
    overflow: hidden !important;
    scrollbar-width: none;
    -ms-overflow-style: none;
  }
  
  html::-webkit-scrollbar {
    width: 0;
    height: 0;
  }
</style>
