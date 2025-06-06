<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GroupChat from '../components/GroupChat.vue'
import GroupPosts from '../components/GroupPosts.vue'
import Notifications from '../components/Notifications.vue'
import axios from '../utils/axiosInstance'

const user = ref<{ email: string; username: string; id: number } | null>(null)
const activities = ref<any[]>([])
const formatDate = (dt: string) => new Date(dt).toLocaleString()

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

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_email')
  localStorage.removeItem('user_username')
  localStorage.removeItem('user_id')
  user.value = null
  router.push('/')
}

const route = useRoute()
const router = useRouter()
const groupId = route.params.id

const group = ref<any>(null)
const isLoading = ref(true)
const showChatModal = ref(false) // Control modal visibility

const currentUserId = parseInt(localStorage.getItem('user_id') || '0')
const token = localStorage.getItem('access_token')

const fetchGroup = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/groups/${groupId}/`)
    const data = await res.json()
    group.value = data
  } catch (err) {
    console.error('Error fetching group details:', err)
  } finally {
    isLoading.value = false
  }
}

const fetchActivities = async (groupId: number|string) => {
  try {
    const res = await axios.get(`/groups/group-activity/?group=${groupId}`)
    activities.value = res.data
  } catch (err) {
    activities.value = []
    console.error('Could not load activities', err)
  }
}

const joinGroup = async () => {
  if (!token) {
    alert('You must be logged in to join a group.')
    return
  }
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/groups/${groupId}/join/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
    })
    const data = await res.json()
    if (res.ok) {
      alert(data.detail || 'Joined the group!')
      fetchGroup()
    } else {
      alert(data.detail || 'Failed to join.')
    }
  } catch (err) {
    console.error('Join error:', err)
  }
}

const leaveGroup = async () => {
  if (!confirm('Are you sure you want to leave this group?')) return
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/groups/${groupId}/leave/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
    })
    if (res.ok) {
      alert('You have left the group.')
      fetchGroup()
    } else {
      const err = await res.json()
      alert('Failed to leave: ' + err.detail)
    }
  } catch (err) {
    console.error('Leave error:', err)
  }
}

const deleteGroup = async () => {
  if (!confirm('Are you sure you want to delete this group?')) return
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/groups/${groupId}/`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` },
    })
    if (res.ok) {
      alert('Group deleted successfully.')
      router.push('/groups')
    } else {
      const err = await res.text()
      alert('Failed to delete: ' + err)
    }
  } catch (err) {
    console.error('Delete error:', err)
  }
}

onMounted(() => {
  checkUser()
  fetchGroup()
})

watch(group, (newGroup) => {
  if (newGroup && newGroup.id) fetchActivities(newGroup.id)
})
</script>

<template>
  <div class="app-container">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="container nav-content">
        <router-link to="/home" class="logo">
          <span class="logo-icon">🤝</span>
          <span>CommunityHelp</span>
        </router-link>
        <div class="nav-links">
          <Notifications />
          <button v-if="user" class="nav-button" @click="router.push('/profile')">
            👤 {{ user.username || user.email }}
          </button>
          <button v-if="user" class="nav-button" @click="router.push('/my-applications')">
            📋 My Applications
          </button>
          <button v-if="user" class="nav-button logout" @click="handleLogout">
            🚪 Logout
          </button>
          <router-link v-if="!user" to="/" class="nav-button primary">Login</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="group-details-page">
      <!-- Hero Section -->
      <div class="hero-section" :style="{ backgroundImage: `url(${group?.image || 'https://images.unsplash.com/photo-1592150621744-aca64f48394a?auto=format&fit=crop&q=80&w=2000'})` }">
        <div class="hero-content container">
          <span class="category-badge">{{ group?.category }}</span>
          <h1>{{ group?.name }}</h1>
        </div>
      </div>

      <div class="main-content container">
        <div class="content-grid">
          <!-- Main Content -->
          <div class="content-main">
            <!-- Quick Info -->
            <div class="quick-info">
              <div class="info-item">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
                <div>
                  <h3>Members</h3>
                  <p>{{ group?.member_count || 0 }} people joined</p>
                </div>
              </div>
              <div class="info-item">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <div>
                  <h3>Created</h3>
                  <p>{{ group ? new Date(group.created_at).toLocaleDateString() : '' }}</p>
                </div>
              </div>
              <div class="info-item">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8h2a2 2 0 012 2v6a2 2 0 01-2 2h-2v4l-4-4H9a1.994 1.994 0 01-1.414-.586m0 0L11 14h4a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2v4l.586-.586z" />
                </svg>
                <div>
                  <h3>Activity</h3>
                  <p>{{ group?.post_count || 0 }} discussions</p>
                </div>
              </div>
            </div>

            <!-- About Group -->
            <div class="content-section">
              <h2>About This Group</h2>
              <p>{{ group?.description }}</p>
            </div>

            <!-- Activity Feed Section -->
            <div v-if="group?.members && group?.members.includes(currentUserId)" class="content-section activity-feed">
              <h2 class="text-lg font-semibold mb-3">Recent Activity</h2>
              <div v-if="activities.length === 0" class="text-gray-400 text-sm mb-2">
                No recent activity yet.
              </div>
              <div v-for="activity in activities" :key="activity.id" class="activity-item mb-2">
                <div v-if="activity.activity_type === 'joined'">
                  <span class="font-semibold">{{ activity.user_name }}</span> joined the group
                  <span class="text-xs text-gray-400 ml-2">{{ formatDate(activity.timestamp) }}</span>
                </div>
                <div v-else-if="activity.activity_type === 'post'">
                  <span class="font-semibold">{{ activity.user_name }}</span> posted:
                  <span class="italic">"{{ activity.post_content }}"</span>
                  <span class="text-xs text-gray-400 ml-2">{{ formatDate(activity.timestamp) }}</span>
                </div>
              </div>
            </div>

            <!-- Group Posts -->
            <div v-if="group?.members && group?.members.includes(currentUserId)" class="content-section">
              <h2>Group Discussions</h2>
              <GroupPosts :groupId="group.id" />
            </div>

            <!-- Join Prompt (for non-members) -->
            <div v-else class="content-section join-prompt">
              <h2>Join to Participate</h2>
              <p>Become a member to view and participate in discussions.</p>
              <button class="join-btn" @click="joinGroup">
                Join Group
              </button>
            </div>
          </div>

          <!-- Sidebar -->
          <div class="sidebar">
            <!-- Action Card -->
            <div class="action-card">
              <template v-if="group?.members && group?.members.includes(currentUserId)">
                <button class="apply-btn cancel-btn" @click="leaveGroup">
                  👋 Leave Group
                </button>
              </template>
              <template v-else>
                <button class="apply-btn" @click="joinGroup">
                  👍 Join Group
                </button>
              </template>

              <!-- Admin Actions -->
              <div v-if="group?.created_by === currentUserId" class="action-buttons mt-4">
                <button class="secondary-btn" @click="router.push(`/groups/edit/${group.id}`)">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                  </svg>
                  Edit
                </button>
                <button class="secondary-btn" @click="deleteGroup">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                  </svg>
                  Delete
                </button>
              </div>
            </div>

            <!-- Group Rules -->
            <div class="rules-card" v-if="group?.rules">
              <h2>Group Rules</h2>
              <ul>
                <li v-for="(rule, index) in group.rules" :key="index">{{ rule }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Button -->
    <button
      v-if="group && group.members && group.members.includes(currentUserId)"
      class="chat-toggle-btn"
      @click="showChatModal = true"
      aria-label="Open group chat"
    >
      💬 Chat
    </button>

    <!-- Chat Modal -->
    <div
      v-if="showChatModal && group && group.members && group.members.includes(currentUserId)"
      class="modal-overlay"
      @click.self="showChatModal = false"
    >
      <div class="modal-container">
        <GroupChat :userId="currentUserId" roomType="group" :roomId="group.id" />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Existing styles unchanged */
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

.activity-feed {
  background: #f9fafb;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}

.activity-item {
  border-left: 3px solid #10b981;
  padding-left: 10px;
  margin-bottom: 10px;
}

.group-details-page {
  min-height: 100vh;
  background-color: #f9fafb;
}

/* Navbar Styles */
.navbar {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  font-size: 1.25rem;
  text-decoration: none;
  color: #1f2937;
}

.logo-icon {
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.nav-button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  background-color: transparent;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.nav-button:hover {
  background-color: #f3f4f6;
}

.nav-button.primary {
  background-color: #10b981;
  color: white;
}

.nav-button.primary:hover {
  background-color: #059669;
}

.nav-button.logout {
  color: #ef4444;
}

.nav-button.logout:hover {
  background-color: #fee2e2;
}

/* Hero Section */
.hero-section {
  height: 400px;
  background-size: cover;
  background-position: center;
  position: relative;
  color: white;
  display: flex;
  align-items: flex-end;
}

.hero-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    to bottom,
    rgba(0, 0, 0, 0.1),
    rgba(0, 0, 0, 0.7)
  );
}

.hero-content {
  position: relative;
  padding: 2rem;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

.category-badge {
  display: inline-block;
  background-color: #3b82f6;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 1rem;
}

.hero-content h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.main-content {
  padding: 3rem 0;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

@media (min-width: 1024px) {
  .content-grid {
    grid-template-columns: 2fr 1fr;
  }
}

.quick-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.info-item svg {
  width: 24px;
  height: 24px;
  color: #3b82f6;
  flex-shrink: 0;
}

.info-item h3 {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
}

.info-item p {
  font-weight: 500;
  color: #1f2937;
}

.content-section {
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.content-section h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.content-section p {
  color: #4b5563;
  line-height: 1.6;
}

.join-prompt {
  text-align: center;
  padding: 2rem;
}

.join-prompt h2 {
  color: #3b82f6;
}

.join-btn {
  background-color: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 1rem;
}

.join-btn:hover {
  background-color: #2563eb;
  transform: translateY(-1px);
}

/* Sidebar */
.sidebar {
  position: sticky;
  top: 2rem;
}

.action-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.apply-btn {
  width: 100%;
  background-color: #10b981;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.apply-btn:hover {
  background-color: #059669;
  transform: translateY(-1px);
}

.apply-btn.cancel-btn {
  background-color: #ef4444;
}

.apply-btn.cancel-btn:hover {
  background-color: #dc2626;
}

.action-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.secondary-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  color: #4b5563;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.secondary-btn:hover {
  background-color: #f3f4f6;
  color: #1f2937;
  border-color: #d1d5db;
}

.rules-card,
.members-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 1.5rem;
}

.rules-card h2,
.members-card h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1rem;
}

.rules-card ul {
  list-style-type: none;
  padding-left: 0;
}

.rules-card li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #e5e7eb;
  color: #4b5563;
}

.rules-card li:last-child {
  border-bottom: none;
}

.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.member {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.member-avatar {
  width: 40px;
  height: 40px;
  background-color: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.member-name {
  font-size: 0.75rem;
  text-align: center;
  color: #4b5563;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 80px;
}

.view-all-btn {
  width: 100%;
  background-color: transparent;
  border: 1px solid #e5e7eb;
  color: #3b82f6;
  padding: 0.5rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.view-all-btn:hover {
  background-color: #eff6ff;
  border-color: #bfdbfe;
}

/* Chat Toggle Button */
.chat-toggle-btn {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  background-color: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 9999px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.chat-toggle-btn:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .chat-toggle-btn {
    bottom: 1rem;
    right: 1rem;
    padding: 0.5rem 1rem;
    font-size: 0.875rem;
  }
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  z-index: 2000;
  animation: fadeIn 0.3s ease;
}

.modal-container {
  width: 320px;
  max-height: 500px;
  background-color: white;
  border-radius: 12px;
  overflow: hidden;
  margin: 1.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  resize: both;
}

@media (max-width: 768px) {
  .modal-overlay {
    align-items: center;
    justify-content: center;
  }

  .modal-container {
    width: 95%;
    max-height: 70vh;
    margin: 0.75rem;
    border-radius: 8px;
  }
}

/* Loading State */
.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(16, 185, 129, 0.2);
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>