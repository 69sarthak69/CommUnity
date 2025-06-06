<template>
  <div class="chatbox">
    <div class="chat-header">
      <h2>Group Chat</h2>
      <button @click="$emit('close')" class="close-btn" aria-label="Close chat">✕</button>
    </div>
    <div class="chat-messages" ref="chatContainer">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        class="message"
        :class="{ 'message-own': msg.sender === username }"
      >
        <div class="message-content">
          <strong>{{ msg.sender }}</strong>: {{ msg.message }}
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


<script>
import { ref, onMounted } from 'vue';

export default {
  props: {
    userId: Number,
    roomType: String,
    roomId: [String, Number],
  },
  emits: ['close'],
  data() {
    return {
      socket: null,
      messages: [],
      newMessage: '',
      username: '',  // <-- Store current username
    };
  },
  computed: {
    roomName() {
      return `${this.roomType}_${this.roomId}`;
    },
    socketUrl() {
      const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
      return `${protocol}://${window.location.hostname}:8001/ws/chat/${this.roomName}/`;
    },
  },
  methods: {
    initSocket() {
      this.socket = new WebSocket(this.socketUrl);
      this.socket.onopen = () => {
        console.log("✅ Connected to chat");
      };
      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.messages.push({
          sender: data.username || data.sender_name || data.sender, // always username
          message: data.message,
        });
        // Auto-scroll to bottom
        this.$nextTick(() => {
          const chatBox = this.$refs.chatContainer;
          if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
        });
      };
      this.socket.onclose = () => {
        console.log("❌ Disconnected from chat");
      };
    },
    async fetchChatHistory() {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/chat/messages/${this.roomName}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json',
          }
        });
        if (!res.ok) {
          const errText = await res.text();
          console.error("❌ Unauthorized or error:", errText);
          return;
        }
        const data = await res.json();
        if (!Array.isArray(data)) {
          console.error("❌ Unexpected data format:", data);
          return;
        }
        this.messages = data.map(m => ({
          sender: m.sender_name || m.username || m.sender, // use username or sender_name
          message: m.content,
        }));
        // Auto-scroll to bottom after loading history
        this.$nextTick(() => {
          const chatBox = this.$refs.chatContainer;
          if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
        });
      } catch (error) {
        console.error("❌ Error fetching messages", error);
      }
    },
    sendMessage() {
      if (this.newMessage.trim() && this.socket && this.socket.readyState === WebSocket.OPEN) {
        const msgData = {
          message: this.newMessage,
          sender: this.userId,
          username: this.username, 
          timestamp: new Date().toISOString(),
        };
        this.socket.send(JSON.stringify(msgData));
        this.newMessage = '';
      }
    }
  },
  async mounted() {
    // Only get localStorage after DOM is ready
    this.username = localStorage.getItem('user_username') || '';
    this.initSocket();
    await this.fetchChatHistory();
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  }
};
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
  background-color: #0056b3;
}

@media (max-width: 768px) {
  .chatbox {
    width: 95%;
    height: 70vh;
    border-radius: 6px;
  }
}
</style>