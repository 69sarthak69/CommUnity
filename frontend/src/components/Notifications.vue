<template>
  <div class="relative">
    <button 
      @click="toggleDropdown" 
      class="relative focus:outline-none h-8 w-8 flex items-center justify-center"
    >
      <!-- Bell Icon -->
      <span class="text-xl">🔔</span>

      <!-- Unread Count -->
      <span
        v-if="unreadCount > 0"
        class="absolute -top-1 -right-1 bg-red-600 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center"
      >
        {{ unreadCount > 9 ? '9+' : unreadCount }}
      </span>
    </button>

    <!-- Dropdown -->
    <div
      v-if="dropdownOpen"
      ref="dropdownRef"
      class="fixed right-4 top-16 w-80 bg-white border border-gray-200 rounded-lg shadow-lg z-50 transition-all duration-200"
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
          @click="markAsRead(notif.id)"
        >
          <router-link
            :to="getLink(notif)"
            class="flex items-center space-x-2"
          >
            <span v-if="!notif.is_read" class="w-2 h-2 rounded-full bg-blue-500 flex-shrink-0"></span>
            <span v-else class="w-2 h-2 flex-shrink-0"></span>
            <span class="text-sm text-gray-700 line-clamp-2">{{ notif.message }}</span>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted,onUnmounted, watch } from 'vue'
import { onClickOutside } from '@vueuse/core'

const dropdownOpen = ref(false)
const dropdownRef = ref(null)
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

const markAsRead = async (id) => {
  try {
    await fetch(`http://127.0.0.1:8000/api/notifications/${id}/mark-read/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    dropdownOpen.value = false
    fetchNotifications()
  } catch (err) {
    console.error('Failed to mark notification as read', err)
  }
}

// Close dropdown when clicking outside
onClickOutside(dropdownRef, () => {
  dropdownOpen.value = false
})

// Fetch notifications on mount
onMounted(fetchNotifications)

// Optional: Poll for new notifications every 30 seconds
const pollInterval = setInterval(fetchNotifications, 30000)

// Clean up interval when component unmounts
onUnmounted(() => {
  clearInterval(pollInterval)
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>