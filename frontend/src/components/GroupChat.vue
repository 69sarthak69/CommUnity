<template>
    <div class="chatbox p-4 border rounded shadow-md">
      <h2 class="text-xl font-semibold mb-3">Group Chat</h2>
  
      <div class="chat-messages h-64 overflow-y-auto mb-3 border p-2 rounded">
        <div v-for="(msg, index) in messages" :key="index" class="mb-1">
          <strong>{{ msg.sender }}:</strong> {{ msg.message }}
        </div>
      </div>
  
      <div class="chat-input flex gap-2">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type your message..."
          class="flex-1 border rounded px-2 py-1"
          @keyup.enter="sendMessage"
        />
        <button @click="sendMessage" class="bg-blue-600 text-white px-3 py-1 rounded">Send</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      userId: Number,       // 👈 from parent
      roomType: String,     // "group" or "event"
      roomId: [String, Number],
    },
    data() {
      return {
        socket: null,
        messages: [],
        newMessage: '',
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
            sender: data.sender,
            message: data.message,
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
      sender: m.sender,
      message: m.content,
    }));

  } catch (error) {
    console.error("❌ Error fetching messages", error);
  }
}
,
      sendMessage() {
        if (this.newMessage.trim() && this.socket.readyState === WebSocket.OPEN) {
          const msgData = {
            message: this.newMessage,
            sender: this.userId,
            timestamp: new Date().toISOString(),
          };
          this.socket.send(JSON.stringify(msgData));
          this.newMessage = '';
        }
      }
    },
    async mounted() {
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
    max-width: 500px;
  }
  </style>
  