<template>
  <div class="comment">
    <p><strong>{{ comment.username }}</strong>: {{ comment.text }}</p>
    <small>{{ new Date(comment.created_at).toLocaleString() }}</small>

    <!-- Reply Input -->
    <div v-if="showReplyBox" class="mt-1">
      <input v-model="replyText" class="form-input" placeholder="Write a reply..." />
      <button @click="submitReply" class="btn btn-primary btn-sm mt-1">Reply</button>
    </div>
    <button @click="showReplyBox = !showReplyBox" class="btn-link text-sm text-blue-500">
      {{ showReplyBox ? 'Cancel' : 'Reply' }}
    </button>

    <!-- Recursive Replies -->
    <div class="ml-4 mt-2" v-if="comment.replies && comment.replies.length > 0">
      <CommentItem
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        :post-id="postId"
        @replied="emit('replied')"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CommentItem from './CommentItem.vue'

const props = defineProps<{
  comment: Comment
  postId: number
}>()

const emit = defineEmits(['replied'])

const replyText = ref('')
const showReplyBox = ref(false)

const submitReply = async () => {
  const token = localStorage.getItem('access_token')
  const userId = localStorage.getItem('user_id')
  if (!token || !replyText.value.trim()) return

  await fetch('http://127.0.0.1:8000/api/comments/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      post: props.postId,
      text: replyText.value,
      parent: props.comment.id,
      user: userId,
    }),
  })

  replyText.value = ''
  showReplyBox.value = false
  emit('replied')
}
</script>

<style scoped>
.comment {
  margin-bottom: 1rem;
  background-color: #f9f9f9;
  padding: 0.75rem;
  border-radius: 8px;
}
</style>
