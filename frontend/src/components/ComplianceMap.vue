<!-- File: frontend/src/components/ComplianceMap.vue -->

<template>
  <div class="compliance-map">
    <div class="header-section">
      <h2>Hydrogen Storage Compliance Map</h2>
      <p class="subtitle">Interactive visualization of hydrogen storage requirements and safety zones</p>
    </div>

    <!-- Alert shown when hydrogen/storage calculations aren't done -->
    <div v-if="!storageStore.totalH2VolumeGallons || !storageStore.results" class="alert info">
      <i class="fas fa-info-circle"></i>
      <span>Please configure hydrogen demand and storage calculations first.</span>
    </div>

    <!-- Loading state -->
    <div v-else-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading compliance data...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="alert error">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ error }}</p>
    </div>

    <div v-else class="result">

      <!-- Dashboard Section -->
      <div class="dashboard">
        <div class="card metrics-card">
          <h3><i class="fas fa-chart-line"></i> Storage Metrics</h3>
          <div class="metrics-grid">
            <div class="metric-item">
              <div class="metric-icon"><i class="fas fa-gas-pump"></i></div>
              <div class="metric-content">
                <div class="metric-label">Total H₂ Demand</div>
                <div class="metric-value">{{ $formatNumber(storageStore.totalH2VolumeGallons) }} gallons</div>
              </div>
            </div>
            <div class="metric-item">
              <div class="metric-icon"><i class="fas fa-ruler-combined"></i></div>
              <div class="metric-content">
                <div class="metric-label">Storage Footprint</div>
                <div class="metric-value">{{ $formatNumber(storageStore.totalFootprint) }} ft²</div>
              </div>
            </div>
            <div class="metric-item">
              <div class="metric-icon"><i class="fas fa-cube"></i></div>
              <div class="metric-content">
                <div class="metric-label">Tank Dimensions</div>
                <div class="metric-value">{{ $formatNumber(storageStore.tankDiameter) }} ft × {{
                  storageStore.tankLength.toFixed(2) }} ft</div>
              </div>
            </div>
            <div class="metric-item">
              <div class="metric-icon"><i class="fas fa-boxes"></i></div>
              <div class="metric-content">
                <div class="metric-label">Number of Tanks</div>
                <div class="metric-value">{{ storageStore.recommendedTankCount }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="card compliance-card">
          <h3><i class="fas fa-check-circle"></i> Compliance Status</h3>
          <div class="compliance-status-grid">
            <div class="status-item" :class="freeSpaceStatus.includes('Sufficient') ? 'status-ok' : 'status-warning'">
              <div class="status-icon">
                <i
                  :class="freeSpaceStatus.includes('Sufficient') ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle'"></i>
              </div>
              <div class="status-content">
                <div class="status-label">Free Space</div>
                <div class="status-value">{{ freeSpaceStatus }}</div>
              </div>
            </div>
            <div class="status-item" :class="deicingStatus.includes('Sufficient') ? 'status-ok' : 'status-warning'">
              <div class="status-icon">
                <i
                  :class="deicingStatus.includes('Sufficient') ? 'fas fa-check-circle' : 'fas fa-exclamation-triangle'"></i>
              </div>
              <div class="status-content">
                <div class="status-label">Deicing Area</div>
                <div class="status-value">{{ deicingStatus }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Map Controls Section -->
      <div class="map-controls">
        <div class="control-panel">
          <div class="filter-group">
            <label for="function-filter">
              <i class="fas fa-filter"></i> Filter by Amenity
            </label>
            <select id="function-filter" :value="selectedFunction" @change="handleFilterChange" class="select-control">
              <option value="storage">Free Space and Deicing Only</option>
              <option value="">All Amenities</option>
              <option v-for="functionType in filteredDropdownOptions" :key="functionType" :value="functionType">
                {{ functionType }}
              </option>
            </select>
          </div>

          <div class="layer-toggles">
            <div class="toggle-item">
              <label class="toggle">
                <input type="checkbox" v-model="layerControls.facilities" @change="toggleLayer('facilities')">
                <span class="toggle-slider"></span>
              </label>
              <span>Facilities</span>
            </div>
            <div class="toggle-item">
              <label class="toggle">
                <input type="checkbox" v-model="layerControls.bufferZones" @change="toggleLayer('bufferZones')">
                <span class="toggle-slider"></span>
              </label>
              <span>Buffer Zones</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Map and Analysis Section -->
      <div class="map-analysis-container">
        <div class="map-container">
          <div id="map"></div>
        </div>

        <!-- Fixed Legend Below Map -->
        <div class="fixed-legend">
          <h4><i class="fas fa-map-signs"></i> Map Legend</h4>

          <div class="legend-grid">
            <!-- Buffer Zones -->
            <div class="legend-section">
              <h5>Buffer Zones</h5>
              <ul>
                <li>
                  <div class="color-box"
                    style="background-color: #FF4500; border: 1px solid rgba(0, 0, 0, 0.2); border-style: dashed;">
                  </div>
                  <span>People Safety Buffer</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #FFD700; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Flammable Liquids Buffer</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #FF0000; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Open Fire Buffer</span>
                </li>
              </ul>
            </div>

            <!-- Storage Areas -->
            <div class="legend-section">
              <h5>Storage Areas</h5>
              <ul>
                <li>
                  <div class="color-box" style="background-color: #32CD32; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Free Space (Available)</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #006400; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Free Space (Insufficient)</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #FFB6C1; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Deicing (Available)</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #8B0000; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Deicing (Insufficient)</span>
                </li>
              </ul>
            </div>

            <!-- Amenities -->
            <div class="legend-section">
              <h5>Amenities</h5>
              <ul class="amenities-grid">
                <li>
                  <div class="color-box" style="background-color: #4169E1; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Cargo</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #DC143C; border: 1px solid rgba(0, 0, 0, 0.2);"></div>
                  <span>Emergency Response</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #FFA500; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Fuel Farm</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #9370DB; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Lease</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #708090; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Maintenance</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #87CEEB; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Parking</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #00CED1; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Support</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #DAA520; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Transportation</span>
                </li>
                <li>
                  <div class="color-box" style="background-color: #8B4513; border: 1px solid rgba(0, 0, 0, 0.2);">
                  </div>
                  <span>Utilities</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Buffer Analysis Section -->
      <div class="analysis-section" v-if="bufferAnalysisResults.length">
        <div class="card">
          <div class="card-header">
            <h3><i class="fas fa-shield-alt"></i> Buffer Zone Impact Analysis</h3>
            <div class="info-badge">
              <i class="fas fa-info-circle"></i>
              <span class="tooltip">This analysis shows how safety buffer zones reduce available storage area</span>
            </div>
          </div>

          <div class="analysis-tabs">
            <button class="tab-button" :class="{ 'active': activeTab === 'table' }" @click="activeTab = 'table'">
              <i class="fas fa-table"></i> Overview
            </button>
            <button class="tab-button" :class="{ 'active': activeTab === 'details' }" @click="activeTab = 'details'">
              <i class="fas fa-search-plus"></i> Detailed Analysis
            </button>
          </div>

          <!-- Table Tab -->
          <div class="tab-content" v-show="activeTab === 'table'">
            <div class="table-container">
              <table class="buffer-analysis-table">
                <thead>
                  <tr>
                    <th>Storage Area</th>
                    <th>Original Area (ft²)</th>
                    <th>Available Area (ft²)</th>
                    <th>Reduction (%)</th>
                    <th>Compliance</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="result in bufferAnalysisResults" :key="result.area_id" :class="{
                    'compliant': result.available_area_sqft >= storageStore.totalFootprint,
                    'non-compliant': result.available_area_sqft < storageStore.totalFootprint
                  }">
                    <td>{{ result.area_name }}</td>
                    <td>{{ $formatNumber(result.original_area_sqft) }}</td>
                    <td>{{ $formatNumber(result.available_area_sqft) }}</td>
                    <td>{{ $formatNumber(result.area_reduction_percent) }}%</td>
                    <td>
                      <span class="status-badge"
                        :class="result.available_area_sqft >= storageStore.totalFootprint ? 'compliant' : 'non-compliant'">
                        {{ result.available_area_sqft >= storageStore.totalFootprint ? 'Sufficient' : 'Insufficient' }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Details Tab -->
          <div class="tab-content" v-show="activeTab === 'details'">
            <div class="area-selector-container">
              <label for="area-select">Select Area for Detailed Analysis: </label>
              <select id="area-select" v-model="selectedAreaId" class="select-control">
                <option v-for="area in bufferAnalysisResults" :key="area.area_id" :value="area.area_id">
                  {{ area.area_name }}
                  ({{ area.overlapping_buffers.length }} buffer{{ area.overlapping_buffers.length !== 1 ? 's' : '' }})
                </option>
              </select>
            </div>

            <div class="buffer-details" v-if="selectedArea && selectedArea.overlapping_buffers.length > 0">
              <div class="details-header">
                <h4>Buffer Overlaps for {{ selectedArea.area_name }}</h4>
                <div class="details-summary">
                  This area is affected by <strong>{{ selectedArea.overlapping_buffers.length }}</strong> safety
                  buffer(s),
                  reducing the available space by <strong>{{ selectedArea.area_reduction_percent.toFixed(1)
                  }}%</strong>.
                </div>
              </div>

              <div class="buffer-cards">
                <div v-for="(buffer, index) in selectedArea.overlapping_buffers" :key="index" class="buffer-card">
                  <div class="buffer-card-header" :class="getHazardClass(buffer.hazard_type)">
                    <span class="buffer-name">{{ buffer.buffer_id }}</span>
                    <span class="buffer-type">{{ formatHazardType(buffer.hazard_type) }}</span>
                  </div>
                  <div class="buffer-card-body">
                    <div class="buffer-stat">
                      <span class="label">Overlap Area:</span>
                      <span class="value">{{ $formatNumber(buffer.overlap_area_sqft) }} ft²</span>
                    </div>
                    <div class="buffer-stat">
                      <span class="label">Percentage of Total:</span>
                      <span class="value">
                        {{ $formatNumber(((buffer.overlap_area_sqft / selectedArea.original_area_sqft) * 100)) }}%
                      </span>
                    </div>
                    <div class="impact-bar">
                      <div class="impact-fill" :style="{
                        width: `${Math.min(((buffer.overlap_area_sqft / selectedArea.original_area_sqft) * 100), 100)}%`,
                        backgroundColor: getHazardColor(buffer.hazard_type)
                      }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import 'leaflet/dist/leaflet.css';
import { useStorageStore } from '../store/storageStore';
import { ref, onMounted, watch, nextTick, computed } from 'vue';
import L from 'leaflet';
import { api } from '@/utils/api';
import turfArea from '@turf/area';
import { polygon as turfPolygon, point as turfPoint } from '@turf/helpers';
import { booleanPointInPolygon } from '@turf/boolean-point-in-polygon';

// Store and state management
const storageStore = useStorageStore();
const map = ref(null);
const error = ref(null);
const isLoading = ref(false);
const legendCollapsed = ref(false);
const activeTab = ref('table');

const facilitiesGeoJsonData = ref(null);
const facilitiesGeoJsonLayer = ref(null);

const bufferZonesGeoJsonData = ref(null);
const bufferZonesGeoJsonLayer = ref(null);

const availableLayers = ref([]);
const selectedAreaId = ref(null);
const bufferAnalysisResults = ref([]);

const selectedFunction = ref("storage"); // Special value to indicate Free Space and Deicing

// Computed property for selected area
const selectedArea = computed(() => {
  if (!selectedAreaId.value || !bufferAnalysisResults.value.length) return null;
  return bufferAnalysisResults.value.find(area => area.area_id === selectedAreaId.value);
});

// Reactive state for layer controls
const layerControls = ref({
  facilities: true,
  bufferZones: true
});

const getHazardClass = (hazardType) => {
  const classes = {
    "contains_people": "hazard-people",
    "contains_flammable_liquids": "hazard-flammable",
    "contains_open_fire": "hazard-fire"
  };
  return classes[hazardType] || "hazard-unknown";
};

const getHazardColor = (hazardType) => {
  const colors = {
    "contains_people": "#FF4500",
    "contains_flammable_liquids": "#FFD700",
    "contains_open_fire": "#FF0000"
  };
  return colors[hazardType] || "#999";
};

const uniqueFunctions = computed(() => {
  if (!facilitiesGeoJsonData.value) return [];
  const functions = facilitiesGeoJsonData.value.features.map((feature) => feature.properties.amenity || "Unknown");
  const uniqueSet = new Set(functions);
  return Array.from(uniqueSet);
});

const handleFilterChange = (event) => {
  selectedFunction.value = event.target.value;
  console.log("Filter changed to:", selectedFunction.value);
  if (map.value && facilitiesGeoJsonData.value) {
    renderFacilitiesGeoJSONLayer();
  }
};

const filteredDropdownOptions = computed(() => {
  if (!facilitiesGeoJsonData.value) return [];

  const amenityTypes = facilitiesGeoJsonData.value.features
    .map(feature => feature.properties.amenity || "Unknown")
    .filter(amenity => amenity !== "Free Space" && amenity !== "Deicing");

  return [...new Set(amenityTypes)].sort();
});

const freeSpaceStatus = computed(() => {
  if (!facilitiesGeoJsonData.value || !storageStore.totalFootprint) return "Data Unavailable";
  const freeSpace = facilitiesGeoJsonData.value.features.find(
    (feature) => feature.properties.amenity === "Free Space"
  );
  return freeSpace && freeSpace.properties.computed_area >= storageStore.totalFootprint
    ? "Sufficient Space"
    : "Insufficient Space";
});

const deicingStatus = computed(() => {
  if (!facilitiesGeoJsonData.value || !storageStore.totalFootprint) return "Data Unavailable";
  const deicing = facilitiesGeoJsonData.value.features.find(
    (feature) => feature.properties.amenity === "Deicing"
  );
  return deicing && deicing.properties.computed_area >= storageStore.totalFootprint
    ? "Sufficient Space"
    : "Insufficient Space";
});

const computeFeatureArea = (feature) => {
  try {
    if (!feature.geometry || feature.geometry.type !== 'Polygon') {
      console.warn('Feature does not have valid polygon geometry:', feature);
      return 0;
    }
    const coordinates = feature.geometry.coordinates[0];
    // Ensure coordinates are in the correct format [longitude, latitude]
    const latLngCoords = coordinates.map(coord => [coord[1], coord[0]]);
    // Close the polygon if not already closed
    if (JSON.stringify(latLngCoords[0]) !== JSON.stringify(latLngCoords[latLngCoords.length - 1])) {
      latLngCoords.push(latLngCoords[0]);
    }
    const poly = turfPolygon([coordinates]);
    const areaInSquareMeters = turfArea(poly);
    const areaInSquareFeet = areaInSquareMeters * 10.764; // Convert to square feet
    return Math.round(areaInSquareFeet);
  } catch (err) {
    console.error('Error computing area:', err);
    return 0;
  }
};

const updateBufferAnalysisResults = () => {
  if (!facilitiesGeoJsonData.value?.features || !bufferZonesGeoJsonData.value?.features) {
    bufferAnalysisResults.value = [];
    return;
  }

  const storageAreas = facilitiesGeoJsonData.value.features.filter(feature =>
    feature.properties.amenity === "Free Space" || feature.properties.amenity === "Deicing"
  );

  bufferAnalysisResults.value = storageAreas.map(feature => {
    const areaAnalysis = calculateAvailableArea(feature, bufferZonesGeoJsonData.value.features);
    return {
      area_id: feature.properties.id,
      area_name: feature.properties.name || `${feature.properties.amenity} Area`,
      area_type: feature.properties.amenity,
      ...areaAnalysis
    };
  });
};

const filteredFacilities = computed(() => {
  if (!facilitiesGeoJsonData.value?.features) return [];
  return facilitiesGeoJsonData.value.features.filter((feature) => {
    const functionType = feature.properties.amenity;
    const isRelevantType = functionType === "Free Space" || functionType === "Deicing";
    const matchesFilter = !selectedFunction.value || functionType === selectedFunction.value;
    if (isRelevantType && matchesFilter) {
      feature.properties.computed_area = computeFeatureArea(feature);
      return true;
    }
    return false;
  });
});

const loadFacilitiesGeoJSON = async () => {
  try {
    console.log("🚀 Fetching facilities.geojson...");
    facilitiesGeoJsonData.value = await api.map.getFacilities();
    console.log("✅ Facilities data loaded:", facilitiesGeoJsonData.value);
    renderFacilitiesGeoJSONLayer();
  } catch (err) {
    console.error("❌ Error loading facilities.geojson:", err.message || err);
    error.value = `Failed to load facilities data: ${err.message || err}`;
  }
};

const loadBufferZones = async () => {
  try {
    console.log("🚀 Fetching buffer zones...");
    bufferZonesGeoJsonData.value = await api.buffer_zones.getBuffers();
    console.log("✅ Buffer Zones data loaded:", bufferZonesGeoJsonData.value);

    renderBufferZonesGeoJSONLayer();

    if (facilitiesGeoJsonData.value) {
      performBufferAnalysis();
    }
  } catch (err) {
    console.error("❌ Error loading buffer zones:", err.message || err);
    error.value = `Failed to load buffer zones data: ${err.message || err}`;
  }
};

const performBufferAnalysis = () => {
  if (!facilitiesGeoJsonData.value || !bufferZonesGeoJsonData.value) {
    console.warn("Cannot perform buffer analysis: missing data");
    return;
  }

  try {
    updateBufferAnalysisResults();

    console.log("✅ Buffer analysis complete:", bufferAnalysisResults.value);

    if (bufferAnalysisResults.value.length > 0) {
      selectedAreaId.value = bufferAnalysisResults.value[0].area_id;
    }

    updateFacilitiesWithAvailableAreas();
  } catch (err) {
    console.error("Error performing buffer analysis:", err);
  }
};

const calculateAvailableArea = (storageFeature, bufferFeatures) => {
  try {
    const originalArea = computeFeatureArea(storageFeature);

    const potentialOverlaps = findPotentialOverlaps(storageFeature, bufferFeatures);

    let totalReduction = 0;
    const overlappingBuffers = [];

    potentialOverlaps.forEach(buffer => {
      const overlapArea = estimateOverlapArea(storageFeature, buffer);

      if (overlapArea > 0) {
        overlappingBuffers.push({
          buffer_id: buffer.properties?.facility_name || 'Unknown',
          hazard_type: buffer.properties?.hazard_categories?.[0] || 'Unknown',
          overlap_area_sqft: overlapArea
        });

        totalReduction += overlapArea;
      }
    });

    const availableArea = Math.max(0, originalArea - totalReduction);

    return {
      original_area_sqft: originalArea,
      available_area_sqft: availableArea,
      area_reduction_percent: originalArea > 0 ? ((originalArea - availableArea) / originalArea * 100) : 0,
      overlapping_buffers: overlappingBuffers,
      available_geometry: storageFeature.geometry
    };
  } catch (err) {
    console.error('Error calculating available area:', err);
    return {
      original_area_sqft: 0,
      available_area_sqft: 0,
      area_reduction_percent: 0,
      overlapping_buffers: [],
      available_geometry: null
    };
  }
};

const findPotentialOverlaps = (feature, buffers) => {
  const featureBounds = getFeatureBounds(feature);

  return buffers.filter(buffer => {
    const bufferBounds = getFeatureBounds(buffer);
    return boundsOverlap(featureBounds, bufferBounds);
  });
};

const getFeatureBounds = (feature) => {
  if (!feature.geometry || !feature.geometry.coordinates || !feature.geometry.coordinates[0]) {
    return { minX: 0, minY: 0, maxX: 0, maxY: 0 };
  }

  const coords = feature.geometry.coordinates[0];

  let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;

  coords.forEach(point => {
    const [x, y] = point;
    minX = Math.min(minX, x);
    minY = Math.min(minY, y);
    maxX = Math.max(maxX, x);
    maxY = Math.max(maxY, y);
  });

  return { minX, minY, maxX, maxY };
};

const boundsOverlap = (bounds1, bounds2) => {
  return !(
    bounds1.maxX < bounds2.minX ||
    bounds1.minX > bounds2.maxX ||
    bounds1.maxY < bounds2.minY ||
    bounds1.minY > bounds2.maxY
  );
};

const estimateOverlapArea = (feature, buffer) => {
  const featureBounds = getFeatureBounds(feature);
  const bufferBounds = getFeatureBounds(buffer);

  const overlapWidth = Math.min(featureBounds.maxX, bufferBounds.maxX) -
    Math.max(featureBounds.minX, bufferBounds.minX);
  const overlapHeight = Math.min(featureBounds.maxY, bufferBounds.maxY) -
    Math.max(featureBounds.minY, bufferBounds.minY);

  if (overlapWidth <= 0 || overlapHeight <= 0) return 0;

  const overlapArea = overlapWidth * overlapHeight;

  const FEET_PER_DEGREE_LAT = 364320;
  const FEET_PER_DEGREE_LON = 364320 * Math.cos((featureBounds.minY + featureBounds.maxY) / 2 * Math.PI / 180);

  const overlapAreaFt2 = overlapArea * FEET_PER_DEGREE_LAT * FEET_PER_DEGREE_LON;

  const CORRECTION_FACTOR = 0.5;

  return overlapAreaFt2 * CORRECTION_FACTOR;
};

const updateFacilitiesWithAvailableAreas = () => {
  if (!facilitiesGeoJsonData.value || !bufferAnalysisResults.value.length) return;

  facilitiesGeoJsonData.value.features.forEach(feature => {
    const analysis = bufferAnalysisResults.value.find(
      result => result.area_id === (feature.properties.id || feature.id)
    );

    if (analysis) {
      feature.properties.original_area = analysis.original_area_sqft;
      feature.properties.available_area = analysis.available_area_sqft;
      feature.properties.area_reduction = analysis.area_reduction_percent;
      feature.properties.overlapping_buffers = analysis.overlapping_buffers;
      feature.properties.available_geometry = analysis.available_geometry;

      feature.properties.computed_area = analysis.available_area_sqft;
    }
  });

  renderFacilitiesGeoJSONLayer();
};

const evaluateCompliance = async (feature) => {
  const area = feature.properties.computed_area;
  const footprintNeeded = storageStore.totalFootprint;
  const enoughSpace = area >= footprintNeeded;

  let complianceData;
  try {
    complianceData = await api.distancesRequirements.checkAreaCompliance(
      storageStore.totalH2VolumeGallons,
      feature.properties.id
    );
  } catch (err) {
    console.error('Error fetching compliance data:', err);
    complianceData = { is_compliant: false, reason: 'Compliance check failed' };
  }

  feature.properties.compliance_reason = complianceData.reason;
  feature.properties.required_safety_distance_ft = complianceData.required_safety_distance_ft;
  feature.properties.actual_distance_ft = complianceData.actual_distance_ft;

  const distancesCompliance = complianceData.is_compliant;

  if (!enoughSpace) return 'non-compliant';
  if (enoughSpace && distancesCompliance) return 'compliant';
  return 'partially-compliant';
};

const pointInPolygon = (point, polygon) => {
  let inside = false;
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const xi = polygon[i][0], yi = polygon[i][1];
    const xj = polygon[j][0], yj = polygon[j][1];

    const intersect = ((yi > point[1]) !== (yj > point[1])) &&
      (point[0] < (xj - xi) * (point[1] - yi) / (yj - yi) + xi);
    if (intersect) inside = !inside;
  }
  return inside;
};

