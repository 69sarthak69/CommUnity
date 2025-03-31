<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const events = ref([])
const isLoading = ref(true)
const currentUserId = parseInt(localStorage.getItem('user_id') || '0')

// ✅ Fetch Events from Backend
const fetchEvents = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/events/')
    const data = await res.json()
    events.value = data
  } catch (err) {
    console.error('Error fetching events:', err)
  } finally {
    isLoading.value = false
  }
}

// ✅ Join Event
const joinEvent = async (eventId: number) => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('You must be logged in to join events.')
    return
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/api/events/${eventId}/join/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (res.ok) {
      alert('Joined event successfully!')
      fetchEvents()  // refresh attendee count
    } else {
      const errorText = await res.text()
      alert(`Failed to join: ${errorText}`)
    }
  } catch (err) {
    console.error('Join error:', err)
  }
}

// ✅ Date Helpers
const getEventMonth = (date: string) => {
  return new Date(date).toLocaleString('default', { month: 'short' })
}

const getEventDay = (date: string) => {
  return new Date(date).getDate()
}

onMounted(fetchEvents)
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

    <main class="feed">
      <div class="tasks-header">
        <h1 class="text-2xl font-bold">Community Events</h1>
        <button class="button-primary" @click="router.push('/events/create')">
          ➕ Create New Event
        </button>
      </div>

      <div v-if="isLoading">Loading events...</div>

      <div class="event-list" v-else>
        <div v-for="event in events" :key="event.id" class="event-card">
          <div class="event-date">
            <div class="event-day">{{ getEventDay(event.date) }}</div>
            <div class="event-month">{{ getEventMonth(event.date) }}</div>
          </div>

          <div class="event-details">
            <h3 class="event-title">
              <router-link :to="`/events/${event.id}`">{{ event.title }}</router-link>
            </h3>
            <div class="event-location">
              📍 {{ event.location }} • {{ event.attendees.length }} attending
            </div>
            <p class="event-description">{{ event.description }}</p>

            <!-- ✅ Only show Join button if not creator AND not already joined -->
            <button
              class="button-primary"
              style="margin-top: 16px"
              v-if="event.created_by !== currentUserId && !event.attendees.includes(currentUserId)"
              @click="joinEvent(event.id)"
            >
              Join Event
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.event-list {
  margin-top: 1.5rem;
  display: grid;
  gap: 1rem;
}
.event-card {
  display: flex;
  background: #fff;
  padding: 1rem;
  border-radius: 10px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}
.event-date {
  width: 60px;
  text-align: center;
  background: #f3f4f6;
  border-radius: 8px;
  padding: 0.5rem;
  margin-right: 1rem;
}
.event-day {
  font-size: 1.5rem;
  font-weight: bold;
}
.event-month {
  text-transform: uppercase;
  font-size: 0.9rem;
  color: #666;
}
.event-title {
  font-size: 1.2rem;
  font-weight: 600;
}
.event-location {
  font-size: 0.9rem;
  color: #666;
  margin: 0.3rem 0;
}
.event-description {
  font-size: 0.95rem;
  color: #444;
}
</style>
