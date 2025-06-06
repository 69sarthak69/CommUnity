<template>
  <div class="my-applications">
    <h2 class="mb-4 text-xl font-bold">📝 My Applications</h2>
    <ul v-if="myApplications.length">
      <li v-for="app in myApplications" :key="app.id" class="mb-3 p-3 rounded bg-white shadow flex justify-between items-center">
        <div>
          <strong>{{ app.help_request_title }}</strong>
          <p class="text-gray-600 text-sm">
            Applied: {{ formatDate(app.created_at) }}
          </p>
          <p class="text-gray-800 text-sm italic mt-1">"{{ app.letter }}"</p>
        </div>
        <div>
          <span
            v-if="app.status === 'approved'"
            class="px-3 py-1 rounded bg-green-100 text-green-700 font-bold"
          >✅ Approved</span>
          <span
            v-else-if="app.status === 'rejected'"
            class="px-3 py-1 rounded bg-red-100 text-red-700 font-bold"
          >❌ Rejected</span>
          <span
            v-else
            class="px-3 py-1 rounded bg-yellow-100 text-yellow-800 font-bold"
          >⏳ Pending</span>
        </div>
      </li>
    </ul>
    <div v-else class="text-gray-500 mt-8 text-center">
      You haven’t applied for any tasks yet.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const token = localStorage.getItem('access_token')
const myApplications = ref([])

const fetchMyApplications = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/my-applications/', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    const data = await res.json()
    myApplications.value = data
  } catch (err) {
    console.error("Failed to fetch my applications:", err)
  }
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString()
}

onMounted(() => {
  fetchMyApplications()
})
</script>

<style scoped>
.my-applications {
  max-width: 700px;
  margin: 40px auto 0;
  background: #f9fafb;
  border-radius: 12px;
  padding: 2rem;
}
.bg-white {
  background: white;
}
.shadow {
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}
.p-3 { padding: 1rem; }
.mb-3 { margin-bottom: 1rem; }
.rounded { border-radius: 10px; }
.text-gray-600 { color: #4b5563; }
.text-gray-800 { color: #1f2937; }
.text-gray-500 { color: #6b7280; }
.text-center { text-align: center; }
.text-xl { font-size: 1.25rem; }
.font-bold { font-weight: 700; }
.mb-4 { margin-bottom: 1rem; }
.mt-1 { margin-top: 0.25rem; }
.mt-8 { margin-top: 2rem; }
.flex { display: flex; }
.justify-between { justify-content: space-between; }
.items-center { align-items: center; }

.bg-green-100 { background: #d1fae5; }
.text-green-700 { color: #047857; }
.bg-red-100 { background: #fee2e2; }
.text-red-700 { color: #b91c1c; }
.bg-yellow-100 { background: #fef9c3; }
.text-yellow-800 { color: #92400e; }
.px-3 { padding-left: 1rem; padding-right: 1rem; }
.py-1 { padding-top: 0.25rem; padding-bottom: 0.25rem; }
</style>
