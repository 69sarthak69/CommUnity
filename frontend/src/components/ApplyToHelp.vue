<script setup lang="ts">
import { ref, onMounted } from 'vue'

const props = defineProps<{ requestId: number }>()
const emit = defineEmits(['close', 'applied', 'toast'])

const letter = ref('')
const isSubmitting = ref(false)

const submitApplication = async () => {
  if (!letter.value.trim()) {
    emit('toast', 'Please write a short letter explaining your interest.', 'error')
    return
  }
  isSubmitting.value = true
  try {
    const res = await fetch(`http://127.0.0.1:8000/api/help-requests/${props.requestId}/apply/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({ letter: letter.value })
    })

    const data = await res.json()
    if (res.ok) {
      emit('toast', data.message || 'Application submitted successfully!', 'success')
      emit('applied')
      emit('close')
    } else {
      emit('toast', data.detail || 'Failed to apply.', 'error')
    }
  } catch (err) {
    console.error(err)
    emit('toast', 'Something went wrong.', 'error')
  } finally {
    isSubmitting.value = false
  }
}

const closeModal = () => {
  if (!isSubmitting.value) {
    emit('close')
  }
}

onMounted(() => {
  console.log('ApplyToHelpModal received requestId:', props.requestId)
})
</script>

<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-container">
      <div class="modal-header">
        <h2 class="modal-title">Apply to Help</h2>
        <p class="modal-subtitle">Share why you'd be great for this task</p>
        <button class="close-btn" @click="closeModal" :disabled="isSubmitting">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="submitApplication" class="application-form">
          <div class="form-group">
            <label class="form-label">Your Message</label>
            <textarea
              v-model="letter"
              class="form-input form-textarea"
              rows="5"
              placeholder="I'd love to help because..."
              :disabled="isSubmitting"
            ></textarea>
            <div class="form-hint">This will be sent to the task creator</div>
          </div>
          <div class="btn-group">
            <button
              type="button"
              class="btn btn-secondary"
              @click="closeModal"
              :disabled="isSubmitting"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="isSubmitting"
            >
              <span v-if="isSubmitting" class="spinner"></span>
              <span v-else>Send Application</span>
            </button>
          </div>
        </form>
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
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
}

.modal-subtitle {
  font-size: 0.875rem;
  margin: 0.5rem 0 0;
  opacity: 0.9;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
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

.close-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.modal-body {
  padding: 2rem;
}

.application-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
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

.form-hint {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-top: 6px;
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
  flex: 1;
}

.btn-primary {
  background-color: #10b981;
  color: white;
}

.btn-primary:hover {
  background-color: #059669;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: white;
  color: #374151;
  border: 1px solid #e5e7eb;
}

.btn-secondary:hover {
  background-color: #f3f4f6;
}

.btn-secondary:disabled {
  background: #f1f5f9;
  color: #94a3b8;
  cursor: not-allowed;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
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
</style>