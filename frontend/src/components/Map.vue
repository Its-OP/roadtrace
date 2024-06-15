<script setup lang="ts">
  import { MapboxMap, MapboxNavigationControl, MapboxMarker } from '@studiometa/vue-mapbox-gl';
  import 'mapbox-gl/dist/mapbox-gl.css';
  import {LatLong, Marker} from "../schemas/latLong.ts";
  import * as mapboxgl from "mapbox-gl";
  import {ref} from "vue";
  import { v4 as uuidv4 } from 'uuid';
  const accessToken = "pk.eyJ1IjoiaXRzb3AiLCJhIjoiY2x2bWxnZXljMDM3NzJpcDFlMTAzeGh2bSJ9.FkHnP5wDLcyy7vrMosVxlA";
  
  const mapCenter: LatLong = { lng: -71.224518, lat: 42.213995 };
  const map = ref<mapboxgl.Map | null>(null);
  
  const emits = defineEmits(['addMarker', 'removeMarker', 'updateMarker']);
  const props = defineProps({
    markers: {
      type: Array as () => Marker[],
      required: true
    }
  });
  
  const updateMarkerPosition = (updatedMarker: mapboxgl.Marker, markerId: number): void => {
    const newCoordinates: LatLong = {
      lng: updatedMarker.getLngLat().lng,
      lat: updatedMarker.getLngLat().lat
    };
    
    emits('updateMarker', markerId, newCoordinates);
  };
  
  const onMapClick = (event: mapboxgl.MapMouseEvent): void => {
    event.preventDefault();
    const clickLatLong: LatLong = {
      lat: event.lngLat.lat,
      lng: event.lngLat.lng
    }
    
    emits('addMarker', clickLatLong);
  }
  
  const onMapCreated = (mapboxMap: mapboxgl.Map) => {
    map.value = mapboxMap;
  };
</script>

<template>
  <MapboxMap 
    class="h-full w-full z-[1]"
    :access-token="accessToken"
    :zoom="12"
    :center="[mapCenter.lng, mapCenter.lat]"
    map-style="mapbox://styles/itsop/clvmljz4901kf01qu3ps6hzs3"
    @mb-dblclick="onMapClick"
    @mb-load="event => onMapCreated(event.target)"
  >
    <MapboxMarker v-for="marker in markers"
                  :key="uuidv4()"
                  :draggable="true"
                  :lng-lat="[marker.coordinates.lng, marker.coordinates.lat]"
                  :color="marker.dirty ? 'red' : null"
                  @mb-dragend="event => updateMarkerPosition(event.target, marker.id)"/>
    <MapboxNavigationControl position="bottom-right" />
  </MapboxMap>
</template>