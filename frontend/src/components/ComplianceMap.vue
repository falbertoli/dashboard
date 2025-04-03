<template>
  <div class="compliance-map">
    <h2>Compliance Map</h2>


    <!-- Results Section -->
    <div class="results-section">
      <div class="result-item">
        <span>Total Hydrogen Demand:</span>
        <strong>{{ storageStore.totalH2VolumeGallons.toFixed(2) }} gallons</strong>
      </div>
      <div class="result-item">
        <span>Total Footprint Storage:</span>
        <strong>{{ storageStore.totalFootprint.toFixed(2) }} ft²</strong>
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
      <table class="compliance-table">
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
          <tr v-for="feature in filteredFacilities" :key="feature.properties.id">
            <td>{{ feature.properties.name || "Unknown" }}</td>
            <td>{{ feature.properties.amenity || "Unknown" }}</td>
            <td>{{ feature.properties.sq_ft || "N/A" }}</td>
            <td>
              {{
                feature.properties.sq_ft && storageStore.totalFootprint
                  ? feature.properties.sq_ft >= storageStore.totalFootprint
                    ? "Yes"
                    : "No"
                  : "Data Unavailable"
              }}
            </td>
            <td>
              {{
                feature.properties.sq_ft
                  ? ((storageStore.totalFootprint / feature.properties.sq_ft) * 100).toFixed(2) + "%"
                  : "N/A"
              }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>


    <!-- Filter by function -->
    <div class="filter-container">
      <label for="function-filter">Filter by Amenity:</label>
      <select id="function-filter" v-model="selectedFunction" @change="renderFacilitiesGeoJSONLayer">
        <option value="">All</option>
        <option v-for="functionType in uniqueFunctions" :key="functionType" :value="functionType">
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


      <!-- Legend -->
      <div class="legend">
        <h4>Legend</h4>
        <ul>
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


const storageStore = useStorageStore();
const map = ref(null);
const geojsonData = ref(null);
const error = ref(null);
const geoJsonLayer = ref(null);
const isLoading = ref(false);


const facilitiesGeoJsonData = ref(null);
const facilitiesGeoJsonLayer = ref(null);
const selectedFunction = ref(""); // Selected function for filtering


// Compute unique functions for the dropdown filter
const uniqueFunctions = computed(() => {
  if (!facilitiesGeoJsonData.value) return [];
  const functions = facilitiesGeoJsonData.value.features.map((feature) => feature.properties.amenity || "Unknown");
  return [...new Set(functions)];
});


// Check if "Free Space" or "Deicing" buildings have enough space
const freeSpaceStatus = computed(() => {
  if (!facilitiesGeoJsonData.value || !storageStore.totalFootprint) return "Data Unavailable";
  const freeSpace = facilitiesGeoJsonData.value.features.find(
    (feature) => feature.properties.amenity === "Free Space"
  );
  return freeSpace && freeSpace.properties.sq_ft >= storageStore.totalFootprint
    ? "Sufficient Space"
    : "Insufficient Space";
});


const deicingStatus = computed(() => {
  if (!facilitiesGeoJsonData.value || !storageStore.totalFootprint) return "Data Unavailable";
  const deicing = facilitiesGeoJsonData.value.features.find(
    (feature) => feature.properties.amenity === "Deicing"
  );
  return deicing && deicing.properties.sq_ft >= storageStore.totalFootprint
    ? "Sufficient Space"
    : "Insufficient Space";
});


// Update the table rendering logic to handle null or undefined data
const facilities = computed(() => facilitiesGeoJsonData.value?.features || []);


// Filter facilities to only include "Free Space" or "Deicing"
const filteredFacilities = computed(() => {
  return facilitiesGeoJsonData.value?.features.filter((feature) => {
    const functionType = feature.properties.amenity;
    return functionType === "Free Space" || functionType === "Deicing";
  }) || [];
});


const loadGeoJSON = async () => {
  isLoading.value = true;
  try {
    // Commenting out the loading of atl_areas.geojson
    // geojsonData.value = await api.map.getAvailableAreas();
    // await processGeoJSON();
  } catch (err) {
    error.value = `Failed to load map data: ${err.message}`;
    console.error('❌ Error fetching map data:', err);
  } finally {
    isLoading.value = false;
  }
};


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


const evaluateCompliance = async (feature) => {
  const area = feature.properties.area_sqft;
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


const processGeoJSON = async () => {
  if (!geojsonData.value) return;
};


const renderGeoJSONLayer = () => {
  if (!map.value || !geojsonData.value) return;


  if (geoJsonLayer.value) {
    geoJsonLayer.value.remove();
  }
};


const renderFacilitiesGeoJSONLayer = () => {
  if (!map.value || !facilitiesGeoJsonData.value) {
    console.error("❌ Map or facilities data is not available.");
    return;
  }


  console.log("🚀 Rendering facilities layer with data:", facilitiesGeoJsonData.value);


  if (facilitiesGeoJsonLayer.value) {
    facilitiesGeoJsonLayer.value.remove();
    console.log("✅ Removed existing facilities layer.");
  }


  facilitiesGeoJsonLayer.value = L.geoJSON(facilitiesGeoJsonData.value, {
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
        "Free Space": feature.properties.sq_ft >= storageStore.totalFootprint ? "limegreen" : "darkgreen",
        Deicing: feature.properties.sq_ft >= storageStore.totalFootprint ? "lightpink" : "darkred",
        Unknown: "black", // Default color for unknown functions
      };
      const functionType = feature.properties.amenity || "Unknown";
      return {
        color: colors[functionType] || "black",
        fillColor: colors[functionType] || "black",
        fillOpacity: 0.5,
        weight: 1,
      };
    },
    onEachFeature: (feature, layer) => {
      const props = feature.properties;
      const isRelevant = props.amenity === "Free Space" || props.amenity === "Deicing";
      const canContainFootprint = isRelevant
        ? props.sq_ft >= storageStore.totalFootprint
          ? "Yes"
          : "No"
        : null;


      let popupContent = `
        <b>${props.name || "Unknown"}</b><br>
        Amenity: ${props.amenity || "Unknown"}<br>
        Area: ${props.sq_ft || "N/A"} sqft<br>
        Address: ${props.address || "N/A"}<br>
        Description: ${props.description || "N/A"}<br>
        Distance Requirements:<br>
        - Contains People: ${props.distance_requirements?.contains_people ? "Yes" : "No"}<br>
        - Contains Flammable Liquids: ${props.distance_requirements?.contains_flammable_liquids ? "Yes" : "No"}<br>
        - Contains Open Fire: ${props.distance_requirements?.contains_open_fire ? "Yes" : "No"}
      `;


      if (isRelevant) {
        popupContent += `<br>Can Contain Footprint: ${canContainFootprint}`;
      }


      layer.bindPopup(popupContent);


      // Add a polygon representing the storage space proportionally if the area can contain the footprint
      if (isRelevant && canContainFootprint === "Yes") {
        const bounds = layer.getBounds();
        const availableArea = props.sq_ft;
        const storageArea = storageStore.totalFootprint;


        // Calculate the proportional size of the storage space
        const proportion = Math.sqrt(storageArea / availableArea);


        const center = bounds.getCenter();
        const latDiff = (bounds.getNorth() - bounds.getSouth()) * proportion / 2;
        const lngDiff = (bounds.getEast() - bounds.getWest()) * proportion / 2;


        const storagePolygonBounds = [
          [center.lat - latDiff, center.lng - lngDiff],
          [center.lat - latDiff, center.lng + lngDiff],
          [center.lat + latDiff, center.lng + lngDiff],
          [center.lat + latDiff, center.lng - lngDiff],
        ];


        L.polygon(storagePolygonBounds, {
          color: "#3b82f6", // Blue border
          fillColor: "#93c5fd", // Light blue fill
          fillOpacity: 0.7,
          weight: 2,
        }).addTo(map.value);
      }
    },
  }).addTo(map.value);


  console.log("✅ Facilities layer added to the map.");
};


