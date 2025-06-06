<script setup lang="ts">
import { ref, onMounted, watchEffect } from 'vue'
import router from '../router'
import MapComponent from './MapComponent.vue'
import Notifications from "../components/Notifications.vue"
import CreateGroupModal from '../components/CreateGroup.vue'

import '../style.css'

const groups = ref([])
const isLoading = ref(true)
const currentUserId = parseInt(localStorage.getItem('user_id') || '0')
const showCreateGroupModal = ref(false) 

const handleGroupCreated = () => {
  fetchGroups() // Refresh the groups list
}
// Fetch groups from Django API
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

// Join group by ID
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
  router.push('/')
}
</script>

<template>
    <div class="app-container">
    <!-- Top Navigation Bar -->
    <nav class="navbar">
      <div class="container nav-content">
        <router-link to="/home" class="logo">
          <span class="logo-icon"></span>
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
            @click="router.push('/my-applications')"
          >
            <span class="button-icon">📋</span>
            <span class="button-text">My Applications</span>
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
            to="/" 
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
        <router-link to="/donations" class="sidebar-link">
          <span class="link-icon">🎁</span>
          <span>Donations</span>
        </router-link>
        <div>
        <h2 class="text-xl font-bold mb-2">Map Preview</h2>
        <MapComponent />
        </div>

      </aside>

    <main class="feed">
      <div class="tasks-header">
        <h1 class="text-2xl font-bold">Community Groups</h1>
         <button class="button-primary" @click="showCreateGroupModal = true">
    ➕ Create New Group
  </button>
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

 <CreateGroupModal 
    v-if="showCreateGroupModal" 
    :userId="currentUserId" 
    @close="showCreateGroupModal = false"
    @created="handleGroupCreated"
  />
</template>

<style scoped>
.button-primary {
  background-color: #2e7d32;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.button-primary:hover {
  background-color: #1b5e20;
}
.groups-grid {
    display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 2rem;
}

/* Make card layout horizontal like events */
.group-card {
 display: flex;
  background: #fff;
  padding: 1.25rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
  border: 1px solid #e0e0e0;
}

.group-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 16px rgba(46, 125, 50, 0.12);
  border-left-color: #4CAF50;
}

/* Left-side circle logo like event date box */
.group-image {
  width: 70px;
  min-width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
  border-radius: 50%;
  font-size: 1.8rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2E7D32;
  margin-right: 1.5rem;
  text-align: center;
}

/* Content area like event-content */
.group-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.group-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2E7D32;
  margin-bottom: 0.5rem;
  position: relative;
  display: inline-block;
}

.group-title a {
  color: #2E7D32;
  text-decoration: none;
}

.group-title::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: #4CAF50;
  transition: width 0.3s ease;
}

.group-card:hover .group-title::after {
  width: 100%;
}

.group-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.9rem;
  color: #689F38;
  margin-bottom: 0.75rem;
}

.group-meta svg {
  width: 16px;
  height: 16px;
  fill: #689F38;
}

.group-description {
  font-size: 0.95rem;
  line-height: 1.5;
  color: #555;
  margin-bottom: 1rem;
  flex-grow: 1;
}

/* Button Section */
.group-actions {
  display: flex;
  gap: 0.75rem;
}

.group-actions button {
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s ease;
  cursor: pointer;
}

.primary-action {
  background: #4CAF50;
  color: white;
  border: none;
}

.primary-action:hover {
  background: #388E3C;
}

.secondary-action {
  background: transparent;
  color: #4CAF50;
  border: 1px solid #81C784;
}

.secondary-action:hover {
  background: #E8F5E9;
}

/* Status indicators (optional) */
.group-status {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  display: inline-block;
  margin-top: 0.5rem;
}

.status-active {
  background-color: #E8F5E9;
  color: #2E7D32;
}

.status-inactive {
  background-color: #FFEBEE;
  color: #C62828;
}

/* Responsive tweaks */
@media (max-width: 768px) {
  .group-card {
    flex-direction: column;
  }

  .group-image {
    width: 100%;
    height: auto;
    border-radius: 8px;
    margin-right: 0;
    margin-bottom: 1rem;
    justify-content: flex-start;
    padding: 1rem;
  }

  .group-actions {
    flex-direction: column;
  }

  .group-actions button {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .group-meta {
    flex-direction: column;
    gap: 0.25rem;
  }
}

</style>
