<script setup lang="ts">
import { ref, computed, onMounted, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import Notifications from "../components/Notifications.vue"

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
  <div class="nav-container">
    <div class="container nav-content">
      <router-link to="/" class="logo">Community Help</router-link>
      <div class="nav-links">
        <Notifications />
        <button class="button-secondary" @click="router.push('/profile')" v-if="user">
          👤 {{ user?.email }}
        </button>
        <button class="button-secondary" @click="handleLogout" v-if="user">🚪 Logout</button>
        <button class="button-secondary" @click="router.push('/chatbox')" v-if="user">💬 Chat</button>
        <router-link to="/login" class="button-primary" v-if="!user">Login</router-link>
      </div>
    </div>
  </div>

  <div class="container main-content">
    <aside class="sidebar">
      <router-link to="/home" class="sidebar-link">Home</router-link>
      <router-link to="/groups" class="sidebar-link">Groups</router-link>
      <router-link to="/events" class="sidebar-link">Events</router-link>
      <router-link to="/notifications" class="sidebar-link">Notifications</router-link>
      <router-link to="/donations" class="sidebar-link">🎁 Donations</router-link>
      
    </aside>

    <main class="feed">
      <div class="tasks-header">
        <h1 class="text-2xl font-bold">Community Help Requests</h1>
        <button class="button-primary" @click="router.push('/post')">Create New Task</button>
        <button class="button-secondary ml-2" @click="router.push('/create-post')">Create Community Post</button>
      </div>

      <div class="task-filters">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search tasks..."
          class="form-input"
          style="width: 300px"
        />
        <button 
          v-for="filter in ['all', 'pending', 'accepted', 'completed']"
          :key="filter"
          :class="['filter-button', { active: activeFilter === filter }]"
          @click="activeFilter = filter"
        >
          {{ filter.charAt(0).toUpperCase() + filter.slice(1) }}
        </button>
      </div>

      <div v-if="helpRequests.length === 0">
        <p class="text-gray-500">No help requests available.</p>
      </div>

      <div v-else>
        <div v-for="request in filteredRequests" :key="request.id" class="post-card">
          <div class="post-header">
            <div class="post-author">
              <div class="author-info">
                <span class="author-name">{{ request.title }}</span>
                <span class="post-meta">
                  {{ request.location }} • {{ new Date(request.created_at).toLocaleDateString() }}
                </span>
              </div>
            </div>
            <span
              :class="{
                'bg-red-100 text-red-800': request.is_emergency,
                'bg-green-100 text-green-800': !request.is_emergency
              }"
              class="px-2 py-1 rounded-full text-sm"
            >
              {{ request.is_emergency ? '🚨 Emergency' : 'Regular' }}
            </span>
          </div>

          <div class="post-content">{{ request.description }}</div>

          <div class="post-actions space-x-4">
            <span class="text-sm text-gray-600">Category: {{ request.category }}</span>

            <button
              v-if="user && user.id === request.created_by"
              class="text-blue-600 font-medium"
              @click="router.push(`/help-request/${request.id}`)"
            >
              👁 View Applicants
            </button>

            <button
              v-else-if="user && !request.is_applied"
              class="button-primary"
              @click="applyToHelp(request.id)"
            >
              🤝 Apply to Help
            </button>

            <span v-else class="text-green-600 font-medium">✅ Already Applied</span>
          </div>
        </div>
      </div>

      <div class="community-posts-section mt-10">
        <h2 class="text-2xl font-bold mb-4">📣 Community Posts</h2>
        <div v-if="posts.length === 0">
          <p class="text-gray-500">No community posts available.</p>
        </div>
        <div v-else>
          <div v-for="post in posts" :key="post.id" class="post-card mb-6 p-4 bg-white rounded shadow">
            <div class="post-header mb-2">
              <div class="author-info">
                <h3 class="text-lg font-semibold">{{ post.title }}</h3>
                <span class="text-sm text-gray-600">
                  {{ post.category }} • {{ new Date(post.created_at).toLocaleDateString() }}
                </span>
              </div>
            </div>
            <div class="post-content mb-2">
              <p>{{ post.content }}</p>
            </div>
            <img
              v-if="post.image"
              :src="`http://127.0.0.1:8000${post.image}`"
              alt="Post Image"
              class="w-full max-w-md rounded-lg mt-3"
            />
            <div class="post-meta text-sm text-gray-500 mt-2">
              Location: {{ post.location || 'Not specified' }}
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
