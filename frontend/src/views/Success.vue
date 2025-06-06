<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

onMounted(async () => {
  const pidx = route.query.pidx

  if (!pidx) {
    alert('Missing payment info!')
    router.push('/donations')
    return
  }

  try {
    const res = await fetch('http://127.0.0.1:8000/api/donation/verify/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access_token')}`  
      },
      body: JSON.stringify({ pidx })
    })

    const data = await res.json()

    if (res.ok) {
      alert('🎉 Thank you for your donation!')
      router.push('/donations')  // Redirect back to donation page
    } else {
      alert(`⚠️ Payment status: ${data.status}`)
      router.push('/donations')  // Still redirect even on fail
    }
  } catch (err) {
    console.error(err)
    alert('Something went wrong while verifying payment.')
    router.push('/donations')  // Redirect in all cases
  }
})
</script>

<template>
  <div class="thank-you">
    <h2>Verifying your donation...</h2>
  </div>
</template>
