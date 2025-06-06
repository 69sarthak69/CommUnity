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
const isSubmitting = ref(false) 
const areaOfInterest = ref('')
const interests = ['Financial', 'Clothing', 'Food', 'Education', 'Medical', 'Technology']
const phoneNumber = ref('')
const location = ref('')

const handleRegister = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  isSubmitting.value = true  // Disable button to prevent double submission

  // Ensure name is properly split into first & last name
  const nameParts = name.value.trim().split(/\s+/)
  const firstName = nameParts[0] || ''
  const lastName = nameParts.slice(1).join(" ") || '.'  // Default to "."

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

    // Redirect to login after 2 seconds
    setTimeout(() => {
      router.push('/')
    }, 2000)

  } catch (error) {
    if (error.response) {
      // Extract all possible error messages from backend response
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
    isSubmitting.value = false  // Re-enable button after response
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
        Already have an account? <router-link to="/">Log in</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Main container */
.form-container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2.5rem;
  background: var(--card-bg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border);
}

/* Form title */
.form-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 1.5rem;
  text-align: center;
}

/* Form groups */
.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--text);
  margin-bottom: 0.5rem;
}

/* Input fields */
.form-input {
  width: 100%;
  padding: 0.875rem 1rem;
  font-size: 0.9375rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  background: var(--background);
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0, 178, 70, 0.1);
}

select.form-input {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1rem;
}

/* Messages */
.error-message {
  color: var(--danger);
  font-size: 0.875rem;
  margin: -0.5rem 0 1rem 0;
  text-align: center;
  padding: 0.5rem;
  background: #fee2e2;
  border-radius: var(--radius-sm);
}

.success-message {
  color: var(--success);
  font-size: 0.875rem;
  margin: -0.5rem 0 1rem 0;
  text-align: center;
  padding: 0.5rem;
  background: #d1fae5;
  border-radius: var(--radius-sm);
}

/* Submit button */
.button-primary {
  width: 100%;
  padding: 1rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius-full);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-top: 0.5rem;
}

.button-primary:hover {
  background: var(--primary-dark);
  box-shadow: var(--shadow-md);
}

.button-primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  background: var(--primary);
}

/* Form footer */
.form-footer {
  margin-top: 1.5rem;
  text-align: center;
  font-size: 0.875rem;
  color: var(--text-light);
}

.form-footer a {
  color: var(--primary);
  text-decoration: none;
  font-weight: 500;
}

.form-footer a:hover {
  text-decoration: underline;
}

/* Password strength indicator */
.password-strength {
  margin-top: 0.25rem;
  height: 4px;
  background: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
}

.password-strength-meter {
  height: 100%;
  width: 0%;
  background: var(--danger);
  transition: width 0.3s ease;
}

/* Responsive design */
@media (max-width: 768px) {
  .form-container {
    padding: 1.5rem;
    margin: 1rem;
  }

  .form-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .form-container {
    padding: 1.25rem;
    margin: 0.5rem;
  }

  .form-input {
    padding: 0.75rem;
  }

  .button-primary {
    padding: 0.875rem;
  }
}
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