const handleMapClick = async (event) => {
  const { lat, lng } = event.latlng;
  console.log("Map clicked at:", lat, lng);


  try {
    // Query Overpass API for building boundaries
    const overpassUrl = `https://overpass-api.de/api/interpreter?data=[out:json];way(around:50,${lat},${lng})["building"];out geom;`;
    const response = await fetch(overpassUrl);
    const data = await response.json();
    console.log("Overpass API result:", data);


    if (data.elements && data.elements.length > 0) {
      const building = data.elements[0];
      const boundaries = building.geometry.map((point) => [point.lat, point.lon]);
      console.log("Building boundaries:", boundaries);


      // Extract building information dynamically
      const buildingInfo = {
        name: building.tags?.name || "Unknown",
        address: building.tags?.addr_full || null, // Address may be null
        amenity: building.tags?.amenity || "Unknown",
        safetyInfo: building.tags?.["fire_hydrant:position"]
          ? "Fire hydrant nearby"
          : "No specific safety information available",
      };


      // Fallback to reverse geocoding if address is missing
      if (!buildingInfo.address) {
        const geocodeResponse = await fetch(
          `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`
        );
        const geocodeData = await geocodeResponse.json();
        buildingInfo.address = geocodeData.display_name || "Unknown";
      }


      // Draw the building boundaries on the map
      const polygon = L.polygon(boundaries, {
        color: "blue",
        weight: 2,
        fillOpacity: 0.3,
      }).addTo(map.value);


      // Bind a popup with building information
      polygon.bindPopup(`
        <b>Building Name:</b> ${buildingInfo.name}<br>
        <b>Address:</b> ${buildingInfo.address}<br>
        <b>Amenity:</b> ${buildingInfo.amenity}<br>
        <b>Safety Info:</b> ${buildingInfo.safetyInfo}
      `).openPopup();


      // Fit the map view to the polygon
      map.value.fitBounds(polygon.getBounds());
    } else {
      alert("No building boundaries found at this location.");
    }
  } catch (error) {
    console.error("Error fetching building boundaries:", error);
    alert("Failed to fetch building boundaries.");
  }
};


onMounted(async () => {
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


  // Commenting out the loading and rendering of atl_areas.geojson
  // await loadGeoJSON();
  await loadFacilitiesGeoJSON();


  // renderGeoJSONLayer();
  renderFacilitiesGeoJSONLayer();


  map.value.on("click", handleMapClick);


  nextTick(() => {
    map.value.invalidateSize();
  });
});


watch(
  () => [storageStore.totalFootprint, storageStore.totalH2VolumeGallons],
  async ([footprint, volume]) => {
    if (footprint && volume) {
      await loadGeoJSON();
      renderGeoJSONLayer();
    }
  }
);
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
</style>