const defaultResult = () => ({
  original_area_sqft: 0,
  available_area_sqft: 0,
  area_reduction_percent: 0,
  overlapping_buffers: [],
  available_geometry: null
});

const renderFacilitiesGeoJSONLayer = () => {
  if (!map.value || !map.value._loaded || !facilitiesGeoJsonData.value) {
    console.error("❌ Map not fully initialized or facilities data not available.");
    return;
  }

  // Remove existing layers first
  if (facilitiesGeoJsonLayer.value) {
    map.value.removeLayer(facilitiesGeoJsonLayer.value);
  }

  availableLayers.value.forEach(layer => {
    if (map.value && layer) {
      map.value.removeLayer(layer);
    }
  });
  availableLayers.value = [];

  const filteredFeatures = {
    type: "FeatureCollection",
    features: facilitiesGeoJsonData.value.features.filter(feature => {
      const amenity = feature.properties.amenity || "Unknown";

      if (selectedFunction.value === "storage") {
        return amenity === "Free Space" || amenity === "Deicing";
      }

      if (!selectedFunction.value) {
        return true;
      }

      return amenity === selectedFunction.value;
    })
  };

  filteredFeatures.features.forEach(feature => {
    // Calculate area for all features, not just storage areas
    feature.properties.computed_area = computeFeatureArea(feature);

    if (feature.properties.amenity === "Free Space" || feature.properties.amenity === "Deicing") {
      if (bufferZonesGeoJsonData.value) {
        const areaAnalysis = calculateAvailableArea(feature, bufferZonesGeoJsonData.value.features);

        feature.properties.original_area = areaAnalysis.original_area_sqft;
        feature.properties.available_area = areaAnalysis.available_area_sqft;
        feature.properties.area_reduction = areaAnalysis.area_reduction_percent;
        feature.properties.overlapping_buffers = areaAnalysis.overlapping_buffers;

        feature.properties.computed_area = areaAnalysis.available_area_sqft;

        feature.properties.available_geometry = areaAnalysis.available_geometry;
      }
    }
  });

  facilitiesGeoJsonLayer.value = L.geoJSON(filteredFeatures, {
    style: (feature) => {
      const functionType = feature.properties.amenity || "Unknown";
      const isStorageType = functionType === "Free Space" || functionType === "Deicing";
      const colors = {
        Cargo: "blue",
        "Emergency Response": "red",
        "Fuel Farm": "orange",
        Lease: "purple",
        Maintenance: "gray",
        Parking: "lightblue",
        Support: "cyan",
        Transportation: "yellow",
        Utilities: "brown",
        "Free Space": feature.properties.computed_area >= storageStore.totalFootprint ? "limegreen" : "darkgreen",
        Deicing: feature.properties.computed_area >= storageStore.totalFootprint ? "lightpink" : "darkred",
        Unknown: "black",
      };

      if (isStorageType) {
        if (feature.properties.available_geometry) {
          const availableLayer = L.geoJSON(feature.properties.available_geometry, {
            style: {
              color: functionType === "Free Space" ? "limegreen" : "lightpink",
              fillColor: functionType === "Free Space" ? "limegreen" : "lightpink",
              fillOpacity: 0.7,
              weight: 2
            }
          }).addTo(map.value);

          availableLayers.value.push(availableLayer);
        }

        return {
          color: colors[functionType] || "black",
          fillColor: colors[functionType] || "black",
          fillOpacity: 0.2,
          weight: 2,
          dashArray: "5,5",
          zIndex: isStorageType ? 1000 : 500
        };
      }

      return {
        color: colors[functionType] || "black",
        fillColor: colors[functionType] || "black",
        fillOpacity: 0.5,
        weight: 1,
        zIndex: 500
      };
    },
    onEachFeature: (feature, layer) => {
      const props = feature.properties;
      const computedArea = props.computed_area != null ? props.computed_area : 0;
      const isRelevant = props.amenity === "Free Space" || props.amenity === "Deicing";
      const storageUtilization = isRelevant && computedArea > 0 ?
        ((storageStore.totalFootprint / computedArea) * 100).toFixed(1) : null;

      const popupContent = `
          <div class="custom-popup">
            <h3>${props.name || "Unknown Building"}</h3>
            <div class="popup-section">
              <h4>General Information</h4>
              <p><strong>Amenity:</strong> ${props.amenity || "Unknown"}</p>
              <p><strong>Total Area:</strong> ${(props.original_area != null ? props.original_area.toFixed(2) : (computedArea != null ? computedArea.toFixed(2) : "N/A"))} ft²</p>
              ${props.address ? `<p><strong>Address:</strong> ${props.address}</p>` : ''}
            </div>
            ${isRelevant ? `
              <div class="popup-section storage-info">
                <h4>Storage Capability</h4>
                <p><strong>Original Area:</strong> ${(props.original_area != null ? props.original_area.toFixed(2) : (computedArea != null ? computedArea.toFixed(2) : "N/A"))} ft²</p>
                <p><strong>Available Area:</strong> ${props.available_area != null ? props.available_area.toFixed(2) : "N/A"} ft²</p>
                <p><strong>Area Reduction:</strong> ${props.area_reduction != null ? props.area_reduction.toFixed(1) : "0"}%</p>
                <p><strong>Can Store:</strong> ${props.available_area >= storageStore.totalFootprint ?
            '<span class="success">Yes</span>' : '<span class="error">No</span>'}</p>
                ${props.available_area != null && props.available_area > 0 ? `
                  <p><strong>Space Utilization:</strong> ${((storageStore.totalFootprint / props.available_area) * 100).toFixed(1)}%</p>
                  <div class="utilization-bar">
                    <div class="fill" style="width: ${Math.min((storageStore.totalFootprint / props.available_area) * 100, 100)}%"></div>
                  </div>
                ` : ''}
              </div>
            ` : ''}
            ${props.overlapping_buffers && props.overlapping_buffers.length > 0 ? `
              <div class="popup-section buffer-info">
                <h4>Buffer Zone Impacts</h4>
                <p><strong>Overlapping Buffers:</strong> ${props.overlapping_buffers.length}</p>
                <ul>
                  ${props.overlapping_buffers.map(buffer => `
                    <li>
                      <strong>${buffer.buffer_id}</strong>: 
                      ${formatHazardType(buffer.hazard_type)} - 
                      ${buffer.overlap_area_sqft != null ? buffer.overlap_area_sqft.toFixed(2) : "N/A"} ft²
                    </li>
                  `).join('')}
                </ul>
              </div>
            ` : ''}
          </div>
        `;
      const popupOptions = {
        maxWidth: 300,
        className: 'custom-popup-container'
      };

      layer.bindPopup(popupContent, popupOptions);
    }
  });

  if (layerControls.value.facilities) {
    facilitiesGeoJsonLayer.value.addTo(map.value);
  }
};

