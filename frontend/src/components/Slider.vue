<!-- File: frontend/src/components/Slider.vue (RunwaySlider) -->

<template>
  <div class="runway-slider-container">
    <div class="slider-header">
      <label :for="id" class="runway-slider-label">
        <i class="fas fa-plane-circle-check"></i> {{ label }}
      </label>
      <div class="percentage-badge">{{ value }}{{ unit }}</div>
    </div>

    <div class="runway-wrapper">
      <!-- Runway Markers -->
      <div class="runway-markers">
        <div class="marker takeoff">
          <div class="marker-label">Takeoff</div>
          <div class="marker-value">0%</div>
        </div>
        <div class="marker cruising">
          <div class="marker-label">Cruising</div>
          <div class="marker-value">50%</div>
        </div>
        <div class="marker landing">
          <div class="marker-label">Landing</div>
          <div class="marker-value">100%</div>
        </div>
      </div>

      <!-- Runway Track -->
      <div class="runway-track" :id="id" ref="track" @click="onTrackClick">
        <!-- Runway Lights -->
        <div class="runway-lights">
          <div v-for="n in 20" :key="n" :class="['runway-light', { 'active': (n / 20) * 100 <= value }]"></div>
        </div>

        <!-- Hydrogen Trail -->
        <div class="hydrogen-trail" ref="trail"></div>

        <!-- Runway Airplane -->
        <div class="runway-airplane" ref="airplane">
          <i class="fas fa-plane"></i>
          <div class="h2-cloud">H₂</div>
        </div>

        <!-- Runway Labels -->
        <div class="runway-labels">
          <div class="runway-end start">0%</div>
          <div class="runway-end end">100%</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';

const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  id: {
    type: String,
    required: true,
  },
  min: {
    type: Number,
    default: 0,
  },
  max: {
    type: Number,
    default: 100,
  },
  step: {
    type: Number,
    default: 1,
  },
  modelValue: {
    type: Number,
    default: 10,
  },
  unit: {
    type: String,
    default: '%'
  },
});

const emit = defineEmits(['update:modelValue']);

const value = ref(props.modelValue);
const track = ref(null);
const airplane = ref(null);
const trail = ref(null);
const dragging = ref(false);

watch(
  () => props.modelValue,
  (newVal) => {
    value.value = newVal;
    updateAirplanePosition();
    updateTrailWidth();
  }
);

const calculateValueFromPosition = (clientX) => {
  const trackRect = track.value.getBoundingClientRect();
  const trackWidth = trackRect.width;
  const offsetX = clientX - trackRect.left;

  // Calculate percentage and round to step
  let percentage = (offsetX / trackWidth) * 100;
  percentage = Math.max(0, Math.min(100, percentage)); // Clamp between 0-100

  // Apply step
  const stepCount = Math.round(percentage / (props.step * (100 / (props.max - props.min))));
  const steppedValue = props.min + (stepCount * props.step);

  return Math.min(props.max, Math.max(props.min, steppedValue));
};

const updateAirplanePosition = () => {
  if (!airplane.value || !track.value) return;

  const trackWidth = track.value.offsetWidth;
  const percentage = (value.value - props.min) / (props.max - props.min);
  const position = percentage * trackWidth;

  airplane.value.style.left = `${position}px`;

  // Adjust airplane rotation based on position
  const rotation = Math.min(20, percentage * 40 - 20); // -20 to 20 degrees
  airplane.value.style.transform = `translateY(-50%) rotate(${rotation}deg)`;
};

const updateTrailWidth = () => {
  if (!trail.value || !track.value || !airplane.value) return;

  const trackWidth = track.value.offsetWidth;
  const percentage = (value.value - props.min) / (props.max - props.min);
  const position = percentage * trackWidth;

  trail.value.style.width = `${position}px`;
};

const onTrackClick = (event) => {
  const newValue = calculateValueFromPosition(event.clientX);
  value.value = newValue;
  emit('update:modelValue', newValue);
  updateAirplanePosition();
  updateTrailWidth();
};

const onDrag = (event) => {
  if (!dragging.value) return;

  const newValue = calculateValueFromPosition(event.clientX);
  value.value = newValue;
  emit('update:modelValue', newValue);
  updateAirplanePosition();
  updateTrailWidth();
};

