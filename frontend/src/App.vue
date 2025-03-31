<script setup lang="ts">
import Footer from './components/Footer.vue'
import NavBar from './views/NavBar.vue';
</script>

<template>
  <NavBar/>
  
  <router-view />
  <Footer />
</template>