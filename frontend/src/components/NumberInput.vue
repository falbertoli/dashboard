<!-- File: frontend/src/components/NumberInput.vue -->

<template>
  <div class="number-input">
    <label :for="id">{{ label }}</label>
    <div class="input-container">
      <button class="decrement" @click="decrement" :disabled="modelValue <= min">-</button>
      <input :id="id" type="number" :min="min" :max="max" :step="step" v-model.number="value" @change="updateValue" />
      <button class="increment" @click="increment" :disabled="modelValue >= max">+</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';

const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  },
  label: {
    type: String,
    default: ''
  },
  min: {
    type: Number,
    default: 0
  },
  max: {
    type: Number,
    default: 100
  },
  step: {
    type: Number,
    default: 1
  }
});

const emit = defineEmits(['update:modelValue']);

// Generate a unique ID for the input
const id = computed(() => `number-input-${Math.random().toString(36).substring(2, 9)}`);

// Create a local value that syncs with the model value
const value = ref(props.modelValue);

// Watch for changes in the model value
watch(() => props.modelValue, (newValue) => {
  value.value = newValue;
});

// Update the model value when the local value changes
const updateValue = () => {
  let newValue = Number(value.value);

  // Ensure the value is within min/max bounds
  if (newValue < props.min) newValue = props.min;
  if (newValue > props.max) newValue = props.max;

  emit('update:modelValue', newValue);
};

// Increment the value
const increment = () => {
  if (props.modelValue < props.max) {
    emit('update:modelValue', props.modelValue + props.step);
  }
};

// Decrement the value
const decrement = () => {
  if (props.modelValue > props.min) {
    emit('update:modelValue', props.modelValue - props.step);
  }
};
</script>

<style scoped>
.number-input {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  color: #aaa;
  font-size: 0.9rem;
}

.input-container {
  display: flex;
  height: 40px;
}

input {
  flex: 1;
  text-align: center;
  background-color: #1e2128;
  color: #fff;
  border: 1px solid #444;
  border-radius: 0;
  padding: 0.5rem;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #64ffda;
}

button {
  width: 40px;
  background-color: #282c34;
  color: #64ffda;
  border: 1px solid #444;
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

button.decrement {
  border-radius: 4px 0 0 4px;
  border-right: none;
}

button.increment {
  border-radius: 0 4px 4px 0;
  border-left: none;
}

button:hover:not(:disabled) {
  background-color: #323742;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Hide spinner buttons in number input */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
  appearance: textfield;
  /* Add this line */
}
</style>