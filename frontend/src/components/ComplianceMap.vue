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

    <!-- Filter by Amenity -->
    <div class="filter-container">
      <label for="function-filter">Filter by Amenity:</label>
      <select id="function-filter" v-model="selectedFunction" @change="renderFacilitiesGeoJSONLayer">
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

const selectedFunction = ref("storage"); // Special value to indicate Free Space and Deicing

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

// Add new computed property for filtered dropdown options
const filteredDropdownOptions = computed(() => {
  return uniqueFunctions.value.filter(type => type !== 'storage');
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

const loadBufferZones = async () => {
  try {
    console.log("🚀 Fetching buffer zones...");
    bufferZonesGeoJsonData.value = await api.buffer_zones.getBuffers();
    console.log("✅ Buffer Zones data loaded:", bufferZonesGeoJsonData.value);
    renderBufferZonesGeoJSONLayer();
  } catch (err) {
    console.error("❌ Error loading buffer zones:", err.message || err);
    error.value = `Failed to load buffer zones data: ${err.message || err}`;
  }
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

// Enhance the renderFacilitiesGeoJSONLayer function
const renderFacilitiesGeoJSONLayer = () => {
  if (!map.value || !facilitiesGeoJsonData.value) {
    console.error("❌ Map or facilities data is not available.");
    return;
  }

  if (facilitiesGeoJsonLayer.value) {
    facilitiesGeoJsonLayer.value.remove();
  }

  // Filter features based on selected function
  const filteredFeatures = {
    type: "FeatureCollection",
    features: facilitiesGeoJsonData.value.features.filter(feature => {
      const amenity = feature.properties.amenity;
      if (selectedFunction.value === "storage") {
        // Show only Free Space and Deicing
        return amenity === "Free Space" || amenity === "Deicing";
      }
      return !selectedFunction.value || amenity === selectedFunction.value;
    })
  };

  // Update areas for all features
  filteredFeatures.features.forEach(feature => {
    feature.properties.computed_area = computeFeatureArea(feature);
  });

  facilitiesGeoJsonLayer.value = L.geoJSON(filteredFeatures, {
    style: (feature) => {
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
      const functionType = feature.properties.amenity || "Unknown";
      const isStorageType = functionType === "Free Space" || functionType === "Deicing";

      return {
        color: colors[functionType] || "black",
        fillColor: colors[functionType] || "black",
        fillOpacity: 0.5,
        weight: 1,
        zIndex: isStorageType ? 1000 : 500 // Higher z-index for storage areas
      };
    },
    onEachFeature: (feature, layer) => {
      const props = feature.properties;
      const computedArea = props.computed_area;
      const isRelevant = props.amenity === "Free Space" || props.amenity === "Deicing";
      const storageUtilization = isRelevant ?
        ((storageStore.totalFootprint / computedArea) * 100).toFixed(1) : null;

      let popupContent = `
        <div class="custom-popup">
          <h3>${props.name || "Unknown Building"}</h3>
          <div class="popup-section">
            <h4>General Information</h4>
            <p><strong>Amenity:</strong> ${props.amenity || "Unknown"}</p>
            <p><strong>Area:</strong> ${computedArea.toFixed(2)} ft²</p>
            ${props.address ? `<p><strong>Address:</strong> ${props.address}</p>` : ''}
          </div>
          ${isRelevant ? `
            <div class="popup-section storage-info">
              <h4>Storage Capability</h4>
              <p><strong>Can Store:</strong> ${computedArea >= storageStore.totalFootprint ?
            '<span class="success">Yes</span>' : '<span class="error">No</span>'}</p>
              <p><strong>Space Utilization:</strong> ${storageUtilization}%</p>
              <div class="utilization-bar">
                <div class="fill" style="width: ${Math.min(storageUtilization, 100)}%"></div>
              </div>
            </div>
          ` : ''}
          ${props.compliance_reason ? `
            <div class="popup-section safety-info">
              <h4>Safety Requirements</h4>
              <p>${props.compliance_reason}</p>
              ${props.required_safety_distance_ft ? `
                <p><strong>Required Distance:</strong> ${props.required_safety_distance_ft} ft</p>
                <p><strong>Actual Distance:</strong> ${props.actual_distance_ft} ft</p>
              ` : ''}
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
</style>