const startDrag = () => {
  dragging.value = true;
  document.addEventListener('mousemove', onDrag);
  document.addEventListener('mouseup', stopDrag);
};

const stopDrag = () => {
  dragging.value = false;
  document.removeEventListener('mousemove', onDrag);
  document.removeEventListener('mouseup', stopDrag);
};

onMounted(() => {
  updateAirplanePosition();
  updateTrailWidth();

  if (airplane.value) {
    airplane.value.addEventListener('mousedown', startDrag);
  }

  window.addEventListener('resize', () => {
    updateAirplanePosition();
    updateTrailWidth();
  });
});
</script>

<style scoped>
.runway-slider-container {
  margin-bottom: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.slider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.runway-slider-label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  color: #eee;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.runway-slider-label i {
  color: #64ffda;
  margin-right: 8px;
}

.percentage-badge {
  background-color: rgba(100, 255, 218, 0.2);
  color: #64ffda;
  font-weight: bold;
  padding: 5px 12px;
  border-radius: 15px;
  font-size: 0.9rem;
  border: 1px solid rgba(100, 255, 218, 0.3);
}

/* Runway Wrapper */
.runway-wrapper {
  position: relative;
  margin-bottom: 20px;
}

/* Runway Markers */
.runway-markers {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.marker {
  text-align: center;
  position: relative;
}

.marker-label {
  font-size: 0.85rem;
  color: #aaa;
  margin-bottom: 3px;
}

.marker-value {
  font-size: 0.75rem;
  color: #64ffda;
  font-weight: 600;
}

.takeoff {
  text-align: left;
}

.landing {
  text-align: right;
}

/* Runway Track */
.runway-track {
  width: 100%;
  height: 60px;
  background-color: #1e2432;
  position: relative;
  cursor: pointer;
  border-radius: 30px;
  overflow: hidden;
  border: 1px solid #35393f;
}

/* Runway Lights */
.runway-lights {
  display: flex;
  justify-content: space-between;
  position: absolute;
  width: 100%;
  height: 100%;
  padding: 0 10px;
  box-sizing: border-box;
  pointer-events: none;
}

.runway-light {
  width: 10px;
  height: 10px;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  margin-top: 25px;
}

.runway-light.active {
  background-color: rgba(100, 255, 218, 0.8);
  box-shadow: 0 0 10px rgba(100, 255, 218, 0.8);
  animation: pulse 2s infinite;
}

/* Hydrogen Trail */
.hydrogen-trail {
  position: absolute;
  height: 100%;
  width: 0;
  background: linear-gradient(90deg,
      rgba(100, 255, 218, 0.1),
      rgba(100, 255, 218, 0.3));
  pointer-events: none;
  transition: width 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Runway Airplane */
.runway-airplane {
  width: 36px;
  height: 36px;
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  cursor: grab;
  z-index: 10;
  transition: transform 0.3s ease;
}

.runway-airplane i {
  font-size: 24px;
  color: #64ffda;
  filter: drop-shadow(0 0 5px rgba(100, 255, 218, 0.8));
}

/* H2 Cloud */
.h2-cloud {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(100, 255, 218, 0.2);
  color: #64ffda;
  padding: 4px 8px;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: bold;
  opacity: 0.9;
  white-space: nowrap;
}

/* Runway Labels */
.runway-labels {
  display: flex;
  justify-content: space-between;
  position: absolute;
  bottom: 5px;
  width: 100%;
  padding: 0 15px;
  box-sizing: border-box;
  pointer-events: none;
}

.runway-end {
  font-size: 0.7rem;
  color: #aaa;
  opacity: 0.7;
}

/* Animations */
@keyframes pulse {
  0% {
    opacity: 1;
    transform: scale(1);
  }

  50% {
    opacity: 0.7;
    transform: scale(1.2);
  }

  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Active state */
.runway-track:hover .h2-cloud {
  animation: float 2s ease-in-out infinite;
}

@keyframes float {

  0%,
  100% {
    transform: translateX(-50%) translateY(0);
  }

  50% {
    transform: translateX(-50%) translateY(-5px);
  }
}

.runway-airplane:active {
  cursor: grabbing;
}
</style>