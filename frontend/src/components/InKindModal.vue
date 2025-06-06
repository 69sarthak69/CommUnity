<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['close', 'submit'])

const item = ref('')
const description = ref('')
const location = ref('')
const drop_off_date = ref('')

const submit = () => {
  if (!item.value || !description.value || !location.value || !drop_off_date.value) {
    alert('Please fill in all fields.')
    return
  }
  emit('submit', {
    item: item.value,
    description: description.value,
    location: location.value,
    drop_off_date: drop_off_date.value,
  })
  item.value = ''
  description.value = ''
  location.value = ''
  drop_off_date.value = ''
}
</script>

<template>
  <div class="modal-overlay">
    <div class="modal">
      <h2>Create In-Kind Donation</h2>
      <form @submit.prevent="submit">
        <div class="form-group">
          <label for="item">Item</label>
          <input v-model="item" id="item" type="text" placeholder="Item Name" required />
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea v-model="description" id="description" placeholder="Item Description" required></textarea>
        </div>
        <div class="form-group">
          <label for="location">Location</label>
          <input v-model="location" id="location" type="text" placeholder="Location" required />
        </div>
        <div class="form-group">
          <label for="drop_off_date">Drop-off Date</label>
          <input v-model="drop_off_date" id="drop_off_date" type="date" required />
        </div>
        <div class="modal-actions">
          <button type="button" class="button-secondary" @click="emit('close')">Cancel</button>
          <button type="submit" class="button-primary">Create In-Kind Donation</button>
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
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2e7d32;
}
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}
.form-group textarea {
  resize: vertical;
  min-height: 100px;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}
.button-primary {
  background-color: #2e7d32;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}
.button-primary:hover {
  background-color: #1b5e20;
}
.button-secondary {
  background-color: white;
  border: 2px solid #2e7d32;
  color: #2e7d32;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
}
.button-secondary:hover {
  background-color: #e8f5e9;
}
</style>