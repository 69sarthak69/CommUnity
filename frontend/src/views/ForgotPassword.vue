
<template>
  <div class="forgot-container">
    <div class="forgot-card">
      <h2>Forgot Password?</h2>
      <input v-model="email" type="email" placeholder="Enter your email" class="input-field" />
      <button @click="sendReset" :disabled="loading" class="send-button">
        {{ loading ? "Sending..." : "Send Reset Link" }}
      </button>
      <div v-if="sent" class="success-message">Check your email for the reset link!</div>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const sent = ref(false)
const loading = ref(false)
const error = ref('')

const sendReset = async () => {
  loading.value = true
  error.value = ''
  sent.value = false
  try {
    const resp = await fetch('http://127.0.0.1:8000/api/password_reset/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value })
    });
    if (resp.ok) {
      sent.value = true
    } else {
      const data = await resp.json()
      error.value = data?.email?.[0] || "Failed to send reset link"
    }
  } catch (e) {
    error.value = "Network or server error"
  }
  loading.value = false
}
</script>

<style scoped>
.forgot-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f6f8; /* Matches reset component background */
}

.forgot-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: #333;
}

.input-field {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  outline: none;
  border-color: #00B246; /* Blue focus border, matching reset component */
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
}

.send-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #00B246; /* Blue, matching reset component */
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.send-button:hover:not(:disabled) {
  background-color: #008C36; /* Darker blue on hover */
}

.send-button:disabled {
  background-color: #6c757d; /* Gray when disabled */
  cursor: not-allowed;
}

.success-message {
  color: #28a745; /* Green, matching reset component */
  margin-top: 1rem;
  font-size: 0.9rem;
}

.error-message {
  color: #dc3545; /* Red, matching reset component */
  margin-top: 1rem;
  font-size: 0.9rem;
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .forgot-card {
    padding: 1.5rem;
    max-width: 90%;
  }

  h2 {
    font-size: 1.25rem;
  }

  .input-field,
  .send-button {
    font-size: 0.9rem;
  }
}
</style>
```