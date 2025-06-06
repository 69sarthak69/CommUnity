<template>
  <div class="notification-wrapper" ref="dropdownRef">
    <!-- Bell Button -->
    <button 
      @click="toggleDropdown" 
      class="notification-button"
    >
      <span class="text-xl">🔔</span>

      <span
        v-if="unreadCount > 0"
        class="notification-badge"
      >
        {{ unreadCount > 9 ? '9+' : unreadCount }}
      </span>
    </button>

    <!-- Dropdown Panel -->
    <div
      v-if="dropdownOpen"
      class="notification-dropdown"
    >
      <div class="notification-header">Notifications</div>

      <div v-if="notifications.length === 0" class="notification-empty">
        No new notifications.
      </div>

      <ul v-else class="notification-list">
        <li
          v-for="notif in notifications"
          :key="notif.id"
          class="notification-item"
          @click="markAsRead(notif.id)"
        >
          <router-link
            :to="getLink(notif)"
            class="notification-link"
          >
            <span
              v-if="!notif.is_read"
              class="notification-dot"
            ></span>
            <span class="notification-text">{{ notif.message }}</span>
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { onClickOutside } from '@vueuse/core'

const dropdownOpen = ref(false)
const dropdownRef = ref(null)
const notifications = ref([])
const unreadCount = ref(0)

const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const token = localStorage.getItem('access_token')

// WebSocket setup for real-time notifications
let socket = null;

const connectWebSocket = () => {
  const userId = localStorage.getItem('user_id');
  if (!userId) return;

  const wsProtocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const wsUrl = `${wsProtocol}://127.0.0.1:8000/ws/notifications/${userId}/`;

  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    console.log('🔗 WebSocket connected!');
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.notification) {
      notifications.value.unshift(data.notification);
      unreadCount.value++;
    }
  };

  socket.onclose = () => {
    console.warn('WebSocket closed, retrying in 3s...');
    setTimeout(connectWebSocket, 3000);
  };

  socket.onerror = (err) => {
    console.error('WebSocket error', err);
    socket.close();
  };
};

const getLink = (notif) => {
  const id = notif.related_object_id
  switch (notif.notif_type) {
    case 'application':
    case 'emergency':
      return `/help-request/${id}`
    case 'application_result':   
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

const pollInterval = setInterval(fetchNotifications, 30000)

onMounted(() => {
  fetchNotifications()
  connectWebSocket()
})

onUnmounted(() => {
  clearInterval(pollInterval)
  if (socket) socket.close()
})
</script>

<style scoped>
.notification-wrapper {
  position: relative;
}

.notification-button {
  position: relative;
  height: 2rem;
  width: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: 9999px;
  transition: background 0.2s ease;
}

.notification-button:hover {
  background-color: rgba(0, 178, 70, 0.08);
}

.notification-badge {
  position: absolute;
  top: -6px;
  right: -6px;
  background: #dc2626;
  color: white;
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 9999px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.notification-dropdown {
  position: absolute;
  top: 44px;
  right: 0;
  width: 320px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  z-index: 200;
  animation: fadeIn 0.2s ease-in-out;
  overflow: hidden;
}

.notification-header {
  font-weight: 600;
  padding: 12px 16px;
  font-size: 1rem;
  border-bottom: 1px solid #e5e7eb;
  color: #1f2937;
}

.notification-empty {
  padding: 16px;
  font-size: 0.875rem;
  color: #6b7280;
}

.notification-list {
  max-height: 300px;
  overflow-y: auto;
}

.notification-list::-webkit-scrollbar {
  width: 6px;
}
.notification-list::-webkit-scrollbar-thumb {
  background-color: #c4c4c4;
  border-radius: 9999px;
}

.notification-item {
  padding: 12px 16px;
  transition: background 0.2s ease;
}

.notification-item:hover {
  background-color: #f9fafb;
}

.notification-link {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}

.notification-dot {
  width: 8px;
  height: 8px;
  background-color: #3b82f6;
  border-radius: 9999px;
  flex-shrink: 0;
}

.notification-text {
  font-size: 0.875rem;
  color: #374151;
  line-height: 1.4;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  word-break: break-word;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 480px) {
  .notification-dropdown {
    width: 90vw;
    right: 1rem;
  }
}
</style>
