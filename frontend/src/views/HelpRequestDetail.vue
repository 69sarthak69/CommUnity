
<style scoped>
/* Base Styles */
.nav-container {
  background-color: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2e7d32;
  text-decoration: none;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.button-primary {
  background-color: #2e7d32;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: none;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.button-primary:hover {
  background-color: #1b5e20;
}

.button-secondary {
  background-color: white;
  color: #2e7d32;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  border: 1px solid #2e7d32;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.button-secondary:hover {
  background-color: #e8f5e9;
}

/* Main Content Layout */
.main-content {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 2rem;
  padding: 2rem 0;
  min-height: calc(100vh - 72px);
}

.sidebar {
  position: sticky;
  top: 1rem;
  align-self: start;
  height: fit-content;
}

.sidebar-link {
  display: block;
  padding: 0.75rem 1rem;
  margin-bottom: 0.5rem;
  border-radius: 8px;
  color: #4b5563;
  text-decoration: none;
  transition: all 0.2s;
}

.sidebar-link:hover {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.sidebar-link.router-link-active {
  background-color: #e8f5e9;
  color: #2e7d32;
  font-weight: 500;
}

.feed {
  background-color: #f9fafb;
  border-radius: 12px;
  padding: 2rem;
}

/* Help Request Card */
.help-request-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 2rem;
}

.help-request-title {
  font-size: 1.75rem;
  color: #1a237e;
  margin-bottom: 1rem;
}

.help-request-description {
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.meta-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.meta-item {
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 8px;
}

.meta-item strong {
  display: block;
  color: #616161;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.meta-item span {
  color: #212121;
  font-weight: 500;
}

.created-at {
  color: #616161;
  font-size: 0.875rem;
  margin-bottom: 2rem;
}

/* Applicants Section */
.applicants-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e0e0e0;
}

.applicants-section h3 {
  font-size: 1.25rem;
  color: #1a237e;
  margin-bottom: 1rem;
}

.applicant-list {
  display: grid;
  gap: 1rem;
}

.applicant-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 8px;
}

.applicant-avatar {
  width: 40px;
  height: 40px;
  background-color: #2e7d32;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

/* Apply Button */
.apply-button {
  background-color: #2e7d32;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
}

.apply-button:hover {
  background-color: #1b5e20;
}

.apply-button:disabled {
  background-color: #81c784;
  cursor: not-allowed;
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .main-content {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    display: none;
  }
  
  .help-request-card {
    padding: 1.5rem;
  }
  
  .meta-info {
    grid-template-columns: 1fr;
  }
}
</style>

<template>
   <nav class="navbar">
   <div class="container nav-content">
    <router-link to="/home" class="logo">
      <span class="logo-icon"></span>
      <span>CommunityHelp</span>
    </router-link>

    <div class="nav-links">
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
        to="/" 
        class="nav-button primary"
      >
        <span class="button-text">Login</span>
      </router-link>
    </div>
  </div>
</nav>

  <div class="container main-content">
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

        <router-link to="/donations" class="sidebar-link">
          <span class="link-icon">🏱</span>
          <span>Donations</span>
        </router-link>
        <div>
          <h2 class="text-xl font-bold mb-2">Map Preview</h2>
        <MapComponent />
       </div>
      </aside>
    <main class="feed">
  <div class="help-request-card">
    <h2 class="help-request-title">{{ helpRequest.title }}</h2>
    <p class="help-request-description">{{ helpRequest.description }}</p>

    <div class="meta-info">
      <div class="meta-item">
        <strong>Category</strong>
        <span>{{ helpRequest.category }}</span>
      </div>
      <div class="meta-item">
        <strong>Location</strong>
        <span>{{ helpRequest.location }}</span>
      </div>
      <div class="meta-item">
        <strong>Status</strong>
        <span>{{ helpRequest.status }}</span>
      </div>
      <div class="meta-item">
        <strong>Emergency</strong>
        <span>{{ helpRequest.is_emergency ? 'Yes' : 'No' }}</span>
      </div>
    </div>

    <p class="created-at">Created: {{ formatDate(helpRequest.created_at) }}</p>

    <div v-if="user && !isCreator">
      <button
        @click="applyToHelp"
        :disabled="isApplied"
        class="apply-button"
      >
        {{ isApplied ? '✅ Already Applied' : '🤝 Apply to Help' }}
      </button>
    </div>

    <!-- Applications for creator -->
    <div v-if="isCreator && applications.length > 0" class="applicants-section">
      <h3>🢑 Applications</h3>
      <ul class="applicant-list">
        <li v-for="app in applications" :key="app.id" class="applicant-item">
          <div class="applicant-avatar">
            {{ app.user_name.charAt(0).toUpperCase() }}
          </div>
          <div class="applicant-details">
            <p><strong>{{ app.user_name }}</strong></p>
            <p class="text-sm text-gray-600 italic">
              📜 {{ app.letter }}
            </p>
            <p class="text-sm text-blue-600">
              📅 {{ new Date(app.created_at).toLocaleString() }}
            </p>
            <div class="mt-2">
              <span
                v-if="app.status === 'approved'"
                class="text-green-600 font-semibold"
              >
                ✅ Approved
              </span>
              <span
                v-else-if="app.status === 'rejected'"
                class="text-red-600 font-semibold"
              >
                ❌ Rejected
              </span>
              <div v-else class="space-x-2">
                <button
                  @click="approve(app.id)"
                  class="btn small bg-green-600 text-white px-3 py-1 rounded"
                  :disabled="approving === app.id || rejecting === app.id"
                >
                  <span v-if="approving === app.id">...</span>
                  <span v-else>Approve</span>
                </button>
                <button
                  @click="reject(app.id)"
                  class="btn small bg-red-500 text-white px-3 py-1 rounded"
                  :disabled="approving === app.id || rejecting === app.id"
                >
                  <span v-if="rejecting === app.id">...</span>
                  <span v-else>Reject</span>
                </button>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</main>
</div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Notifications from '../components/Notifications.vue'
import MapComponent from './MapComponent.vue'

const route = useRoute()
const router = useRouter()

const helpRequestId = route.params.id
const helpRequest = ref({ applicants: [] })
const applications = ref([])
const isApplied = ref(false)
const isCreator = ref(false)
const user = {
  id: parseInt(localStorage.getItem('user_id') || '0'),
  email: localStorage.getItem('user_email'),
  username: localStorage.getItem('user_username')
}
const token = localStorage.getItem('access_token')

// Track which applicant is being approved/rejected
const approving = ref(null)
const rejecting = ref(null)

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
    // Handle applicants as objects or IDs (for isApplied)
    if (Array.isArray(data.applicants)) {
      isApplied.value = data.applicants.some(applicant =>
        applicant.id ? applicant.id === user.id : applicant === user.id
      )
    } else {
      isApplied.value = false
    }
  } catch (err) {
    console.error("Failed to fetch help request:", err)
  }
}

