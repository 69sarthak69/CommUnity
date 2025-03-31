<script setup lang="ts">
import { ref,  onMounted, watchEffect } from 'vue'
import { useRouter } from 'vue-router'


const user = ref<{ email: string; username: string } | null>(null)
const router = useRouter()
// ✅ Function to check logged-in user from localStorage
const checkUser = () => {
  const storedEmail = localStorage.getItem('user_email')
  const storedUsername = localStorage.getItem('user_username')

  if (storedEmail && storedUsername) {
    user.value = { email: storedEmail, username: storedUsername }
  } else {
    user.value = null
  }
}
// ✅ Watch for user login changes
window.addEventListener('userLoggedIn', checkUser)
watchEffect(() => {
  checkUser()
})

// ✅ Fetch help requests when component mounts
onMounted(() => {
  checkUser()
})

// ✅ Logout function
const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_email')
  localStorage.removeItem('user_username')
  user.value = null
  router.push('/login')
}
</script>
<template>
 <!-- ✅ Top Navigation Bar -->
 <div class="nav-container">
    <div class="container nav-content">
      <router-link to="/" class="logo">Community Help</router-link>

      <div class="nav-links">
        <!-- ✅ Notification Bell Icon -->
        <Notifications />

        <!-- ✅ Show Profile when user is logged in -->
        <button class="button-secondary" @click="router.push('/profile')" v-if="user">
          👤 {{ user?.email }}
        </button>

        <!-- ✅ Show Logout only when user is logged in -->
        <button class="button-secondary" @click="handleLogout" v-if="user">
          🚪 Logout
        </button>

        <!-- ✅ Show Chat button only when user is logged in -->
        <button class="button-secondary" @click="router.push('/chatbox')" v-if="user">
          💬 Chat
        </button>

        <!-- ❌ Hide Login when user is logged in -->
        <router-link to="/login" class="button-primary" v-if="!user">
          Login
        </router-link>
      </div>
    </div>
  </div>
</template>
