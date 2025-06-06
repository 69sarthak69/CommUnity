<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Donation {
  amount: number;
  status: string;
  created_at: string;
  help_request_title?: string;
  group_name?: string;
  type: 'cash' | 'goods';
  item_name?: string;
  description?: string;
  quantity?: string;
}

const donations = ref<Donation[]>([])

const fetchMyDonations = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/api/donation/my-donations/', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })

    if (res.ok) {
      donations.value = await res.json()
    } else {
      alert('Failed to load donations')
    }
  } catch (err) {
    console.error(err)
    alert('Something went wrong')
  }
}

onMounted(() => {
  fetchMyDonations()
})
</script>

<template>
  <div class="my-donations">
    <h2>🧾 My Donations</h2>

    <div v-if="donations.length === 0" class="empty">
      You haven't made any donations yet.
    </div>

    <ul v-else class="donation-list">
      <li v-for="(donation, index) in donations" :key="index" class="donation-item">
        <div class="info">
          <p><strong>{{ donation.type === 'goods' ? '📦 In-Kind Donation:' : '💸 Cash Donation:' }}</strong></p>
          <p v-if="donation.type === 'cash'">
            Amount: Rs. {{ donation.amount }} | Status: {{ donation.status }}
            <br />
            <span v-if="donation.help_request_title">To Task: {{ donation.help_request_title }}</span>
            <span v-if="donation.group_name">To Group: {{ donation.group_name }}</span>
          </p>
          <p v-else>
            Item: {{ donation.item_name }} (x{{ donation.quantity }})
            <br />{{ donation.description }}
          </p>
          <p class="date">🕓 {{ new Date(donation.created_at).toLocaleString() }}</p>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.my-donations {
  max-width: 700px;
  margin: 60px auto;
  padding: 20px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

h2 {
  text-align: center;
  margin-bottom: 24px;
}

.donation-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.donation-item {
  background-color: #f9f9f9;
  padding: 15px;
  border-radius: 10px;
}

.date {
  font-size: 12px;
  color: gray;
  margin-top: 4px;
}

.empty {
  text-align: center;
  padding: 30px;
  color: #888;
  font-size: 16px;
}
</style>
