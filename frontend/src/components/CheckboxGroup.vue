<!-- File: frontend/src/components/CheckboxGroup.vue -->

<template>
  <div class="checkbox-group-container">
    <div class="checkbox-group-header">
      <label class="checkbox-group-label">
        <i class="fas fa-truck"></i> {{ label }}
      </label>
      <div class="vehicle-counter">
        <span class="counter-text">{{ selectedCount }}/{{ options.length }}</span>
        <span class="counter-label">vehicles selected</span>
      </div>
    </div>

    <div class="airport-map-container" ref="airportMapRef">
      <!-- Airport runway visualization -->
      <div class="airport-runway">
        <div class="runway-center-line"></div>
        <div class="runway-end left">
          <div class="runway-marker"></div>
          <div class="runway-marker"></div>
        </div>
        <div class="runway-end right">
          <div class="runway-marker"></div>
          <div class="runway-marker"></div>
        </div>
      </div>

      <!-- Control tower -->
      <div class="control-tower">
        <div class="tower-top">
          <div class="tower-window"></div>
        </div>
        <div class="tower-body"></div>
        <div class="tower-base"></div>
      </div>

      <!-- Vehicles grid with categorization -->
      <div class="vehicles-grid">
        <div class="vehicle-category">
          <div class="category-header">
            <i class="fas fa-truck-loading"></i>
            <span>Ground Support Equipment</span>
          </div>

          <div class="category-items">
            <label v-for="option in filteredOptions('TUG', 'TLS', 'TLD')" :key="option.value"
              :class="['vehicle-item', isChecked(option.value) ? 'vehicle-selected' : '']">
              <input type="checkbox" :value="option.value" :checked="isChecked(option.value)"
                @change="toggleSelection(option.value)" />
              <span class="vehicle-icon">
                <i :class="getVehicleIcon(option.value)"></i>
              </span>
              <span class="vehicle-name">{{ option.text }}</span>
              <span class="h2-indicator" v-if="isChecked(option.value)">H₂</span>
              <div class="hydrogen-bubbles" v-if="isChecked(option.value)">
                <div class="bubble bubble-1">H₂</div>
                <div class="bubble bubble-2">H₂</div>
                <div class="bubble bubble-3">H₂</div>
              </div>
              <div class="runway-connector-left" v-if="isChecked(option.value)"></div>
              <div class="runway-connector-right" v-if="isChecked(option.value)"></div>
            </label>
          </div>
        </div>

        <div class="vehicle-category">
          <div class="category-header">
            <i class="fas fa-car"></i>
            <span>Service Vehicles</span>
          </div>

          <div class="category-items">
            <label v-for="option in filteredOptions('F250', 'F650', 'Commander')" :key="option.value"
              :class="['vehicle-item', isChecked(option.value) ? 'vehicle-selected' : '']">
              <input type="checkbox" :value="option.value" :checked="isChecked(option.value)"
                @change="toggleSelection(option.value)" />
              <span class="vehicle-icon">
                <i :class="getVehicleIcon(option.value)"></i>
              </span>
              <span class="vehicle-name">{{ option.text }}</span>
              <span class="h2-indicator" v-if="isChecked(option.value)">H₂</span>
              <div class="hydrogen-bubbles" v-if="isChecked(option.value)">
                <div class="bubble bubble-1">H₂</div>
                <div class="bubble bubble-2">H₂</div>
                <div class="bubble bubble-3">H₂</div>
              </div>
            </label>
          </div>
        </div>

        <div class="vehicle-category">
          <div class="category-header">
            <i class="fas fa-truck-moving"></i>
            <span>Other Equipment</span>
          </div>

          <div class="category-items">
            <label v-for="option in filteredOptions('Other')" :key="option.value"
              :class="['vehicle-item', isChecked(option.value) ? 'vehicle-selected' : '']">
              <input type="checkbox" :value="option.value" :checked="isChecked(option.value)"
                @change="toggleSelection(option.value)" />
              <span class="vehicle-icon">
                <i :class="getVehicleIcon(option.value)"></i>
              </span>
              <span class="vehicle-name">{{ option.text }}</span>
              <span class="h2-indicator" v-if="isChecked(option.value)">H₂</span>
              <div class="hydrogen-bubbles" v-if="isChecked(option.value)">
                <div class="bubble bubble-1">H₂</div>
                <div class="bubble bubble-2">H₂</div>
                <div class="bubble bubble-3">H₂</div>
              </div>
            </label>
          </div>
        </div>
      </div>

      <!-- Quick selection toolbar -->
      <div class="selection-toolbar">
        <button class="toolbar-button select-all" @click="selectAll">
          <i class="fas fa-check-square"></i> Select All Vehicles
        </button>
        <button class="toolbar-button select-none" @click="selectNone">
          <i class="fas fa-square"></i> Clear Selection
        </button>
        <button class="toolbar-button" @click="selectCategory('TUG')">
          <i class="fas fa-truck-pickup"></i> Tugs
        </button>
        <button class="toolbar-button" @click="selectCategory('F')">
          <i class="fas fa-car"></i> Ford Vehicles
        </button>
      </div>

      <!-- Airport terminal illustration -->
      <div class="terminal-building">
        <div class="terminal-roof"></div>
        <div class="terminal-body">
          <div class="terminal-window"></div>
          <div class="terminal-window"></div>
          <div class="terminal-window"></div>
          <div class="terminal-door"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch, ref } from 'vue';

