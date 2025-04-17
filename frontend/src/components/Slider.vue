<template>
  <div class="custom-slider-container">
    <label :for="id" class="custom-slider-label">{{ label }}</label>
    <div class="custom-slider-wrapper">
      <div class="custom-slider-track" :id="id" ref="track">
        <div class="custom-slider-thumb" ref="thumb"></div>
        <div class="custom-slider-background" ref="background"></div>
      </div>
      <span class="custom-slider-value">{{ value }}{{ unit }}</span>
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
    default: 10, // Default value
  },
  unit: {
    type: String,
    default: '' // Empty string as default unit
  },
});

const emit = defineEmits(['update:modelValue']);

const value = ref(props.modelValue);
const track = ref(null);
const thumb = ref(null);
const background = ref(null);

watch(
  () => props.modelValue,
  (newVal) => {
    value.value = newVal;
    updateThumbPosition();
    updateTrackBackground();
  }
);

const updateThumbPosition = () => {
  const trackWidth = track.value.offsetWidth;
  const thumbWidth = thumb.value.offsetWidth;
  const maxOffset = trackWidth - thumbWidth;
  const percentage = (value.value - props.min) / (props.max - props.min);
  thumb.value.style.left = `${percentage * maxOffset}px`;
};

const updateTrackBackground = () => {
  const trackWidth = track.value.offsetWidth;
  const thumbWidth = thumb.value.offsetWidth;
  const maxOffset = trackWidth - thumbWidth;
  const percentage = (value.value - props.min) / (props.max - props.min);
  const backgroundWidth = percentage * maxOffset;
  background.value.style.width = `${backgroundWidth}px`;
};

const onThumbDrag = (event) => {
  const trackRect = track.value.getBoundingClientRect();
  const thumbWidth = thumb.value.offsetWidth;
  const maxOffset = trackRect.width - thumbWidth;
  const offsetX = event.clientX - trackRect.left;
  const percentage = Math.min(Math.max(offsetX / maxOffset, 0), 1);
  value.value = Math.round(percentage * (props.max - props.min) + props.min);
  emit('update:modelValue', value.value);
  updateTrackBackground();
};

onMounted(() => {
  updateThumbPosition();
  updateTrackBackground();
  thumb.value.addEventListener('mousedown', () => {
    document.addEventListener('mousemove', onThumbDrag);
    document.addEventListener('mouseup', () => {
      document.removeEventListener('mousemove', onThumbDrag);
    });
  });
});
</script>

<style scoped>
/* General container */
.custom-slider-container {
  margin-bottom: 20px;
}

/* Style for the label */
.custom-slider-label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  /* color: #64ffda; */
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Wrapper for the slider and its value, for better layout control */
.custom-slider-wrapper {
  display: flex;
  align-items: center;
  position: relative;
}

/* Basic styling for the slider track */
.custom-slider-track {
  flex: 1;
  height: 40px;
  background: rgba(100, 255, 218, 0.3);
  position: relative;
  margin-right: 10px;
  border-radius: 20px;
  /* Rounded corners for better appearance */
  overflow: hidden;
  /* Ensure the thumb stays within the track */
}

/* Styling for the slider background */
.custom-slider-background {
  height: 40px;
  background: url('@/assets/images/hydrogen-molecule.png') repeat-x center;
  background-size: contain;
  position: absolute;
  top: 0;
  left: 0;
  transition: width 0.1s ease-in-out;
  /* Smooth transition for background width */
}

/* Styling for the slider thumb */
.custom-slider-thumb {
  width: 40px;
  height: 40px;
  background: url('@/assets/images/airplane.png') no-repeat center;
  background-size: contain;
  position: absolute;
  top: 0;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(100, 255, 218, 0.5), 0 0 20px rgba(100, 255, 218, 0.3);
  transition: left 0.1s ease-in-out;
  /* Smooth transition for thumb movement */
}

/* Styling for the slider value display */
.custom-slider-value {
  font-size: 1rem;
  color: #64ffda;
  width: 60px;
  text-align: right;
  font-weight: bold;
}
</style>