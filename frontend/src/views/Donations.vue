<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import MapComponent from './MapComponent.vue';
import Notifications from '../components/Notifications.vue';
import DonateModal from '../components/DonateModal.vue';
import InKindDonateModal from '../components/InKindDonateModal.vue';
import CreateDonationModal from '../components/CreateDonationModal.vue';
import axios from 'axios';

const router = useRouter();

// Interfaces
interface Donation {
  id: number;
  title: string;
  description: string;
  target_amount: number;
  current_amount: number;
  location: string;
  created_by: number;
  created_at: string;
}

interface InKindDonation {
  id: number;
  item: string;
  description: string;
  location: string;
  drop_off_date: string;
}

// State
const donations = ref<Donation[]>([]);
const inKindDonations = ref<InKindDonation[]>([]);
const user = ref<{ email: string; username: string; id: number } | null>(null);
const showDonateModal = ref(false);
const showInKindModal = ref(false);
const showCreateDonationModal = ref(false);
const selectedDonation = ref<Donation | null>(null);

// API Calls
const fetchDonations = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/donation/', {
      headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` },
    });

    donations.value = response.data.cash_donations.map((d: any) => ({
      id: d.id,
      title: d.title,
      description: d.description,
      target_amount: d.target_amount,
      current_amount: d.current_amount,
      location: d.location,
      created_by: d.created_by,
      created_at: d.created_at,
    }));

    inKindDonations.value = response.data.in_kind_donations.map((d: any) => ({
    id: d.id,
    item: d.item,
    description: d.description,
    quantity: d.quantity,
    location: d.location,
    drop_off_date: d.drop_off_date,
    status: d.status,
    image: d.image,
  }));

  } catch (error) {
    console.error('Error fetching donations:', error);
  }
};

const checkUser = () => {
  const email = localStorage.getItem('user_email');
  const username = localStorage.getItem('user_username');
  const id = localStorage.getItem('user_id');
  user.value = email && username && id ? { email, username, id: parseInt(id) } : null;
};

// Modal handlers
const openDonateModal = (donation: Donation) => {
  selectedDonation.value = donation;
  showDonateModal.value = true;
};
const openInKindModal = () => showInKindModal.value = true;
const openCreateDonationModal = () => showCreateDonationModal.value = true;

const handleDonationSubmitted = () => {
  fetchDonations();
};

const handleLogout = () => {
  localStorage.clear();
  user.value = null;
  router.push('/');
};

onMounted(() => {
  checkUser();
  fetchDonations();

  const socket = new WebSocket("ws://localhost:8000/ws/donations/");

  socket.onopen = () => {
    console.log("✅ WebSocket connected");
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("📡 Received via WebSocket:", data);
    fetchDonations(); // Auto-refresh UI
  };

  socket.onerror = (error) => {
    console.error("❌ WebSocket error:", error);
  };

  socket.onclose = () => {
    console.warn("🔌 WebSocket disconnected");
  };

  // Fallback: Refresh every 30 seconds just in case
  setInterval(() => {
    fetchDonations();
  }, 30000);
});

</script>

<template>
  <div class="app-container">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <div class="container nav-content">
        <router-link to="/home" class="logo">
          <span class="logo-icon"></span>
          <span>CommunityHelp</span>
        </router-link>

        <div class="nav-links">
          <Notifications />
          <button v-if="user" class="nav-button" @click="router.push('/profile')">
            <span class="button-icon">👤</span>
            <span class="button-text">{{ user.username || user.email }}</span>
          </button>
          <button v-if="user" class="nav-button" @click="router.push('/my-applications')">
            <span class="button-icon">📋</span>
            <span class="button-text">My Applications</span>
          </button>
          <button v-if="user" class="nav-button logout" @click="handleLogout">
            <span class="button-icon">🚪</span>
            <span class="button-text">Logout</span>
          </button>
          <router-link v-if="!user" to="/" class="nav-button primary">
            <span class="button-text">Login</span>
          </router-link>
        </div>
      </div>
    </nav>

    <div class="container main-content">
      <!-- Sidebar -->
      <aside class="sidebar">
        <router-link to="/home" class="sidebar-link">
          <span class="link-icon">🏠</span>
          <span>Home</span>
        </router-link>
        <router-link to="/groups" class="sidebar-link">
          <span class="link-icon">👥</span>
          <span>Groups</span>
        </router-link>
        <router-link to="/events" class="sidebar-link">
          <span class="link-icon">📅</span>
          <span>Events</span>
        </router-link>
        <router-link to="/donations" class="sidebar-link active">
          <span class="link-icon">🎁</span>
          <span>Donations</span>
        </router-link>
        <div>
          <h2 class="text-xl font-bold mb-2">Map Preview</h2>
          <MapComponent />
        </div>
      </aside>

      <!-- Main Content -->
      <main class="feed">
        <!-- Cash Donations -->
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-2xl font-bold">Donation Campaigns</h1>
          <button class="button-secondary" @click="openCreateDonationModal">
            ➕ Create Donation
          </button>
        </div>

        <div class="event-list">
          <div v-for="donation in donations" :key="donation.id" class="event-card">
            <div class="event-date">
              <div class="event-day">🎁</div>
              <div class="event-month">Donate</div>
            </div>

            <div class="event-details">
              <h3 class="event-title">{{ donation.title }}</h3>
              <div class="event-location">📍 {{ donation.location }}</div>
              <p class="event-description">{{ donation.description }}</p>
              <p class="event-description">
                Raised: Rs. {{ donation.current_amount }} / Rs. {{ donation.target_amount }}
              </p>

              <p v-if="donation.current_amount >= donation.target_amount" class="goal-reached">
                🎉 Goal Reached!
              </p>

              <button
                class="button-primary"
                :disabled="donation.current_amount >= donation.target_amount"
                @click="openDonateModal(donation)"
              >
                💰 Donate Now
              </button>
            </div>
          </div>
        </div>

        <!-- In-Kind Donations -->
        <section class="inkind-section mt-12">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold text-green-800">📦 In-Kind Donations</h2>
            <button class="button-secondary" @click="openInKindModal">
              ➕ Donate Goods
            </button>
          </div>

          <div class="event-list">
            <div v-for="item in inKindDonations" :key="item.id" class="event-card">
              <div class="event-date">
                <div class="event-day">📦</div>
                <div class="event-month">Drop</div>
              </div>

             <div class="event-details">
              <h3 class="event-title">{{ item.item }}</h3>
              <div class="event-location">📍 {{ item.location }}</div>
              <p class="event-description">{{ item.description }}</p>

              <p class="event-description">
                📦 Quantity: {{ item.quantity }}
              </p>

              <p class="event-description">
                📅 Drop-off by:
                <span v-if="item.drop_off_date">{{ item.drop_off_date }}</span>
                <span v-else class="text-gray-400 italic">Not specified</span>
              </p>

              <p class="event-description status-badge" :class="{
                'bg-yellow-100 text-yellow-800': item.status === 'pending',
                'bg-green-100 text-green-800': item.status === 'approved',
                'bg-red-100 text-red-800': item.status === 'rejected',
              }">
                Status: {{ item.status }}
              </p>

              <img
                v-if="item.image"
                :src="item.image"
                alt="donated item image"
                class="rounded-md mt-2 max-w-xs"
              />
            </div>

            </div>
          </div>
        </section>
      </main>
    </div>
  </div>

  <!-- Modals -->
  <DonateModal
    v-if="showDonateModal"
    :donation="selectedDonation"
    @close="showDonateModal = false"
  />
  <InKindDonateModal
    v-if="showInKindModal"
    @close="showInKindModal = false"
    @submitted="fetchDonations"
  />
  <CreateDonationModal
    v-if="showCreateDonationModal"
    @close="showCreateDonationModal = false"
    @submitted="handleDonationSubmitted"
  />
</template>

<style scoped>


.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-weight: 500;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

.goal-reached {
  font-weight: bold;
  color: #2e7d32;
  margin-top: 0.5rem;
}
button[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-primary {
  background-color: #2e7d32;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}
.button-primary:hover {
  background-color: #1b5e20;
}
.button-secondary {
  background-color: white;
  border: 2px solid #2e7d32;
  color: #2e7d32;
  padding: 0.5rem 1rem;
  font-weight: 500;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.button-secondary:hover {
  background-color: #e8f5e9;
}
.event-list {
  margin-top: 1.5rem;
  display: grid;
  gap: 1.5rem;
}
.event-card {
  display: flex;
  background: #fff;
  padding: 1.25rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
}
.event-card:hover {
  transform: translateY(-3px);
  border-left-color: #4caf50;
}
.event-date {
  width: 70px;
  text-align: center;
  background: #e8f5e9;
  border-radius: 8px;
  padding: 0.75rem;
  margin-right: 1.25rem;
  color: #2e7d32;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.event-day {
  font-size: 1.75rem;
  font-weight: bold;
}
.event-month {
  font-size: 0.8rem;
  color: #388e3c;
  margin-top: 0.25rem;
  text-transform: uppercase;
}
.event-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2e7d32;
}
.event-description {
  font-size: 0.95rem;
  color: #555;
  margin: 0.5rem 0;
}
.event-location {
  font-size: 0.9rem;
  color: #689f38;
}
.inkind-section {
  margin-top: 3rem;
}
</style>