<!-- File: frontend/src/components/Dropdown.vue -->

<template>
  <div class="dropdown-container">
    <label :for="id" class="dropdown-label">{{ label }}</label>
    <select :id="id" v-model="value" @change="emitValue" class="dropdown-select">
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.text }}
      </option>
    </select>
  </div>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  name: 'Dropdown',
  props: {
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
      type: [String, Number, Boolean, Object, Array],
      default: null,
    },
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const value = ref(props.modelValue);

    watch(
      () => props.modelValue,
      (newVal) => {
        value.value = newVal;
      }
    );

    const emitValue = (event) => {
      console.log(`Dropdown: emitting update:modelValue with value ${parseInt(event.target.value)}`);
      emit('update:modelValue', parseInt(event.target.value));
    };

    return { value, emitValue };
  },
};
</script>

<style scoped>
/* Container for the dropdown */
.dropdown-container {
  margin-bottom: 20px;
  width: 100%;
}

/* Style for the label */
.dropdown-label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  color: #eee;
  /* Light gray, futuristic */
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Basic styling for the select element */
.dropdown-select {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: none;
  /* Remove default border */
  border-radius: 6px;
  background-color: #282c34;
  /* Dark background */
  color: #ddd;
  /* Light text */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  /* Stronger shadow */
  transition: border-color 0.3s, box-shadow 0.3s;
  appearance: none;
  /* Remove default arrow */
  -webkit-appearance: none;
  /* Safari */
  padding-right: 25px;
  /* Make space for custom arrow */
  position: relative;
}

/* Add a custom arrow */
.dropdown-select::after {
  content: '\25BC';
  /* Down arrow Unicode */
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  color: #64ffda;
  /* Cyan arrow */
  pointer-events: none;
  /* Make the arrow unclickable */
}

/* Hover and focus states */
.dropdown-select:hover,
.dropdown-select:focus {
  border-color: #64ffda;
  /* Cyan border on focus */
  box-shadow: 0 3px 7px rgba(0, 0, 0, 0.4);
  /* Stronger shadow on focus */
  outline: none;
  /* Remove default focus outline */
}

/* Style for the options */
.dropdown-select option {
  padding: 8px 10px;
  font-size: 0.9rem;
  background-color: #282c34;
  color: #ddd;
}

/* Selected option */
.dropdown-select option:checked {
  color: #111;
}
</style>