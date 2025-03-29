<!-- File: frontend/src/components/CheckboxGroup.vue -->

<template>
  <div class="checkbox-group-container">
    <label class="checkbox-group-label">{{ label }}</label>
    <div class="checkbox-group">
      <label v-for="option in options" :key="option.value" class="checkbox-item">
        <input type="checkbox" :value="option.value" :checked="isChecked(option.value)"
          @change="toggleSelection(option.value)" />
        <span>{{ option.text }}</span>
      </label>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';

export default {
  name: 'CheckboxGroup',
  props: {
    label: {
      type: String,
      default: '',
    },
    options: {
      type: Array,
      required: true,
      validator: (options) => {
        return options.every(option => typeof option === 'object' && option !== null && 'value' in option && 'text' in option);
      }
    },
    modelValue: {
      type: Array,
      default: () => [],
    },
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const isChecked = (value) => {
      return props.modelValue.includes(value);
    };

    const toggleSelection = (value) => {
      let newValues = [...props.modelValue];
      if (isChecked(value)) {
        newValues = newValues.filter(item => item !== value);
      } else {
        newValues.push(value);
      }
      emit('update:modelValue', newValues);
    };

    return { isChecked, toggleSelection };
  },
};
</script>

<style scoped>
/* General container */
.checkbox-group-container {
  margin-bottom: 20px;
}

/* Label styling */
.checkbox-group-label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  color: #eee;
  /* Light gray, futuristic */
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Container for checkboxes */
.checkbox-group {
  display: flex;
  flex-direction: column;
}

/* Individual checkbox item */
.checkbox-item {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  margin-bottom: 8px;
  background-color: #282c34;
  /* Dark background */
  border-radius: 6px;
  transition: background-color 0.3s ease;
  color: #fff;
  /* White text */
  border: 1px solid #444;
}

.checkbox-item:hover {
  background-color: #383e4b;
  /* Lighter dark on hover */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

/* Style for the checkbox input */
.checkbox-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin-right: 8px;
  appearance: none;
  background-color: #222;
  border: 1px solid #666;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.2s ease, border-color 0.2s ease;
  position: relative;
  outline: none;
}

/* Checked state of the checkbox */
.checkbox-item input[type="checkbox"]:checked {
  background-color: #64ffda;
  /* Cyan when checked */
  border-color: #64ffda;
}

/* Add a checkmark using pseudo-element */
.checkbox-item input[type="checkbox"]:checked::before {
  content: '\2713';
  /* Unicode checkmark */
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 14px;
  color: #111;
  /* Dark color for the check */
}

/* Style the span holding the text */
.checkbox-item span {
  font-size: 1rem;
  color: #ddd;
  transition: color 0.3s ease;
}

.checkbox-item:hover span {
  color: #fff;
  /* Lighten text on hover */
}
</style>