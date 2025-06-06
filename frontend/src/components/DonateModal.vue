<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';



const emit = defineEmits(['close']);
const amount = ref<number | null>(null);
const error = ref<string | null>(null);
const loading = ref(false);
const props = defineProps<{
  donation: { id: number; title: string } | null;
}>();

const submitDonation = async () => {
  if (!amount.value || amount.value <= 0) {
    error.value = 'Please enter a valid amount';
    return;
  }

  try {
    loading.value = true;
    const response = await axios.post(
      `http://localhost:8000/api/donation/initiate/`,
      {
        amount: amount.value,
        campaign_id: props.donation?.id,
        anonymous: false,
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      }
    );
    window.location.href = response.data.payment_url;
  } catch (err) {
    error.value = 'Failed to process donation';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

</script>

<template>
  <div class="modal">
    <div class="modal-content">
      <h2>Donate to {{ donation?.title }}</h2>
      <input v-model.number="amount" type="number" placeholder="Enter amount (Rs.)" min="1" />
      <p v-if="error" class="error">{{ error }}</p>
      <button :disabled="loading" class="button-primary" @click="submitDonation">
        {{ loading ? 'Processing...' : 'Donate Now' }}
      </button>
      <button class="button-secondary" @click="emit('close')">Cancel</button>
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
}
.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 400px;
  width: 100%;
}
input {
  width: 100%;
  padding: 0.5rem;
  margin: 1rem 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.error {
  color: red;
  margin-bottom: 1rem;
}
</style>