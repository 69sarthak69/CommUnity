<template>
  <div class="group-posts-container">
    <h2 class="text-xl font-semibold mb-4">📣 Group Posts</h2>

    <!-- Post Form -->
    <form @submit.prevent="createPost" class="post-form">
      <div class="form-group">
        <label>Content</label>
        <textarea
          v-model="newPost"
          required
          placeholder="Write your message..."
          class="form-input"
          rows="3"
        ></textarea>
      </div>

      <div class="form-group">
        <label>Upload Image (optional)</label>
        <input type="file" accept="image/*" @change="handleImageUpload" class="form-file-input" />
      </div>

      <button type="submit" class="button-primary" :disabled="isSubmitting">
        {{ isSubmitting ? 'Posting...' : 'Post' }}
      </button>
    </form>

    <!-- Posts List -->
    <div v-for="post in posts" :key="post.id" class="post-item" :class="{ pinned: post.is_pinned }">
      <p class="post-meta">
        <strong>{{ post.author_name }}</strong> • {{ formatDate(post.created_at) }}
      </p>
      <p class="post-content">{{ post.content }}</p>
      <img
        v-if="post.image"
        :src="fixMediaUrl(post.image)"
        class="post-image"
        alt="Post image"
      />
      <div class="post-actions">
        <button
          @click="toggleLike(post)"
          class="post-action-btn"
          :class="{ liked: post.user_liked }"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m0-2V9a2 2 0 012-2h1.5l3.5-4.5A2 2 0 0116.5 4v1.333L14 10z"
            />
          </svg>
          {{ post.like_count }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../utils/axiosInstance'

const props = defineProps({ groupId: Number })

const posts = ref([])
const newPost = ref('')
const image = ref(null)
const isSubmitting = ref(false)

const toggleLike = async (post) => {
  await axios.post(`/groups/group-posts/${post.id}/like/`)
  fetchPosts()
}

const fetchPosts = async () => {
  const res = await axios.get(`/groups/group-posts/?group=${props.groupId}`)
  posts.value = res.data
}

const handleImageUpload = (e) => {
  image.value = e.target.files[0]
}

const createPost = async () => {
  if (!newPost.value.trim()) return

  const formData = new FormData()
  formData.append('group', props.groupId)
  formData.append('content', newPost.value)
  if (image.value) {
    formData.append('image', image.value)
  }

  isSubmitting.value = true
  try {
    await axios.post('/groups/group-posts/', formData)
    newPost.value = ''
    image.value = null
    fetchPosts()
  } catch (err) {
    alert('Failed to post')
    console.error(err)
  } finally {
    isSubmitting.value = false
  }
}

const formatDate = (dt) => new Date(dt).toLocaleString()
const fixMediaUrl = (url) => {
  if (url && !url.startsWith('http')) {
    return 'http://127.0.0.1:8000' + url
  }
  return url
}

onMounted(fetchPosts)
</script>

<style scoped>
.group-posts-container {
  background: #ffffff;
  border-radius: 0.75rem;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  max-width: 800px;
  margin: 0 auto;
}

.post-form {
  background: #f9fafb;
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background: #ffffff;
  resize: vertical;
  min-height: 120px;
  font-size: 0.875rem;
  color: #1f2937;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-file-input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  background: #ffffff;
  font-size: 0.875rem;
  color: #4b5563;
}

.form-file-input:focus {
  outline: none;
  border-color: #3b82f6;
}

.button-primary {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
}

.button-primary:hover {
  background-color: #059669;
  transform: translateY(-1px);
}

.button-primary:disabled {
  background-color: #6b7280;
  cursor: not-allowed;
  transform: none;
}

.post-item {
  background-color: #f9fafb;
  padding: 1.25rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  border-left: 4px solid #10b981;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  animation: fadeIn 0.3s ease-in;
}

.post-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
}

.post-item.pinned {
  background-color: #eff6ff;
  border-left-color: #3b82f6;
}

.post-item.pinned::before {
  content: "📌 Pinned";
  font-size: 0.75rem;
  color: #3b82f6;
  margin-bottom: 0.5rem;
  display: block;
}

.post-meta {
  font-size: 0.85rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.post-meta strong {
  color: #1f2937;
}

.post-content {
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 0.75rem;
}

.post-image {
  max-width: 100%;
  width: 300px;
  border-radius: 0.5rem;
  margin-top: 0.75rem;
  object-fit: cover;
}

.post-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.75rem;
}

.post-action-btn {
  background-color: transparent;
  border: 1px solid #d1d5db;
  color: #3b82f6;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.post-action-btn:hover {
  background-color: #eff6ff;
  border-color: #bfdbfe;
}

.post-action-btn.liked {
  background-color: #eff6ff;
  border-color: #3b82f6;
  color: #3b82f6;
  font-weight: 600;
}

.post-action-btn svg {
  width: 16px;
  height: 16px;
}

@media (max-width: 768px) {
  .group-posts-container {
    padding: 1.5rem;
  }

  .post-form {
    padding: 1rem;
  }

  .post-item {
    padding: 1rem;
  }

  .post-image {
    width: 100%;
  }

  .post-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.25rem;
  }

  .post-actions {
    flex-direction: column;
    gap: 0.5rem;
  }

  .button-primary {
    padding: 0.75rem;
  }

  .form-input {
    font-size: 0.875rem;
    min-height: 100px;
  }
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
</style>