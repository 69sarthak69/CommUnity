<template>
  <div class="applications-modal-overlay" @click.self="closeModal">
    <div class="applications-modal">
      <div class="modal-header">
        <h2>📝 My Applications</h2>
        <button class="close-btn" @click="closeModal">×</button>
      </div>
      
      <div class="modal-content">
        <ul v-if="myApplications.length" class="applications-list">
          <li v-for="app in myApplications" :key="app.id" class="application-item">
            <div class="application-content">
              <h3>{{ app.help_request_title }}</h3>
              <p class="application-meta">
                Applied: {{ formatDate(app.created_at) }}
              </p>
              <p class="application-letter">"{{ app.letter }}"</p>
            </div>
            <div class="application-status">
              <span
                v-if="app.status === 'approved'"
                class="status-badge approved"
              >✅ Approved</span>
              <span
                v-else-if="app.status === 'rejected'"
                class="status-badge rejected"
              >❌ Rejected</span>
              <span
                v-else
                class="status-badge pending"
              >⏳ Pending</span>
            </div>
          </li>
        </ul>
        <div v-else class="empty-state">
          You haven't applied for any tasks yet.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['close'])

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

const closeModal = () => {
  emit('close')
}

onMounted(() => {
  fetchMyApplications()
})
</script>

<style scoped>
.applications-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.applications-modal {
  background: white;
  width: 100%;
  max-width: 600px;
  max-height: 80vh;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem;
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748b;
  padding: 0.25rem;
}

.modal-content {
  padding: 1.5rem;
  overflow-y: auto;
}

.applications-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.application-item {
  padding: 1rem;
  margin-bottom: 1rem;
  background: #f9fafb;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.application-content h3 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
}

.application-meta {
  font-size: 0.875rem;
  color: #64748b;
  margin: 0 0 0.5rem;
}

.application-letter {
  font-size: 0.875rem;
  color: #334155;
  font-style: italic;
  margin: 0;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.approved {
  background: #d1fae5;
  color: #047857;
}

.status-badge.rejected {
  background: #fee2e2;
  color: #b91c1c;
}

.status-badge.pending {
  background: #fef9c3;
  color: #92400e;
}

.empty-state {
  text-align: center;
  color: #64748b;
  padding: 2rem 0;
}
</style>