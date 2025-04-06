<!-- File: frontend/src/components/ComplianceMap.vue -->

<template>
  <div class="compliance-map">
    <h2>Compliance Map</h2>

    <!-- Results Section -->
    <div class="results-section">
      <div class="result-item">
        <i class="fas fa-gas-pump"></i>
        <span>Total Hydrogen Demand:</span>
        <strong>{{ storageStore.totalH2VolumeGallons.toFixed(2) }} gallons</strong>
      </div>
      <div class="result-item">
        <i class="fas fa-ruler-combined"></i>
        <span>Total Footprint Storage:</span>
        <strong>{{ storageStore.totalFootprint.toFixed(2) }} ft²</strong>
      </div>
      <div class="result-item">
        <i class="fas fa-cube"></i>
        <span>Tank Dimensions:</span>
        <strong>{{ storageStore.tankDiameter.toFixed(2) }} ft (D) × {{ storageStore.tankLength.toFixed(2) }} ft
          (L)</strong>
      </div>
      <div class="result-item">
        <i class="fas fa-boxes"></i>
        <span>Number of Tanks:</span>
        <strong>{{ storageStore.recommendedTankCount }}</strong>
      </div>
    </div>

    <!-- Free Space and Deicing Check -->
    <div class="space-check-section">
      <div class="space-check-item">
        <span>Free Space:</span>
        <strong>{{ freeSpaceStatus }}</strong>
      </div>
      <div class="space-check-item">
        <span>Deicing:</span>
        <strong>{{ deicingStatus }}</strong>
      </div>
    </div>

    <!-- Table for Building Compliance -->
    <div class="compliance-table-section">
      <h3>Building Compliance</h3>
      <table class="compliance-table" v-if="tableCompliance.length">
        <thead>
          <tr>
            <th>Building</th>
            <th>Amenity</th>
            <th>Area (ft²)</th>
            <th>Can Contain Footprint</th>
            <th>Proportion (%)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in tableCompliance" :key="row.building">
            <td>{{ row.building }}</td>
            <td>{{ row.amenity }}</td>
            <td>{{ row.area }} ft²</td>
            <td>{{ row.canContainFootprint }}</td>
            <td>{{ row.proportion }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="no-data-message">No buildings meet the compliance criteria.</p>
    </div>

    <!-- Add this after the compliance-table-section -->
    <div class="buffer-analysis-section" v-if="bufferAnalysisResults.length">
      <h3>Buffer Zone Impact Analysis</h3>
      <div class="alert info">
        <i class="fas fa-info-circle"></i>
        <span>This analysis shows how safety buffer zones reduce available storage area.</span>
      </div>

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
            <td>{{ result.original_area_sqft.toFixed(2) }}</td>
            <td>{{ result.available_area_sqft.toFixed(2) }}</td>
            <td>{{ result.area_reduction_percent.toFixed(1) }}%</td>
            <td>
              <span class="status-badge"
                :class="result.available_area_sqft >= storageStore.totalFootprint ? 'compliant' : 'non-compliant'">
                {{ result.available_area_sqft >= storageStore.totalFootprint ? 'Sufficient' : 'Insufficient' }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Details for selected area -->
      <div class="buffer-details" v-if="selectedArea && selectedArea.overlapping_buffers.length > 0">
        <h4>Buffer Overlaps for {{ selectedArea.area_name }}</h4>
        <p class="buffer-details-intro">
          This area is affected by {{ selectedArea.overlapping_buffers.length }} safety buffer(s),
          reducing the available space by {{ selectedArea.area_reduction_percent.toFixed(1) }}%.
        </p>

        <div class="buffer-list">
          <div v-for="(buffer, index) in selectedArea.overlapping_buffers" :key="index" class="buffer-item">
            <div class="buffer-item-header">
              <span class="buffer-name">{{ buffer.buffer_id }}</span>
              <span class="buffer-type">{{ formatHazardType(buffer.hazard_type) }}</span>
            </div>
            <div class="buffer-item-details">
              <div class="buffer-stat">
                <span class="label">Overlap Area:</span>
                <span class="value">{{ buffer.overlap_area_sqft.toFixed(2) }} ft²</span>
              </div>
              <div class="buffer-stat">
                <span class="label">Percentage of Total:</span>
                <span class="value">
                  {{ ((buffer.overlap_area_sqft / selectedArea.original_area_sqft) * 100).toFixed(1) }}%
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Area selection controls -->
      <div class="area-selector">
        <label for="area-select">Select Area for Detailed Analysis:</label>
        <select id="area-select" v-model="selectedAreaId">
          <option v-for="area in bufferAnalysisResults" :key="area.area_id" :value="area.area_id">
            {{ area.area_name }}
            ({{ area.overlapping_buffers.length }} buffer{{ area.overlapping_buffers.length !== 1 ? 's' : '' }})
          </option>
        </select>
      </div>
    </div>

    <!-- Filter by Amenity -->
    <div class="filter-container">
      <label for="function-filter">Filter by Amenity:</label>
      <select id="function-filter" :value="selectedFunction" @change="handleFilterChange">
        <option value="storage">Free Space and Deicing Only</option>
        <option value="">All Amenities</option>
        <option v-for="functionType in filteredDropdownOptions" :key="functionType" :value="functionType">
          {{ functionType }}
        </option>
      </select>
    </div>

    <!-- Alert shown when hydrogen/storage calculations aren't done -->
    <div v-if="!storageStore.totalH2VolumeGallons || !storageStore.totalFootprint" class="alert info">
      <i class="fas fa-info-circle"></i>
      <span>Please configure hydrogen demand and storage calculations first.</span>
    </div>

    <!-- Loading state -->
    <div v-else-if="isLoading" class="loading">
      <div class="spinner"></div>
      <p>Loading compliance data...</p>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="error-message">
      <i class="fas fa-exclamation-triangle"></i>
      <p>{{ error }}</p>
    </div>

    <!-- Compliance Map -->
    <div v-else>
      <div id="map" style="height: 400px; width: 100%;"></div>
      <!-- Layer Controls -->
      <div class="layer-controls">
        <h4>Map Layers</h4>
        <div class="layer-toggles">
          <label>
            <input type="checkbox" v-model="layerControls.facilities" @change="toggleLayer('facilities')">
            Facilities
          </label>
          <label>
            <input type="checkbox" v-model="layerControls.bufferZones" @change="toggleLayer('bufferZones')">
            Buffer Zones
          </label>
        </div>
      </div>
      <!-- Legend -->
      <div class="legend">
        <h4>Legend</h4>
        <ul>
          <li><span class="color-box" style="background-color: #FF4500;"></span> People Safety Buffer</li>
          <li><span class="color-box" style="background-color: #FFD700;"></span> Flammable Liquids Buffer</li>
          <li><span class="color-box" style="background-color: #FF0000;"></span> Open Fire Buffer</li>
          <li><span class="color-box" style="background-color: green;"></span> Free Space (Sufficient)</li>
          <li><span class="color-box" style="background-color: darkgreen;"></span> Free Space (Insufficient)</li>
          <li><span class="color-box" style="background-color: pink;"></span> Deicing (Sufficient)</li>
          <li><span class="color-box" style="background-color: darkred;"></span> Deicing (Insufficient)</li>
          <li><span class="color-box" style="background-color: blue;"></span> Cargo</li>
          <li><span class="color-box" style="background-color: red;"></span> Emergency Response</li>
          <li><span class="color-box" style="background-color: orange;"></span> Fuel Farm</li>
          <li><span class="color-box" style="background-color: purple;"></span> Lease</li>
          <li><span class="color-box" style="background-color: gray;"></span> Maintenance</li>
          <li><span class="color-box" style="background-color: lightblue;"></span> Parking</li>
          <li><span class="color-box" style="background-color: cyan;"></span> Support</li>
          <li><span class="color-box" style="background-color: yellow;"></span> Transportation</li>
          <li><span class="color-box" style="background-color: brown;"></span> Utilities</li>
          <li><span class="color-box" style="background-color: black;"></span> Unknown</li>
        </ul>
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

const storageStore = useStorageStore();
const map = ref(null);
const error = ref(null);
const isLoading = ref(false);

const facilitiesGeoJsonData = ref(null);
const facilitiesGeoJsonLayer = ref(null);

const bufferZonesGeoJsonData = ref(null);
const bufferZonesGeoJsonLayer = ref(null);

const availableLayers = ref([]);
const selectedAreaId = ref(null);
const bufferAnalysisResults = ref([]);

const selectedFunction = ref("storage"); // Special value to indicate Free Space and Deicing

// Add computed property for selected area
const selectedArea = computed(() => {
  if (!selectedAreaId.value || !bufferAnalysisResults.value.length) return null;
  return bufferAnalysisResults.value.find(area => area.area_id === selectedAreaId.value);
});

// Add new reactive state for layer controls
const layerControls = ref({
  facilities: true,
  bufferZones: true
});

// Compute unique functions for the dropdown filter
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

  // Get all unique amenity types
  const amenityTypes = facilitiesGeoJsonData.value.features
    .map(feature => feature.properties.amenity || "Unknown")
    .filter(amenity => amenity !== "Free Space" && amenity !== "Deicing");

  // Create a Set to remove duplicates and convert back to array
  return [...new Set(amenityTypes)].sort();
});

