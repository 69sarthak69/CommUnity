<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
const emit = defineEmits(['close'])

const router = useRouter()

const title = ref('')
const description = ref('')
const category = ref('')
const location = ref('')
const isEmergency = ref(false)
const lat = ref('')
const lng = ref('')
const categories = [
  { value: "food", label: "Food" },
  { value: "medical", label: "Medical Aid" },
  { value: "education", label: "Education" },
  { value: "emergency", label: "Emergency" },
  { value: "other", label: "Other" }
]

const isSubmitting = ref(false)

const handleSubmit = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('You must be logged in to create a help request.')
    return
  }
  const latitude = localStorage.getItem('user_lat')
  const longitude = localStorage.getItem('user_lng')

  if (!latitude || !longitude) {
    alert("Location not detected. Please allow location access on the home page first.");
    return
  }


  isSubmitting.value = true

  try {
    const response = await fetch('http://127.0.0.1:8000/api/help-requests/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: title.value,
        description: description.value,
        category: category.value,
        location: location.value,
        is_emergency: isEmergency.value,
        latitude: lat.value ? parseFloat(lat.value) : null,
        longitude: lng.value ? parseFloat(lng.value) : null  
      })
    })

    const responseData = await response.json()

    if (response.ok) {
      alert('Help request submitted successfully!')
      emit('close')  // close modal after submission
    } else {
      alert(`Error: ${JSON.stringify(responseData)}`)
    }
  } catch (error) {
    console.error('Error submitting help request:', error)
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  const storedLat = localStorage.getItem('user_lat');
  const storedLng = localStorage.getItem('user_lng');
  if (storedLat && storedLng) {
    lat.value = storedLat
    lng.value = storedLng
  } else {
    // Optional: Show an alert or ask user to allow location
    alert('Location not detected. Please allow location access on the home page first.');
  }
});
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-container">
      <div class="modal-header">
        <h2 class="form-title">Ask for Help</h2>
        <button class="close-btn" @click="emit('close')">×</button>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="title" class="form-label">Title</label>
          <input id="title" type="text" v-model="title" required class="form-input" placeholder="Brief title of your request" />
        </div>

        <div class="form-group">
          <label for="description" class="form-label">Description</label>
          <textarea id="description" v-model="description" required class="form-input" placeholder="Describe your need in detail"></textarea>
        </div>

        <div class="form-group">
          <label for="category" class="form-label">Category</label>
          <select id="category" v-model="category" required class="form-input">
            <option value="" disabled>Select a category</option>
            <option v-for="cat in categories" :key="cat.value" :value="cat.value">{{ cat.label }}</option>
          </select>
        </div>

        <div class="form-group">
          <label for="location" class="form-label">Location</label>
          <input id="location" type="text" v-model="location" required class="form-input" placeholder="Enter city name" />
          <input type="hidden" v-model="lat" />
            <input type="hidden" v-model="lng" />

        </div>

        <div class="form-group checkbox-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="isEmergency" /> Mark as Emergency 🚨
          </label>
        </div>

        <button type="submit" class="button-primary" :disabled="isSubmitting">
          {{ isSubmitting ? 'Submitting...' : 'Submit Request' }}
        </button>
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
  background: rgba(0, 0, 0, 0.4);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.modal-container {
  background: white;
  width: 100%;
  max-width: 600px;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  position: relative;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
  color: #999;
}

.form-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
}

.form-group {
  margin: 1rem 0;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: #f9fafb;
}

textarea.form-input {
  resize: vertical;
  min-height: 100px;
}

.button-primary {
  width: 100%;
  padding: 0.75rem 1rem;
  background-color: var(--primary, #10b981);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  margin-top: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.button-primary:hover {
  background-color: var(--primary-dark, #059669);
}

.checkbox-label {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
</style>