const props = defineProps({
  label: {
    type: String,
    default: 'Ground vehicles to Transition',
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

// Filter options for different categories
const filteredOptions = (...types) => {
  if (types.includes('Other')) {
    // Show options that don't match any of the specific types
    return props.options.filter(option => {
      const value = option.value;
      return !['TUG', 'TLS', 'TLD', 'F250', 'F650', 'Commander'].some(type => value.includes(type));
    });
  }

  // Show options that match any of the specified types
  return props.options.filter(option => {
    const value = option.value;
    return types.some(type => value.includes(type));
  });
};

// Selection actions
const selectAll = () => {
  const allValues = props.options.map(option => option.value);
  emit('update:modelValue', allValues);
};

const selectNone = () => {
  emit('update:modelValue', []);
};

const selectCategory = (category) => {
  const categoryValues = props.options
    .filter(option => option.value.includes(category))
    .map(option => option.value);

  const currentValues = [...props.modelValue];
  const allCategorySelected = categoryValues.every(value => currentValues.includes(value));

  let newValues;
  if (allCategorySelected) {
    // If all are selected, unselect them
    newValues = currentValues.filter(value => !categoryValues.includes(value));
  } else {
    // Otherwise, select all in category (while keeping others selected)
    const valuesToAdd = categoryValues.filter(value => !currentValues.includes(value));
    newValues = [...currentValues, ...valuesToAdd];
  }

  emit('update:modelValue', newValues);
};

// Create reference for the animation elements
const airportMapRef = ref(null);
const hydrogenMolecules = ref([]);
const maxMolecules = 15;

// Create a fueling station element
const createFuelingStation = () => {
  const fuelingStation = document.createElement('div');
  fuelingStation.className = 'fueling-station';

  const stationBase = document.createElement('div');
  stationBase.className = 'station-base';

  const stationPump = document.createElement('div');
  stationPump.className = 'station-pump';

  const stationDisplay = document.createElement('div');
  stationDisplay.className = 'station-display';

  const stationNozzle = document.createElement('div');
  stationNozzle.className = 'station-nozzle';

  stationPump.appendChild(stationDisplay);
  stationPump.appendChild(stationNozzle);
  fuelingStation.appendChild(stationBase);
  fuelingStation.appendChild(stationPump);

  return fuelingStation;
};

// Create the hydrogen network
const createHydrogenNetwork = () => {
  const networkContainer = document.createElement('div');
  networkContainer.className = 'hydrogen-network';

  // Create SVG for paths
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', '100%');
  svg.setAttribute('height', '100%');
  svg.style.position = 'absolute';
  svg.style.top = '0';
  svg.style.left = '0';
  svg.style.pointerEvents = 'none';

  networkContainer.appendChild(svg);
  return { networkContainer, svg };
};

// Create a dancing H₂ molecule
const createMolecule = (startX, startY, endX, endY) => {
  const molecule = document.createElement('div');
  molecule.className = 'molecule';
  molecule.innerHTML = '<span>H₂</span>';

  // Set explicit positioning
  molecule.style.position = 'absolute';
  molecule.style.left = `${startX}px`;
  molecule.style.top = `${startY}px`;

  // Calculate distance for animation
  const tx = endX - startX;
  const ty = endY - startY;

  // Set animation properties explicitly
  molecule.style.setProperty('--tx', `${tx}px`);
  molecule.style.setProperty('--ty', `${ty}px`);

  // Randomize animation parameters
  const duration = 8 + Math.random() * 7; // 8-15 seconds
  molecule.style.setProperty('--duration', `${duration}s`);

  const delay = Math.random() * 2;
  molecule.style.animationDelay = `${delay}s`;

  return molecule;
}

// Update network paths connecting vehicles to runway
const updateNetworkPaths = (selectedVehicles, svg) => {
  // Clear existing paths
  while (svg.firstChild) {
    svg.removeChild(svg.firstChild);
  }

  // Get runway position
  const runway = document.querySelector('.airport-runway');
  if (!runway) return;

  const runwayRect = runway.getBoundingClientRect();
  const containerRect = airportMapRef.value.getBoundingClientRect();

  const runwayY = runwayRect.top - containerRect.top + runwayRect.height / 2;
  const runwayLeft = runwayRect.left - containerRect.left;
  const runwayRight = runwayLeft + runwayRect.width;

  // Create paths from each selected vehicle to the runway
  selectedVehicles.forEach(vehicle => {
    const vehicleElem = document.querySelector(`.vehicle-item[data-value="${vehicle}"]`);
    if (!vehicleElem) return;

    const vehicleRect = vehicleElem.getBoundingClientRect();
    const vehicleX = vehicleRect.left - containerRect.left + vehicleRect.width / 2;
    const vehicleY = vehicleRect.top - containerRect.top + vehicleRect.height / 2;

    // Determine if vehicle is above or below runway
    const isAbove = vehicleY < runwayY;

    // Create path
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.classList.add('network-path');

    // Calculate control points for bezier curve
    const controlX = vehicleX;
    const controlY = isAbove ?
      runwayY - 30 :
      runwayY + 30;

    // Draw path
    let d;
    if (vehicleX < runwayLeft) {
      // Connect to left side of runway
      d = `M ${vehicleX} ${vehicleY} Q ${controlX} ${controlY}, ${runwayLeft} ${runwayY}`;
    } else if (vehicleX > runwayRight) {
      // Connect to right side of runway
      d = `M ${vehicleX} ${vehicleY} Q ${controlX} ${controlY}, ${runwayRight} ${runwayY}`;
    } else {
      // Connect directly to runway below/above
      d = `M ${vehicleX} ${vehicleY} L ${vehicleX} ${runwayY}`;
    }

    path.setAttribute('d', d);
    svg.appendChild(path);
  });
};

// Create and position random H₂ molecules
const createMolecules = () => {
  if (!airportMapRef.value) return;

  // First, remove any existing molecule container
  const existingContainer = airportMapRef.value.querySelector('.molecules-container');
  if (existingContainer) {
    airportMapRef.value.removeChild(existingContainer);
  }

  // Clear reference array
  hydrogenMolecules.value = [];

  // Only create molecules if there are selected vehicles
  if (props.modelValue.length === 0) return;

  // Create container with proper positioning
  const moleculesContainer = document.createElement('div');
  moleculesContainer.className = 'molecules-container';
  airportMapRef.value.appendChild(moleculesContainer);

  const containerRect = airportMapRef.value.getBoundingClientRect();
  const runway = airportMapRef.value.querySelector('.airport-runway');

  if (!runway) return;

  const runwayRect = runway.getBoundingClientRect();
  const runwayY = runwayRect.top - containerRect.top + runwayRect.height / 2;

  // Create molecules with better positioning calculation
  for (let i = 0; i < maxMolecules; i++) {
    // More precise positioning
    const startX = Math.random() * (runwayRect.width - 40) + (runwayRect.left - containerRect.left) + 20;
    const startY = runwayY - 5; // Slightly adjust vertical position

    // Keep molecules within safer bounds
    const safeAreaHeight = containerRect.height * 0.6;
    const endX = Math.random() * (containerRect.width - 60) + 30;
    const endY = Math.random() * safeAreaHeight + 30;

    const molecule = createMolecule(startX, startY, endX, endY);
    moleculesContainer.appendChild(molecule);
    hydrogenMolecules.value.push(molecule);
  }
};


// Initialize dynamic elements
onMounted(() => {
  if (!airportMapRef.value) return;

  // Add data-value attributes to vehicle items for easier selection
  const vehicleItems = document.querySelectorAll('.vehicle-item');
  vehicleItems.forEach(item => {
    const checkbox = item.querySelector('input[type="checkbox"]');
    if (checkbox) {
      item.setAttribute('data-value', checkbox.value);
    }
  });

  // Create and add fueling station
  const fuelingStation = createFuelingStation();
  airportMapRef.value.appendChild(fuelingStation);

  // Create and add hydrogen network
  const { networkContainer, svg } = createHydrogenNetwork();
  airportMapRef.value.appendChild(networkContainer);

  // Initialize network paths and molecules
  updateNetworkPaths(props.modelValue, svg);
  createMolecules();

  // Watch for changes in selection
  watch(() => props.modelValue, (newValue) => {
    updateNetworkPaths(newValue, svg);

    // Recreate all molecules to ensure proper cleanup
    createMolecules();

    // Toggle visibility of fueling station based on selection
    if (newValue.length > 0) {
      fuelingStation.style.display = 'block';
    } else {
      fuelingStation.style.display = 'none';
    }
  }, { deep: true });
});
</script>

<style scoped>
/* Base container styling */
.checkbox-group-container {
  margin-bottom: 30px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Header styling with improved counter */
.checkbox-group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.checkbox-group-label {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  font-weight: 600;
  color: #eee;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.checkbox-group-label i {
  margin-right: 8px;
  color: #64ffda;
  font-size: 1.2rem;
}

.vehicle-counter {
  background: linear-gradient(135deg, rgba(100, 255, 218, 0.15), rgba(100, 255, 218, 0.05));
  padding: 5px 15px;
  border-radius: 20px;
  border: 1px solid rgba(100, 255, 218, 0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.counter-text {
  font-size: 1.1rem;
  font-weight: 700;
  color: #64ffda;
}

.counter-label {
  font-size: 0.7rem;
  color: #aaa;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Enhanced airport map container */
.airport-map-container {
  position: relative;
  background-color: #12151e;
  border-radius: 12px;
  padding: 30px 20px;
  box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.4);
  overflow: hidden;
  border: 1px solid #2c3040;
}

/* Airport runway visualization */

.runway-end {
  position: absolute;
  width: 30px;
  height: 100%;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.runway-end.left {
  left: 5px;
}

.runway-end.right {
  right: 5px;
}

.runway-marker {
  width: 5px;
  height: 15px;
  background-color: #64ffda;
  box-shadow: 0 0 10px rgba(100, 255, 218, 0.7);
}

/* Enhanced Runway Animations */
.airport-runway {
  position: absolute;
  width: 90%;
  height: 30px;
  background-color: #1a1e27;
  left: 5%;
  top: 70px;
  border-radius: 15px;
  z-index: 1;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}

.runway-center-line {
  position: absolute;
  width: 100%;
  height: 2px;
  background: repeating-linear-gradient(90deg, #ddd, #ddd 15px, transparent 15px, transparent 30px);
  top: 50%;
  transform: translateY(-50%);
  animation: runway-dash 20s linear infinite;
}

@keyframes runway-dash {
  0% {
    background-position: 0 0;
  }

  100% {
    background-position: 60px 0;
  }
}

.runway-end.left .runway-marker,
.runway-end.right .runway-marker {
  width: 5px;
  height: 15px;
  background-color: #64ffda;
  box-shadow: 0 0 10px rgba(100, 255, 218, 0.7);
  animation: marker-pulse 2s ease-in-out infinite alternate;
}

.runway-end.left .runway-marker:nth-child(2),
.runway-end.right .runway-marker:nth-child(2) {
  animation-delay: 1s;
}

@keyframes marker-pulse {
  0% {
    opacity: 0.5;
    height: 12px;
  }

  100% {
    opacity: 1;
    height: 18px;
  }
}

/* Control tower */
.tower-body {
  width: 10px;
  height: 35px;
  background-color: #3d4251;
  margin: 0 auto;
}

.tower-base {
  width: 20px;
  height: 5px;
  background-color: #2c3040;
  margin: 0 auto;
  border-radius: 2px;
}

/* Enhanced Control Tower Animations */
.control-tower {
  position: absolute;
  top: 20px;
  right: 40px;
  z-index: 2;
  filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.5));
  animation: tower-sway 10s ease-in-out infinite;
}

@keyframes tower-sway {

  0%,
  100% {
    transform: rotate(0deg);
  }

  25% {
    transform: rotate(1deg);
  }

  75% {
    transform: rotate(-1deg);
  }
}

.tower-top {
  width: 40px;
  height: 20px;
  background-color: #64ffda;
  border-radius: 20px 20px 0 0;
  position: relative;
  overflow: hidden;
}

.tower-window {
  position: absolute;
  width: 30px;
  height: 10px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.3), rgba(255, 255, 255, 0.1));
  border-radius: 10px;
  top: 5px;
  left: 5px;
  animation: window-pulse 4s ease-in-out infinite;
}

@keyframes window-pulse {

  0%,
  100% {
    opacity: 0.3;
  }

  50% {
    opacity: 0.8;
  }
}

/* Radar on top of control tower */
.tower-top::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 2px;
  background-color: #333;
  top: 2px;
  left: 10px;
  transform-origin: 50% 100%;
  animation: radar-spin 4s linear infinite;
}

@keyframes radar-spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* Terminal building */

.terminal-roof {
  width: 120px;
  height: 10px;
  background-color: #3d4251;
  border-radius: 5px 5px 0 0;
}

.terminal-body {
  width: 120px;
  height: 30px;
  background-color: #2c3040;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 0 5px;
}

/* Enhanced Terminal Building Animations */
.terminal-building {
  position: absolute;
  bottom: 15px;
  left: 30px;
  z-index: 2;
  filter: drop-shadow(0 5px 10px rgba(0, 0, 0, 0.4));
}

.terminal-window {
  width: 10px;
  height: 15px;
  background: rgba(100, 255, 218, 0.2);
  border-radius: 2px;
  animation: window-flicker 5s infinite;
}

.terminal-window:nth-child(2) {
  animation-delay: 1.5s;
}

.terminal-window:nth-child(3) {
  animation-delay: 3s;
}

@keyframes window-flicker {

  0%,
  100% {
    background: rgba(100, 255, 218, 0.2);
  }

  50% {
    background: rgba(100, 255, 218, 0.5);
  }
}

.terminal-door {
  width: 15px;
  height: 20px;
  background: rgba(100, 255, 218, 0.3);
  border-radius: 2px;
  position: relative;
  overflow: hidden;
}

.terminal-door::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, transparent 0%, rgba(100, 255, 218, 0.2) 50%, transparent 100%);
  animation: door-scan 3s ease-in-out infinite;
}

@keyframes door-scan {

  0%,
  100% {
    transform: translateY(-100%);
  }

  50% {
    transform: translateY(100%);
  }
}

/* Categorized vehicles grid */
.vehicles-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  position: relative;
  z-index: 5;
  margin-top: 80px;
  margin-bottom: 15px;
}

