<script setup lang="ts">
import { ref, onMounted, watchEffect } from 'vue'
import router from '../router'
import Notifications from "../components/Notifications.vue"

import '../style.css'

const groups = ref([])
const isLoading = ref(true)
const currentUserId = parseInt(localStorage.getItem('user_id') || '0')

// ✅ Fetch groups from Django API
const fetchGroups = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/groups/')
    const data = await res.json()
    groups.value = data
  } catch (err) {
    console.error('Error fetching groups:', err)
  } finally {
    isLoading.value = false
  }
}

// ✅ Join group by ID
const joinGroup = async (groupId: number) => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('You must be logged in to join a group.')
    return
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/api/groups/${groupId}/join/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    if (res.ok) {
      alert('Successfully joined the group!')
      fetchGroups()
    } else {
      const error = await res.text()
      alert(`Failed to join: ${error}`)
    }
  } catch (err) {
    console.error('Join error:', err)
  }
}

onMounted(fetchGroups)
const user = ref<{ email: string; username: string; id: number } | null>(null)

const checkUser = () => {
  const storedEmail = localStorage.getItem('user_email')
  const storedUsername = localStorage.getItem('user_username')
  const storedUserId = localStorage.getItem('user_id')

  if (storedEmail && storedUsername && storedUserId) {
    user.value = {
      email: storedEmail,
      username: storedUsername,
      id: parseInt(storedUserId)
    }
  } else {
    user.value = null
  }
}
window.addEventListener('userLoggedIn', checkUser)
watchEffect(() => {
  checkUser()
})
const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_email')
  localStorage.removeItem('user_username')
  localStorage.removeItem('user_id')
  user.value = null
  router.push('/login')
}
</script>

<template>
    <div class="app-container">
    <!-- Top Navigation Bar -->
    <nav class="navbar">
      <div class="container nav-content">
        <router-link to="/" class="logo">
          <span class="logo-icon">🤝</span>
          <span>CommunityHelp</span>
        </router-link>
        
        <div class="nav-links">
          <Notifications />
          
          <button 
            v-if="user"
            class="nav-button"
            @click="router.push('/profile')"
          >
            <span class="button-icon">👤</span>
            <span class="button-text">{{ user.username || user.email }}</span>
          </button>
          
          <button 
            v-if="user"
            class="nav-button"
            @click="router.push('/chatbox')"
          >
            <span class="button-icon">💬</span>
            <span class="button-text">Chat</span>
          </button>
          
          <button 
            v-if="user"
            class="nav-button logout"
            @click="handleLogout"
          >
            <span class="button-icon">🚪</span>
            <span class="button-text">Logout</span>
          </button>
          
          <router-link 
            v-if="!user"
            to="/login" 
            class="nav-button primary"
          >
            <span class="button-text">Login</span>
          </router-link>
        </div>
      </div>
    </nav>
  <div class="container main-content">
    <!-- Left Sidebar -->
    <aside class="sidebar">
        <router-link to="/home" class="sidebar-link ">
          <span class="link-icon">🏠</span>
          <span>Home</span>
        </router-link>
        <router-link to="/groups" class="sidebar-link active">
          <span class="link-icon">👥</span>
          <span>Groups</span>
        </router-link>
        <router-link to="/events" class="sidebar-link">
          <span class="link-icon">📅</span>
          <span>Events</span>
        </router-link>
        <router-link to="/notifications" class="sidebar-link">
          <span class="link-icon">🔔</span>
          <span>Notifications</span>
        </router-link>
        <router-link to="/donations" class="sidebar-link">
          <span class="link-icon">🎁</span>
          <span>Donations</span>
        </router-link>
      </aside>

    <main class="feed">
      <div class="tasks-header">
        <h1 class="text-2xl font-bold">Community Groups</h1>
        <button class="button-primary" @click="router.push('/groups/create')">➕ Create New Group</button>
      </div>

      <div v-if="isLoading">Loading groups...</div>

      <div v-else class="groups-grid">
        <div v-for="group in groups" :key="group.id" class="group-card">
          <div class="group-image">{{ group.name[0] }}</div>
          <div class="group-content">
            <h3 class="group-title">
              <router-link :to="`/groups/${group.id}`">{{ group.name }}</router-link>
            </h3>
            <div class="group-meta">
              {{ group.member_count }} members • {{ group.category }}
            </div>
            <p class="text-sm text-gray-600">{{ group.description }}</p>
            <button
              v-if="!group.members.includes(currentUserId)"
              class="button-primary"
              style="width: 100%; margin-top: 16px"
              @click="joinGroup(group.id)"
            >
              Join Group
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</div>

</template>

<style scoped>
.groups-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}
.group-card {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 1rem;
  background: #fff;
  display: flex;
  flex-direction: column;
}
.group-image {
  font-size: 2rem;
  font-weight: bold;
  background: #eee;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.group-title {
  margin-top: 0.5rem;
  font-weight: 600;
  font-size: 1.2rem;
}
.group-meta {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
}
</style>
