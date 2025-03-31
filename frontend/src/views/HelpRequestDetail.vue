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
      <!-- ✅ Sidebar -->
      <aside class="sidebar">
        <router-link to="/home" class="sidebar-link">Home</router-link>
        <router-link to="/groups" class="sidebar-link">Groups</router-link>
        <router-link to="/events" class="sidebar-link">Events</router-link>
        <router-link to="/notifications" class="sidebar-link">Notifications</router-link>
        <router-link to="/donations" class="sidebar-link">🎁 Donations</router-link>
      </aside>
  
      <!-- ✅ Main Detail Content -->
      <main class="feed">
        <div class="max-w-2xl p-6 bg-white rounded-xl shadow-md mt-10 space-y-4">
          <h2 class="text-2xl font-bold">{{ helpRequest.title }}</h2>
          <p class="text-gray-700">{{ helpRequest.description }}</p>
  
          <div class="text-sm text-gray-600">
            <p><strong>Category:</strong> {{ helpRequest.category }}</p>
            <p><strong>Location:</strong> {{ helpRequest.location }}</p>
            <p><strong>Status:</strong> {{ helpRequest.status }}</p>
            <p><strong>Emergency:</strong> {{ helpRequest.is_emergency ? 'Yes' : 'No' }}</p>
            <p><strong>Created:</strong> {{ formatDate(helpRequest.created_at) }}</p>
          </div>
  
          <!-- Apply Button -->
          <div v-if="user && !isCreator">
            <button
              @click="applyToHelp"
              :disabled="isApplied"
              class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
            >
              {{ isApplied ? '✅ Already Applied' : '🤝 Apply to Help' }}
            </button>
          </div>
  
          <!-- Applicants (for creator only) -->
          <div v-if="isCreator && helpRequest.applicants.length > 0" class="mt-6">
            <h3 class="text-lg font-semibold mb-2">🧑‍🤝‍🧑 Applicants</h3>
            <ul class="list-disc ml-6">
              <li v-for="applicant in helpRequest.applicants" :key="applicant.id">
                {{ applicant.first_name }} {{ applicant.last_name }} ({{ applicant.email }})
              </li>
            </ul>
          </div>
  
          <!-- Debug Info -->
          <div class="mt-6 text-xs text-gray-500">
            <p><strong>Logged in user ID:</strong> {{ user?.id }}</p>
            <p><strong>Task creator ID:</strong> {{ helpRequest.created_by }}</p>
            <p><strong>Is Creator?</strong> {{ isCreator ? 'Yes' : 'No' }}</p>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  
  const route = useRoute()
  const router = useRouter()
  
  const helpRequestId = route.params.id
  const helpRequest = ref({ applicants: [] })
  const isApplied = ref(false)
  const isCreator = ref(false)
  const user = {
  id: parseInt(localStorage.getItem('user_id') || '0'),
  email: localStorage.getItem('user_email'),
  username: localStorage.getItem('user_username')
}

  const token = localStorage.getItem('access_token')
  
  const fetchHelpRequest = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/help-requests/${helpRequestId}/`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      const data = await res.json()
      helpRequest.value = data
      isCreator.value = user?.id === data.created_by
      isApplied.value = data.applicants?.some(applicant => applicant.id === user?.id)
    } catch (err) {
      console.error("❌ Failed to fetch help request:", err)
    }
  }
  
  const applyToHelp = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/help-requests/${helpRequestId}/apply/`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })
      const data = await res.json()
      alert(data.message)
      fetchHelpRequest()
    } catch (err) {
      console.error("❌ Failed to apply:", err)
    }
  }
  
  const handleLogout = () => {
    localStorage.clear()
    router.push('/login')
  }
  
  const formatDate = (dateStr) => new Date(dateStr).toLocaleString()
  
  onMounted(fetchHelpRequest)
  </script>
  