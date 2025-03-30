<!-- File: frontend/src/views/RegulationsView.vue -->
<template>
  <div class="regulations-view">
    <h1>Regulatory Compliance</h1>

    <h2>Applicable Regulations</h2>
    <DataTable :headers="regulationHeaders" :items="regulationsStore.regulations" />

    <h2>Distances requirements</h2>
    <DataTable :headers="distancesRequirementsHeaders" :items="regulationsStore.distancesRequirements" />

    <h2>Compliance Map</h2>
    <ComplianceMap :storageVolume="storageStore.totalH2VolumeFromHydrogenStore" />
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import DataTable from "../components/DataTable.vue";
import ComplianceMap from "../components/ComplianceMap.vue"; // Import ComplianceMap
import { useStorageStore } from "../store/storageStore";
import { useRegulationsStore } from "../store/regulationsStore"; // Import the new store

export default {
  components: {
    DataTable,
    ComplianceMap, // Register ComplianceMap
  },
  setup() {
    const storageStore = useStorageStore();
    const regulationsStore = useRegulationsStore(); // Use the regulations store

    const regulationColumns = ref([
      { key: "regulation_id", label: "ID" },
      { key: "regulation_name", label: "Name" },
      { key: "regulation_info", label: "Info" },
      { key: "storage_gal_min", label: "Min Storage (Gal)" },
    ]);
    const distancesRequirementsColumns = ref([
      { key: "regulation_id", label: "ID" },
      { key: "regulation_name", label: "Name" },
      { key: "regulation_info" },
      { key: "storage_gal_min", label: "Min Storage (Gal)" },
      { key: "storage_gal_max", label: "Max Storage (Gal)" },
      { key: "safety_distance_ft", label: "Safety Distance (ft)" },
    ]);

    const regulationHeaders = ref(regulationColumns.value.map(col => col.key));
    const distancesRequirementsHeaders = ref(distancesRequirementsColumns.value.map(col => col.key));

    onMounted(async () => {
      await regulationsStore.loadRegulations();
      await regulationsStore.loadDistancesRequirements();
    });

    return {
      regulationHeaders,
      distancesRequirementsHeaders,
      storageStore,
      regulationsStore, // Return the store
    };
  },
};
</script>

<style scoped>
.regulations-view {
  padding: 20px;
}
</style>