.vehicle-category {
  flex: 1;
  min-width: 260px;
  background-color: rgba(255, 255, 255, 0.03);
  border-radius: 10px;
  overflow: hidden;
  z-index: 5;
}

.category-header {
  background-color: rgba(100, 255, 218, 0.1);
  padding: 10px 15px;
  font-weight: 600;
  color: #64ffda;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid rgba(100, 255, 218, 0.2);
}

.category-header i {
  font-size: 0.9rem;
}

.category-items {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 15px;
  padding: 15px;
}

/* Enhanced vehicle item styling */
.vehicle-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #1e222c;
  border-radius: 10px;
  padding: 15px 10px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  cursor: pointer;
  border: 2px solid #35393f;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  z-index: 5;
}

.vehicle-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  border-color: rgba(100, 255, 218, 0.5);
}

.vehicle-item::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, transparent, #64ffda, transparent);
  transform: scaleX(0);
  transition: transform 0.5s ease;
}

.vehicle-item:hover::before {
  transform: scaleX(1);
}

/* Improved selected vehicle styling */
.vehicle-selected {
  border-color: #64ffda;
  background: linear-gradient(135deg, rgba(100, 255, 218, 0.15), rgba(100, 255, 218, 0.05));
  box-shadow: 0 0 20px rgba(100, 255, 218, 0.2);
  transform: translateY(-5px);
}

