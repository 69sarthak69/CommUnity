<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const tasks = ref([
  { id: 1, title: 'Help with Grocery Shopping', status: 'Open', urgency: 'Normal' },
  { id: 2, title: 'Emergency Medical Transport', status: 'In Progress', urgency: 'High' },
  { id: 3, title: 'Garden Maintenance', status: 'Open', urgency: 'Low' }
])
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <header class="bg-white shadow">
      <nav class="container mx-auto px-6 py-4">
        <div class="flex justify-between items-center">
          <h1 class="text-2xl font-bold text-gray-800">Dashboard</h1>
          <button @click="router.push('/')" class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
            Logout
          </button>
        </div>
      </nav>
    </header>

    <main class="container mx-auto px-6 py-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Tasks Overview -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h2 class="text-xl font-semibold mb-4">Recent Tasks</h2>
          <div class="space-y-4">
            <div v-for="task in tasks" :key="task.id" class="border-b pb-4">
              <h3 class="font-medium">{{ task.title }}</h3>
              <div class="flex justify-between mt-2">
                <span :class="{
                  'text-green-600': task.status === 'Open',
                  'text-blue-600': task.status === 'In Progress'
                }">{{ task.status }}</span>
                <span :class="{
                  'text-red-600': task.urgency === 'High',
                  'text-yellow-600': task.urgency === 'Normal',
                  'text-green-600': task.urgency === 'Low'
                }">{{ task.urgency }}</span>
              </div>
            </div>
          </div>
          <button
            @click="router.push('/tasks')"
            class="mt-4 w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            View All Tasks
          </button>
        </div>

        <!-- Statistics -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h2 class="text-xl font-semibold mb-4">Your Impact</h2>
          <div class="space-y-4">
            <div class="flex justify-between">
              <span>Tasks Completed</span>
              <span class="font-semibold">12</span>
            </div>
            <div class="flex justify-between">
              <span>Hours Contributed</span>
              <span class="font-semibold">24</span>
            </div>
            <div class="flex justify-between">
              <span>People Helped</span>
              <span class="font-semibold">8</span>
            </div>
          </div>
        </div>

        <!-- Upcoming Tasks -->
        <div class="bg-white p-6 rounded-lg shadow">
          <h2 class="text-xl font-semibold mb-4">Upcoming Tasks</h2>
          <div class="space-y-4">
            <p class="text-gray-600">No upcoming tasks scheduled</p>
            <button
              class="w-full px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >
              Find Tasks Near You
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>