const renderBufferZonesGeoJSONLayer = () => {
  if (!map.value || !map.value._loaded || !bufferZonesGeoJsonData.value) {
    console.error("❌ Map not fully initialized or buffer zones data not available.");
    return;
  }

  if (bufferZonesGeoJsonLayer.value) {
    bufferZonesGeoJsonLayer.value.remove();
  }

  const bufferFeatures = [];

  let bufferPopupShown = false;

  const layerGroup = L.layerGroup();

  bufferZonesGeoJsonData.value.features.forEach(feature => {
    const hazardType = feature.properties.hazard_categories[0];
    const facilityName = feature.properties.facility_name;

    const hazardColors = {
      "contains_people": "#FF4500",
      "contains_flammable_liquids": "#FFD700",
      "contains_open_fire": "#FF0000"
    };

    const layer = L.geoJSON(feature, {
      style: {
        color: hazardColors[hazardType] || "#3388ff",
        weight: 2,
        opacity: 0.6,
        fillOpacity: 0.2,
        dashArray: hazardType === "contains_people" ? "5,5" : null
      }
    });

    bufferFeatures.push({
      geometry: feature.geometry,
      properties: {
        facility_name: facilityName,
        hazard_type: hazardType,
        buffer_distance_ft: feature.properties.buffer_distance_ft
      }
    });

    layerGroup.addLayer(layer);
  });

  map.value.on('click', (e) => {
    if (!layerControls.value.bufferZones) return;

    const clickedPoint = turfPoint([e.latlng.lng, e.latlng.lat]);
    const overlappingBuffers = bufferFeatures.filter(feature =>
      booleanPointInPolygon(clickedPoint, feature.geometry)
    );

    if (overlappingBuffers.length > 0) {
      bufferPopupShown = true;
      const popupContent = `
        <div class="custom-popup buffer-zones-popup">
          <h3>Safety Buffer Zones</h3>
          ${overlappingBuffers.map(buffer => `
            <div class="popup-section">
              <h4>${buffer.properties.facility_name}</h4>
              <p><strong>Type:</strong> ${formatHazardType(buffer.properties.hazard_type)}</p>
              <p><strong>Required Distance:</strong> ${buffer.properties.buffer_distance_ft} ft</p>
            </div>
          `).join('')}
        </div>
      `;

      L.popup()
        .setLatLng(e.latlng)
        .setContent(popupContent)
        .openOn(map.value);

      e.originalEvent.stopPropagation();
      e.originalEvent.preventDefault();
    }
  });

  if (layerControls.value.bufferZones) {
    layerGroup.addTo(map.value);
  }
  bufferZonesGeoJsonLayer.value = layerGroup;
};

