<script setup lang="ts">
import { ref, computed, onMounted,  watchEffect } from 'vue'
import { useRouter } from 'vue-router'

import Notifications from "../components/Notifications.vue"
import '../style.css' 

interface HelpRequest {
  id: number;
  title: string;
  description: string;
  category: string;
  location: string;
  status: string;
  is_emergency: boolean;
  created_at: string;
  created_by: number;
  applicants: number[];
  urgency?: string;
  is_applied?: boolean;
}

interface CommunityPost {
  id: number;
  title: string;
  category: string;
  created_at: string;
  content: string;
  image?: string;
  location?: string;
}

const posts = ref<CommunityPost[]>([])
const helpRequests = ref<HelpRequest[]>([])
const isLoading = ref(true)

const router = useRouter()
const user = ref<{ email: string; username: string; id: number } | null>(null)

const activeFilter = ref('all')
const searchQuery = ref('')

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

const fetchHelpRequests = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) return

  try {
    const response = await fetch('http://127.0.0.1:8000/api/help-requests/', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      const data: HelpRequest[] = await response.json()
      const userId = user.value?.id

      // Add `is_applied` flag for logic
      helpRequests.value = data.map(request => {
  const applied = request.applicants.some(applicant => applicant.id === userId)
  return { ...request, is_applied: applied }
})
    } else {
      console.error('Failed to fetch help requests')
    }
  } catch (error) {
    console.error('Error fetching help requests:', error)
  }
}

const fetchCommunityPosts = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/community-posts/')
    const data = await res.json()
    posts.value = data
  } catch (error) {
    console.error('Error fetching community posts:', error)
  }
}

const applyToHelp = async (requestId: number) => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('Login required to apply.')
    return
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/api/help-requests/${requestId}/apply/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    })

    const data = await res.json()
    alert(data.message)
    fetchHelpRequests()  // refresh status
  } catch (error) {
    console.error('Error applying to help:', error)
  }
}

const filteredRequests = computed(() => {
  return helpRequests.value.filter(request => {
    const matchesFilter =
      activeFilter.value === 'all' || request.status?.toLowerCase() === activeFilter.value
    const matchesSearch =
      request.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      request.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesFilter && matchesSearch
  })
})

window.addEventListener('userLoggedIn', checkUser)
watchEffect(() => {
  checkUser()
})

onMounted(() => {
  checkUser()
  fetchHelpRequests()
  fetchCommunityPosts()
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
    <router-link to="/home" class="logo">
      <span class="logo-icon">🤝</span>
      <span>CommunityHelp</span>
    </router-link>
    
    <div class="nav-links">
      <!-- Notification Component -->
      <div class="flex items-center">
        <Notifications />
      </div>
      
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
        <router-link to="/home" class="sidebar-link active">
          <span class="link-icon">🏠</span>
          <span>Home</span>
        </router-link>
        <router-link to="/groups" class="sidebar-link">
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

      <!-- Main Content -->
      <main class="feed">
        <!-- Help Requests Section -->
        <section class="section">
          <div class="section-header">
            <h1 class="section-title">Community Help Requests</h1>
            <div class="action-buttons">
              <button class="btn primary" @click="router.push('/post')">
                <span class="btn-icon">+</span>
                <span>Create Task</span>
              </button>
              <button class="btn secondary" @click="router.push('/create-post')">
                <span class="btn-icon">✏️</span>
                <span>Create Post</span>
              </button>
            </div>
          </div>

          <div class="filters">
            <div class="search-container">
              <span class="search-icon">🔍</span>
              <input
                type="text"
                v-model="searchQuery"
                placeholder="Search tasks..."
                class="search-input"
              />
            </div>
            <div class="filter-buttons">
              <button 
                v-for="filter in ['all', 'pending', 'accepted', 'completed']"
                :key="filter"
                :class="['filter-btn', { active: activeFilter === filter }]"
                @click="activeFilter = filter"
              >
                {{ filter.charAt(0).toUpperCase() + filter.slice(1) }}
              </button>
            </div>
          </div>

          <div v-if="helpRequests.length === 0" class="empty-state">
            <span class="empty-icon">📭</span>
            <p>No help requests available</p>
          </div>

          <div v-else class="cards-grid">
            <div 
              v-for="request in filteredRequests" 
              :key="request.id" 
              class="card"
            >
              <div class="card-header">
                <div class="card-title">
                  <h3>{{ request.title }}</h3>
                  <div class="card-meta">
                    <span>{{ request.location }}</span>
                    <span class="dot">•</span>
                    <span>{{ new Date(request.created_at).toLocaleDateString() }}</span>
                  </div>
                </div>
                <div 
                  :class="{
                    'tag emergency': request.is_emergency,
                    'tag regular': !request.is_emergency
                  }"
                >
                  {{ request.is_emergency ? '🚨 Emergency' : '🟢 Regular' }}
                </div>
              </div>

              <div class="card-content">
                <p>{{ request.description }}</p>
              </div>

              <div class="card-footer">
                <span class="category">{{ request.category }}</span>
                <div class="card-actions">
                  <button
                    v-if="user && user.id === request.created_by"
                    class="btn small"
                    @click="router.push(`/help-request/${request.id}`)"
                  >
                    👁 View Applicants
                  </button>
                  <button
                    v-else-if="user && !request.is_applied"
                    class="btn small primary"
                    @click="applyToHelp(request.id)"
                  >
                    🤝 Apply to Help
                  </button>
                  <span v-else class="applied-status">
                    ✅ Applied
                  </span>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Community Posts Section -->
        <section class="section">
          <h2 class="section-title">📣 Community Posts</h2>
          
          <div v-if="posts.length === 0" class="empty-state">
            <span class="empty-icon">📭</span>
            <p>No community posts available</p>
          </div>

          <div v-else class="cards-grid">
            <div v-for="post in posts" :key="post.id" class="card post-card">
              <div class="card-header">
                <div class="card-title">
                  <h3>{{ post.title }}</h3>
                  <div class="card-meta">
                    <span>{{ post.category }}</span>
                    <span class="dot">•</span>
                    <span>{{ new Date(post.created_at).toLocaleDateString() }}</span>
                  </div>
                </div>
              </div>

              <div class="card-content">
                <p>{{ post.content }}</p>
                <img
                  v-if="post.image"
                  :src="`http://127.0.0.1:8000${post.image}`"
                  alt="Post Image"
                  class="post-image"
                />
              </div>

              <div class="card-footer">
                <span class="location">
                  📍 {{ post.location || 'Location not specified' }}
                </span>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>
