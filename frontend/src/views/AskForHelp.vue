<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ✅ Form fields for creating a help request (Matching Django Model)
const title = ref('')
const description = ref('')
const category = ref('')
const location = ref('')
const isEmergency = ref(false)  // Boolean for emergency status

const categories = [
  { value: "food", label: "Food" },
  { value: "medical", label: "Medical Aid" },
  { value: "education", label: "Education" },
  { value: "emergency", label: "Emergency" },
  { value: "other", label: "Other" }
]

const isSubmitting = ref(false)  // Prevent multiple submissions

// ✅ Function to Submit Help Request to Django API
const handleSubmit = async () => {
  const token = localStorage.getItem('access_token')  
  if (!token) {
    alert('You must be logged in to create a help request.')
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
        category: category.value,  // ✅ Matches Django Choices
        location: location.value,  // ✅ Stores city name only
        is_emergency: isEmergency.value  // ✅ Boolean for emergency status
      })
    })

    const responseData = await response.json()
    console.log('API Response:', responseData)

    if (response.ok) {
      alert('Help request submitted successfully!')
      router.push('/home')  // Redirect to Home page
    } else {
      console.error('Failed to submit help request:', responseData)
      alert(`Error: ${JSON.stringify(responseData)}`)  // Show error message
    }
  } catch (error) {
    console.error('Error submitting help request:', error)
  } finally {
    isSubmitting.value = false  
  }
}
</script>

<template>
  <div class="form-container">
    <h2 class="form-title">Ask for Help</h2>
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
      </div>

      <div class="form-group checkbox-group">
        <label class="checkbox-label">
          <input type="checkbox" v-model="isEmergency" /> Mark as Emergency 🚨
        </label>
      </div>

      <button type="submit" class="button-primary" style="width: 100%" :disabled="isSubmitting">
        {{ isSubmitting ? 'Submitting...' : 'Submit Request' }}
      </button>
    </form>
  </div>
</template>
