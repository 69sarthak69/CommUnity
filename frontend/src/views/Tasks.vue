<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'


const router = useRouter()


const activeFilter = ref('all')
const searchQuery = ref('')

const tasks = ref([
  {
    id: 1,
    title: 'Help with Grocery Shopping',
    description: 'Need assistance with weekly grocery shopping for an elderly couple',
    location: 'Downtown Area',
    urgency: 'Normal',
    status: 'Open',
    date: '2024-03-20',
    category: 'Shopping'
  },
  {
    id: 2,
    title: 'Emergency Medical Transport',
    description: 'Transport needed for medical appointment',
    location: 'North Side',
    urgency: 'High',
    status: 'In Progress',
    date: '2024-03-19',
    category: 'Transportation'
  },
  {
    id: 3,
    title: 'Garden Maintenance',
    description: 'Help needed with basic garden maintenance for disabled person',
    location: 'South Side',
    urgency: 'Low',
    status: 'Open',
    date: '2024-03-21',
    category: 'Maintenance'
  }
])

const filteredTasks = computed(() => {
  return tasks.value.filter(task => {
    const matchesFilter = activeFilter.value === 'all' || task.status.toLowerCase() === activeFilter.value
    const matchesSearch = 
      task.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      task.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    return matchesFilter && matchesSearch
  })
})
</script>

<template>
  <div class="container main-content">
    <aside class="sidebar">
      <router-link to="/" class="sidebar-link">Home</router-link>
      <router-link to="/tasks" class="sidebar-link">Tasks</router-link>
      <router-link to="/groups" class="sidebar-link">Groups</router-link>
      <router-link to="/events" class="sidebar-link">Events</router-link>
      <router-link to="/notifications" class="sidebar-link">Notifications</router-link>
      <router-link to="/donations" class="sidebar-link">🎁 Donations</router-link> <!-- NEW BUTTON -->
    </aside>

    <main class="feed">
      <div class="tasks-header">
        <h1 class="text-2xl font-bold">Community Tasks</h1>
        <button class="button-primary" @click="router.push('/post')">Create New Task</button>
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
          v-for="filter in ['all', 'open', 'in progress', 'completed']"
          :key="filter"
          :class="['filter-button', { active: activeFilter === filter }]"
          @click="activeFilter = filter"
        >
          {{ filter.charAt(0).toUpperCase() + filter.slice(1) }}
        </button>
      </div>

      <div v-for="task in filteredTasks" :key="task.id" class="post-card">
        <div class="post-header">
          <div class="post-author">
            <div class="author-info">
              <span class="author-name">{{ task.title }}</span>
              <span class="post-meta">{{ task.location }} • {{ task.date }}</span>
            </div>
          </div>
          <span
            :class="{
              'bg-green-100 text-green-800': task.status === 'Open',
              'bg-blue-100 text-blue-800': task.status === 'In Progress',
              'bg-gray-100 text-gray-800': task.status === 'Completed'
            }"
            class="px-2 py-1 rounded-full text-sm"
          >
            {{ task.status }}
          </span>
        </div>

        <div class="post-content">
          {{ task.description }}
        </div>

        <div class="post-actions">
          <span class="text-sm text-gray-600">Category: {{ task.category }}</span>
          <span
            :class="{
              'text-red-600': task.urgency === 'High',
              'text-yellow-600': task.urgency === 'Normal',
              'text-green-600': task.urgency === 'Low'
            }"
            class="text-sm"
          >
            Urgency: {{ task.urgency }}
          </span>
          <button class="button-primary" v-if="task.status === 'Open'">
            Volunteer
          </button>
        </div>
      </div>
    </main>
  </div>
</template>