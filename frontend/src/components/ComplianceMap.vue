<template>
  <div class="compliance-map">
    <h2>Compliance Map</h2>

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
    <div v-else id="map"></div>
  </div>
</template>

<script setup>
import 'leaflet/dist/leaflet.css';
import { useStorageStore } from '../store/storageStore';
import { ref, onMounted, watch, nextTick } from 'vue';
import L from 'leaflet';
import { api } from '@/utils/api';

const storageStore = useStorageStore();
const map = ref(null);
const geojsonData = ref(null);
const error = ref(null);
const geoJsonLayer = ref(null);
const isLoading = ref(false);

const loadGeoJSON = async () => {
  isLoading.value = true;
  try {
    geojsonData.value = await api.map.getAvailableAreas();
    await processGeoJSON();
  } catch (err) {
    error.value = `Failed to load map data: ${err.message}`;
    console.error('❌ Error fetching map data:', err);
  } finally {
    isLoading.value = false;
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

  const compliancePromises = geojsonData.value.features.map(async (feature) => {
    feature.properties.compliance_status = await evaluateCompliance(feature);
  });

  await Promise.all(compliancePromises);
};

const renderGeoJSONLayer = () => {
  if (!map.value || !geojsonData.value) return;

  if (geoJsonLayer.value) {
    geoJsonLayer.value.remove();
  }

  geoJsonLayer.value = L.geoJSON(geojsonData.value, {
    style: (feature) => {
      const colors = {
        compliant: 'green',
        'partially-compliant': 'yellow',
        'non-compliant': 'red'
      };
      return {
        color: colors[feature.properties.compliance_status],
        fillColor: colors[feature.properties.compliance_status],
        fillOpacity: 0.6,
        weight: 2
      };
    },
    onEachFeature: (feature, layer) => {
      const props = feature.properties;
      const compliance = props.compliance_status;

      layer.bindPopup(`
        <b>${props.name}</b><br>
        Available Area: ${props.area_sqft} sqft<br>
        Required Footprint: ${storageStore.totalFootprint} sqft<br>
        Required Safety Distance: ${props.required_safety_distance_ft || 'N/A'} ft<br>
        Actual Distance: ${props.actual_distance_ft || 'N/A'} ft<br>
        <strong>Status: ${compliance}</strong><br>
        Reason: ${props.compliance_reason || 'N/A'}
      `);
    }
  }).addTo(map.value);
};

onMounted(async () => {
  if (!storageStore.totalH2VolumeGallons || !storageStore.totalFootprint) return;

  await loadGeoJSON();

  map.value = L.map('map').setView([33.6407, -84.4277], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
  }).addTo(map.value);

  renderGeoJSONLayer();

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
  background-color: #282c34;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  color: #ddd;
}

h2 {
  margin-bottom: 15px;
  color: #fff;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 8px;
}

#map {
  width: 100%;
  height: 400px;
  border-radius: 6px;
}

.alert {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 6px;
  background-color: rgba(54, 162, 235, 0.1);
  border-left: 4px solid rgba(54, 162, 235, 0.8);
  color: #ddd;
}

.alert i {
  margin-right: 10px;
  font-size: 1.2rem;
}

.loading,
.error-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  color: #64ffda;
}

.spinner {
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top: 4px solid #64ffda;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.error-message {
  color: #e74c3c;
  border-left: 4px solid #e74c3c;
  background-color: rgba(231, 76, 60, 0.1);
  border-radius: 6px;
}
</style>