<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// ✅ Form Fields
const title = ref('')
const description = ref('')
const location = ref('')
const date = ref('')
const isSubmitting = ref(false)
const category = ref('')

const categories = [
  'Education',
  'Emergency',
  'Elderly Care',
  'Health',
  'Environment',
  'Others'
]


const handleSubmit = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert('You must be logged in to create an event.')
    return
  }

  isSubmitting.value = true

  try {
    const res = await fetch('http://127.0.0.1:8000/api/events/', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: title.value,
        description: description.value,
        location: location.value,
        date: date.value
      })
    })

    if (res.ok) {
      alert('Event created successfully!')
      router.push('/events')
    } else {
      const errorText = await res.text()
      alert(`Failed to create event: ${errorText}`)
    }
  } catch (err) {
    console.error('Create error:', err)
    alert('Something went wrong.')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="form-container">
    <h2 class="form-title">📅 Create New Event</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="title">Title</label>
        <input id="title" v-model="title" type="text" required class="form-input" placeholder="Event title" />
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea id="description" v-model="description" required class="form-input" placeholder="Details..."></textarea>
      </div>

      <div class="form-group">
        <label for="location">Location</label>
        <input id="location" v-model="location" type="text" required class="form-input" placeholder="e.g. Community Hall" />
      </div>

      <div class="form-group">
        <label for="category">Category</label>
        <select id="category" v-model="category" required class="form-input">
          <option value="" disabled>Select a category</option>
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>
    
      <div class="form-group">
        <label for="date">Event Date</label>
        <input id="date" v-model="date" type="date" required class="form-input" />
      </div>

      <button class="button-primary" type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Creating...' : 'Create Event' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.form-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}
.form-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
}
.form-group {
  margin-bottom: 1rem;
}
.form-input {
  width: 100%;
  padding: 0.5rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 1rem;
}
</style>
