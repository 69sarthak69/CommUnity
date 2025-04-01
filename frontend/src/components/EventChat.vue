<template>
    <div class="chat-container">
      <div class="messages">
        <div v-for="msg in messages" :key="msg.id" class="message">
          <strong>{{ msg.username || msg.sender_name || 'Anonymous' }}:</strong> {{ msg.content }}
        </div>
      </div>
      <div class="input-area">
        <input
          v-model="newMessage"
          @keyup.enter="sendMessage"
          placeholder="Type a message..."
        />
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref, onUnmounted } from 'vue'
  
  const props = defineProps({
    userId: Number,
    roomId: Number,
    roomType: String // "event"
  })
  
  const newMessage = ref('')
  const messages = ref([])
  let socket = null
  
  const fetchChatHistory = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const res = await fetch(
        `http://127.0.0.1:8000/api/chat/messages/${props.roomType}_${props.roomId}/`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      const data = await res.json()
      messages.value = Array.isArray(data) ? data : []
    } catch (err) {
      console.error('❌ Error fetching messages', err)
    }
  }
  
  const initSocket = () => {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
    socket = new WebSocket(`${protocol}://localhost:8001/ws/chat/${props.roomType}_${props.roomId}/`)
  
    socket.onmessage = (event) => {
      const msg = JSON.parse(event.data)
      messages.value.push(msg)
    }
  
    socket.onopen = () => console.log('✅ Connected to event chat')
    socket.onclose = () => console.log('❌ Disconnected from chat')
  }
  
  const sendMessage = () => {
    if (socket && newMessage.value.trim()) {
      const username = localStorage.getItem('user_username') || 'Unknown'
  
      socket.send(JSON.stringify({
        message: newMessage.value,
        sender: props.userId,
        username: username, // ✅ added username
        timestamp: new Date().toISOString()
      }))
  
      newMessage.value = ''
    }
  }
  
  onMounted(() => {
    fetchChatHistory()
    initSocket()
  })
  
  onUnmounted(() => {
    if (socket) socket.close()
  })
  </script>
  
  <style scoped>
  .chat-container {
    border: 1px solid #ddd;
    border-radius: 10px;
    padding: 1rem;
    max-height: 500px;
    overflow-y: auto;
    background-color: #f9f9f9;
  }
  .messages {
    max-height: 300px;
    overflow-y: auto;
    margin-bottom: 1rem;
  }
  .message {
    margin-bottom: 0.5rem;
  }
  .input-area {
    display: flex;
    gap: 0.5rem;
  }
  input {
    flex: 1;
    padding: 0.5rem;
  }
  button {
    background-color: #10b981;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 8px;
  }
  </style>
  