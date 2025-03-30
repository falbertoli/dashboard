<template>
  <div class="compliance-map">
    <div id="map"></div>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css';
import { useStorageStore } from "../store/storageStore";
import { ref, onMounted, watch, nextTick } from "vue";
import L from 'leaflet';
import { api } from '@/utils/api';

export default {
  setup() {
    const storageStore = useStorageStore();
    const map = ref(null);
    const geojsonData = ref(null);
    const error = ref(null);
    const geoJsonLayer = ref(null);

    const loadGeoJSON = async () => {
      try {
        geojsonData.value = await api.map.getAvailableAreas();
        console.log("✅ GeoJSON data loaded:", geojsonData.value);
      } catch (err) {
        error.value = `Failed to load geoJSON: ${err.message}`;
        console.error("❌ Error fetching map data:", err);
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
      } catch (error) {
        console.error("Error fetching compliance data:", error);
        complianceData = { is_compliant: false, reason: 'Compliance check failed' };
      }

      feature.properties.compliance_reason = complianceData.reason;
      feature.properties.required_safety_distance_ft = complianceData.required_safety_distance_ft;
      feature.properties.actual_distance_ft = complianceData.actual_distance_ft;

      const distancesCompliance = complianceData.is_compliant;

      if (!enoughSpace) return "non-compliant";
      if (enoughSpace && distancesCompliance) return "compliant";
      return "partially-compliant";
    };

    const processGeoJSON = async () => {
      if (!geojsonData.value) return;

      const compliancePromises = geojsonData.value.features.map(async feature => {
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
            "compliant": "green",
            "partially-compliant": "yellow",
            "non-compliant": "red"
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
            Required Distance: ${props.required_safety_distance_ft || 'N/A'} ft<br>
            Actual Distance: ${props.actual_distance_ft || 'N/A'} ft<br>
            <strong>Status: ${compliance}</strong><br>
            Reason: ${props.compliance_reason || 'N/A'}
          `);
        }
      }).addTo(map.value);
    };

    onMounted(async () => {
      await loadGeoJSON();
      await processGeoJSON();

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

    watch(() => storageStore.totalFootprint, async () => {
      await processGeoJSON();
      renderGeoJSONLayer();
    });

    return { map, error };
  }
};
</script>

<style scoped>
.compliance-map {
  width: 100%;
  height: 400px;
  position: relative;
}

#map {
  width: 100%;
  height: 100%;
}

.error {
  color: red;
}
</style>