<template>
  <div id="app">
    <Header />
    <NotificationToast />
    <div class="main-container">
      <Sidebar />
      <main>
        <router-view /> <!-- Loads the selected page here -->
      </main>
    </div>
  </div>
</template>

<script setup>
import Header from './components/Header.vue';
import Sidebar from './components/Sidebar.vue';
import NotificationToast from '@/components/Common/NotificationToast.vue';
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  /* Header stays on top */
}

.main-container {
  display: flex;
  flex-grow: 1;
}

Sidebar {
  width: 250px;
  background: #2c3e50;
  color: white;
  padding: 15px;
}

main {
  flex-grow: 1;
  padding: 20px;
}
</style>
