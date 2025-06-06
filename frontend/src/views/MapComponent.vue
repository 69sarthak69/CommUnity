<template>
  <div
    id="map"
    style="height: 300px; width: 100%; border-radius: 12px; margin-top: 12px;"
  ></div>
</template>

<script setup lang="ts">
import { onMounted, nextTick, ref } from 'vue'
import { Loader } from '@googlemaps/js-api-loader'

declare const google: any

const apiKey = 'AIzaSyAS7aBWvCP0nj1SlYs-H-grA1Zs35TE4QE'

const events = ref([])

const fetchEvents = async () => {
  const res = await fetch('http://127.0.0.1:8000/api/events/')
  const data = await res.json()
  events.value = data
}

onMounted(async () => {
  await nextTick()
  await fetchEvents()

  const loader = new Loader({ apiKey, version: 'weekly' })

  loader.load().then(() => {
    const map = new google.maps.Map(document.getElementById('map'), {
      center: { lat: 27.7172, lng: 85.324 }, // Kathmandu
      zoom: 7,
    })

    const categoryIcons: Record<string, any> = {
  Education: {
    url: 'https://maps.google.com/mapfiles/kml/shapes/schools.png',
    scaledSize: new google.maps.Size(32, 32),
  },
  Emergency: {
    url: 'https://maps.google.com/mapfiles/kml/shapes/caution.png',
    scaledSize: new google.maps.Size(32, 32),
  },
  'Elderly Care': {
    url: 'https://maps.google.com/mapfiles/kml/shapes/info-i_maps.png',
    scaledSize: new google.maps.Size(32, 32),
  },
  Health: {
    url: 'https://maps.google.com/mapfiles/kml/shapes/hospitals.png',
    scaledSize: new google.maps.Size(32, 32),
  },
  Environment: {
    url: 'https://maps.google.com/mapfiles/kml/shapes/parks.png',
    scaledSize: new google.maps.Size(32, 32),
  },
  Others: {
    url: 'https://maps.google.com/mapfiles/kml/shapes/flag.png',
    scaledSize: new google.maps.Size(32, 32),
  },
}


    events.value.forEach((event: any) => {
      if (event.latitude && event.longitude) {
        const marker = new google.maps.Marker({
          position: { lat: event.latitude, lng: event.longitude },
          map,
          title: event.title,
          icon: categoryIcons[event.category] || categoryIcons['Others'],
        })

        const infoWindow = new google.maps.InfoWindow({
          content: `
            <strong>${event.title}</strong><br/>
            🏷️ <em>${event.category}</em><br/>
            📍 ${event.location}<br/>
            📅 ${new Date(event.date).toDateString()}
          `
        })

        marker.addListener('click', () => {
          infoWindow.open(map, marker)
        })
      }
    })
  })
})
</script>