/* Improved hydrogen indicator */
.h2-indicator {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #64ffda, #4fc3c3);
  color: #12151e;
  font-weight: bold;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  box-shadow: 0 0 15px rgba(100, 255, 218, 0.6);
  z-index: 5;
}

/* Hydrogen bubbles animation */
.hydrogen-bubbles {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: visible;
  z-index: 4;
}

.bubble {
  position: absolute;
  background-color: rgba(100, 255, 218, 0.15);
  border: 1px solid rgba(100, 255, 218, 0.3);
  color: rgba(100, 255, 218, 0.8);
  font-size: 0.6rem;
  font-weight: bold;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  animation: float 4s ease-in infinite;
}

.bubble-1 {
  left: 20%;
  bottom: 10px;
  animation-delay: 0s;
}

.bubble-2 {
  left: 50%;
  bottom: 10px;
  animation-delay: 1s;
}

.bubble-3 {
  left: 70%;
  bottom: 10px;
  animation-delay: 2s;
}

@keyframes float {
  0% {
    opacity: 0;
    transform: translateY(0);
  }

  10% {
    opacity: 1;
  }

  90% {
    opacity: 1;
  }

  100% {
    opacity: 0;
    transform: translateY(-60px);
  }
}

.hydrogen-bubbles .bubble {
  position: absolute;
  background-color: rgba(100, 255, 218, 0.15);
  border: 1px solid rgba(100, 255, 218, 0.3);
  color: rgba(100, 255, 218, 0.8);
  font-size: 0.6rem;
  font-weight: bold;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  animation: float 4s ease-in infinite;
  overflow: hidden;
}

