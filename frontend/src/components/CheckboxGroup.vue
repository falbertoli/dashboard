<!-- File: frontend/src/components/CheckboxGroup.vue -->

<template>
  <div class="checkbox-group-container">
    <div class="checkbox-group-header">
      <label class="checkbox-group-label">
        <i class="fas fa-truck"></i> {{ label }}
      </label>
      <div class="vehicle-counter">{{ selectedCount }}/{{ options.length }} vehicles</div>
    </div>
    <div class="airport-map-container">
      <div class="airport-map">
        <div class="vehicles-grid">
          <label v-for="option in options" :key="option.value"
            :class="['vehicle-item', isChecked(option.value) ? 'vehicle-selected' : '']">
            <input type="checkbox" :value="option.value" :checked="isChecked(option.value)"
              @change="toggleSelection(option.value)" />
            <span class="vehicle-icon">
              <i :class="getVehicleIcon(option.value)"></i>
            </span>
            <span class="vehicle-name">{{ option.text }}</span>
            <span class="h2-indicator" v-if="isChecked(option.value)">H₂</span>
            <div class="runway-connector-left" v-if="isChecked(option.value)"></div>
            <div class="runway-connector-right" v-if="isChecked(option.value)"></div>
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
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
});

const emit = defineEmits(['update:modelValue']);

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

const selectedCount = computed(() => props.modelValue.length);

const getVehicleIcon = (value) => {
  if (value.includes('TUG')) return 'fas fa-truck-pickup';
  if (value.includes('F250')) return 'fas fa-car';
  if (value.includes('F650')) return 'fas fa-truck';
  if (value.includes('Commander')) return 'fas fa-shuttle-van';
  if (value.includes('TLS')) return 'fas fa-dolly';
  if (value.includes('TLD')) return 'fas fa-truck-loading';
  return 'fas fa-truck-moving';
};
</script>

<style scoped>
/* General container */
.checkbox-group-container {
  margin-bottom: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Label styling */
.checkbox-group-label {
  display: block;
  font-size: 1.1rem;
  font-weight: 600;
  color: #eee;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.checkbox-group-label i {
  margin-right: 8px;
  color: #64ffda;
}

/* Header styling */
.checkbox-group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.vehicle-counter {
  background-color: rgba(100, 255, 218, 0.2);
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.9rem;
  color: #64ffda;
  border: 1px solid rgba(100, 255, 218, 0.3);
}

/* Map container */
.airport-map-container {
  position: relative;
  background-color: #1a1e24;
  border-radius: 12px;
  padding: 20px;
  border: 1px dashed #3a3f48;
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.3);
}

.airport-map {
  position: relative;
  min-height: 100px;
}

/* Grid for vehicles */
.vehicles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
  position: relative;
  z-index: 2;
}

/* Vehicle item styling */
.vehicle-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #242830;
  border-radius: 8px;
  padding: 15px 10px;
  transition: all 0.3s ease;
  position: relative;
  cursor: pointer;
  border: 2px solid #383d47;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.vehicle-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  border-color: #4a4f5c;
}

/* Selected vehicle styling */
.vehicle-selected {
  border-color: #64ffda;
  background-color: rgba(100, 255, 218, 0.08);
  box-shadow: 0 0 15px rgba(100, 255, 218, 0.2);
}

/* Runway connectors */
.runway-connector-left,
.runway-connector-right {
  position: absolute;
  top: 50%;
  height: 3px;
  background: repeating-linear-gradient(90deg, #64ffda, #64ffda 5px, transparent 5px, transparent 10px);
  transform: translateY(-50%);
  z-index: 1;
}

.runway-connector-left {
  right: 100%;
  width: 30px;
}

.runway-connector-right {
  left: 100%;
  width: 30px;
}

/* Checkbox styling */
.vehicle-item input[type="checkbox"] {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 18px;
  height: 18px;
  appearance: none;
  background-color: rgba(255, 255, 255, 0.05);
  border: 1px solid #4e5566;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.vehicle-item input[type="checkbox"]:checked {
  background-color: #64ffda;
  border-color: #64ffda;
}

.vehicle-item input[type="checkbox"]:checked::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #1a1e24;
  font-size: 12px;
  font-weight: bold;
}

/* Vehicle icon styling */
.vehicle-icon {
  font-size: 2.2rem;
  margin-bottom: 12px;
  color: #aaa;
  transition: color 0.3s ease;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.03);
  border-radius: 50%;
}

.vehicle-selected .vehicle-icon {
  color: #64ffda;
  text-shadow: 0 0 10px rgba(100, 255, 218, 0.4);
}

/* Vehicle name styling */
.vehicle-name {
  font-size: 0.9rem;
  text-align: center;
  color: #ddd;
  transition: color 0.2s ease;
}

.vehicle-selected .vehicle-name {
  color: #fff;
}

/* H2 indicator styling */
.h2-indicator {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #64ffda;
  color: #1a1e24;
  font-weight: bold;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  box-shadow: 0 0 8px rgba(100, 255, 218, 0.4);
  z-index: 3;
}

/* Animation for selected vehicles */
@keyframes glow {
  0% {
    box-shadow: 0 0 5px rgba(100, 255, 218, 0.2);
  }

  50% {
    box-shadow: 0 0 15px rgba(100, 255, 218, 0.4);
  }

  100% {
    box-shadow: 0 0 5px rgba(100, 255, 218, 0.2);
  }
}

.vehicle-selected {
  animation: glow 2s infinite ease-in-out;
}
</style>