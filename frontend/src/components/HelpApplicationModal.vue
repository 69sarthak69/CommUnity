<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-container">
      <div class="modal-header">
        <h2>✉️ Apply to Help</h2>
        <button class="close-btn" @click="emit('close')">×</button>
      </div>
      <div class="modal-body">
        <p>Please write a short letter explaining why you're suitable to help with this task.</p>
        <textarea v-model="letter" placeholder="Write your letter here..." rows="6"></textarea>
        <button class="submit-btn" :disabled="loading" @click="submit">
          {{ loading ? 'Submitting...' : 'Submit Application' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
const props = defineProps<{ requestId: number | string }>()
const emit = defineEmits(['close', 'applied'])

const letter = ref('')
const isSubmitting = ref(false)

const submitApplication = async () => {
  if (!letter.value.trim()) {
    alert('Please write a short letter explaining your interest.')
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
      alert(data.message || 'Application submitted successfully.')
      emit('applied')
      emit('close')
    } else {
      alert(data.detail || 'Failed to apply.')
    }
  } catch (err) {
    console.error(err)
    alert('Something went wrong.')
  } finally {
    isSubmitting.value = false
  }
}
</script>


<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-container {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.modal-body textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  margin-bottom: 1rem;
}
.submit-btn {
  background-color: #2e7d32;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
}
.submit-btn:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}
</style>