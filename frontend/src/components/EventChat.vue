<template>
  <div class="chatbox">
    <div class="chat-header">
      <h2>Event Chat</h2>
      <button @click="$emit('close')" class="close-btn" aria-label="Close chat">✕</button>
    </div>
    <div class="chat-messages" ref="chatContainer">
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="message"
        :class="{ 'message-own': msg.username === currentUsername }"
      >
        <div class="message-content">
          <strong>{{ msg.username }}</strong>: {{ msg.content }}
        </div>
      </div>
    </div>
    <div class="chat-input">
      <input
        v-model="newMessage"
        type="text"
        placeholder="Type your message..."
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, onUnmounted, nextTick } from 'vue'

const currentUsername = ref('')
const props = defineProps({
  userId: Number,
  roomId: Number,
  roomType: String // "event"
})

const emit = defineEmits(['close'])

const newMessage = ref('')
const messages = ref([])
const chatContainer = ref(null)
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
    // Normalize message objects for consistent UI
    messages.value = Array.isArray(data)
      ? data.map(msg => ({
          id: msg.id,
          username: msg.username || msg.sender_name || 'Anonymous',
          sender: msg.sender,
          content: msg.content || msg.message,
        }))
      : []
    await nextTick()
    if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  } catch (err) {
    console.error('❌ Error fetching messages', err)
  }
}

const initSocket = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
  socket = new WebSocket(`${protocol}://localhost:8001/ws/chat/${props.roomType}_${props.roomId}/`)

  socket.onmessage = (event) => {
    const msg = JSON.parse(event.data)
    // Normalize for UI and guarantee a unique id for Vue reactivity
    messages.value.push({
      id: msg.id || Date.now() + Math.random(),
      username: msg.username || msg.sender_name || 'Anonymous',
      sender: msg.sender,
      content: msg.content || msg.message,
    })
    nextTick(() => {
      if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    })
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
      username: username,
      timestamp: new Date().toISOString()
    }))
    newMessage.value = ''
  }
}

onMounted(() => {
  currentUsername.value = localStorage.getItem('user_username') || 'Unknown'
  fetchChatHistory()
  initSocket()
})

onUnmounted(() => {
  if (socket) socket.close()
})
</script>

<style scoped>
.chatbox {
  width: 320px;
  height: 500px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f5f5f5;
  padding: 10px 15px;
  border-bottom: 1px solid #e0e0e0;
}

.chat-header h2 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 0.9rem;
  color: #666;
  cursor: pointer;
  padding: 5px;
}

.close-btn:hover {
  color: #333;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px 15px;
  background-color: #fafafa;
}

.message {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.message-own {
  align-items: flex-end;
}

.message-content {
  max-width: 75%;
  padding: 8px 12px;
  border-radius: 12px;
  background-color: #e0e0e0;
  color: #333;
  font-size: 0.9rem;
}

.message-own .message-content {
  background-color: #0fac5d;
  color: white;
}

.chat-input {
  display: flex;
  gap: 10px;
  padding: 10px 15px;
  background-color: white;
  border-top: 1px solid #e0e0e0;
}

.chat-input input {
  flex: 1;
  border: 1px solid #ccc;
  border-radius: 15px;
  padding: 8px 12px;
  font-size: 0.9rem;
  outline: none;
}

.chat-input input:focus {
  border-color: #0fac5d;
}

.chat-input button {
  background-color: #0fac5d;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 15px;
  font-size: 0.9rem;
  cursor: pointer;
}

.chat-input button:hover {
  background-color: #0fac5d;
}

@media (max-width: 768px) {
  .chatbox {
    width: 95%;
    height: 70vh;
    border-radius: 6px;
  }
}
</style>
