<template>
  <nav :class="['sidebar', { 'collapsed': isCollapsed }]">
    <div class="nav-items">
      <router-link to="/" class="nav-item" active-class="active">
        <i class="fas fa-home"></i>
        <span>Dashboard</span>
      </router-link>
      <router-link to="/hydrogen" class="nav-item" active-class="active">
        <i class="fas fa-atom"></i>
        <span>Hydrogen</span>
      </router-link>
      <router-link to="/economy" class="nav-item" active-class="active">
        <i class="fas fa-clock"></i>
        <span>Turnaround Time</span>
      </router-link>
      <router-link to="/sustainability" class="nav-item" active-class="active">
        <i class="fas fa-leaf"></i>
        <span>Sustainability</span>
      </router-link>
      <router-link to="/storage" class="nav-item" active-class="active">
        <i class="fas fa-warehouse"></i>
        <span>Storage</span>
      </router-link>
      <router-link to="/regulations" class="nav-item" active-class="active">
        <i class="fas fa-clipboard-list"></i>
        <span>Regulations</span>
      </router-link>
    </div>

    <div class="sidebar-footer">
      <div class="nav-item">
        <i class="fas fa-question-circle"></i>
        <span>Help Center</span>
      </div>
      <div class="nav-item">
        <i class="fas fa-cog"></i>
        <span>Settings</span>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Sidebar',
  props: {
    isCollapsed: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.sidebar {
  width: 260px;
  background: rgba(22, 28, 36, 0.95);
  backdrop-filter: blur(8px);
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  padding-top: 70px;
  border-right: 1px solid rgba(100, 255, 218, 0.1);
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  z-index: 900;
}

.sidebar.collapsed {
  width: 70px;
}

.nav-items {
  padding: 20px 12px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  border-radius: 8px;
  margin-bottom: 4px;
  transition: all 0.2s ease;
  cursor: pointer;
}

.nav-item i {
  font-size: 1.2rem;
  width: 24px;
  text-align: center;
}

.nav-item:hover {
  background: rgba(100, 255, 218, 0.1);
  color: #64ffda;
}

.nav-item.active {
  background: rgba(100, 255, 218, 0.15);
  color: #64ffda;
}

.sidebar-footer {
  padding: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.collapsed .nav-item span {
  display: none;
}

.collapsed .nav-item {
  padding: 12px;
  justify-content: center;
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }

  .sidebar.collapsed {
    transform: translateX(0);
    width: 260px;
  }

  .collapsed .nav-item span {
    display: inline;
  }

  .collapsed .nav-item {
    padding: 12px 16px;
    justify-content: flex-start;
  }
}
</style>
