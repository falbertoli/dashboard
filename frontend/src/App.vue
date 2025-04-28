<template>
  <div id="app">
    <CustomCursor />
    <Header @toggle-sidebar="toggleSidebar" />
    <NotificationToast />
    <div class="main-container">
      <Sidebar :is-collapsed="isSidebarCollapsed" />
      <main :class="{ 'sidebar-expanded': !isSidebarCollapsed }">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import CustomCursor from './components/Common/CustomCursor.vue';
import Header from './components/Header.vue';
import Sidebar from './components/Sidebar.vue';
import NotificationToast from '@/components/Common/NotificationToast.vue';

export default {
  components: {
    CustomCursor,
    Header,
    Sidebar,
    NotificationToast
  },
  data() {
    return {
      isSidebarCollapsed: false
    }
  },
  methods: {
    toggleSidebar() {
      this.isSidebarCollapsed = !this.isSidebarCollapsed;
    }
  }
}
</script>

<style>
#app {
  min-height: 100vh;
  background: #161c24;
  color: #fff;
}

.main-container {
  display: flex;
  min-height: 100vh;
  padding-top: 60px;
  /* Height of header */
}

main {
  flex-grow: 1;
  transition: padding 0.3s ease;
  padding: 20px 20px 20px 290px;
  /* Added left padding for sidebar */
}

main.sidebar-expanded {
  padding-left: 290px;
}

@media (max-width: 768px) {
  main {
    padding: 20px;
  }

  main.sidebar-expanded {
    padding-left: 20px;
  }
}
</style>
