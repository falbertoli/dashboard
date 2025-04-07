<!-- frontend/src/components/Common/NotificationToast.vue -->
<template>
  <div class="notifications-container">
    <transition-group name="notification">
      <div v-for="notification in notifications" :key="notification.id" class="notification" :class="notification.type">
        <i :class="getIconClass(notification.type)"></i>
        <span class="message">{{ notification.message }}</span>
        <button class="close-btn" @click="removeNotification(notification.id)">×</button>
      </div>
    </transition-group>
  </div>
</template>

<script>
import { useNotificationStore } from '@/store/notificationStore';
import { computed } from 'vue';

export default {
  setup() {
    const notificationStore = useNotificationStore();

    const notifications = computed(() => notificationStore.notifications);

    const getIconClass = (type) => {
      switch (type) {
        case 'success': return 'fas fa-check-circle';
        case 'error': return 'fas fa-exclamation-circle';
        case 'warning': return 'fas fa-exclamation-triangle';
        default: return 'fas fa-info-circle';
      }
    };

    const removeNotification = (id) => {
      notificationStore.removeNotification(id);
    };

    return {
      notifications,
      getIconClass,
      removeNotification
    };
  }
}
</script>

<style scoped>
.notifications-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1000;
  max-width: 350px;
}

.notification {
  padding: 15px;
  margin-bottom: 10px;
  border-radius: 4px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  background: white;
  border-left: 4px solid #ccc;
}

.notification i {
  margin-right: 10px;
}

.notification.info {
  border-left-color: #2196F3;
}

.notification.success {
  border-left-color: #4CAF50;
}

.notification.warning {
  border-left-color: #FF9800;
}

.notification.error {
  border-left-color: #F44336;
}

.message {
  flex-grow: 1;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  opacity: 0.6;
}

.close-btn:hover {
  opacity: 1;
}

/* Transition effects */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from,
.notification-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>