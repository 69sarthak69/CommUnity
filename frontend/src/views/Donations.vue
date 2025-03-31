<script setup lang="ts">
import { ref } from 'vue';

const donations = ref([
  {
    id: 1,
    donor: 'Emily R.',
    location: 'Downtown',
    time: '1 hour ago',
    content: 'I have extra winter clothes in good condition. Let me know if anyone needs them!',
    likes: 15,
    comments: 4
  },
  {
    id: 2,
    donor: 'Michael T.',
    location: 'Westside',
    time: '3 hours ago',
    content: 'Giving away a study desk and chair. Free for students in need!',
    likes: 10,
    comments: 2
  },
  {
    id: 3,
    donor: 'Olivia P.',
    location: 'Eastside',
    time: '5 hours ago',
    content: 'Donating a grocery package for a family in need. Please reach out!',
    likes: 18,
    comments: 6
  }
]);
</script>

<template>
    
  <div class="container main-content">
    <aside class="sidebar">
      <router-link to="/home" class="sidebar-link">Home</router-link>
      <router-link to="/groups" class="sidebar-link">Groups</router-link>
      <router-link to="/events" class="sidebar-link">Events</router-link>
      <router-link to="/notifications" class="sidebar-link">Notifications</router-link>
      <router-link to="/donations" class="sidebar-link">🎁 Donations</router-link> <!-- NEW BUTTON -->
    </aside>
    <main class="feed">
      <div class="post-card">
        <div class="post-header">
          <button class="button-primary">
            Offer a Donation
          </button>
        </div>
      </div>

      <div v-for="donation in donations" :key="donation.id" class="post-card">
        <div class="post-header">
          <div class="post-author">
            <div class="author-avatar">
              {{ donation.donor[0] }}
            </div>
            <div class="author-info">
              <span class="author-name">{{ donation.donor }}</span>
              <span class="post-meta">{{ donation.location }} • {{ donation.time }}</span>
            </div>
          </div>
        </div>

        <div class="post-content">
          {{ donation.content }}
        </div>

        <div class="post-actions">
          <button class="action-button">
            👍 {{ donation.likes }}
          </button>
          <button class="action-button">
            💬 {{ donation.comments }}
          </button>
          <button class="action-button">
            Share
          </button>
        </div>
      </div>
    </main>
  </div>
</template>
