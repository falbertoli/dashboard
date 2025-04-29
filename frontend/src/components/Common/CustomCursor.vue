<template>
  <div>
    <div class="custom-cursor" :style="{ left: x + 'px', top: y + 'px' }">
      <font-awesome-icon :icon="currentIcon" :class="{ 'pointer': isPointer, 'clicking': isClicking }" size="lg" />
    </div>
    <!-- SVG Filters Definition -->
    <svg width="0" height="0" style="position: absolute;">
      <defs>
        <filter id="default-contour" x="-20%" y="-20%" width="140%" height="140%">
          <feMorphology operator="dilate" radius="1" in="SourceAlpha" result="thicken" />
          <feFlood flood-color="#FFFFFF" result="contour-color" />
          <feComposite in="contour-color" in2="thicken" operator="in" result="contour" />
          <feComposite in="SourceGraphic" in2="contour" operator="over" />
        </filter>

        <filter id="pointer-contour" x="-20%" y="-20%" width="140%" height="140%">
          <feMorphology operator="dilate" radius="1.5" in="SourceAlpha" result="thicken" />
          <feFlood flood-color="#FFFFFF" result=" contour-color" />
          <feComposite in="contour-color" in2="thicken" operator="in" result="contour" />
          <feComposite in="SourceGraphic" in2="contour" operator="over" />
        </filter>

        <filter id="clicking-contour" x="-20%" y="-20%" width="140%" height="140%">
          <feMorphology operator="dilate" radius="2" in="SourceAlpha" result="thicken" />
          <feFlood flood-color="#FFFFFF" result="contour-color" />
          <feComposite in="contour-color" in2="thicken" operator="in" result="contour" />
          <feComposite in="SourceGraphic" in2="contour" operator="over" />
        </filter>
      </defs>
    </svg>
  </div>
</template>

<script>
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlaneUp, faHandPointer } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faPlaneUp, faHandPointer)

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
      defaultIcon: 'plane-up',
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
  color: #B3A369;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.custom-cursor svg {
  width: 24px;
  height: 24px;
  filter: url(#default-contour);
  transition: transform 0.2s ease, filter 0.3s ease;
}

.custom-cursor .pointer {
  filter: url(#pointer-contour);
  transform: scale(1.2);
}

.custom-cursor .clicking {
  filter: url(#clicking-contour);
  transform: scale(0.8);
  opacity: 0.8;
}
</style>