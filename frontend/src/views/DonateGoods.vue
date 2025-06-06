<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['close'])

const itemName = ref('')
const description = ref('')
const quantity = ref('')
const location = ref('')
const image = ref<File | null>(null)

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    image.value = target.files[0]
  }
}

const submitInKindDonation = async () => {
  if (!itemName.value || !description.value || !quantity.value || !location.value) {
    alert('Please fill all required fields.')
    return
  }

  const formData = new FormData()
  formData.append('item_name', itemName.value)
  formData.append('description', description.value)
  formData.append('quantity', quantity.value)
  formData.append('location', location.value)
  if (image.value) {
    formData.append('image', image.value)
  }

  try {
    const res = await fetch('http://127.0.0.1:8000/api/donation/in-kind-donations/', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      },
      body: formData
    })

    if (res.ok) {
      alert('Thank you for your in-kind donation!')
      itemName.value = ''
      description.value = ''
      quantity.value = ''
      location.value = ''
      image.value = null
      emit('close')
    } else {
      alert('Failed to submit donation')
    }
  } catch (err) {
    console.error(err)
    alert('Something went wrong')
  }
}
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-container">
      <div class="modal-header">
        <h2>📦 Donate Goods (In-Kind)</h2>
        <button class="close-btn" @click="emit('close')">×</button>
      </div>
      <form @submit.prevent="submitInKindDonation">
        <label>Item Name *</label>
        <input type="text" v-model="itemName" required />

        <label>Description *</label>
        <textarea v-model="description" rows="3" required></textarea>

        <label>Quantity *</label>
        <input type="text" v-model="quantity" required />

        <label>Drop-off / Pickup Location *</label>
        <input type="text" v-model="location" required />

        <label>Optional Image</label>
        <input type="file" @change="handleFileChange" />

        <button type="submit">Submit In-Kind Donation</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background-color: #fff;
  padding: 2rem;
  border-radius: 16px;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  position: relative;
  animation: fadeIn 0.2s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.close-btn {
  font-size: 1.5rem;
  background: none;
  border: none;
  color: #999;
  cursor: pointer;
}

label {
  display: block;
  margin-top: 12px;
  font-weight: 600;
}

input[type="text"],
textarea,
input[type="file"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-top: 4px;
  font-size: 1rem;
}

button[type="submit"] {
  margin-top: 20px;
  padding: 12px;
  width: 100%;
  background-color: #00a86b;
  color: white;
  font-weight: 600;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
