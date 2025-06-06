<script setup lang="ts">
import { ref, onMounted, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import MapComponent from './MapComponent.vue'
import Notifications from '../components/Notifications.vue'
import CreateEventModal from '../components/CreateEvent.vue'

const router = useRouter()
const showCreateEventModal = ref(false)

// Define Event interface
interface Event {
  id: number
  title: string
  description: string
  date: string
  location: string
  category: string
  latitude?: number
  longitude?: number
  created_by: number
  attendees: number[]
  created_at: string
}

// Use ref<Event[]> for proper typing
const events = ref<Event[]>([])
const isLoading = ref(true)

// User state
const user = ref<{ email: string; username: string; id: number } | null>(null)
const currentUserId = ref<number>(0)

const checkUser = () => {
  const storedEmail = localStorage.getItem('user_email')
  const storedUsername = localStorage.getItem('user_username')
  const storedUserId = localStorage.getItem('user_id')

  if (storedEmail && storedUsername && storedUserId) {
    user.value = {
      email: storedEmail,
      username: storedUsername,
      id: parseInt(storedUserId),
    }
    currentUserId.value = parseInt(storedUserId)
  } else {
    user.value = null
    currentUserId.value = 0
  }
}

// Fetch events from API
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

// Join an event
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
        Authorization: `Bearer ${token}`,
      },
    })

    if (res.ok) {
      alert('Joined event successfully!')
      fetchEvents() // refresh attendee count
    } else {
      const errorText = await res.text()
      alert(`Failed to join: ${errorText}`)
    }
  } catch (err) {
    console.error('Join error:', err)
  }
}

// Date helpers
const getEventMonth = (date: string) =>
  new Date(date).toLocaleString('default', { month: 'short' })
const getEventDay = (date: string) => new Date(date).getDate()

// Lifecycle hooks
onMounted(() => {
  checkUser()
  fetchEvents()
})

window.addEventListener('userLoggedIn', checkUser)

watchEffect(() => {
  checkUser()
})

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_email')
  localStorage.removeItem('user_username')
  localStorage.removeItem('user_id')
  user.value = null
  router.push('/')
}

const handleEventCreated = () => {
  fetchEvents() // Refresh the events list
}
</script>


<template>
  <!-- Navbar -->
  <nav class="navbar">
    <div class="container nav-content">
      <router-link to="/home" class="logo">
        <span class="logo-icon"></span>
        <span>CommunityHelp</span>
      </router-link>

      <div class="nav-links">
        <Notifications />

        <button v-if="user" class="nav-button" @click="router.push('/profile')">
          👤 {{ user.username || user.email }}
        </button>

        <button v-if="user" class="nav-button" @click="router.push('/my-applications')">
          📋 My Applications
        </button>

        <button v-if="user" class="nav-button logout" @click="handleLogout">
          🚪 Logout
        </button>

        <router-link v-if="!user" to="/" class="nav-button primary">Login</router-link>
      </div>
    </div>
  </nav>

  <!-- Main layout -->
  <div class="container main-content">
    <!-- Left Sidebar -->
      <aside class="sidebar">
        <router-link to="/home" class="sidebar-link ">
          <span class="link-icon">🏠</span>
          <span>Home</span>
        </router-link>
        <router-link to="/groups" class="sidebar-link">
          <span class="link-icon">👥</span>
          <span>Groups</span>
        </router-link>
        <router-link to="/events" class="sidebar-link  active " >
          <span class="link-icon">📅</span>
          <span>Events</span>
        </router-link>
        
        <router-link to="/donations" class="sidebar-link">
          <span class="link-icon">🎁</span>
          <span>Donations</span>
        </router-link>
        <div>
          <h2 class="text-xl font-bold mb-2">Map Preview</h2>
        <MapComponent />
       </div>
      </aside>

    <!-- Event Feed -->
    <main class="feed">
      <div class="tasks-header">
        <h1 class="text-2xl font-bold">Community Events</h1>
        <button class="button-primary" @click="showCreateEventModal = true">
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

   <CreateEventModal 
    v-if="showCreateEventModal" 
    :userId="currentUserId" 
    @close="showCreateEventModal = false"
    @created="handleEventCreated"
  />
</template>

<style scoped>

.button-primary {
  background-color: #2e7d32;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.button-primary:hover {
  background-color: #1b5e20;
}
.event-list {
  margin-top: 2rem;
  display: grid;
  gap: 1.5rem;
}

.event-card {
  display: flex;
  background: #fff;
  padding: 1.25rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
}

.event-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(46, 125, 50, 0.12);
  border-left-color: #4CAF50;
}

.event-date {
  width: 70px;
  min-width: 70px;
  text-align: center;
  background: #E8F5E9;
  border-radius: 8px;
  padding: 0.75rem 0.5rem;
  margin-right: 1.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #2E7D32;
}

.event-day {
  font-size: 1.75rem;
  font-weight: bold;
  line-height: 1;
}

.event-month {
  text-transform: uppercase;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-top: 0.25rem;
  color: #388E3C;
}

.event-content {
  flex: 1;
}

.event-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2E7D32;
  margin-bottom: 0.5rem;
  position: relative;
  display: inline-block;
}

.event-title a {
  color: #2e7d32;
  text-decoration: none;
}
.event-title::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: #4CAF50;
  transition: width 0.3s ease;
}

.event-card:hover .event-title::after {
  width: 100%;
}

.event-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.event-location,
.event-time {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.9rem;
  color: #689F38;
}

.event-location svg,
.event-time svg {
  width: 16px;
  height: 16px;
  fill: #81C784;
}

.event-description {
  font-size: 0.95rem;
  line-height: 1.5;
  color: #555;
  margin-bottom: 1rem;
}

.event-actions {
  display: flex;
  gap: 0.75rem;
}

.event-actions button {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
  cursor: pointer;
}

.event-rsvp {
  background: #4CAF50;
  color: white;
  border: none;
}

.event-rsvp:hover {
  background: #388E3C;
}

.event-details {
  background: transparent;
  color: #4CAF50;
}



/* Responsive adjustments */
@media (max-width: 768px) {
  .event-card {
    flex-direction: column;
  }
  
  .event-date {
    width: 100%;
    flex-direction: row;
    justify-content: flex-start;
    gap: 1rem;
    margin-right: 0;
    margin-bottom: 1rem;
    padding: 0.75rem 1rem;
  }
  
  .event-day,
  .event-month {
    display: inline-block;
  }
  
  .event-meta {
    flex-wrap: wrap;
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .event-actions {
    flex-direction: column;
  }
  
  .event-actions button {
    width: 100%;
  }
}
</style>
