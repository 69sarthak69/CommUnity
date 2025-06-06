<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['close', 'created'])

const props = defineProps({
  userId: {
    type: Number,
    required: true
  }
})

const newGroup = ref({
  name: '',
  description: '',
  category: '',
  created_by: props.userId
})

const categories = [
  'Education',
  'Emergency',
  'Elderly Care',
  'Health',
  'Environment',
  'Others'
]

const isSubmitting = ref(false)

const handleSubmit = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('You must be logged in to create a group.')
    return
  }

  isSubmitting.value = true

  try {
    const res = await fetch('http://127.0.0.1:8000/api/groups/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newGroup.value)
    })

    if (res.ok) {
      emit('created')
      emit('close')
    } else {
      const errorText = await res.text()
      alert(`Failed to create group: ${errorText}`)
    }
  } catch (err) {
    console.error('Network error:', err)
    alert('Something went wrong.')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <button class="close-button" @click="$emit('close')">&times;</button>
      <h2 class="modal-title">👥 Create New Group</h2>
      
      <form @submit.prevent="handleSubmit" class="modal-form">
        <div class="form-group">
          <label>Group Name</label>
          <input 
            v-model="newGroup.name" 
            type="text" 
            required 
            placeholder="Enter group name" 
          />
        </div>

        <div class="form-group">
          <label>Category</label>
          <select v-model="newGroup.category" required>
            <option value="" disabled>Select a category</option>
            <option v-for="cat in categories" :key="cat" :value="cat">
              {{ cat }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>Description</label>
          <textarea 
            v-model="newGroup.description" 
            required 
            placeholder="Group purpose..."
          ></textarea>
        </div>

        <div class="form-actions">
          <button type="button" class="button-cancel" @click="$emit('close')">
            Cancel
          </button>
          <button type="submit" class="button-submit" :disabled="isSubmitting">
            {{ isSubmitting ? 'Creating...' : 'Create Group' }}
          </button>
        </div>
      </form>
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
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  padding: 2rem;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.5rem;
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
}

.close-button:hover {
  color: #333;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #2E7D32;
}

.modal-form .form-group {
  margin-bottom: 1.25rem;
}

.modal-form label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #444;
}

.modal-form input,
.modal-form textarea,
.modal-form select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.modal-form input:focus,
.modal-form textarea:focus,
.modal-form select:focus {
  outline: none;
  border-color: #4CAF50;
}

.modal-form textarea {
  min-height: 100px;
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.button-cancel {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: 1px solid #ddd;
  background: white;
  color: #666;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.button-cancel:hover {
  background: #f5f5f5;
}

.button-submit {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: none;
  background-color: #2E7D32;
  color: white;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s;
}

.button-submit:hover {
  background-color: #1B5E20;
}

.button-submit:disabled {
  background-color: #81C784;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    padding: 1.5rem;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .button-cancel,
  .button-submit {
    width: 100%;
  }
}
</style>