const formatHazardType = (hazardType) => {
  const displayNames = {
    "contains_people": "People Safety Zone",
    "contains_flammable_liquids": "Flammable Liquids Zone",
    "contains_open_fire": "Open Fire Zone"
  };
  return displayNames[hazardType] || hazardType;
};

const toggleLayer = (layerType) => {
  if (layerType === 'facilities' && facilitiesGeoJsonLayer.value) {
    if (layerControls.value.facilities) {
      facilitiesGeoJsonLayer.value.addTo(map.value);
    } else {
      facilitiesGeoJsonLayer.value.remove();
    }
  } else if (layerType === 'bufferZones' && bufferZonesGeoJsonLayer.value) {
    if (layerControls.value.bufferZones) {
      bufferZonesGeoJsonLayer.value.addTo(map.value);
    } else {
      bufferZonesGeoJsonLayer.value.remove();
    }
  }
};

const handleMapClick = async (event) => {
  const popup = event.target.getContainer()?.querySelector('.buffer-zones-popup');
  if (popup) return;

  const { lat, lng } = event.latlng;
  console.log("Map clicked at:", lat, lng);

  try {
    const overpassUrl = `https://overpass-api.de/api/interpreter?data=[out:json];way(around:50,${lat},${lng})["building"];out geom;`;
    const response = await fetch(overpassUrl);
    const data = await response.json();
    console.log("Overpass API result:", data);

    if (data.elements && data.elements.length > 0) {
      const building = data.elements[0];
      const boundaries = building.geometry.map((point) => [point.lat, point.lon]);
      console.log("Building boundaries:", boundaries);

      // Calculate area using turf.js
      const coordinates = boundaries.map(point => [point[1], point[0]]);
      coordinates.push(coordinates[0]); // Close the polygon
      const poly = turfPolygon([coordinates]);
      const areaInSquareMeters = turfArea(poly);
      const areaInSquareFeet = areaInSquareMeters * 10.764; // Convert to square feet

      const buildingInfo = {
        name: building.tags?.name || "Unknown",
        address: building.tags?.addr_full || null,
        amenity: building.tags?.amenity || "Unknown",
        safetyInfo: building.tags?.["fire_hydrant:position"]
          ? "Fire hydrant nearby"
          : "No specific safety information available",
        area: areaInSquareFeet
      };

      if (!buildingInfo.address) {
        const geocodeResponse = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
        );
        const geocodeData = await geocodeResponse.json();
        buildingInfo.address = geocodeData.display_name || "Unknown";
      }

      const polygon = L.polygon(boundaries, {
        color: "blue",
        weight: 2,
        fillOpacity: 0.3,
      }).addTo(map.value);

      polygon.bindPopup(`
        <b>Building Name:</b> ${buildingInfo.name}<br>
        <b>Address:</b> ${buildingInfo.address}<br>
        <b>Amenity:</b> ${buildingInfo.amenity}<br>
        <b>Area:</b> ${Math.round(buildingInfo.area).toLocaleString()} ft²<br>
        <b>Safety Info:</b> ${buildingInfo.safetyInfo}
      `).openPopup();

      map.value.fitBounds(polygon.getBounds());
    } else {
      alert("No building boundaries found at this location.");
    }
  } catch (error) {
    console.error("Error fetching building boundaries:", error);
    if (!event.target.getContainer()?.querySelector('.buffer-zones-popup')) {
      alert("Failed to fetch building boundaries.");
    }
  }
};

