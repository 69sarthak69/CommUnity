<template>
  <div class="chat-container">
    <div class="chat-header">
      <h2 class="text-xl font-bold">💬 Live Chat - Room: {{ roomName }}</h2>
    </div>

    <div class="chat-messages" ref="messageContainer">
      <div v-for="(msg, index) in messages" :key="index" class="message">
        <span class="sender">{{ msg.sender }}:</span>
        <span class="text">{{ msg.text }}</span>
      </div>
    </div>

    <div class="chat-input">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        type="text"
        placeholder="Type your message..."
        class="input"
      />
      <button @click="sendMessage" class="send-btn">Send</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const roomName = route.params.room || 'general'

const socket = ref(null)
const newMessage = ref('')
const messages = ref([])
const messageContainer = ref(null)
const username = localStorage.getItem('user_username') || 'Anonymous'

onMounted(() => {
  socket.value = new WebSocket(`ws://localhost:8000/ws/chat/${roomName}/`)

  socket.value.onopen = () => {
    console.log('✅ Connected to WebSocket')
  }

  socket.value.onmessage = (event) => {
    const data = JSON.parse(event.data)
    messages.value.push({ sender: 'Server', text: data.message })
    nextTick(() => {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight
    })
  }

  socket.value.onclose = () => {
    console.log('❌ WebSocket closed')
  }
})

const sendMessage = () => {
  if (newMessage.value.trim() === '') return

  socket.value.send(JSON.stringify({ message: `${username}: ${newMessage.value}` }))
  messages.value.push({ sender: 'You', text: newMessage.value })
  newMessage.value = ''
  nextTick(() => {
    messageContainer.value.scrollTop = messageContainer.value.scrollHeight
  })
}
</script>

<style scoped>
.chat-container {
  max-width: 600px;
  margin: 20px auto;
  border: 1px solid #ddd;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  height: 80vh;
  background-color: #f9f9f9;
}

.chat-header {
  padding: 15px;
  border-bottom: 1px solid #ccc;
  background-color: #4f46e5;
  color: white;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.chat-messages {
  flex-grow: 1;
  overflow-y: auto;
  padding: 15px;
  background-color: white;
}

.message {
  margin-bottom: 10px;
  padding: 8px;
  border-radius: 6px;
  background-color: #f1f5f9;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.sender {
  font-weight: bold;
  margin-right: 5px;
  color: #1f2937;
}

.text {
  color: #374151;
}

.chat-input {
  display: flex;
  padding: 10px;
  border-top: 1px solid #ccc;
  background-color: #f3f4f6;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}

.input {
  flex-grow: 1;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  outline: none;
  margin-right: 10px;
}

.send-btn {
  background-color: #4f46e5;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.send-btn:hover {
  background-color: #4338ca;
}
</style>
