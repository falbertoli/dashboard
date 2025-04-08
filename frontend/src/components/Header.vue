<template>
  <header class="header">
    <div class="header-content">
      <div class="header-left">
        <button class="menu-toggle" @click="$emit('toggle-sidebar')">
          <i class="fas fa-bars"></i>
        </button>
        <img src="@/assets/images/gt-asdl-logo.png" alt="ASDL Logo" class="header-logo" />
        <h1>Hydrogen Infrastructure</h1>
      </div>
      <div class="header-right">
        <button class="action-button">
          <i class="fas fa-bell"></i>
          <span class="notification-badge">2</span>
        </button>
        <div class="user-menu">
          <img src="https://api.dicebear.com/7.x/initials/svg?seed=Admin" alt="User" class="user-avatar" />
          <span>Admin User</span>
          <i class="fas fa-chevron-down"></i>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  emits: ['toggle-sidebar']
}
</script>

<style scoped>
.header {
  background: rgba(22, 28, 36, 0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(100, 255, 218, 0.1);
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-logo {
  height: 32px;
  width: auto;
}

.menu-toggle {
  display: none;
  background: none;
  border: none;
  color: #64ffda;
  font-size: 1.2rem;
  padding: 8px;
  cursor: pointer;
  border-radius: 8px;
}

.menu-toggle:hover {
  background: rgba(100, 255, 218, 0.1);
}

h1 {
  color: white;
  font-size: 1.2rem;
  font-weight: 500;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.action-button {
  background: none;
  border: none;
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1rem;
  padding: 8px;
  cursor: pointer;
  border-radius: 8px;
  position: relative;
}

.action-button:hover {
  color: #64ffda;
  background: rgba(100, 255, 218, 0.1);
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  background: #ff4d4f;
  color: white;
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: bold;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 12px;
  border-radius: 8px;
  cursor: pointer;
  color: white;
  transition: all 0.2s ease;
}

.user-menu:hover {
  background: rgba(255, 255, 255, 0.1);
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #64ffda;
}

@media (max-width: 768px) {
  .menu-toggle {
    display: block;
  }

  .header-logo {
    height: 28px;
  }

  h1 {
    font-size: 1rem;
  }

  .user-menu span {
    display: none;
  }
}
</style>