onMounted(async () => {
  const mapContainer = document.getElementById('map');
  if (!mapContainer) {
    console.error("Map container not found!");
    return;
  }

  try {
    console.log("🚀 Initializing map...");
    map.value = L.map('map', {
      center: [33.6407, -84.4277],
      zoom: 13,
      zoomAnimation: true,
      fadeAnimation: true
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap'
    }).addTo(map.value);

    // Wait for map to be ready
    map.value.whenReady(async () => {
      console.log("✅ Map initialized successfully.");

      if (!storageStore.totalH2VolumeGallons || !storageStore.totalFootprint) return;

      await loadFacilitiesGeoJSON();
      await loadBufferZones();

      map.value.on("click", handleMapClick);

      nextTick(() => {
        map.value.invalidateSize();
      });
    });

  } catch (error) {
    console.error("Error initializing map:", error);
    error.value = "Failed to initialize map";
  }
});

// Update the watch handler to check for map initialization
watch(selectedFunction, () => {
  if (map.value && map.value._loaded && facilitiesGeoJsonData.value) {
    console.log("Filter changed to:", selectedFunction.value);
    renderFacilitiesGeoJSONLayer();
  }
});
</script>

<style scoped>
/* Modern, clean styling with improved visual hierarchy */
.compliance-map {
  background-color: #1e1e2f;
  border-radius: 12px;
  padding: 24px;
  color: #e4e4e4;
  font-family: 'Inter', 'Segoe UI', Roboto, -apple-system, sans-serif;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
}

