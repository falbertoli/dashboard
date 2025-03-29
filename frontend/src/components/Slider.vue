<!-- File: frontend/src/components/Slider.vue -->

<template>
  <div class="slider-container">
    <label :for="id" class="slider-label">{{ label }}</label>
    <div class="slider-wrapper">
      <input type="range" :id="id" :min="min" :max="max" :step="step" v-model.number="value" @input="emitValue"
        class="slider-input" />
      <span class="slider-value">{{ value }}{{ unit }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

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

watch(
  () => props.modelValue,
  (newVal) => {
    value.value = newVal;
  }
);

const emitValue = (event) => {
  console.log(`Slider: emitting update:modelValue with value ${parseInt(event.target.value)}`);
  emit('update:modelValue', parseInt(event.target.value));
};
</script>

<style scoped>
/* General container */
.slider-container {
  margin-bottom: 20px;
}

/* Style for the label */
.slider-label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  color: #eee;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Wrapper for the slider and its value, for better layout control */
.slider-wrapper {
  display: flex;
  align-items: center;
}

/* Basic styling for the range input */
.slider-input {
  flex: 1;
  height: 8px;
  border-radius: 6px;
  background: #444;
  outline: none;
  -webkit-transition: .2s;
  transition: opacity .2s;
  margin-right: 10px;
}

/* Hover effect */
.slider-input:hover {
  opacity: 0.8;
}

/* Thumb styling for WebKit browsers */
.slider-input::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #64ffda;
  cursor: pointer;
  border: none;
  box-shadow: 0 0 5px rgba(100, 255, 218, 0.5);
}

/* Thumb styling for Firefox */
.slider-input::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #64ffda;
  cursor: pointer;
  border: none;
  box-shadow: 0 0 5px rgba(100, 255, 218, 0.5);
}

/* Styling for the slider value display */
.slider-value {
  font-size: 1rem;
  color: #ddd;
  width: 60px;
  text-align: right;
}
</style>