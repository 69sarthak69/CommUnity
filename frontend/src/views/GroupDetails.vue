<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import GroupChat from '../components/GroupChat.vue'

const route = useRoute()
const router = useRouter()
const groupId = route.params.id

const group = ref<any>(null)
const isLoading = ref(true)

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

const joinGroup = async () => {
  if (!token) {
    alert('You must be logged in to join a group.')
    return
  }

  try {
    const res = await fetch(`http://127.0.0.1:8000/api/groups/${groupId}/join/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
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

const deleteGroup = async () => {
  const confirmDelete = confirm('Are you sure you want to delete this group?')
  if (!confirmDelete) return

  try {
    const res = await fetch(`http://127.0.0.1:8000/api/groups/${groupId}/`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (res.ok) {
      alert('Group deleted.')
      router.push('/groups')
    } else {
      const err = await res.text()
      alert('Failed to delete: ' + err)
    }
  } catch (err) {
    console.error('Delete error:', err)
  }
}

onMounted(fetchGroup)
</script>

<template>
  <div class="container main-content flex">
    <aside class="sidebar mr-8">
      <router-link to="/home" class="sidebar-link">Home</router-link>
      <router-link to="/groups" class="sidebar-link">Groups</router-link>
      <router-link to="/events" class="sidebar-link">Events</router-link>
      <router-link to="/notifications" class="sidebar-link">Notifications</router-link>
      <router-link to="/donations" class="sidebar-link">🎁 Donations</router-link>
    </aside>

    <div class="flex-1">
      <div v-if="isLoading">Loading group...</div>

      <div v-else-if="group">
        <h1 class="text-3xl font-bold">{{ group.name }}</h1>
        <p class="mt-2 text-gray-600">{{ group.description }}</p>
        <p class="text-sm text-gray-500 mt-1">Category: {{ group.category }}</p>
        <p class="text-sm text-gray-500 mt-1">Members: {{ group.member_count }}</p>

        <!-- Admin Controls -->
        <div v-if="currentUserId === group.created_by" class="mt-4">
          <button class="button-primary mr-2" @click="router.push(`/groups/edit/${group.id}`)">✏️ Edit Group</button>
          <button class="button-secondary" @click="deleteGroup">🗑️ Delete Group</button>
        </div>

        <!-- Join Button -->
        <div v-else-if="!group.members.includes(currentUserId)" class="mt-4">
          <button class="button-primary" @click="joinGroup">➕ Join Group</button>
        </div>

        <!-- ✅ Chatbox for group members -->
        <div v-else class="mt-8">
          <GroupChat :userId="currentUserId" roomType="group" :roomId="group.id" />
        </div>
      </div>

      <div v-else>
        <p>Group not found.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sidebar-link {
  display: block;
  padding: 0.5rem 1rem;
  margin-bottom: 0.5rem;
  background: #f4f4f4;
  border-radius: 8px;
  text-decoration: none;
  color: #333;
}
.sidebar-link:hover {
  background: #e2e2e2;
}

.button-primary {
  background-color: #10b981;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}
.button-primary:hover {
  background-color: #059669;
}

.button-secondary {
  background-color: #ef4444;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}
.button-secondary:hover {
  background-color: #dc2626;
}
</style>
