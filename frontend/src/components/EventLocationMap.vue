<!-- components/EventLocationMap.vue -->
<template>
  <div
    id="event-map"
    style="height: 300px; width: 100%; border-radius: 12px; margin-top: 8px;"
  ></div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { Loader } from '@googlemaps/js-api-loader'

const props = defineProps({
  latitude: Number,
  longitude: Number,
  title: String,
})

// const apiKey = 'your api key' 

onMounted(async () => {
  if (!props.latitude || !props.longitude) return

  const loader = new Loader({ apiKey, version: 'weekly' })
  loader.load().then(() => {
    const map = new google.maps.Map(document.getElementById('event-map'), {
      center: { lat: props.latitude, lng: props.longitude },
      zoom: 15,
    })

    const marker = new google.maps.Marker({
      position: { lat: props.latitude, lng: props.longitude },
      map,
      title: props.title,
    })

    const infoWindow = new google.maps.InfoWindow({
      content: `<strong>${props.title}</strong>`,
    })

    marker.addListener('click', () => {
      infoWindow.open(map, marker)
    })
  })
})
</script>
