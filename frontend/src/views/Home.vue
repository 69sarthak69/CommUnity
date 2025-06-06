<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watchEffect } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import MapComponent from './MapComponent.vue'
import Notifications from '../components/Notifications.vue'
import '../style.css'
import AskForHelpModal from '../components/AskForHelp.vue'
import CreatePostModal from '../components/CreateCommunityPost.vue'
import CommentItem from '../components/CommentItem.vue'
import ApplyToHelpModal from '../components/ApplyToHelp.vue'
import MyApplicationsModal from '../components/MyApplicationsModal.vue'
import ProfileModal from '../components/ProfileModal.vue'

const showNearbyOnly = ref(false)
const hideApplied = ref(true) // New toggle to hide applied requests

const displayedRequests = computed(() =>
  showNearbyOnly.value
    ? filteredRequests.value.filter(r => r.is_nearby)
    : filteredRequests.value
)

const showEventModal = ref(false)
const showApplicationsModal = ref(false)
const showProfileModal = ref(false)

const props = defineProps<{ requestId: number | string }>()

const lat = ref<number | null>(null)
const lng = ref<number | null>(null)

const toastMessage = ref('')
const toastType = ref<'success' | 'error'>('success')

function showToast(message: string, type: 'success' | 'error' = 'success') {
  toastMessage.value = message
  toastType.value = type
  setTimeout(() => (toastMessage.value = ''), 3000)
}

function getUserLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        lat.value = position.coords.latitude
        lng.value = position.coords.longitude
        localStorage.setItem('user_lat', String(lat.value))
        localStorage.setItem('user_lng', String(lng.value))
        fetchHelpRequests()
      },
      (error) => {
        showToast('Location access denied or not available.', 'error')
        fetchHelpRequests()
      }
    )
  } else {
    showToast('Geolocation is not supported by this browser.', 'error')
    fetchHelpRequests()
  }
}

const showHelpModal = ref(false)
const showPostModal = ref(false)
const newComments = ref<Record<number, string>>({})
const selectedRequestId = ref<number | null>(null)
const showApplyModal = ref(false)

interface HelpRequest {
  id: number
  title: string
  description: string
  category: string
  location: string
  status: string
  is_emergency: boolean
  created_at: string
  created_by: number
  applicants: number[]
  urgency?: string
  is_applied?: boolean
  distance?: number | null
  is_nearby?: boolean
}

interface CommunityPost {
  id: number
  title: string
  category: string
  created_at: string
  content: string
  image?: string
  location?: string
  comments?: any[]
}

let ws: WebSocket | null = null

const goToProfile = () => {
  showProfileModal.value = true
}

const openApplicationModal = (requestId: number) => {
  if (!user.value) {
    showToast('Please log in to apply.', 'error')
    router.push('/')
    return
  }
  selectedRequestId.value = requestId
  showApplyModal.value = true
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

  isLoading.value = true
  try {
    let url = 'http://127.0.0.1:8000/api/help-requests/'
    if (lat.value && lng.value) {
      url += `?lat=${lat.value}&lng=${lng.value}`
    }
    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })

    if (response.ok) {
      const data: HelpRequest[] = await response.json()
      const userId = user.value?.id
      helpRequests.value = data.map(request => ({
  ...request,
  is_applied: request.applicants.includes(userId ?? -1),
  is_nearby: typeof request.distance === 'number' && request.distance <= 5
}))
    } else {
      showToast('Failed to fetch help requests.', 'error')
    }
  } catch (error) {
    console.error('Error fetching help requests:', error)
    showToast('Error fetching help requests.', 'error')
  } finally {
    isLoading.value = false
  }
}

const fetchCommunityPosts = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/community-posts/')
    const data = await res.json()
    for (const post of data) {
      post.comments = await fetchCommentsForPost(post.id)
    }
    posts.value = data
  } catch (error) {
    console.error('Error fetching community posts:', error)
    showToast('Error fetching community posts.', 'error')
  }
}

