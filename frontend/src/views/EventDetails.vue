
<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import EventChat from '../components/EventChat.vue'
import EventLocationMap from '../components/EventLocationMap.vue'
import Notifications from '../components/Notifications.vue'

const user = ref<{ email: string; username: string; id: number } | null>(null)
const showChatModal = ref(false)

const route = useRoute()
const router = useRouter()
const eventId = route.params.id

const event = ref<any>(null)
const isLoading = ref(true)

const currentUserId = parseInt(localStorage.getItem('user_id') || '0')
const token = localStorage.getItem('access_token')

const countdown = ref('')
let intervalId: any = null

const checkUser = () => {
  const storedEmail = localStorage.getItem('user_email')
  const storedUsername = localStorage.getItem('user_username')
  const storedUserId = localStorage.getItem('user_id')
  if (storedEmail && storedUsername && storedUserId) {
    user.value = {
      email: storedEmail,
      username: storedUsername,
      id: parseInt(storedUserId)
    }
  } else {
    user.value = null
  }
}

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_email')
  localStorage.removeItem('user_username')
  localStorage.removeItem('user_id')
  user.value = null
  router.push('/')
}

// Fetch event details
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

// Countdown logic
function updateCountdown(eventDateStr: string) {
  const eventDate = new Date(eventDateStr).getTime()
  const now = new Date().getTime()
  const diff = eventDate - now
  if (diff <= 0) {
    countdown.value = "Event has started!"
    if (intervalId) clearInterval(intervalId)
    return
  }
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diff / (1000 * 60 * 60)) % 24)
  const minutes = Math.floor((diff / (1000 * 60)) % 60)
  const seconds = Math.floor((diff / 1000) % 60)
  countdown.value = `${days}d ${hours}h ${minutes}m ${seconds}s`
}

// Google Calendar link
const getCalendarUrl = (eventObj) => {
  if (!eventObj) return "#"
  const start = new Date(eventObj.date)
  // 2-hour default duration
  const end = new Date(start.getTime() + 2 * 60 * 60 * 1000)
  const format = (d: Date) => d.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z'

  const params = new URLSearchParams({
    action: "TEMPLATE",
    text: eventObj.title,
    details: eventObj.description,
    location: eventObj.location,
    dates: `${format(start)}/${format(end)}`
  })

  return `https://www.google.com/calendar/render?${params.toString()}`
}

// RSVP, Cancel, Delete logic
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

// On mount: fetch event and watch for changes to setup timer
onMounted(() => {
  checkUser()
  fetchEvent()
  // Watch for event loaded or updated, start countdown
  watch(event, (newEvent) => {
    if (intervalId) clearInterval(intervalId)
    if (newEvent && newEvent.date) {
      updateCountdown(newEvent.date)
      intervalId = setInterval(() => updateCountdown(newEvent.date), 1000)
    }
  }, { immediate: true })
})

// Clear timer on destroy
onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})
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

  <div class="event-details-page">
    <!-- Hero Section -->
    <div class="hero-section" :style="{ backgroundImage: `url(${event?.image || 'https://images.unsplash.com/photo-1592150621744-aca64f48394a?auto=format&fit=crop&q=80&w=2000'})` }">
      <div class="hero-content container">
        <span class="category-badge">{{ event?.category }}</span>
        <h1>{{ event?.title }}</h1>
      </div>
    </div>

    <div class="main-content container">
      <div class="content-grid">
        <!-- Main Content -->
        <div class="content-main">
          <!-- Quick Info -->
          <div class="quick-info">
            <div class="info-item">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              <div>
                <h3>Date & Time</h3>
                <p>{{ event ? new Date(event.date).toLocaleString() : '' }}</p>
              </div>
              <div v-if="countdown" class="event-countdown mb-3">
                <strong>⏳ Starts in:</strong> <span>{{ countdown }}</span>
              </div>
            </div>
            <div class="info-item">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              <div>
                <h3>Location</h3>
                <p>{{ event?.location || 'Online' }}</p>
              </div>
            </div>
            <div class="info-item">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              <div>
                <h3>Attendees</h3>
                <p>{{ event?.attendee_count || 0 }} registered</p>
              </div>
            </div>
          </div>

          <!-- About Event -->
          <div class="content-section">
            <h2>About This Event</h2>
            <p>{{ event?.description }}</p>
          </div>

          <EventLocationMap
            v-if="event?.latitude && event?.longitude"
            :latitude="event.latitude"
            :longitude="event.longitude"
            :title="event.title"
          />
          <a
            v-if="event?.latitude && event?.longitude"
            :href="`https://maps.google.com/?q=${event.latitude},${event.longitude}`"
            target="_blank"
            class="view-map-link"
          >
            🌐 View on Google Maps
          </a>

          <a
            v-if="event"
            :href="getCalendarUrl(event)"
            target="_blank"
            rel="noopener"
            class="secondary-btn"
          >
            📅 Add to Google Calendar
          </a>

          <!-- Schedule -->
          <div class="content-section" v-if="event?.schedule">
            <h2>Schedule</h2>
            <div class="schedule-info">
              <div class="schedule-item" v-for="(item, index) in event.schedule" :key="index">
                <strong>{{ item.time }}</strong> {{ item.activity }}
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="sidebar">
          <!-- Action Card -->
          <div class="action-card">
            <button v-if="!event?.attendees.includes(currentUserId)" class="apply-btn" @click="rsvp">
              ✅ RSVP to Event
            </button>
            <button v-else class="apply-btn cancel-btn" @click="cancelRSVP">
              ❌ Cancel RSVP
            </button>
           

            <!-- Admin Actions -->
            <div v-if="event?.created_by === currentUserId" class="action-buttons mt-4">
              <button class="secondary-btn" @click="router.push(`/events/edit/${event.id}`)">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
                Edit
              </button>
              <button class="secondary-btn" @click="deleteEvent">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <button
              v-if="event && (event.attendees.includes(currentUserId) || event.created_by === currentUserId)"
              class="chat-toggle-btn"
              @click="showChatModal = true"
            >
              💬 Chat
            </button>

    <!-- Chat Modal -->
    <div
      v-if="showChatModal && event"
      class="modal-overlay"
      @click.self="showChatModal = false"
    >
      <div class="modal-container">
        <EventChat
          :userId="currentUserId"
          roomType="event"
          :roomId="event.id"
          @close="showChatModal = false"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.event-countdown {
  background: #fffbea;
  color: #ca8a04;
  border-radius: 6px;
  padding: 0.5em 1em;
  margin-bottom: 1em;
  font-weight: 500;
  font-size: 1.1em;
  display: inline-block;
}

