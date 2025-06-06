<template>
  <div v-if="activeAlert" class="emergency-banner">
    <span>🚨 <strong>{{ activeAlert.title }}</strong>: {{ activeAlert.message }}</span>
    <span v-if="activeAlert.location">📍 {{ activeAlert.location }}</span>
    <button v-if="showClose" class="close-btn" @click="activeAlert = null">✖</button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from '../utils/axiosInstance'

const activeAlert = ref(null)
const ws = ref(null)
const showClose = false // true if you want user to dismiss; false = always show until resolved by admin

const fetchActiveAlert = async () => {
  try {
    const res = await axios.get('/emergency/active/')
    if (res.data && res.data.length > 0) {
      activeAlert.value = res.data[0] // Show latest active alert
    }
  } catch (err) {
    activeAlert.value = null
  }
}

onMounted(() => {
  fetchActiveAlert()
  // Set up WebSocket connection
  const socket = new WebSocket('ws://127.0.0.1:8000/ws/emergency/')
  ws.value = socket

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data)
    // If resolved, hide
    if (data.active === false) {
      activeAlert.value = null
    } else if (data.active === true) {
      activeAlert.value = data
    }
  }
  socket.onclose = () => {
    // Reconnect logic if you want, but not strictly needed
  }
})

onUnmounted(() => {
  if (ws.value) ws.value.close()
})
</script>

<style scoped>
.emergency-banner {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 9999;
  background: #dc2626;
  color: white;
  padding: 1rem 2rem;
  text-align: center;
  font-size: 1.1rem;
  font-weight: 600;
  box-shadow: 0 2px 10px rgba(220,38,38,0.08);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1.2rem;
}
.close-btn {
  background: transparent;
  border: none;
  color: white;
  font-size: 1.3rem;
  cursor: pointer;
}
</style>
