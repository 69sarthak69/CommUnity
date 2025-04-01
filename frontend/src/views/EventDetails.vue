<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import EventChat from '../components/EventChat.vue'

const route = useRoute()
const router = useRouter()
const eventId = route.params.id

const event = ref<any>(null)
const isLoading = ref(true)

const currentUserId = parseInt(localStorage.getItem('user_id') || '0')
const token = localStorage.getItem('access_token')

const fetchEvent = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/events/${eventId}/`)
    const data = await res.json()
    event.value = data
  } catch (err) {
    console.error('Error fetching event:', err)
  } finally {
    isLoading.value = false
  }
}

const rsvp = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/events/${eventId}/join/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    const data = await res.json()
    alert(data.message)
    fetchEvent()
  } catch (err) {
    console.error(err)
    alert('Failed to RSVP.')
  }
}

const cancelRSVP = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/events/${eventId}/cancel/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    const data = await res.json()
    alert(data.message)
    fetchEvent()
  } catch (err) {
    console.error(err)
    alert('Failed to cancel RSVP.')
  }
}

const deleteEvent = async () => {
  const confirmDelete = confirm('Delete this event?')
  if (!confirmDelete) return

  try {
    const res = await fetch(`http://127.0.0.1:8000/api/events/${eventId}/edit/`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    if (res.ok) {
      alert('Event deleted.')
      router.push('/events')
    } else {
      alert('You are not allowed to delete this event.')
    }
  } catch (err) {
    console.error(err)
  }
}

onMounted(fetchEvent)
</script>

<template>
  <div class="container main-content">
    <aside class="sidebar">
      <router-link to="/home" class="sidebar-link">Home</router-link>
      <router-link to="/groups" class="sidebar-link">Groups</router-link>
      <router-link to="/events" class="sidebar-link">Events</router-link>
      <router-link to="/notifications" class="sidebar-link">Notifications</router-link>
      <router-link to="/donations" class="sidebar-link">🎁 Donations</router-link>
    </aside>

    <div v-if="isLoading">Loading event...</div>

    <div v-else-if="event">
      <h1 class="text-2xl font-bold">{{ event.title }}</h1>
      <p class="mt-2">{{ event.description }}</p>
      <p class="text-sm text-gray-600">📅 {{ new Date(event.date).toLocaleString() }}</p>
      <p class="text-sm text-gray-600">📍 {{ event.location }}</p>
      <p class="text-sm text-gray-600">🎯 Category: {{ event.category }}</p>
      <p class="text-sm text-gray-600">👥 Attendees: {{ event.attendee_count }}</p>

      <!-- Admin Controls -->
      <div v-if="currentUserId === event.created_by" class="mt-4">
        <button class="button-primary mr-2" @click="router.push(`/events/edit/${event.id}`)">✏️ Edit</button>
        <button class="button-secondary" @click="deleteEvent">🗑️ Delete</button>
      </div>

      <!-- RSVP Actions -->
      <div v-else class="mt-4">
        <button v-if="!event.attendees.includes(currentUserId)" class="button-primary" @click="rsvp">
          ✅ RSVP to Event
        </button>
        <button v-else class="button-secondary" @click="cancelRSVP">
          ❌ Cancel RSVP
        </button>
      </div>

      <!-- ✅ Chat Component for attendees or creator -->
      <div v-if="event.attendees.includes(currentUserId) || event.created_by === currentUserId" class="mt-8">
        <EventChat :userId="currentUserId" roomType="event" :roomId="event.id" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.button-primary {
  background-color: #10b981;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: bold;
  margin-right: 8px;
}
.button-primary:hover {
  background-color: #059669;
}

.button-secondary {
  background-color: #ef4444;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: bold;
}
.button-secondary:hover {
  background-color: #dc2626;
}
</style>
