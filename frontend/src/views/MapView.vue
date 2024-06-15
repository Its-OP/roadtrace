<script setup lang="ts">
import Map from "../components/Map.vue";
import Sidebar from "../components/Sidebar.vue";
import {ref} from "vue";
import {LatLong, Marker} from "../schemas/latLong.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {faUsers} from "@fortawesome/free-solid-svg-icons";

const markers = ref<Marker[]>([]);

const save = () => {
  for (const marker of markers.value) {
    marker.dirty = false;
  }
    
  localStorage.setItem('markers', JSON.stringify(markers.value));
}

const reset = () => {
  markers.value = [];
  for (const marker of JSON.parse(localStorage.getItem('markers') ?? '') as Marker[]) {
    markers.value.push(marker);
  }
}

const handleUpdateMarker = (markerId: number, newCoordinates: LatLong): void => {
  const markerIndex = markers.value.findIndex(m => m.id === markerId);
  if (markerIndex === -1)
    return;
  
  const marker = markers.value[markerIndex];
  marker.coordinates = newCoordinates;
  marker.dirty = true;
  markers.value.splice(markerIndex, 1, marker);
}

const handleAddMarker = (markerLatLong: LatLong): void => {
  const marker: Marker = {
    id: markers.value.length,
    coordinates: markerLatLong,
    source: '',
    dirty: true
  };
  
  markers.value.push(marker);
}
</script>

<template>
  <div class="absolute top-4 right-4 z-50">
    <router-link to="/users">
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold rounded-full h-10 w-10">
        <FontAwesomeIcon :icon="faUsers" />
      </button>
    </router-link>
  </div>
  <div class="h-screen w-screen flex relative">
    <div class="w-[30%]">
      <Sidebar :marker="markers[0]" />
    </div>
    <div class="w-[70%] relative">
      <Map :markers="markers"
           @addMarker="handleAddMarker"
           @updateMarker="handleUpdateMarker"
           :onSave="save"
           :onReset="reset"/>
    </div>
  </div>
</template>

<style scoped>

</style>