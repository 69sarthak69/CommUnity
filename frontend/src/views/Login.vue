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
    const user = response.data.user  

    localStorage.setItem('access_token', token)
    localStorage.setItem('user_email', user.email)
    localStorage.setItem('user_username', user.username)
    localStorage.setItem('user_id', user.id.toString()) // STORE user ID in localStorage


    // Notify Home.vue to update UI dynamically
    window.dispatchEvent(new Event('userLoggedIn'))

    // Redirect to Home
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
        <router-link to="/forgot-password">Forgot Password?</router-link>

      </p>
    </div>
  </div>
</template>
<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh; /* Full viewport height */
  padding: 20px; /* Prevents touching edges on mobile */
  background: var(--background); 
}
.form-container {
  max-width: 400px;
  width: 100%;
  padding: 40px;
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border);
  margin: auto; /* Additional centering */
}

.form-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 24px;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text);
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  font-size: 0.9375rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  background: var(--background);
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0, 178, 70, 0.1);
}

.error-message {
  color: var(--danger);
  font-size: 0.875rem;
  margin: -10px 0 16px 0;
  text-align: center;
}

.button-primary {
  background: var(--primary);
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: var(--radius-full);
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.button-primary:hover {
  background: var(--primary-dark);
  box-shadow: var(--shadow-md);
}

.button-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.form-footer {
  margin-top: 24px;
  text-align: center;
  font-size: 0.875rem;
  color: var(--text-light);
}

.form-footer a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 500;
}

.form-footer a:hover {
  text-decoration: underline;
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .login-page {
    padding: 16px;
    align-items: flex-start; /* Better mobile experience */
    padding-top: 40px; /* Space from top on mobile */
  }
  .form-container {
    padding: 24px;
  }

  .form-title {
    font-size: 1.25rem;
  }
}
.error-message {
  color: red;
  font-size: 14px;
  margin-bottom: 10px;
}
</style>
