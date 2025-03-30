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

    const evaluateCompliance = (feature) => {
      const area = feature.properties.area_sqft;
      const footprintNeeded = storageStore.totalFootprint;
      const enoughSpace = area >= footprintNeeded;

      const distancesCompliance =
        feature.properties.distance_to_flammable_liquids_compliant &&
        feature.properties.distance_to_people_compliant &&
        feature.properties.distance_to_open_fire_compliant;

      if (!enoughSpace) return "non-compliant";
      if (enoughSpace && distancesCompliance) return "compliant";
      return "partially-compliant";
    };

    const processGeoJSON = () => {
      if (!geojsonData.value) return;

      geojsonData.value.features.forEach(feature => {
        feature.properties.compliance_status = evaluateCompliance(feature);
      });
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

          let reasons = [];

          const enoughSpace = props.area_sqft >= storageStore.totalFootprint;
          if (!enoughSpace) {
            reasons.push("Insufficient space");
          }

          if (!props.distance_to_flammable_liquids_compliant) {
            reasons.push("Flammable liquids distance issue");
          }

          if (!props.distance_to_people_compliant) {
            reasons.push("People distance issue");
          }

          if (!props.distance_to_open_fire_compliant) {
            reasons.push("Open fire distance issue");
          }

          const reasonText = reasons.length > 0 ? reasons.join(", ") : "Fully compliant";

          layer.bindPopup(`
    <b>${props.name}</b><br>
    Available Area: ${props.area_sqft} sqft<br>
    Required Footprint: ${storageStore.totalFootprint} sqft<br>
    <strong>Status: ${compliance}</strong><br>
    Reason: ${reasonText}
  `);
        }
      }).addTo(map.value);
    };

    onMounted(async () => {
      await loadGeoJSON();
      processGeoJSON();

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

    watch(() => storageStore.totalFootprint, () => {
      processGeoJSON();
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