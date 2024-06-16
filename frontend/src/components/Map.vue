<script setup lang="ts">
  import { MapboxMap, MapboxNavigationControl, MapboxMarker } from '@studiometa/vue-mapbox-gl';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import {LatLong, Marker} from "../schemas/latLong.ts";
  import * as mapboxgl from "mapbox-gl";
  import {computed, ref} from "vue";
  import { v4 as uuidv4 } from 'uuid';
  const accessToken = "pk.eyJ1IjoiaXRzb3AiLCJhIjoiY2x2bWxnZXljMDM3NzJpcDFlMTAzeGh2bSJ9.FkHnP5wDLcyy7vrMosVxlA";
  
  const mapCenter: LatLong = { lng: -71.224518, lat: 42.213995 };
  const map = ref<mapboxgl.Map | null>(null);
  
  const emits = defineEmits(['addMarker', 'removeMarker', 'updateMarker', 'setSelectedMarker']);
  const props = defineProps({
    markers: {
      type: Array as () => Marker[],
      required: true
    },
    onSave: {
      type: Function,
      required: true
    },
    onReset: {
      type: Function,
      required: true
    }
  });

  const findClosestMarker = (clickLat: number, clickLon: number) : Marker | null => {
    const boundaryLat = 0.005;
    const boundaryLon = 0.005;
    let closestMarker: Marker | null = null;
    let minDistance = Number.MAX_VALUE;

    props.markers.forEach((marker) => {
      const markerLat = marker.coordinates.lat;
      const markerLon = marker.coordinates.lng;

      if (
          Math.abs(markerLat - clickLat) <= boundaryLat &&
          Math.abs(markerLon - clickLon) <= boundaryLon
      ) {
        const distance = Math.sqrt(
            Math.pow(markerLat - clickLat, 2) + Math.pow(markerLon - clickLon, 2)
        );

        if (distance < minDistance) {
          minDistance = distance;
          closestMarker = marker;
        }
      }
    });

    return closestMarker;
  };

  const showButtons = computed(() => props.markers.some(marker => marker.dirty));
  const updateMarkerPosition = (updatedMarker: mapboxgl.Marker, markerId: number): void => {
    const newCoordinates: LatLong = {
      lng: updatedMarker.getLngLat().lng,
      lat: updatedMarker.getLngLat().lat
    };
    
    emits('updateMarker', markerId, newCoordinates);
  };
  
  const onMapDblClick = (event: mapboxgl.MapMouseEvent): void => {
    event.preventDefault();
    const clickLatLong: LatLong = {
      lat: event.lngLat.lat,
      lng: event.lngLat.lng
    }
    
    emits('addMarker', clickLatLong);
  }
  
  const onMapClick = (event: mapboxgl.MapMouseEvent): void => {
    const closestMarker = findClosestMarker(event.lngLat.lat, event.lngLat.lng);
    if (closestMarker) {
      setSelectedMarker(closestMarker);
    }
  }
  
  const setSelectedMarker = (marker: Marker) => {
    emits('setSelectedMarker', marker)
  }
  
  const onMapCreated = (mapboxMap: mapboxgl.Map) => {
    map.value = mapboxMap;
    props.onReset();
  };
</script>

<template>
  <div v-if="showButtons" class="absolute top-4 left-1/2 transform -translate-x-1/2 z-10 flex space-x-6">
    <button @click="onReset" class="bg-red-600 hover:bg-red-800 text-white py-2 px-4 rounded-md w-[100px]">
      RESET
    </button>
    <button @click="onSave" class="bg-green-600 hover:bg-green-800 text-white py-2 px-4 rounded-md w-[100px]">
      SAVE
    </button>
  </div>
  <MapboxMap 
    class="h-full w-full z-[1]"
    :access-token="accessToken"
    :zoom="12"
    :center="[mapCenter.lng, mapCenter.lat]"
    map-style="mapbox://styles/itsop/clvmljz4901kf01qu3ps6hzs3"
    @mb-dblclick="onMapDblClick"
    @mb-click="onMapClick"
    @mb-load="event => onMapCreated(event.target)"
  >
    <MapboxMarker v-for="marker in markers"
                  :key="uuidv4()"
                  :id="marker.id"
                  :draggable="true"
                  :lng-lat="[marker.coordinates.lng, marker.coordinates.lat]"
                  :color="marker.dirty ? 'red' : null"
                  @mb-dragend="event => updateMarkerPosition(event.target, marker.id)"
                  @mb-dragstart="_ => setSelectedMarker(marker)"/>
    <MapboxNavigationControl position="bottom-right" />
  </MapboxMap>
</template>