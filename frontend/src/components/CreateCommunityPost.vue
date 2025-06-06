<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const emit = defineEmits(['close'])

const router = useRouter()

const title = ref('')
const content = ref('')
const category = ref('')
const location = ref('')
const image = ref(null)
const isSubmitting = ref(false)

const categories = [
  { value: "general", label: "General" },
  { value: "event", label: "Event" },
  { value: "alert", label: "Alert" },
  { value: "lost_found", label: "Lost & Found" },
  { value: "recommendation", label: "Recommendation" }
]

const handleImageUpload = (e) => {
  image.value = e.target.files[0]
}

const handleSubmit = async () => {
  const token = localStorage.getItem('access_token')
  if (!token) {
    alert("You must be logged in to post.")
    return
  }

  isSubmitting.value = true

  const formData = new FormData()
  formData.append('title', title.value)
  formData.append('content', content.value)
  formData.append('category', category.value)
  formData.append('location', location.value)
  if (image.value) formData.append('image', image.value)

  try {
    const res = await fetch('http://127.0.0.1:8000/api/community-posts/create/', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      },
      body: formData
    })

    if (res.ok) {
      const data = await res.json()
      alert('Post created successfully!')
      emit('close')  //  Close modal on success
    } else {
      const errorText = await res.text()
      console.error('Post error:', errorText)
      alert(`Post failed: ${res.status}`)
    }
  } catch (error) {
    console.error('Error creating post:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>
<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-container">
      <div class="modal-header">
        <h2 class="form-title">📣 Create Community Post</h2>
        <button class="close-btn" @click="emit('close')">×</button>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Title</label>
          <input type="text" v-model="title" required class="form-input" placeholder="Your post title" />
        </div>

        <div class="form-group">
          <label>Content</label>
          <textarea v-model="content" required class="form-input" placeholder="What's going on?"></textarea>
        </div>

        <div class="form-group">
          <label>Category</label>
          <select v-model="category" required class="form-input">
            <option value="" disabled>Select category</option>
            <option v-for="cat in categories" :key="cat.value" :value="cat.value">{{ cat.label }}</option>
          </select>
        </div>

        <div class="form-group">
          <label>Location</label>
          <input type="text" v-model="location" required class="form-input" placeholder="E.g. Kathmandu" />
        </div>

        <div class="form-group">
          <label>Upload Image (optional)</label>
          <input type="file" accept="image/*" @change="handleImageUpload" />
        </div>

        <button type="submit" class="button-primary" :disabled="isSubmitting">
          {{ isSubmitting ? 'Posting...' : 'Post' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  right: 0; bottom: 0;
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
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
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

.form-group {
  margin: 1rem 0;
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
}

.button-primary:hover {
  background-color: var(--primary-dark, #059669);
}
</style>
