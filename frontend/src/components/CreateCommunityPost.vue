<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Form fields
const title = ref('')
const content = ref('')
const category = ref('')
const location = ref('')
const image = ref(null)

const categories = [
  { value: "general", label: "General" },
  { value: "event", label: "Event" },
  { value: "alert", label: "Alert" },
  { value: "lost_found", label: "Lost & Found" },
  { value: "recommendation", label: "Recommendation" }
]

const isSubmitting = ref(false)

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
        // Do NOT add Content-Type here – let FormData handle it
      },
      body: formData
    })

    if (res.ok) {
      const data = await res.json()
      alert('Post created successfully!')
      router.push('/home')
    } else {
      const errorText = await res.text()  // 👈 Only use this once
      console.error('Post error response:', errorText)
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
  <div class="form-container">
    <h2 class="form-title">📣 Create Community Post</h2>
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
</template>
