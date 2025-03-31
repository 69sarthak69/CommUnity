<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const user = ref<{ email: string; username: string } | null>(null)

// ✅ Fetch user details if logged in
const fetchUserDetails = async () => {
  const token = localStorage.getItem('access_token')
  if (token) {
    try {
      const response = await axios.get('http://localhost:8000/api/auth/user/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      user.value = response.data
    } catch (error) {
      console.error('Failed to fetch user:', error)
      localStorage.removeItem('access_token')
      user.value = null
      router.push('/login') // Redirect if unauthorized
    }
  }
}

// ✅ Logout function
const handleLogout = () => {
  localStorage.removeItem('access_token')
  user.value = null
  router.push('/login')
}

onMounted(() => {
  fetchUserDetails()
})
</script>

<template>
  <div class="profile-container">
    <h2>👤 Profile</h2>
    <div v-if="user">
      <p><strong>Username:</strong> {{ user.username }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <button class="button-secondary" @click="handleLogout">🚪 Logout</button>
    </div>
    <p v-else>Loading profile...</p>
  </div>
</template>
