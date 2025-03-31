<template>
    <div class="chat-container">
      <h2 class="text-2xl font-bold mb-4">💬 Chat Room: {{ roomName }}</h2>
  
      <div class="messages" ref="messageBox">
        <div v-for="msg in messages" :key="msg.id" class="message">
          <strong>{{ msg.sender }}:</strong> {{ msg.content }}
        </div>
      </div>
  
      <form @submit.prevent="sendMessage" class="chat-input mt-4 flex gap-2">
        <input
          v-model="newMessage"
          placeholder="Type a message..."
          class="form-input flex-1"
        />
        <button class="button-primary">Send</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref, watch, nextTick } from 'vue'
  import { useRoute } from 'vue-router'
  
  const route = useRoute()
  const roomName = route.params.roomName || 'general'
  
  const messages = ref([])
  const newMessage = ref('')
  const messageBox = ref(null)
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  
  let socket = null
  
  const scrollToBottom = () => {
    nextTick(() => {
      messageBox.value.scrollTop = messageBox.value.scrollHeight
    })
  }
  
  const connectWebSocket = () => {
    socket = new WebSocket(`ws://localhost:8000/ws/chat/${roomName}/`)
  
    socket.onopen = () => {
      console.log('✅ Connected to WebSocket')
    }
  
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      messages.value.push(data)
      scrollToBottom()
    }
  
    socket.onclose = () => {
      console.log('🔌 WebSocket closed. Retrying in 3s...')
      setTimeout(connectWebSocket, 3000)
    }
  
    socket.onerror = (error) => {
      console.error('❌ WebSocket error:', error)
    }
  }
  
  const sendMessage = () => {
    if (newMessage.value.trim()) {
      socket.send(JSON.stringify({
        message: newMessage.value,
        sender: user?.username || 'Anonymous'
      }))
      newMessage.value = ''
    }
  }
  
  onMounted(() => {
    connectWebSocket()
  })
  </script>
  
  <style scoped>
  .chat-container {
    max-width: 600px;
    margin: 0 auto;
  }
  .messages {
    max-height: 400px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
  }
  .message {
    padding: 6px;
    margin-bottom: 6px;
    background-color: #fff;
    border-radius: 5px;
  }
  </style>
  