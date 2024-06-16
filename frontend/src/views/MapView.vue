<script setup lang="ts">
import Map from "../components/Map.vue";
import Sidebar from "../components/Sidebar.vue";
import {ref} from "vue";
import {LatLong, Marker} from "../schemas/latLong.ts";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {faUsers} from "@fortawesome/free-solid-svg-icons";

const getMarkersFromLocalStorage = (): Marker[] => {
  const markers = (JSON.parse(localStorage.getItem('markers') ?? '', (key, value) => {
    if (key === 'date') {
      return new Date(value);
    }
    return value;
  }) as Marker[]);
  
  markers.forEach(m => m.numbers = m.numbers.sort((a, b) => b.date.getTime() - a.date.getTime()));
  return markers;
}

const markers = ref<Marker[]>(getMarkersFromLocalStorage());
const selectedMarker = ref<Marker | null>(markers.value[0]);

console.log(markers.value);

const save = () => {
  for (const marker of markers.value) {
    marker.dirty = false;
  }
    
  localStorage.setItem('markers', JSON.stringify(markers.value));
}

const handleDeleteMarker = (id: number) => {
  const markerIndex = markers.value.findIndex(m => m.id === id);
  if (markerIndex === -1)
    return;

  markers.value.splice(markerIndex, 1);
  save();
  selectedMarker.value = markers.value[0]
}

const reset = () => {
  markers.value = [];
  for (const marker of getMarkersFromLocalStorage()) {
    markers.value.push(marker);
  }
  
  if (!selectedMarker.value) {
    selectedMarker.value = markers.value.length ? markers.value[0] : null;
  } 
}

const setSelectedMarker = (marker: Marker) => {
  selectedMarker.value = marker;
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
    code: '',
    dirty: true,
    numbers: []
  };
  
  markers.value.push(marker);
}

const handleUpdateMarkerDetails = (markerId: number, newSource: string, newCode: string) => {
  const markerIndex = markers.value.findIndex(m => m.id === markerId);
  if (markerIndex === -1)
    return;

  const marker = markers.value[markerIndex];
  marker.source = newSource;
  marker.code = newCode;
  markers.value.splice(markerIndex, 1, marker);
  save();
  reset();
  setSelectedMarker(marker);
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
      <Sidebar :marker="selectedMarker" :onDelete="handleDeleteMarker" :onUpdate="handleUpdateMarkerDetails"/>
    </div>
    <div class="w-[70%] relative">
      <Map :markers="markers"
           @addMarker="handleAddMarker"
           @updateMarker="handleUpdateMarker"
           :onSave="save"
           :onReset="reset"
           @setSelectedMarker="setSelectedMarker"/>
    </div>
  </div>
</template>

<style scoped>

</style>