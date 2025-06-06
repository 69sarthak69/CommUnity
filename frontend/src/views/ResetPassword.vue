<template>
  <div class="reset-container">
    <div class="reset-card">
      <h2>Set New Password</h2>
      <input v-model="password" type="password" placeholder="New Password" class="input-field" />
      <input v-model="confirmPassword" type="password" placeholder="Confirm Password" class="input-field" />
      <button @click="submitReset" :disabled="loading" class="reset-button">
        {{ loading ? "Resetting..." : "Reset Password" }}
      </button>
      <div v-if="success" class="success-message">Password reset! Please login.</div>
      <div v-if="error" class="error-message">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const password = ref('')
const confirmPassword = ref('')
const route = useRoute()
const router = useRouter()
const success = ref(false)
const error = ref('')
const loading = ref(false)

const submitReset = async () => {
  error.value = ''
  success.value = false

  if (!password.value || !confirmPassword.value) {
    error.value = "Both password fields are required."
    return
  }
  if (password.value !== confirmPassword.value) {
    error.value = "Passwords do not match."
    return
  }

  loading.value = true
  const uid = route.params.uid
  const token = route.params.token

  try {
    const resp = await fetch('http://127.0.0.1:8000/api/password_reset/confirm/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        uid: uid,
        token: token,
        password: password.value,
      }),
    });
    const data = await resp.json();
    if (resp.ok) {
      success.value = true
      setTimeout(() => router.push('/'), 2000)
    } else {
      error.value = data?.password?.[0] || data?.detail || "Reset failed. Try again."
    }
  } catch (e) {
    error.value = "Network or server error"
  }
  loading.value = false
}
</script>

<style scoped>
.reset-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f6f8; /* Light gray background */
}

.reset-card {
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
  border-color: #00B246; /* Blue focus border */
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
}

.reset-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #00B246;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.reset-button:hover:not(:disabled) {
  background-color: #008C36; /* Darker blue on hover */
}

.reset-button:disabled {
  background-color: #6c757d; /* Gray when disabled */
  cursor: not-allowed;
}

.success-message {
  color: #28a745; /* Green */
  margin-top: 1rem;
  font-size: 0.9rem;
}

.error-message {
  color: #dc3545; /* Red */
  margin-top: 1rem;
  font-size: 0.9rem;
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .reset-card {
    padding: 1.5rem;
    max-width: 90%;
  }

  h2 {
    font-size: 1.25rem;
  }

  .input-field,
  .reset-button {
    font-size: 0.9rem;
  }
}
</style>