.header-section {
  margin-bottom: 24px;
  text-align: center;
}

.header-section h2 {
  color: #64ffda;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 8px;
  letter-spacing: -0.5px;
}

.subtitle {
  color: #a0aec0;
  font-size: 1.1rem;
  font-weight: 400;
}

/* Dashboard Section */
.dashboard {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

@media (max-width: 992px) {
  .dashboard {
    grid-template-columns: 1fr;
  }
}

.card {
  background: rgba(30, 41, 59, 0.8);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
}

.card h3 {
  color: #64ffda;
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card h3 i {
  font-size: 1.1rem;
  opacity: 0.9;
}

/* Metrics Card */
.metrics-card {
  padding: 24px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
}

.metric-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  transition: background 0.2s ease;
}

.metric-item:hover {
  background: rgba(255, 255, 255, 0.08);
}

.metric-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: rgba(100, 255, 218, 0.15);
  border-radius: 12px;
  color: #64ffda;
  font-size: 1.5rem;
}

.metric-content {
  flex: 1;
}

.metric-label {
  font-size: 0.9rem;
  color: #a0aec0;
  margin-bottom: 4px;
}

.metric-value {
  font-size: 1.25rem;
  font-weight: 600;
  color: #ffffff;
}

/* Compliance Card */
.compliance-card {
  padding: 24px;
}

