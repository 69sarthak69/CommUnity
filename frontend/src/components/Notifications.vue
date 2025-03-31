<template>
  <div class="relative">
    <button @click="toggleDropdown" class="relative focus:outline-none">
      <!-- Bell Icon -->🔔
      <svg class="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>
      </svg>

      <!-- Unread Count -->
      <span
        v-if="unreadCount > 0"
        class="absolute -top-1 -right-1 bg-red-600 text-white text-xs rounded-full px-1.5"
      >
        {{ unreadCount }}
      </span>
    </button>

    <!-- Dropdown -->
    <div
      v-if="dropdownOpen"
      class="absolute right-0 mt-2 w-80 bg-white border border-gray-200 rounded-lg shadow-lg z-50"
    >
      <div class="p-4 text-sm font-medium text-gray-800 border-b">Notifications</div>

      <div v-if="notifications.length === 0" class="p-4 text-sm text-gray-500">
        No new notifications.
      </div>

      <ul v-else class="divide-y max-h-64 overflow-y-auto">
        <li
          v-for="notif in notifications"
          :key="notif.id"
          class="p-3 hover:bg-gray-50 transition cursor-pointer"
        >
          <!-- 👇 Link to related object -->
          <router-link
            :to="getLink(notif)"
            class="flex items-center space-x-2"
          >
            <span v-if="!notif.is_read" class="w-2 h-2 rounded-full bg-blue-500"></span>
            <span v-else class="w-2 h-2"></span>
            <span class="text-sm text-gray-700">{{ notif.message }}</span>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const dropdownOpen = ref(false)
const notifications = ref([])
const unreadCount = ref(0)

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const token = localStorage.getItem('access_token')

const getLink = (notif) => {
  const id = notif.related_object_id
  switch (notif.notif_type) {
    case 'application':
    case 'emergency':
      return `/help-request/${id}`
    case 'event':
      return `/events/${id}`
    case 'group':
      return `/groups/${id}`
    case 'post':
      return `/community-posts/${id}`
    default:
      return '#'
  }
}

const fetchNotifications = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/notifications/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    const data = await res.json()
    notifications.value = data
    unreadCount.value = data.filter(n => !n.is_read).length
  } catch (err) {
    console.error('❌ Notification fetch failed', err)
  }
}

onMounted(fetchNotifications)
</script>
