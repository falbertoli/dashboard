// Create a new store: frontend/src/store/notificationStore.js
import { defineStore } from "pinia";

export const useNotificationStore = defineStore("notification", {
  state: () => ({
    notifications: [],
    nextId: 1,
  }),

  actions: {
    addNotification(message, type = "info", timeout = 5000) {
      const id = this.nextId++;
      const notification = { id, message, type, timestamp: new Date() };
      this.notifications.push(notification);

      // Auto-remove after timeout
      if (timeout > 0) {
        setTimeout(() => {
          this.removeNotification(id);
        }, timeout);
      }

      return id;
    },

    removeNotification(id) {
      const index = this.notifications.findIndex((n) => n.id === id);
      if (index !== -1) {
        this.notifications.splice(index, 1);
      }
    },
  },
});