.compliance-status-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.status-item:hover {
  transform: translateX(4px);
}

.status-item.status-ok {
  background: rgba(52, 211, 153, 0.1);
  border-left: 4px solid #34d399;
}

.status-item.status-warning {
  background: rgba(251, 191, 36, 0.1);
  border-left: 4px solid #fbbf24;
}

.status-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1.25rem;
}

.status-ok .status-icon {
  background: rgba(52, 211, 153, 0.2);
  color: #34d399;
}

.status-warning .status-icon {
  background: rgba(251, 191, 36, 0.2);
  color: #fbbf24;
}

.status-content {
  flex: 1;
}

.status-label {
  font-size: 0.9rem;
  color: #a0aec0;
  margin-bottom: 4px;
}

.status-value {
  font-size: 1.1rem;
  font-weight: 600;
}

.status-ok .status-value {
  color: #34d399;
}

.status-warning .status-value {
  color: #fbbf24;
}

/* Map Controls */
.map-controls {
  margin-bottom: 20px;
}

.control-panel {
  background: rgba(30, 41, 59, 0.8);
  border-radius: 12px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-group {
  flex: 1;
  min-width: 250px;
}

.filter-group label {
  display: block;
  margin-bottom: 8px;
  color: #a0aec0;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 6px;
}

.select-control {
  width: 100%;
  padding: 10px 14px;
  background: rgba(17, 24, 39, 0.7);
  color: #e4e4e4;
  border: 1px solid rgba(100, 255, 218, 0.3);
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2364ffda' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  padding-right: 30px;
}

.select-control:focus {
  border-color: #64ffda;
  outline: none;
  box-shadow: 0 0 0 3px rgba(100, 255, 218, 0.2);
}

.layer-toggles {
  display: flex;
  gap: 16px;
}

.toggle-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.toggle {
  position: relative;
  display: inline-block;
  width: 48px;
  height: 24px;
}

.toggle input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(100, 255, 218, 0.2);
  transition: .4s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: #64ffda;
  transition: .4s;
  border-radius: 50%;
}

input:checked+.toggle-slider {
  background-color: rgba(100, 255, 218, 0.6);
}

input:focus+.toggle-slider {
  box-shadow: 0 0 1px rgba(100, 255, 218, 0.8);
}

input:checked+.toggle-slider:before {
  transform: translateX(24px);
}

/* Map and Analysis Container */
.map-analysis-container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

@media (min-width: 1200px) {
  .map-analysis-container {
    grid-template-columns: 3fr 2fr;
  }
}

/* Updated Map Container */
.map-container {
  background: rgba(30, 41, 59, 0.95);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 20px;
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
}

#map {
  flex: 1;
  border-radius: 8px;
  overflow: hidden;
  min-height: 500px;
}

