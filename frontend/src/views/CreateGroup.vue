<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const name = ref('')
const description = ref('')
const category = ref('')
const isSubmitting = ref(false)

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
      body: JSON.stringify({
        name: name.value,
        description: description.value,
        category: category.value
      })
    })

    const data = await res.json()

    if (res.ok) {
      alert('Group created successfully!')
      router.push('/groups')
    } else {
      console.error('Create error:', data)
      alert('Failed to create group.')
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
  <div class="form-container">
    <h2 class="form-title">➕ Create a New Group</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="name">Group Name</label>
        <input id="name" v-model="name" type="text" required class="form-input" placeholder="Enter group name" />
      </div>

      <div class="form-group">
        <label for="category">Category</label>
        <select id="category" v-model="category" required class="form-input">
          <option value="" disabled>Select a category</option>
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea id="description" v-model="description" required class="form-input" placeholder="Group purpose..."></textarea>
      </div>

      <button type="submit" class="button-primary" :disabled="isSubmitting">
        {{ isSubmitting ? 'Creating...' : 'Create Group' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.form-container {
  max-width: 600px;
  margin: 2rem auto;
  background: #fff;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
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
  border: 1px solid #ddd;
  font-size: 1rem;
}
</style>
