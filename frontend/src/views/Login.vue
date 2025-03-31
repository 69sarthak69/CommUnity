<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false) // Prevent multiple logins

const handleLogin = async () => {
  if (isSubmitting.value) return
  errorMessage.value = ''
  isSubmitting.value = true

  try {
    const response = await axios.post(
      'http://localhost:8000/api/auth/login/',
      { email: email.value, password: password.value },
      { headers: { 'Content-Type': 'application/json' } }
    )

    const token = response.data.access
    const user = response.data.user  // 👈 this must exist in your API response

    localStorage.setItem('access_token', token)
    localStorage.setItem('user_email', user.email)
    localStorage.setItem('user_username', user.username)
    localStorage.setItem('user_id', user.id.toString()) // ✅ STORE user ID in localStorage


    // ✅ Notify Home.vue to update UI dynamically
    window.dispatchEvent(new Event('userLoggedIn'))

    // ✅ Redirect to Home
    router.push('/home')
  } catch (error) {
    errorMessage.value = error.response?.data?.error || 'Invalid email or password.'
    console.error('Login failed:', errorMessage.value)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="form-container">
    <h2 class="form-title">Welcome back</h2>

    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="email" class="form-label">Email</label>
        <input
          id="email"
          type="email"
          v-model="email"
          required
          class="form-input"
          placeholder="Enter your email"
        />
      </div>

      <div class="form-group">
        <label for="password" class="form-label">Password</label>
        <input
          id="password"
          type="password"
          v-model="password"
          required
          class="form-input"
          placeholder="Enter your password"
        />
      </div>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <button type="submit" class="button-primary" style="width: 100%" :disabled="isSubmitting">
        {{ isSubmitting ? 'Logging in...' : 'Log in' }}
      </button>
    </form>

    <div class="form-footer">
      <p>
        New here?
        <router-link to="/register">Join Community Help</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.error-message {
  color: red;
  font-size: 14px;
  margin-bottom: 10px;
}
</style>
