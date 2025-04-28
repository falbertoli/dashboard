<template>
  <div class="custom-cursor" :style="{ left: x + 'px', top: y + 'px' }">
    <font-awesome-icon :icon="currentIcon" :class="{ 'pointer': isPointer, 'clicking': isClicking }" size="lg" />
  </div>
</template>

<script>
import { library } from '@fortawesome/fontawesome-svg-core'
import { faArrowPointer, faHandPointer } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faArrowPointer, faHandPointer)

export default {
  components: {
    FontAwesomeIcon
  },
  data() {
    return {
      x: 0,
      y: 0,
      isPointer: false,
      isClicking: false,
      defaultIcon: 'arrow-pointer',
      pointerIcon: 'hand-pointer'
    }
  },
  computed: {
    currentIcon() {
      return this.isPointer ? this.pointerIcon : this.defaultIcon
    }
  },
  mounted() {
    // Add a style tag to hide cursors globally
    const styleTag = document.createElement('style');
    styleTag.textContent = '* { cursor: none !important; }';
    document.head.appendChild(styleTag);
    this.styleTag = styleTag;

    // Track mouse movement
    document.addEventListener('mousemove', this.updateCursorPosition);

    // Check for hoverable elements
    document.addEventListener('mouseover', this.checkElement);
    document.addEventListener('mouseout', this.resetCursor);
    document.addEventListener('mousedown', this.startClick);
    document.addEventListener('mouseup', this.endClick);
  },
  beforeUnmount() {
    // Remove the style tag when component is destroyed
    if (this.styleTag) {
      document.head.removeChild(this.styleTag);
    }

    document.removeEventListener('mousemove', this.updateCursorPosition);
    document.removeEventListener('mouseover', this.checkElement);
    document.removeEventListener('mouseout', this.resetCursor);
    document.removeEventListener('mousedown', this.startClick);
    document.removeEventListener('mouseup', this.endClick);
  },
  methods: {
    updateCursorPosition(e) {
      this.x = e.clientX;
      this.y = e.clientY;
    },
    checkElement(e) {
      const hoverableElements = ['A', 'BUTTON', 'SELECT', 'INPUT[type="submit"]'];
      const element = e.target;

      this.isPointer = hoverableElements.includes(element.tagName) ||
        element.classList.contains('primary-button') ||
        element.classList.contains('secondary-button') ||
        element.getAttribute('role') === 'button';
    },
    resetCursor() {
      this.isPointer = false;
    },
    startClick() {
      this.isClicking = true;
    },
    endClick() {
      this.isClicking = false;
    }
  }
}
</script>

<style scoped>
.custom-cursor {
  position: fixed;
  z-index: 9999;
  pointer-events: none;
  transform: translate(-50%, -50%);
  color: #ff9f43;
  filter: drop-shadow(0 0 2px rgba(0, 0, 0, 0.5));
  transition: transform 0.1s ease;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-cursor svg {
  width: 24px;
  height: 24px;
}

.custom-cursor .pointer {
  color: #ff9f43;
  transform: scale(1.2);
}

.custom-cursor .clicking {
  transform: scale(0.8);
  opacity: 0.8;
}

.custom-cursor svg {
  width: 24px;
  height: 24px;
  transition: transform 0.2s ease, color 0.2s ease;
}
</style>