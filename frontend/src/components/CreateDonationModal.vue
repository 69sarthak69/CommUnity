<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

const emit = defineEmits(['close', 'submitted']);
const form = ref({
  title: '',
  description: '',
  target_amount: null as number | null,
  location: '',
});
const error = ref<string | null>(null);
const loading = ref(false);

const submit = async () => {
  if (!form.value.title || !form.value.description || !form.value.target_amount || !form.value.location) {
    error.value = 'Please fill all fields';
    return;
  }

  try {
    loading.value = true;
    const token = localStorage.getItem('access_token');
    await axios.post(
      'http://localhost:8000/api/donation/',
      form.value,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    );

    emit('submitted');
    emit('close');
  } catch (err) {
    error.value = 'Failed to create campaign';
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="modal">
    <div class="modal-content">
      <button class="close-button" @click="emit('close')">
        &times;
      </button>
      <h2>Create Donation Campaign</h2>
      <input v-model="form.title" placeholder="Campaign Title" />
      <textarea v-model="form.description" placeholder="Description"></textarea>
      <input v-model.number="form.target_amount" type="number" placeholder="Target Amount (Rs.)" min="1" />
      <input v-model="form.location" placeholder="Location" />
      <p v-if="error" class="error">{{ error }}</p>
      <div class="button-group">
        <button :disabled="loading" class="button-primary" @click="submit">
          {{ loading ? 'Creating...' : 'Create Campaign' }}
        </button>
        <button class="button-secondary" @click="emit('close')">Cancel</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  position: relative;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.close-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0.25rem;
  line-height: 1;
}

.close-button:hover {
  color: #333;
}

h2 {
  margin-top: 0.5rem;
  margin-bottom: 1.5rem;
  color: #2c3e50;
  text-align: center;
}

input, textarea {
  width: 100%;
  padding: 0.75rem;
  margin: 0.75rem 0;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

textarea {
  height: 120px;
  resize: vertical;
}

.error {
  color: #e74c3c;
  margin: 1rem 0;
  text-align: center;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.button-primary, .button-secondary {
  flex: 1;
  padding: 0.75rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.button-primary {
  background-color: #42b983;
  color: white;
  border: none;
}

.button-primary:hover:not(:disabled) {
  background-color: #3aa876;
}

.button-primary:disabled {
  background-color: #a0d9bb;
  cursor: not-allowed;
}

.button-secondary {
  background-color: white;
  color: #666;
  border: 1px solid #ddd;
}

.button-secondary:hover {
  background-color: #f5f5f5;
  border-color: #ccc;
}

@media (max-width: 480px) {
  .button-group {
    flex-direction: column;
  }
  
  .modal-content {
    padding: 1.5rem;
  }
}
</style>