/* Fixed Legend Below Map */
.fixed-legend {
  background: rgba(30, 41, 59, 0.95);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.fixed-legend h4 {
  color: #64ffda;
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0 0 16px 0;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.legend-section {
  background: rgba(17, 24, 39, 0.7);
  border-radius: 8px;
  padding: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.legend-section h5 {
  color: #64ffda;
  font-size: 1rem;
  margin: 0 0 12px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-weight: 600;
}

.fixed-legend ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.fixed-legend li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 0.9rem;
  color: #e4e4e4;
}

.fixed-legend li:last-child {
  margin-bottom: 0;
}

.amenities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 10px;
}

.fixed-legend .color-box {
  min-width: 20px;
  width: 20px;
  height: 20px;
  margin-right: 10px;
  border-radius: 4px;
  flex-shrink: 0;
  display: inline-block;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

/* Analysis Section */
.analysis-section {
  display: flex;
  flex-direction: column;
}

.card-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-badge {
  position: relative;
  display: inline-block;
  color: #64ffda;
  cursor: help;
}

.info-badge .tooltip {
  visibility: hidden;
  width: 240px;
  background-color: rgba(17, 24, 39, 0.95);
  color: #e4e4e4;
  text-align: center;
  border-radius: 6px;
  padding: 8px 12px;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  transform: translateX(-50%);
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 0.85rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  pointer-events: none;
}

.info-badge:hover .tooltip {
  visibility: visible;
  opacity: 1;
}

/* Tabs */
.analysis-tabs {
  display: flex;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tab-button {
  flex: 1;
  background: transparent;
  border: none;
  color: #a0aec0;
  padding: 14px;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border-bottom: 2px solid transparent;
}

.tab-button:hover {
  color: #e4e4e4;
  background: rgba(255, 255, 255, 0.05);
}

.tab-button.active {
  color: #64ffda;
  border-bottom: 2px solid #64ffda;
  font-weight: 500;
}

.tab-content {
  padding: 20px;
}

/* Table styles */
.table-container {
  overflow-x: auto;
  border-radius: 6px;
  background: rgba(17, 24, 39, 0.5);
}

.buffer-analysis-table {
  width: 100%;
  border-collapse: collapse;
  border-spacing: 0;
  font-size: 0.9rem;
}

.buffer-analysis-table th,
.buffer-analysis-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.buffer-analysis-table th {
  background-color: rgba(30, 41, 59, 0.8);
  color: #64ffda;
  font-weight: 600;
  position: sticky;
  top: 0;
  z-index: 10;
}

.buffer-analysis-table tr:last-child td {
  border-bottom: none;
}

.buffer-analysis-table tr.compliant {
  background-color: rgba(52, 211, 153, 0.05);
}

.buffer-analysis-table tr.non-compliant {
  background-color: rgba(239, 68, 68, 0.05);
}

.buffer-analysis-table tr:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  text-align: center;
}

.status-badge.compliant {
  background-color: rgba(52, 211, 153, 0.2);
  color: #34d399;
}

.status-badge.non-compliant {
  background-color: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

/* Area selector */
.area-selector-container {
  margin-bottom: 20px;
}

.area-selector-container label {
  display: block;
  margin-bottom: 8px;
  color: #a0aec0;
  font-size: 0.9rem;
}

/* Buffer details */
.buffer-details {
  background: rgba(17, 24, 39, 0.5);
  border-radius: 8px;
  overflow: hidden;
}

.details-header {
  padding: 16px;
  background: rgba(30, 41, 59, 0.8);
}

.details-header h4 {
  color: #64ffda;
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.details-summary {
  color: #a0aec0;
  font-size: 0.9rem;
  line-height: 1.5;
}

.buffer-cards {
  padding: 16px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.buffer-card {
  background: rgba(30, 41, 59, 0.6);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.buffer-card:hover {
  transform: translateY(-4px);
}

.buffer-card-header {
  padding: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.buffer-card-header.hazard-people {
  background: rgba(255, 69, 0, 0.2);
}

.buffer-card-header.hazard-flammable {
  background: rgba(255, 215, 0, 0.2);
}

.buffer-card-header.hazard-fire {
  background: rgba(255, 0, 0, 0.2);
}

.buffer-name {
  font-weight: 600;
  font-size: 0.95rem;
  color: #e4e4e4;
}

.buffer-type {
  font-size: 0.8rem;
  color: #a0aec0;
  background: rgba(0, 0, 0, 0.2);
  padding: 2px 6px;
  border-radius: 4px;
}

.buffer-card-body {
  padding: 12px;
}

.buffer-stat {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.85rem;
}

.impact-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  overflow: hidden;
  margin-top: 12px;
}

.impact-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

/* Alert styles */
.alert {
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.alert i {
  font-size: 1.25rem;
}

.alert.info {
  background: rgba(59, 130, 246, 0.1);
  border-left: 4px solid #3b82f6;
  color: #93c5fd;
}

.alert.error {
  background: rgba(239, 68, 68, 0.1);
  border-left: 4px solid #ef4444;
  color: #fca5a5;
}

/* Loading container */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px;
  background: rgba(17, 24, 39, 0.5);
  border-radius: 8px;
  gap: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(100, 255, 218, 0.2);
  border-top-color: #64ffda;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Custom Popup Styles */
:deep(.custom-popup-container) {
  background: #1a1a2e;
  color: #e4e4e4;
  border: 1px solid #64ffda;
  border-radius: 8px;
  padding: 0;
  margin: 0;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}

:deep(.custom-popup) {
  padding: 12px;
  font-size: 0.9rem;
  line-height: 1.5;
}

:deep(.custom-popup h3) {
  color: #64ffda;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 8px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.popup-section) {
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

:deep(.popup-section) {
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

:deep(.popup-section:last-child) {
  border-bottom: none;
}

:deep(.popup-section h4) {
  color: #64ffda;
  margin: 0 0 8px 0;
  font-size: 0.95rem;
  font-weight: 600;
}

:deep(.success) {
  color: #34d399;
  font-weight: 600;
}

:deep(.error) {
  color: #ef4444;
  font-weight: 600;
}

:deep(.utilization-bar) {
  height: 6px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
  margin-top: 8px;
  overflow: hidden;
}

:deep(.utilization-bar .fill) {
  height: 100%;
  background: #64ffda;
  border-radius: 3px;
  transition: width 0.3s ease;
}

:deep(.buffer-zones-popup) {
  max-width: 320px;
}

:deep(.buffer-zones-popup .popup-section) {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 6px;
  padding: 10px;
  margin: 8px 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .compliance-map {
    padding: 16px;
  }

  .header-section h2 {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 0.9rem;
  }

  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .control-panel {
    flex-direction: column;
    align-items: stretch;
  }

  .layer-toggles {
    justify-content: space-between;
  }

  #map {
    height: 400px;
  }

  .buffer-cards {
    grid-template-columns: 1fr;
  }

  .legend-panel {
    width: 250px;
  }
}
</style>
