<script setup lang="ts">
import Map from "../components/Map.vue";
import Sidebar from "../components/Sidebar.vue";
import {ref} from "vue";
import {LatLong, Marker} from "../schemas/latLong.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {faUsers} from "@fortawesome/free-solid-svg-icons";

const markers = ref<Marker[]>([
  { id: 0, coordinates: { lng: -71.214518, lat: 42.203995 }, source: 'test', dirty: false },
  { id: 1, coordinates: { lng: -71.234518, lat: 42.2203995 }, source: 'test', dirty: false },
  { id: 2, coordinates: { lng: -71.254518, lat: 42.2403995 }, source: 'test', dirty: false },
]);

const handleUpdateMarker = (markerId: number, newCoordinates: LatLong): void => {
  console.log(markerId);
  console.log(newCoordinates);
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
  <div class="h-screen w-screen flex">
    <div class="w-[30%]">
      <Sidebar :marker="markers[0]" />
    </div>
    <div class="w-[70%]">
      <Map :markers="markers" @addMarker="handleAddMarker" @updateMarker="handleUpdateMarker"/>
    </div>
  </div>
</template>

<style scoped>

</style>