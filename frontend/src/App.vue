<script setup lang="ts">
import MainView from "./views/MainView.vue";
import UsersView from "./views/UsersView.vue";
import LoginView from "./views/LoginView.vue";
</script>

<template>
<!--  <MainView />-->
  <UsersView />
<!--  <LoginView />-->
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