// Check if "Free Space" or "Deicing" buildings have enough space
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

// Compute area from coordinates using Turf
const computeFeatureArea = (feature) => {
  try {
    if (!feature.geometry || feature.geometry.type !== 'Polygon') {
      console.warn('Feature does not have valid polygon geometry:', feature);
      return 0;
    }
    // Ensure the first and last coordinates are the same
    const coordinates = feature.geometry.coordinates[0];
    if (coordinates[0][0] !== coordinates[coordinates.length - 1][0] ||
      coordinates[0][1] !== coordinates[coordinates.length - 1][1]) {
      coordinates.push(coordinates[0]);
    }
    const poly = turfPolygon([coordinates]);
    const areaInSquareMeters = turfArea(poly);
    // Convert square meters to square feet (1 sq meter = 10.764 sq ft)
    return areaInSquareMeters * 10.764;
  } catch (err) {
    console.error('Error computing area:', err);
    return 0;
  }
};

// const bufferAnalysisResults = computed(() => {
//   if (!facilitiesGeoJsonData.value?.features || !bufferZonesGeoJsonData.value?.features) return [];

//   const storageAreas = facilitiesGeoJsonData.value.features.filter(feature =>
//     feature.properties.amenity === "Free Space" || feature.properties.amenity === "Deicing"
//   );

