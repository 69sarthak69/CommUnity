<!-- src/components/ProfileModal.vue -->
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const emit = defineEmits(['close'])

const user = ref({
  email: localStorage.getItem('user_email') || '',
  username: localStorage.getItem('user_username') || ''
})

const handleLogout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_email')
  localStorage.removeItem('user_username')
  localStorage.removeItem('user_id')
  emit('close')
  router.push('/')
}

const goToFullProfile = () => {
  emit('close')
  router.push('/profile')
}
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-container">
      <div class="modal-header">
        <h3 class="modal-title">User Profile</h3>
        <button class="close-btn" @click="emit('close')">
          &times;
        </button>
      </div>
      
      <div class="modal-body">
        <div class="profile-summary">
          <div class="avatar">
            {{ user.username.charAt(0).toUpperCase() }}
          </div>
          <h4>{{ user.username }}</h4>
          <p>{{ user.email }}</p>
        </div>
        
        <div class="profile-actions">
          <button class="btn primary" @click="goToFullProfile">
            View Full Profile
          </button>
          <button class="btn secondary" @click="handleLogout">
            Logout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
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
  z-index: 1000;
}

.modal-container {
  background: white;
  width: 90%;
  max-width: 400px;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  animation: modalFadeIn 0.3s ease-out;
}

.modal-header {
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, #059669, #0dd495);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  margin: 0;
  font-size: 1.2rem;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.25rem;
}

.modal-body {
  padding: 1.5rem;
}

.profile-summary {
  text-align: center;
  margin-bottom: 1.5rem;
}

.avatar {
  width: 60px;
  height: 60px;
  background-color: #059669;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0 auto 1rem;
}

.profile-summary h4 {
  margin: 0.5rem 0 0.25rem;
  font-size: 1.1rem;
}

.profile-summary p {
  margin: 0;
  color: #64748b;
}

.profile-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.75rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  width: 100%;
}

.btn.primary {
  background-color: #10b981;
  color: white;
}

.btn.primary:hover {
  background-color: #059669;
}

.btn.secondary {
  background-color: #f1f5f9;
  color: #334155;
  border: 1px solid #e2e8f0;
}

.btn.secondary:hover {
  background-color: #e2e8f0;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>