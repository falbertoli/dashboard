<!-- File: frontend/src/components/FlightBoardSelector.vue -->

<template>
  <div class="flight-board-container">
    <label :for="id" class="flight-board-label">
      <i class="fas fa-plane-departure"></i>
      {{ label }}
    </label>

    <div class="flight-board">
      <!-- Current Selected Year Display -->
      <div class="current-flight" @click="toggleSelector">
        <div class="flight-info">
          <div class="flight-number">H2-{{ modelValue }}</div>
          <div class="destination">TARGET YEAR</div>
        </div>
        <div class="flight-status">{{ modelValue ? 'SCHEDULED' : 'SELECT' }}</div>
        <div class="dropdown-arrow">
          <i :class="['fas', isOpen ? 'fa-chevron-up' : 'fa-chevron-down']"></i>
        </div>
      </div>

      <!-- Flight Board Selector -->
      <transition name="board-flip">
        <div v-if="isOpen" class="flight-board-selector">
          <div class="selector-header">
            <div>FLIGHT</div>
            <div>DESTINATION</div>
            <div>STATUS</div>
          </div>

          <div class="flight-options">
            <div v-for="option in options" :key="option.value"
              :class="['flight-option', { 'selected': modelValue === option.value }]" @click="selectYear(option.value)">
              <div class="option-flight-number">H2-{{ option.value }}</div>
              <div class="option-destination">{{ option.text }}</div>
              <div class="option-status" :class="{ 'option-scheduled': modelValue === option.value }">
                {{ modelValue === option.value ? 'SCHEDULED' : 'AVAILABLE' }}
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- Progress Visualization -->
    <div class="boarding-progress">
      <div class="gate-track">
        <div class="gate gate-start">NOW</div>
        <div class="progress-airplane" :style="{ left: progressPosition + '%' }">
          <i class="fas fa-plane"></i>
        </div>
        <div class="gate gate-end">H₂</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  id: {
    type: String,
    required: true,
  },
  options: {
    type: Array,
    required: true,
    validator: (options) => {
      return options.every(option => typeof option === 'object' && option !== null && 'value' in option && 'text' in option);
    }
  },
  modelValue: {
    type: [String, Number],
    default: null,
  },
});

const emit = defineEmits(['update:modelValue']);

const isOpen = ref(false);

const toggleSelector = () => {
  isOpen.value = !isOpen.value;
};

const selectYear = (yearValue) => {
  emit('update:modelValue', yearValue);
  isOpen.value = false;
};

const progressPosition = computed(() => {
  if (!props.modelValue || !props.options.length) return 0;

  const min = props.options[0].value;
  const max = props.options[props.options.length - 1].value;
  const range = max - min;

  // Calculate raw position
  const rawPosition = ((props.modelValue - min) / range) * 100;

  // Limit the position to stay within 0% and 95% of the track
  // This ensures the airplane is always visible
  return Math.min(Math.max(rawPosition, 0), 97);
});

// Close selector when clicking outside
const handleClickOutside = (event) => {
  const container = document.querySelector('.flight-board-container');
  if (container && !container.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<style scoped>
.flight-board-container {
  margin-bottom: 30px;
  width: 100%;
  font-family: 'Roboto Mono', monospace;
}

.flight-board-label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  color: #eee;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.flight-board-label i {
  margin-right: 8px;
  color: #64ffda;
}

/* Flight Board Styling */
.flight-board {
  position: relative;
  border-radius: 8px;
  overflow: visible;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.current-flight {
  background-color: #1a1f28;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #35393f;
  border-radius: 8px;
}

.current-flight:hover {
  background-color: #22293a;
}

.flight-info {
  display: flex;
  flex-direction: column;
}

.flight-number {
  font-size: 1.2rem;
  font-weight: bold;
  color: #64ffda;
  margin-bottom: 4px;
  letter-spacing: 1px;
}

.destination {
  font-size: 0.7rem;
  color: #888;
  letter-spacing: 1px;
}

.flight-status {
  color: #64ffda;
  font-weight: bold;
  font-size: 0.8rem;
  background-color: rgba(100, 255, 218, 0.1);
  padding: 4px 10px;
  border-radius: 12px;
  letter-spacing: 1px;
}

.dropdown-arrow {
  margin-left: 15px;
  color: #64ffda;
  transition: transform 0.3s ease;
}

/* Flight Board Selector Styling */
.flight-board-selector {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  width: 100%;
  background-color: #12151d;
  border-radius: 8px;
  z-index: 100;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
  border: 1px solid #35393f;
  overflow: hidden;
}

.selector-header {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  padding: 12px 20px;
  background-color: rgba(100, 255, 218, 0.1);
  color: #64ffda;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.flight-options {
  max-height: 300px;
  overflow-y: auto;
}

.flight-option {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  padding: 15px 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.flight-option:hover {
  background-color: rgba(100, 255, 218, 0.1);
}

.flight-option:last-child {
  border-bottom: none;
}

.selected {
  background-color: rgba(100, 255, 218, 0.15);
}

.option-flight-number {
  color: #64ffda;
  font-weight: bold;
}

.option-destination {
  color: #ddd;
}

.option-status {
  color: #aaa;
  font-size: 0.8rem;
}

.option-scheduled {
  color: #64ffda;
  font-weight: bold;
}

/* Boarding Gate Progress Bar */
.boarding-progress {
  margin-top: 15px;
}

.gate-track {
  position: relative;
  height: 30px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 0%, rgba(100, 255, 218, 0.1) 100%);
  border-radius: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 15px;
}

.gate {
  font-size: 0.8rem;
  font-weight: bold;
}

.gate-start {
  color: #aaa;
}

.gate-end {
  color: #64ffda;
}

.progress-airplane {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: #64ffda;
  transition: left 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.progress-airplane i {
  font-size: 1.2rem;
  transform: rotate(90deg);
  filter: drop-shadow(0 0 8px rgba(100, 255, 218, 0.6));
}

/* Animations */
.board-flip-enter-active,
.board-flip-leave-active {
  transition: all 0.3s ease;
}

.board-flip-enter-from,
.board-flip-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>