const fetchCommentsForPost = async (postId: number) => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/comments/?post=${postId}`)
    return response.data
  } catch (error) {
    console.error('Failed to fetch comments for post', error)
    return []
  }
}

const submitComment = async (postId: number) => {
  const text = newComments.value[postId]
  if (!text) return showToast('Comment cannot be empty.', 'error')

  try {
    const response = await axios.post(
      'http://127.0.0.1:8000/api/comments/',
      { post: postId, text, parent: null },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      }
    )
    newComments.value[postId] = ''
    fetchCommunityPosts()
    showToast('Comment submitted successfully!', 'success')
  } catch (error) {
    console.error('Failed to submit comment:', error)
    showToast('Failed to submit comment.', 'error')
  }
}

const filteredRequests = computed(() => {
  return helpRequests.value.filter(request => {
    const matchesFilter =
      activeFilter.value === 'all' || request.status?.toLowerCase() === activeFilter.value
    const matchesSearch =
      request.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      request.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesApplied = !hideApplied.value || !request.is_applied
    return matchesFilter && matchesSearch && matchesApplied
  })
})

const setupFeedSocket = () => {
  ws = new WebSocket('ws://127.0.0.1:8000/ws/feed/')
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.type === 'new_help_request') {
      const userId = user.value?.id
      helpRequests.value.unshift({
        ...data,
        is_applied: data.applicants.includes(userId ?? -1)
      })
    }
    if (data.type === 'new_community_post') {
      fetchCommentsForPost(data.id).then(comments => {
        posts.value.unshift({ ...data, comments })
      })
    }
  }
  ws.onclose = () => {
    setTimeout(setupFeedSocket, 1000)
  }
}

window.addEventListener('userLoggedIn', checkUser)
watchEffect(() => {
  checkUser()
})

onMounted(() => {
  checkUser()
  fetchCommunityPosts()
  setupFeedSocket()
  getUserLocation()
})
onUnmounted(() => {
  if (ws) ws.close()
})

const showLogoutConfirm = ref(false)

const handleLogout = () => {
  showLogoutConfirm.value = true
}

const confirmLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_email')
  localStorage.removeItem('user_username')
  localStorage.removeItem('user_id')
  user.value = null
  router.push('/')
  showLogoutConfirm.value = false
}

const cancelLogout = () => {
  showLogoutConfirm.value = false
}
</script>

<template>
  <div class="app-container">
    <!-- Toast Notification -->
    <div
      v-if="toastMessage"
      :class="['toast', toastType === 'success' ? 'toast-success' : 'toast-error']"
    >
      {{ toastMessage }}
    </div>

    <!-- Top Navigation Bar -->
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
           <ProfileModal 
      v-if="showProfileModal" 
      @close="showProfileModal = false" 
    />
          <button
  v-if="user"
  class="nav-button profile-btn"
  @click="goToProfile"
>
  <span class="button-icon">👤</span>
  <span class="button-text">{{ user.username || user.email }}</span>
</button>
          <button
            v-if="user"
            class="nav-button"
            @click="showApplicationsModal = true"
          >
            <span class="button-icon">📋</span>
            <span class="button-text">My Applications</span>
          </button>
          <MyApplicationsModal
            v-if="showApplicationsModal"
            @close="showApplicationsModal = false"
          />
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

    <!-- Logout Confirmation Modal -->
    <div v-if="showLogoutConfirm" class="logout-confirm-modal">
      <div class="modal-content">
        <h3>Confirm Logout</h3>
        <p>Are you sure you want to logout?</p>
        <div class="modal-actions">
          <button @click="cancelLogout" class="cancel-btn">Cancel</button>
          <button @click="confirmLogout" class="confirm-btn">Logout</button>
        </div>
      </div>
    </div>

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
        <router-link to="/donations" class="sidebar-link">
          <span class="link-icon">🎁</span>
          <span>Donations</span>
        </router-link>
        <div>
          <h2 class="text-xl font-bold mb-2">Map Preview</h2>
          <MapComponent />
        </div>
      </aside>

      <!-- Main Content -->
      <main class="feed">
        <!-- Help Requests Section -->
        <section class="section">
          <div class="section-header">
            <h1 class="section-title">Community Help Requests</h1>
            <div class="action-buttons">
              <button class="btn primary" @click="showHelpModal = true">➕ Create Task</button>
              <AskForHelpModal v-if="showHelpModal" @close="showHelpModal = false" />
              <button class="btn secondary" @click="showPostModal = true">
                <span class="btn-icon">✏️</span>
                <span>Create Post</span>
              </button>
              <CreatePostModal v-if="showPostModal" @close="showPostModal = false" />
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
              
            </div>
            <div class="filter-toggles">
              <label class="nearby-filter">
                <input type="checkbox" v-model="showNearbyOnly" />
                Show Nearby Only
              </label>
             
            </div>
          </div>

          <div v-if="isLoading" class="loading-state">
            <svg class="animate-spin h-8 w-8 text-green-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8h8a8 8 0 01-16 0z"></path>
            </svg>
            <p>Loading help requests...</p>
          </div>
          <div v-else-if="displayedRequests.length === 0" class="empty-state">
            <span class="empty-icon">📭</span>
            <p>No help requests available</p>
          </div>

          <div v-else class="cards-grid">
            <div
              v-for="request in displayedRequests"
              :key="request.id"
              class="card"
            >
              <div class="card-header">
                <div class="card-title">
                  <h3>
                    {{ request.title }}
                    <span v-if="request.is_nearby" class="nearby-badge">Nearby</span>
                  </h3>
                  <div class="card-meta">
                    <span>{{ request.location }}</span>
                    <span class="dot">•</span>
                    <span>{{ new Date(request.created_at).toLocaleDateString() }}</span>
                    <span v-if="request.distance !== null && request.is_nearby" class="distance">
                      • {{ request.distance }} km away
                    </span>
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
                    @click="openApplicationModal(request.id)"
                  >
                    🤝 Apply to Help
                  </button>
                  <span v-else class="applied-status">
                    ✅ Already Applied
                  </span>
                  <ApplyToHelpModal
                    v-if="showApplyModal && selectedRequestId === request.id"
                    :request-id="request.id"
                    @close="showApplyModal = false"
                    @applied="fetchHelpRequests"
                    @toast="showToast"
                  />
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
                  :src="post.image"
                  alt="Post Image"
                  class="post-image"
                />
              </div>
              <div class="card-footer">
                <span class="location">
                  📍 {{ post.location || 'Location not specified' }}
                </span>
              </div>
              <div class="mt-4">
                <CommentItem
                  v-for="comment in post.comments"
                  :key="comment.id"
                  :comment="comment"
                  :post-id="post.id"
                  @replied="fetchCommunityPosts"
                />
                <div class="mt-2">
                  <input
                    v-model="newComments[post.id]"
                    placeholder="Write a comment..."
                    class="border p-1 w-full rounded"
                  />
                  <button
                    @click="submitComment(post.id)"
                    class="bg-blue-500 text-white px-2 py-1 rounded mt-1"
                  >
                    Comment
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* Add to your style section */
.profile-btn {
  background-color: #f0f9ff;
  color: #0369a1;
  margin-right: 0.5rem;
}

.profile-btn:hover {
  background-color: #e0f2fe;
}

.logout-btn {
  background-color: #fef2f2;
  color: #b91c1c;
}

.logout-btn:hover {
  background-color: #fee2e2;
}

.logout-confirm-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  max-width: 400px;
  width: 90%;
  text-align: center;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1.5rem;
}

.cancel-btn {
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
}

.confirm-btn {
  padding: 0.5rem 1rem;
  background: #ef4444;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
}

.confirm-btn:hover {
  background: #dc2626;
}

.location-debug {
  display: none;
}

.nearby-badge {
  background: #4caf50;
  color: #fff;
  border-radius: 8px;
  padding: 2px 8px;
  margin-left: 8px;
  font-size: 0.85em;
  font-weight: 600;
}

.distance {
  color: #388e3c;
  font-size: 0.9em;
  margin-left: 8px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  animation: fadeIn 0.3s ease-out;
}

.modal-container {
  background: white;
  width: 100%;
  max-width: 600px;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  transform: translateY(0);
  transition: transform 0.3s ease, opacity 0.3s ease;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-container:hover {
  transform: translateY(-2px);
}

.modal-header {
  padding: 1.5rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  transition: transform 0.2s;
  padding: 0.5rem;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: rotate(90deg);
}

.modal-body {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #374151;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.form-textarea {
  min-height: 120px;
  resize: vertical;
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1rem;
}

.btn-group {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-primary {
  background-color: #10b981;
  color: white;
  flex: 1;
}

.btn-primary:hover {
  background-color: #059669;
  transform: translateY(-1px);
}

.btn-secondary {
  background-color: white;
  color: #374151;
  border: 1px solid #e5e7eb;
  flex: 1;
}

.btn-secondary:hover {
  background-color: #f3f4f6;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-container::-webkit-scrollbar {
  width: 8px;
}

.modal-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.modal-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}

.modal-container::-webkit-scrollbar-thumb:hover {
  background: #a1a1a1;
}

@media (max-width: 640px) {
  .modal-container {
    max-width: 95%;
  }
  .btn-group {
    flex-direction: column;
  }
  .btn {
    width: 100%;
  }
}

.emergency-tag {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background-color: #ef4444;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.toast {
  position: fixed;
  top: 1rem;
  right: 1rem;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  color: white;
  z-index: 3000;
  animation: slideIn 0.3s ease-out;
}

.toast-success {
  background: #10b981;
}

.toast-error {
  background: #ef4444;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  color: #4b5563;
}

.nearby-filter,
.applied-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: #4b5563;
}

.filter-toggles {
  display: flex;
  gap: 1rem;
}


</style>