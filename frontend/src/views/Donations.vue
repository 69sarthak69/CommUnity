<script setup lang="ts">
import { ref } from 'vue'

const amount = ref('')

const donate = async () => {
  if (!amount.value || parseFloat(amount.value) < 10) {
    alert('Minimum donation is Rs. 10')
    return
  }

  try {
    const res = await fetch('http://127.0.0.1:8000/api/donation/initiate/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 👇 Include auth ONLY if your backend needs it
        Authorization: `Bearer ${localStorage.getItem('access')}`
      },
      body: JSON.stringify({ amount: amount.value })
    })

    const data = await res.json()

    if (res.ok && data.payment_url) {
      window.location.href = data.payment_url
    } else {
      console.error(data)
      alert(' Failed to initiate payment')
    }
  } catch (err) {
    console.error(err)
    alert('Something went wrong')
  }
}
</script>

<template>
  <div class="donation-container">
    <h2> Support the Community</h2>

    <div class="donation-box">
      <label for="amount">Enter Donation Amount (Rs):</label>
      <input
        v-model="amount"
        type="number"
        id="amount"
        placeholder="e.g. 500"
      />

      <button @click="donate" class="button-primary">
        Donate with Khalti
      </button>
    </div>
  </div>
</template>

<style scoped>
.donation-container {
  max-width: 500px;
  margin: 60px auto;
  padding: 20px;
  text-align: center;
  background-color: #fff;
  border-radius: 16px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
}

.donation-box {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

input[type='number'] {
  padding: 10px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
}

.button-primary {
  padding: 12px;
  font-size: 16px;
  background-color: #5c2d91;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.button-primary:hover {
  background-color: #4a1c7c;
}
</style>