const fetchApplications = async () => {
  if (!isCreator.value) return // Only fetch if owner
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/${helpRequestId}/applications/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    const data = await res.json()
    applications.value = data
  } catch (err) {
    console.error("Failed to fetch applications", err)
  }
}

// --- Approve/Reject logic, refetch both data afterwards ---
const approve = async (appId) => {
  approving.value = appId
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/applications/${appId}/approve/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    })

    let data = {}
    try {
      data = await res.json()
    } catch (jsonErr) {
      console.warn('Response was not JSON:', jsonErr)
    }

    if (res.ok) {
      alert(data.message || "✅ Applicant approved!")
      await fetchApplications()
      await fetchHelpRequest()
    } else {
      alert(data.detail || `❌ Failed to approve (status ${res.status})`)
    }

  } catch (err) {
    console.error("❌ Network or unexpected error:", err)
    alert("Something went wrong during approval.")
  } finally {
    approving.value = null
  }
}


const reject = async (appId) => {
  rejecting.value = appId
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/applications/${appId}/reject/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    })

    let data = {}
    try {
      data = await res.json()
    } catch (jsonErr) {
      console.warn('Response was not JSON:', jsonErr)
    }

    if (res.ok) {
      alert(data.message || "❌ Applicant rejected!")
      await fetchApplications()
      await fetchHelpRequest()
    } else {
      alert(data.detail || `❌ Failed to reject (status ${res.status})`)
    }

  } catch (err) {
    console.error("❌ Network or unexpected error:", err)
    alert("Something went wrong during rejection.")
  } finally {
    rejecting.value = null
  }
}


const applyToHelp = async () => {
  const letter = prompt("Why are you suitable for this task?")
  if (!letter) return
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/help-requests/${helpRequestId}/apply/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ letter })
    })
    const data = await res.json()
    alert(data.message)
    fetchHelpRequest()
  } catch (err) {
    console.error("Failed to apply:", err)
  }
}

const handleLogout = () => {
  localStorage.clear()
  router.push('/')
}

const formatDate = (dateStr) => new Date(dateStr).toLocaleString()

// --- Mount logic ---
onMounted(async () => {
  await fetchHelpRequest()
  await fetchApplications()
})

// --- If creator changes (rare but for safety), update applications
watch(isCreator, async (val) => {
  if (val) {
    await fetchApplications()
  }
})
</script>
