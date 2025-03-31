<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const name = ref('')
const email = ref('')
const password = ref('')
const errorMessage = ref('')
const successMessage = ref('')
const isSubmitting = ref(false)  // ✅ Prevents double submission
const areaOfInterest = ref('')
const interests = ['Financial', 'Clothing', 'Food', 'Education', 'Medical', 'Technology']
const phoneNumber = ref('')
const location = ref('')

const handleRegister = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  isSubmitting.value = true  // ✅ Disable button to prevent double submission

  // ✅ Ensure name is properly split into first & last name
  const nameParts = name.value.trim().split(/\s+/)
  const firstName = nameParts[0] || ''
  const lastName = nameParts.slice(1).join(" ") || '.'  // ✅ Default to "."

  try {
    await axios.post('http://localhost:8000/api/auth/register/', {
      first_name: firstName,
      last_name: lastName,
      email: email.value.trim(),
      password: password.value,
      phone_number: phoneNumber.value.trim(),
      location: location.value.trim(),
      area_of_interest: areaOfInterest.value,
    })

    successMessage.value = 'Registration successful! Redirecting to login...'

    // ✅ Redirect to login after 2 seconds
    setTimeout(() => {
      router.push('/login')
    }, 2000)

  } catch (error) {
    if (error.response) {
      // ✅ Extract all possible error messages from backend response
      const errorData = error.response.data?.error || error.response.data

      errorMessage.value =
        errorData?.email?.[0] ||
        errorData?.password?.[0] ||
        errorData?.phone_number?.[0] ||
        errorData?.first_name?.[0] ||
        errorData?.last_name?.[0] ||
        errorData?.location?.[0] ||
        errorData?.area_of_interest?.[0] ||
        errorData?.detail ||
        'Registration failed due to an unknown error.'
    } else if (error.request) {
      errorMessage.value = 'Server is unreachable. Please check your internet connection and try again.'
    } else {
      errorMessage.value = 'An unexpected error occurred. Please try again.'
    }
    console.error('Registration error:', errorMessage.value)
  } finally {
    isSubmitting.value = false  // ✅ Re-enable button after response
  }
}
</script>

<template>
  <div class="form-container">
    <h2 class="form-title">Join Community Help</h2>

    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="name" class="form-label">Full Name</label>
        <input id="name" type="text" v-model="name" required class="form-input" placeholder="Enter your full name" />
      </div>

      <div class="form-group">
        <label for="email" class="form-label">Email</label>
        <input id="email" type="email" v-model="email" required class="form-input" placeholder="Enter your email" />
      </div>

      <div class="form-group">
        <label for="password" class="form-label">Password</label>
        <input id="password" type="password" v-model="password" required class="form-input" placeholder="Create a password" />
      </div>

      <div class="form-group">
        <label for="phone" class="form-label">Phone Number</label>
        <input id="phone" type="tel" v-model="phoneNumber" required class="form-input" placeholder="Enter your phone number" />
      </div>

      <div class="form-group">
        <label for="location" class="form-label">Location</label>
        <input id="location" type="text" v-model="location" required class="form-input" placeholder="Enter your location" />
      </div>

      <div class="form-group">
        <label for="interest" class="form-label">Area of Interest</label>
        <select id="interest" v-model="areaOfInterest" required class="form-input">
          <option value="" disabled>Select an interest</option>
          <option v-for="interest in interests" :key="interest" :value="interest">
            {{ interest }}
          </option>
        </select>
      </div>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>

      <button type="submit" class="button-primary" style="width: 100%" :disabled="isSubmitting">
        {{ isSubmitting ? 'Registering...' : 'Join Community Help' }}
      </button>
    </form>

    <div class="form-footer">
      <p>
        Already have an account? <router-link to="/login">Log in</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.error-message {
  color: red;
  font-size: 14px;
  margin-bottom: 10px;
}
.success-message {
  color: green;
  font-size: 14px;
  margin-bottom: 10px;
}
</style>
