<script setup lang="ts">
import Map from "../components/Map.vue";
import Sidebar from "../components/Sidebar.vue";
import {ref} from "vue";
import {Marker} from "../schemas/schemas.ts";

const markers = ref<Marker[]>([
  { id: 1, coordinates: { lng: -71.214518, lat: 42.203995 }, dirty: false },
  { id: 2, coordinates: { lng: -71.234518, lat: 42.2203995 }, dirty: false },
  { id: 3, coordinates: { lng: -71.254518, lat: 42.2403995 }, dirty: false },
]);

const handleUpdateMarker = (marker: Marker): void => {
  console.log('handle update')
  const markerIndex = markers.value.findIndex(m => m.id === marker.id);
  markers.value.splice(markerIndex, 1, marker);
}

const handleAddMarker = (marker: Marker): void => {
  marker.id = markers.value.length;
  markers.value.push(marker);
}
</script>

<template>
  <div class="h-screen w-screen flex">
    <div class="w-[70%]">
      <Map :markers="markers" @addMarker="handleAddMarker" @updateMarker="handleUpdateMarker"/>
    </div>
    <div class="w-[30%]">
      <Sidebar />
    </div>
  </div>
</template>

<style scoped>

</style>