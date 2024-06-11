<script setup lang="ts"> </script>

<template>
 <router-view></router-view>
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