//   return storageAreas.map(feature => {
//     const areaAnalysis = calculateAvailableArea(feature, bufferZonesGeoJsonData.value.features);
//     return {
//       area_id: feature.properties.id,
//       area_name: feature.properties.name || `${feature.properties.amenity} Area`,
//       area_type: feature.properties.amenity,
//       ...areaAnalysis
//     };
//   });
// });

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

// Update the filtered facilities computed property
const filteredFacilities = computed(() => {
  if (!facilitiesGeoJsonData.value?.features) return [];
  return facilitiesGeoJsonData.value.features.filter((feature) => {
    const functionType = feature.properties.amenity;
    // First filter by Free Space or Deicing
    const isRelevantType = functionType === "Free Space" || functionType === "Deicing";
    // Then apply the selected function filter if one is selected
    const matchesFilter = !selectedFunction.value || functionType === selectedFunction.value;
    // Calculate area if feature passes filters
    if (isRelevantType && matchesFilter) {
      feature.properties.computed_area = computeFeatureArea(feature);
      return true;
    }
    return false;
  });
});

const tableCompliance = computed(() => {
  if (!facilitiesGeoJsonData.value?.features) return [];
  return facilitiesGeoJsonData.value.features
    .filter((feature) => {
      const amenity = feature.properties.amenity;
      return amenity === "Free Space" || amenity === "Deicing";
    })
    .map((feature) => {
      const area = feature.properties.computed_area || computeFeatureArea(feature);
      const canContainFootprint = area >= storageStore.totalFootprint ? "Yes" : "No";
      const proportion = ((storageStore.totalFootprint / area) * 100).toFixed(2) + "%";

      return {
        building: feature.properties.name || "Unknown",
        amenity: feature.properties.amenity || "Unknown",
        area: area.toFixed(2),
        canContainFootprint,
        proportion,
      };
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


// Update the loadBufferZones function
const loadBufferZones = async () => {
  try {
    console.log("🚀 Fetching buffer zones...");
    bufferZonesGeoJsonData.value = await api.buffer_zones.getBuffers();
    console.log("✅ Buffer Zones data loaded:", bufferZonesGeoJsonData.value);

    // Render the buffer zones
    renderBufferZonesGeoJSONLayer();

    // Perform buffer analysis if facilities are loaded
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
    // Update buffer analysis results
    updateBufferAnalysisResults();

    console.log("✅ Buffer analysis complete:", bufferAnalysisResults.value);

    // Auto-select first area
    if (bufferAnalysisResults.value.length > 0) {
      selectedAreaId.value = bufferAnalysisResults.value[0].area_id;
    }

    // Update the facilities layer to show available areas
    updateFacilitiesWithAvailableAreas();
  } catch (err) {
    console.error("Error performing buffer analysis:", err);
  }
};

// // Add the simplified buffer analysis function
// const performBufferAnalysis = () => {
//   if (!facilitiesGeoJsonData.value || !bufferZonesGeoJsonData.value) {
//     console.warn("Cannot perform buffer analysis: missing data");
//     return;
//   }

//   // Find storage areas (Free Space and Deicing)
//   const storageAreas = facilitiesGeoJsonData.value.features.filter(feature =>
//     feature.properties.amenity === "Free Space" || feature.properties.amenity === "Deicing"
//   );

//   if (!storageAreas.length) {
//     console.warn("No storage areas found for buffer analysis");
//     return;
//   }

//   try {
//     // Process each storage area
//     bufferAnalysisResults.value = storageAreas.map(feature => {
//       const analysis = calculateAvailableArea(feature, bufferZonesGeoJsonData.value.features);

//       return {
//         area_id: feature.properties.id || feature.id || Math.random().toString(36).substring(2, 9),
//         area_name: feature.properties.name || `${feature.properties.amenity} Area`,
//         area_type: feature.properties.amenity,
//         ...analysis
//       };
//     });

//     console.log("✅ Buffer analysis complete:", bufferAnalysisResults.value);

//     // Auto-select first area
//     if (bufferAnalysisResults.value.length > 0) {
//       selectedAreaId.value = bufferAnalysisResults.value[0].area_id;
//     }

//     // Update the facilities layer to show available areas
//     updateFacilitiesWithAvailableAreas();
//   } catch (err) {
//     console.error("Error performing buffer analysis:", err);
//   }
// };

// Add a simplified version of calculateAvailableArea
const calculateAvailableArea = (storageFeature, bufferFeatures) => {
  try {
    // Calculate original area of the storage feature
    const originalArea = computeFeatureArea(storageFeature);

    // Find buffers that might intersect with this storage area
    const potentialOverlaps = findPotentialOverlaps(storageFeature, bufferFeatures);

    // Calculate total area reduction (simplified approach)
    let totalReduction = 0;
    const overlappingBuffers = [];

    potentialOverlaps.forEach(buffer => {
      // Estimate overlap area (simplified)
      // In a real implementation, you'd use proper geometric operations
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

    // Calculate available area
    const availableArea = Math.max(0, originalArea - totalReduction);

    return {
      original_area_sqft: originalArea,
      available_area_sqft: availableArea,
      area_reduction_percent: originalArea > 0 ? ((originalArea - availableArea) / originalArea * 100) : 0,
      overlapping_buffers: overlappingBuffers,
      available_geometry: storageFeature.geometry // Use original geometry
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

// Helper function to find potential buffer overlaps using bounding box comparison
const findPotentialOverlaps = (feature, buffers) => {
  // Extract feature bounds
  const featureBounds = getFeatureBounds(feature);

  // Find buffers that might overlap
  return buffers.filter(buffer => {
    const bufferBounds = getFeatureBounds(buffer);
    return boundsOverlap(featureBounds, bufferBounds);
  });
};

// Get bounding box of a feature
const getFeatureBounds = (feature) => {
  if (!feature.geometry || !feature.geometry.coordinates || !feature.geometry.coordinates[0]) {
    return { minX: 0, minY: 0, maxX: 0, maxY: 0 };
  }

  // Get coordinates from the first ring
  const coords = feature.geometry.coordinates[0];

  // Find min/max values
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

// Check if two bounding boxes overlap
const boundsOverlap = (bounds1, bounds2) => {
  return !(
    bounds1.maxX < bounds2.minX ||
    bounds1.minX > bounds2.maxX ||
    bounds1.maxY < bounds2.minY ||
    bounds1.minY > bounds2.maxY
  );
};

// Estimate overlap area (simplified)
const estimateOverlapArea = (feature, buffer) => {
  // In a production environment, you would use proper geometric operations
  // For this simplified version, we'll use a rough estimation

  // Get feature and buffer bounds
  const featureBounds = getFeatureBounds(feature);
  const bufferBounds = getFeatureBounds(buffer);

  // Calculate overlap area of bounds
  const overlapWidth = Math.min(featureBounds.maxX, bufferBounds.maxX) -
    Math.max(featureBounds.minX, bufferBounds.minX);
  const overlapHeight = Math.min(featureBounds.maxY, bufferBounds.maxY) -
    Math.max(featureBounds.minY, bufferBounds.minY);

  if (overlapWidth <= 0 || overlapHeight <= 0) return 0;

  // Approximate overlap area (this is a very rough estimate)
  // In geographic coordinates, this isn't accurate for area
  // but we're just looking for a reasonable approximation
  const overlapArea = overlapWidth * overlapHeight;

  // Convert to square feet using a rough approximation
  // 1 degree of latitude ≈ 69 miles ≈ 364,320 feet
  // 1 degree of longitude varies but around equator ≈ 69 miles
  const FEET_PER_DEGREE_LAT = 364320;
  const FEET_PER_DEGREE_LON = 364320 * Math.cos((featureBounds.minY + featureBounds.maxY) / 2 * Math.PI / 180);

  const overlapAreaFt2 = overlapArea * FEET_PER_DEGREE_LAT * FEET_PER_DEGREE_LON;

  // Apply a correction factor since this is a rough estimate
  // and account for the fact that the real overlap is likely smaller
  // than the bounding box overlap
  const CORRECTION_FACTOR = 0.5; // Assume 50% of bounding box overlap is actual overlap

  return overlapAreaFt2 * CORRECTION_FACTOR;
};

// Add a function to update facilities with available areas
const updateFacilitiesWithAvailableAreas = () => {
  if (!facilitiesGeoJsonData.value || !bufferAnalysisResults.value.length) return;

  // Update each facility with its available area information
  facilitiesGeoJsonData.value.features.forEach(feature => {
    const analysis = bufferAnalysisResults.value.find(
      result => result.area_id === (feature.properties.id || feature.id)
    );

    if (analysis) {
      // Store analysis results in feature properties
      feature.properties.original_area = analysis.original_area_sqft;
      feature.properties.available_area = analysis.available_area_sqft;
      feature.properties.area_reduction = analysis.area_reduction_percent;
      feature.properties.overlapping_buffers = analysis.overlapping_buffers;
      feature.properties.available_geometry = analysis.available_geometry;

      // Update computed area to reflect available space
      feature.properties.computed_area = analysis.available_area_sqft;
    }
  });

  // Re-render the facilities layer
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


// Helper function to check if a point is inside a polygon
const pointInPolygon = (point, polygon) => {
  // Ray casting algorithm
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

// Helper function to return default result
const defaultResult = () => ({
  original_area_sqft: 0,
  available_area_sqft: 0,
  area_reduction_percent: 0,
  overlapping_buffers: [],
  available_geometry: null
});

// Enhance the renderFacilitiesGeoJSONLayer function
const renderFacilitiesGeoJSONLayer = () => {
  console.log("Rendering facilities with filter:", selectedFunction.value);
  console.log("Available filter options:", filteredDropdownOptions.value);
  if (!map.value || !facilitiesGeoJsonData.value) {
    console.error("❌ Map or facilities data is not available.");
    return;
  }

  if (facilitiesGeoJsonLayer.value) {
    facilitiesGeoJsonLayer.value.remove();
  }

  // Clear any existing available layers
  availableLayers.value.forEach(layer => {
    if (map.value) map.value.removeLayer(layer);
  });
  availableLayers.value = [];

  // Filter features based on selected function
  const filteredFeatures = {
    type: "FeatureCollection",
    features: facilitiesGeoJsonData.value.features.filter(feature => {
      const amenity = feature.properties.amenity || "Unknown";

      // Special case for "storage" to show only Free Space and Deicing
      if (selectedFunction.value === "storage") {
        return amenity === "Free Space" || amenity === "Deicing";
      }

      // If no filter is selected (empty string), show all features
      if (!selectedFunction.value) {
        return true;
      }

      // Otherwise, match the exact amenity type
      return amenity === selectedFunction.value;
    })
  };

  // Update areas for all features
  filteredFeatures.features.forEach(feature => {
    // Only process storage areas
    if (feature.properties.amenity === "Free Space" || feature.properties.amenity === "Deicing") {
      // Calculate area without buffer consideration first
      feature.properties.computed_area = computeFeatureArea(feature);

      // If buffer zones are loaded, calculate available area
      if (bufferZonesGeoJsonData.value) {
        const areaAnalysis = calculateAvailableArea(feature, bufferZonesGeoJsonData.value.features);

        // Store analysis results in feature properties
        feature.properties.original_area = areaAnalysis.original_area_sqft;
        feature.properties.available_area = areaAnalysis.available_area_sqft;
        feature.properties.area_reduction = areaAnalysis.area_reduction_percent;
        feature.properties.overlapping_buffers = areaAnalysis.overlapping_buffers;

        // Update computed area to be the available area
        feature.properties.computed_area = areaAnalysis.available_area_sqft;

        // Store available geometry for visualization
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

      // For storage areas, show different colors based on available area
      if (isStorageType) {
        // Use a different color for available vs. unavailable portions
        if (feature.properties.available_geometry) {
          // Create a separate layer for the available area
          const availableLayer = L.geoJSON(feature.properties.available_geometry, {
            style: {
              color: functionType === "Free Space" ? "limegreen" : "lightpink",
              fillColor: functionType === "Free Space" ? "limegreen" : "lightpink",
              fillOpacity: 0.7,
              weight: 2
            }
          }).addTo(map.value);

          // Store reference to clean up later
          availableLayers.value.push(availableLayer);
        }

        return {
          color: colors[functionType] || "black",
          fillColor: colors[functionType] || "black",
          fillOpacity: 0.2,
          weight: 2,
          dashArray: "5,5", // Dashed line to show original boundary
          zIndex: isStorageType ? 1000 : 500 // Higher z-index for storage areas
        };
      }

      // Non-storage areas use normal styling
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
  if (!map.value || !bufferZonesGeoJsonData.value) {
    console.error("❌ Map or buffer zones data is not available.");
    return;
  }

  if (bufferZonesGeoJsonLayer.value) {
    bufferZonesGeoJsonLayer.value.remove();
  }

  // Store all buffer features for click detection
  const bufferFeatures = [];

  // Track if buffer popup was shown
  let bufferPopupShown = false;

  // Create a layer group for all buffer zones
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

    // Store feature data for click detection
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

  // Add click handler to map for buffer detection
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

      // Prevent event from reaching the building boundaries handler
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

// Add toggle layer function
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

// Update handleMapClick to check if buffer popup was shown
const handleMapClick = async (event) => {
  // Skip if clicking inside a buffer zone popup
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

      const buildingInfo = {
        name: building.tags?.name || "Unknown",
        address: building.tags?.addr_full || null,
        amenity: building.tags?.amenity || "Unknown",
        safetyInfo: building.tags?.["fire_hydrant:position"]
          ? "Fire hydrant nearby"
          : "No specific safety information available",
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
        <b>Safety Info:</b> ${buildingInfo.safetyInfo}
      `).openPopup();

      map.value.fitBounds(polygon.getBounds());
    } else {
      alert("No building boundaries found at this location.");
    }
  } catch (error) {
    console.error("Error fetching building boundaries:", error);
    // Don't show alert if we're in a buffer zone
    if (!event.target.getContainer()?.querySelector('.buffer-zones-popup')) {
      alert("Failed to fetch building boundaries.");
    }
  }
};

onMounted(async () => {
  const mapContainer = document.getElementById('map');
  console.log("Map container:", mapContainer); // Should not be null.
  if (!mapContainer) {
    console.error("Map container not found!");
    return;
  }
  console.log("🚀 Initializing map...");
  if (!map.value) {
    map.value = L.map('map').setView([33.6407, -84.4277], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap'
    }).addTo(map.value);
    console.log("✅ Map initialized successfully.");
  } else {
    console.warn("⚠️ Map is already initialized.");
  }

  if (!storageStore.totalH2VolumeGallons || !storageStore.totalFootprint) return;

  // Move map click handler registration after buffer zones are loaded
  await loadFacilitiesGeoJSON();
  renderFacilitiesGeoJSONLayer();

  await loadBufferZones();
  renderBufferZonesGeoJSONLayer();

  // Add click handler last to ensure proper event order
  map.value.on("click", handleMapClick);

  nextTick(() => {
    setTimeout(() => {
      map.value.invalidateSize();
    }, 300);
  });
});

// Add this after your computed properties
watch(selectedFunction, () => {
  console.log("Filter changed to:", selectedFunction.value);
  if (map.value && facilitiesGeoJsonData.value) {
    renderFacilitiesGeoJSONLayer();
  }
});
</script>

<style scoped>
.compliance-map {
  background-color: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  padding: 20px;
  color: #ddd;
}

h2 {
  color: #64ffda;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 20px;
}

.results-section,
.space-check-section,
.compliance-table-section {
  margin-bottom: 20px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
}

.results-section .result-item,
.space-check-section .space-check-item {
  margin-bottom: 10px;
  color: #aaa;
}

.results-section .result-item strong,
.space-check-section .space-check-item strong {
  color: #64ffda;
  font-weight: 600;
}

.results-section .result-item i {
  margin-right: 8px;
  color: #64ffda;
}

.compliance-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  background-color: #282c34;
  border-radius: 8px;
  overflow: hidden;
}

.compliance-table th,
.compliance-table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #ddd;
}

.compliance-table th {
  background-color: rgba(255, 255, 255, 0.05);
  font-weight: 600;
}

.compliance-table tr:nth-child(even) {
  background-color: rgba(255, 255, 255, 0.03);
}

.compliance-table tr:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.no-data-message {
  color: #aaa;
  font-style: italic;
  margin-top: 10px;
}

.legend {
  margin-top: 20px;
  padding: 15px;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: #ddd;
}

.legend h4 {
  margin-bottom: 10px;
  font-size: 1.2rem;
  font-weight: 600;
  color: #64ffda;
}

.legend ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.legend li {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.legend .color-box {
  width: 20px;
  height: 20px;
  margin-right: 10px;
  border-radius: 3px;
}

#map {
  height: 400px;
  width: 100%;
  border: 1px solid #ddd;
}

.layer-controls {
  margin-top: 10px;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.layer-toggles {
  display: flex;
  gap: 15px;
}

.layer-toggles label {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

/* Custom Popup Styles */
:deep(.custom-popup-container) {
  background: #1a1a1a;
  color: #fff;
  border: 1px solid #64ffda;
  border-radius: 4px;
  padding: 0;
  margin: 0;
}

:deep(.custom-popup) {
  padding: 8px;
  font-size: 12px;
  line-height: 1.4;
}

:deep(.custom-popup h3) {
  color: #64ffda;
  font-size: 14px;
  margin: 5px 0;
  padding-bottom: 5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.popup-section:last-child) {
  border-bottom: none;
}

:deep(.popup-section h4) {
  color: #64ffda;
  margin: 2px 0;
  font-size: 1em;
}

:deep(.success) {
  color: #4caf50;
}

:deep(.error) {
  color: #f44336;
}

:deep(.utilization-bar) {
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  margin-top: 5px;
}

:deep(.utilization-bar .fill) {
  height: 100%;
  background: #64ffda;
  border-radius: 2px;
  transition: width 0.3s ease;
}

/* Add these new styles */
:deep(.buffer-zones-popup) {
  max-width: 300px;
}

:deep(.buffer-zones-popup .popup-section) {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  padding: 4px;
  margin: 2px 0;
}

.buffer-analysis-section {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: #282c34;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.buffer-analysis-section h3 {
  margin-bottom: 1rem;
  color: #64ffda;
  border-bottom: 1px solid rgba(100, 255, 218, 0.3);
  padding-bottom: 0.5rem;
}

.buffer-analysis-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.5rem;
}

.buffer-analysis-table th,
.buffer-analysis-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.buffer-analysis-table th {
  background-color: rgba(100, 255, 218, 0.1);
  color: #64ffda;
  font-weight: 600;
}

.buffer-analysis-table tr.compliant {
  background-color: rgba(0, 255, 0, 0.05);
}

.buffer-analysis-table tr.non-compliant {
  background-color: rgba(255, 0, 0, 0.05);
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-badge.compliant {
  background-color: rgba(0, 255, 0, 0.2);
  color: #64ffda;
}

.status-badge.non-compliant {
  background-color: rgba(255, 0, 0, 0.2);
  color: #ff6384;
}

.buffer-details {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
}

.buffer-details h4 {
  margin-bottom: 0.75rem;
  color: #fff;
}

.buffer-details-intro {
  margin-bottom: 1rem;
  color: #aaa;
}

.buffer-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.buffer-item {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 6px;
  overflow: hidden;
}

.buffer-item-header {
  padding: 0.75rem;
  background-color: rgba(100, 255, 218, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.buffer-name {
  font-weight: 600;
  color: #fff;
}

.buffer-type {
  font-size: 0.85rem;
  color: #64ffda;
}

.buffer-item-details {
  padding: 0.75rem;
}

.buffer-stat {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.buffer-stat .label {
  color: #aaa;
}

.buffer-stat .value {
  font-weight: 600;
  color: #fff;
}

.area-selector {
  margin-top: 1.5rem;
}

.area-selector label {
  display: block;
  margin-bottom: 0.5rem;
  color: #aaa;
}

.area-selector select {
  width: 100%;
  padding: 0.75rem;
  background-color: #3a3f4b;
  color: #fff;
  border: 1px solid rgba(100, 255, 218, 0.3);
  border-radius: 4px;
  outline: none;
}

.area-selector select:focus {
  border-color: #64ffda;
}
</style>
