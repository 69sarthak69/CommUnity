<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const user = ref<{ email: string; username: string } | null>(null)

// Fetch user details if logged in
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
      router.push('/login')
    }
  }
}

// Logout function
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
    <div class="profile-card">
      <h2 class="profile-title">👤 Profile</h2>
      
      <div v-if="user" class="profile-content">
        <div class="user-avatar">
          {{ user.username.charAt(0).toUpperCase() }}
        </div>
        
        <div class="user-info">
          <div class="info-item">
            <span class="info-label">Username:</span>
            <span class="info-value">{{ user.username }}</span>
          </div>
          
          <div class="info-item">
            <span class="info-label">Email:</span>
            <span class="info-value">{{ user.email }}</span>
          </div>
        </div>
        
        <button class="logout-btn" @click="handleLogout">
          <span class="logout-icon">🚪</span>
          <span>Logout</span>
        </button>
      </div>
      
      <div v-else class="loading-message">
        Loading profile...
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.profile-card {
  width: 100%;
  max-width: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  text-align: center;
}

.profile-title {
  font-size: 1.8rem;
  color: #2d3748;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.profile-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.user-avatar {
  width: 80px;
  height: 80px;
  background-color: #4299e1;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.user-info {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #edf2f7;
}

.info-label {
  font-weight: 600;
  color: #4a5568;
}

.info-value {
  color: #2d3748;
}

.logout-btn {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #fed7d7;
  color: #e53e3e;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background-color: #feebeb;
  transform: translateY(-1px);
}

.logout-icon {
  font-size: 1.2rem;
}

.loading-message {
  color: #718096;
  font-size: 1.1rem;
  padding: 2rem 0;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .profile-card {
    padding: 1.5rem;
  }
  
  .profile-title {
    font-size: 1.5rem;
  }
  
  .user-avatar {
    width: 70px;
    height: 70px;
    font-size: 1.8rem;
  }
}
</style>