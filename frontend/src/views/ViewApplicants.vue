<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const helpRequestId = route.params.id
const applicants = ref([])
const isLoading = ref(true)

const fetchApplicants = async () => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/help-requests/${helpRequestId}/applications/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })

    if (res.ok) {
      applicants.value = await res.json()
    } else {
      console.error('Failed to fetch applicants')
    }
  } catch (error) {
    console.error('Error fetching applicants:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchApplicants()
})
</script>

<template>
  <div class="applicants-container">
    <h2>👥 Applicants for this Task</h2>

    <div v-if="isLoading">Loading...</div>

    <div v-else-if="applicants.length === 0">
      <p>No one has applied yet.</p>
    </div>

    <ul v-else class="applicants-list">
      <li v-for="app in applicants" :key="app.id" class="applicant-item">
        <h3>{{ app.user_name }}</h3>
        <p><strong>Letter:</strong></p>
        <p>{{ app.letter }}</p>
        <p class="timestamp">🕓 {{ new Date(app.created_at).toLocaleString() }}</p>
      </li>
    </ul>

    <div style="text-align: center; margin-top: 24px">
      <button @click="router.push('/home')" class="back-btn">⬅ Back to Home</button>
    </div>
  </div>
</template>

<style scoped>
.applicants-container {
  max-width: 700px;
  margin: 50px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
}

.applicants-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.applicant-item {
  background-color: #f1f1f1;
  padding: 16px;
  border-radius: 10px;
}

.timestamp {
  font-size: 13px;
  color: gray;
  margin-top: 8px;
}

.back-btn {
  padding: 10px 20px;
  font-size: 15px;
  background-color: #5c2d91;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.back-btn:hover {
  background-color: #4a1c7c;
}
</style>