.event-details-page {
  min-height: 100vh;
  background-color: #f9fafb;
}

.hero-section {
  height: 400px;
  background-size: cover;
  background-position: center;
  position: relative;
  color: white;
  display: flex;
  align-items: flex-end;
}

.hero-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.1),
    rgba(0, 0, 0, 0.7)
  );
}

.hero-content {
  position: relative;
  padding: 2rem;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.category-badge {
  display: inline-block;
  background-color: #10b981;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

.hero-content h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.hero-content .organization {
  font-size: 1.125rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.main-content {
  padding: 3rem 0;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 1024px) {
  .content-grid {
    grid-template-columns: 2fr 1fr;
  }
}

.quick-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.info-item svg {
  width: 24px;
  height: 24px;
  color: #10b981;
  flex-shrink: 0;
}

.info-item h3 {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.info-item p {
  font-weight: 500;
  color: #1f2937;
}

.content-section {
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.content-section h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.content-section p {
  color: #4b5563;
  line-height: 1.6;
}

.schedule-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.schedule-item {
  color: #4b5563;
  padding: 0.5rem;
  background-color: #f9fafb;
  border-radius: 0.25rem;
}

.schedule-item strong {
  color: #1f2937;
  margin-right: 0.5rem;
}

.sidebar {
  position: sticky;
  top: 2rem;
}

.action-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.apply-btn {
  width: 100%;
  background-color: #10b981;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.apply-btn:hover {
  background-color: #059669;
  transform: translateY(-1px);
}

.apply-btn.cancel-btn {
  background-color: #ef4444;
}

.apply-btn.cancel-btn:hover {
  background-color: #dc2626;
}

.button-chat {
  width: 100%;
  background-color: #007bff;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.button-chat:hover {
  background-color: #0056b3;
  transform: translateY(-1px);
}

.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.secondary-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  color: #4b5563;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.secondary-btn:hover {
  background-color: #f3f4f6;
  color: #1f2937;
  border-color: #d1d5db;
}

.organization-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.organization-card h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.organization-card p {
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.org-contact {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.contact-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.contact-item strong {
  color: #1f2937;
  font-size: 0.875rem;
}

.contact-item a {
  color: #2563eb;
  text-decoration: none;
}

.contact-item a:hover {
  text-decoration: underline;
}

/* Loading State */
.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(16, 185, 129, 0.2);
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Chat Toggle Button */
.chat-toggle-btn {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  background-color: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 9999px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.chat-toggle-btn:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .chat-toggle-btn {
    bottom: 1rem;
    right: 1rem;
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }
}


.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  z-index: 2000;
}

.modal-container {
  width: 320px;
  max-height: 500px;
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  margin: 1.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .modal-overlay {
    align-items: center;
    justify-content: center;
  }

  .modal-container {
    width: 95%;
    max-height: 70vh;
    margin: 0.75rem;
    border-radius: 6px;
  }
}
</style>
