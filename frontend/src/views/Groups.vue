<script setup lang="ts">
import { ref, onMounted } from 'vue'
import router from '../router'

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
</script>

<template>
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