/* Enhanced Runway Connectors */
.runway-connector-left,
.runway-connector-right {
  position: absolute;
  top: 50%;
  height: 3px;
  transform: translateY(-50%);
  z-index: 1;
}

.runway-connector-left {
  right: 100%;
  width: 0;
  /* Start with 0 width */
  background: linear-gradient(90deg, transparent, #64ffda);
  animation: connector-extend-left 1s forwards, pulse-left 2s infinite 1s;
}

.runway-connector-right {
  left: 100%;
  width: 0;
  /* Start with 0 width */
  background: linear-gradient(90deg, #64ffda, transparent);
  animation: connector-extend-right 1s forwards, pulse-right 2s infinite 1s;
}

@keyframes connector-extend-left {
  0% {
    width: 0;
  }

  100% {
    width: 50px;
  }
}

@keyframes connector-extend-right {
  0% {
    width: 0;
  }

  100% {
    width: 50px;
  }
}

@keyframes pulse-left {

  0%,
  100% {
    background: linear-gradient(90deg, transparent, #64ffda);
    opacity: 0.7;
  }

  50% {
    background: linear-gradient(90deg, #64ffda, #64ffda);
    opacity: 1;
  }
}

@keyframes pulse-right {

  0%,
  100% {
    background: linear-gradient(90deg, #64ffda, transparent);
    opacity: 0.7;
  }

  50% {
    background: linear-gradient(90deg, #64ffda, #64ffda);
    opacity: 1;
  }
}

/* Enhanced checkbox styling */
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
  transition: all 0.3s ease;
  z-index: 5;
}

.vehicle-item input[type="checkbox"]:checked {
  background-color: #64ffda;
  border-color: #64ffda;
  box-shadow: 0 0 10px rgba(100, 255, 218, 0.7);
}

.vehicle-item input[type="checkbox"]:checked::after {
  content: '✓';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #12151e;
  font-size: 12px;
  font-weight: bold;
}

/* Enhanced vehicle icon styling */
.vehicle-icon {
  font-size: 2.2rem;
  margin-bottom: 15px;
  color: #aaa;
  transition: all 0.3s ease;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 50%;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.2);
}

.vehicle-selected .vehicle-icon {
  color: #64ffda;
  text-shadow: 0 0 10px rgba(100, 255, 218, 0.6);
  transform: scale(1.1);
  background: radial-gradient(circle, rgba(100, 255, 218, 0.15), rgba(100, 255, 218, 0.05));
}

.vehicle-icon i {
  transition: transform 0.5s ease;
}

.vehicle-selected .vehicle-icon i {
  animation: wiggle 2s ease-in-out infinite;
}

@keyframes wiggle {

  0%,
  100% {
    transform: rotate(0deg);
  }

  25% {
    transform: rotate(-10deg);
  }

  75% {
    transform: rotate(10deg);
  }
}



/* Enhanced vehicle name styling */
.vehicle-name {
  font-size: 0.9rem;
  text-align: center;
  color: #ddd;
  transition: color 0.3s ease;
  font-weight: 500;
  max-width: 90%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.vehicle-selected .vehicle-name {
  color: #fff;
  font-weight: 600;
}

/* Pulse ring effect for selected vehicles */
.vehicle-selected::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  border-radius: 10px;
  border: 2px solid rgba(100, 255, 218, 0.5);
  transform: translate(-50%, -50%);
  animation: pulse-ring 2s infinite;
  pointer-events: none;
}

@keyframes pulse-ring {
  0% {
    width: 100%;
    height: 100%;
    opacity: 1;
  }

  100% {
    width: 130%;
    height: 130%;
    opacity: 0;
  }
}

/* Selection toolbar */
.selection-toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
  background-color: rgba(0, 0, 0, 0.2);
  padding: 15px;
  border-radius: 8px;
  justify-content: center;
  position: relative;
  z-index: 6;
}

.toolbar-button {
  background-color: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 6px;
  padding: 8px 15px;
  color: #aaa;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.toolbar-button:hover {
  background-color: rgba(100, 255, 218, 0.1);
  color: #64ffda;
  transform: translateY(-2px);
}

.toolbar-button.select-all {
  background-color: rgba(100, 255, 218, 0.1);
  color: #64ffda;
}

.toolbar-button.select-none {
  background-color: rgba(255, 255, 255, 0.05);
}

.toolbar-button i {
  font-size: 0.9rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .vehicles-grid {
    flex-direction: column;
  }

  .category-items {
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  }

  .control-tower {
    display: none;
  }

  .terminal-building {
    display: none;
  }

  .selection-toolbar {
    flex-direction: column;
    align-items: stretch;
  }
}

@media (max-width: 480px) {
  .vehicle-category {
    min-width: 100%;
  }

  .category-items {
    grid-template-columns: repeat(2, 1fr);
  }

  .checkbox-group-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .vehicle-counter {
    align-self: flex-start;
  }
}

/* Add hydrogen network paths conditionally when vehicles are selected */
.hydrogen-network {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.network-path {
  stroke: rgba(100, 255, 218, 0.3);
  stroke-width: 2;
  stroke-dasharray: 5;
  fill: none;
  animation: flow-path 4s linear infinite;
}

@keyframes flow-path {
  to {
    stroke-dashoffset: -20;
  }
}

/* Hydrogen fueling station that animates when vehicles are selected */
.fueling-station {
  position: absolute;
  right: 120px;
  bottom: 30px;
  width: 40px;
  height: 50px;
  z-index: 3;
}

.station-base {
  width: 40px;
  height: 15px;
  background-color: #3d4251;
  border-radius: 4px;
  position: absolute;
  bottom: 0;
}

.station-pump {
  width: 20px;
  height: 35px;
  background-color: #2c3040;
  position: absolute;
  bottom: 15px;
  left: 10px;
  border-radius: 4px 4px 0 0;
}

.station-display {
  width: 16px;
  height: 10px;
  background-color: rgba(100, 255, 218, 0.3);
  position: absolute;
  top: 5px;
  left: 2px;
  border-radius: 2px;
  animation: display-pulse 1s ease-in-out infinite alternate;
}

@keyframes display-pulse {
  0% {
    background-color: rgba(100, 255, 218, 0.3);
  }

  100% {
    background-color: rgba(100, 255, 218, 0.8);
  }
}

.station-nozzle {
  width: 10px;
  height: 20px;
  background-color: #64ffda;
  position: absolute;
  top: 20px;
  left: 5px;
  border-radius: 5px;
  overflow: hidden;
}

.station-nozzle::after {
  content: 'H₂';
  position: absolute;
  color: #12151e;
  font-size: 8px;
  font-weight: bold;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Dancing H₂ molecules */
.molecules-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
  z-index: 2;
  /* Above runway but below UI elements */
}

.molecule {
  position: absolute;
  pointer-events: none;
  z-index: 2;
  animation: float-molecule var(--duration, 10s) linear forwards;
  animation-delay: var(--delay, 0s);
}

.molecule span {
  display: inline-block;
  font-size: 12px;
  color: #64ffda;
  text-shadow: 0 0 5px rgba(100, 255, 218, 0.7);
  background-color: rgba(18, 21, 30, 0.6);
  border-radius: 50%;
  padding: 3px;
  font-weight: bold;
}

/* Update animation for molecules */
@keyframes float-molecule {
  0% {
    transform: translate(0, 0);
    opacity: 0;
  }

  10% {
    opacity: 1;
  }

  90% {
    opacity: 1;
  }

  100% {
    transform: translate(var(--tx), var(--ty));
    opacity: 0;
  }
}
</style>