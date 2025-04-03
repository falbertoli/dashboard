<!-- File: frontend/src/views/RegulationsView.vue -->
<template>
  <div class="regulations-view">
    <h1>Regulatory Compliance</h1>

    <section>
      <h2>Regulations Overview</h2>
      <div class="table-container">
        <RegulationsTable :items="formattedRegulations"
          caption="List of regulations and their minimum storage requirements." />
      </div>
    </section>

    <section>
      <h2>Distance Requirements</h2>
      <div class="table-container">
        <RegulationsTable :items="formattedDistancesRequirements"
          caption="Distance requirements for various storage scenarios." />
      </div>
    </section>

    <section>
      <h2>Compliance Map</h2>
      <ComplianceMap :storageVolume="storageStore.totalH2VolumeFromHydrogenStore" />
      <!-- <p v-if="!isStorageVolumeValid" class="error">
        Warning: Hydrogen storage volume is not defined. Please configure it.
      </p> -->
    </section>
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import RegulationsTable from "../components/RegulationsTable.vue";
import ComplianceMap from "../components/ComplianceMap.vue";
import { useStorageStore } from "../store/storageStore";
import { useRegulationsStore } from "../store/regulationsStore";

export default {
  components: {
    RegulationsTable,
    ComplianceMap,
  },
  setup() {
    const storageStore = useStorageStore();
    const regulationsStore = useRegulationsStore();

    // Debug log for storage volume
    console.log("Hydrogen Storage Volume:", storageStore.totalH2VolumeFromHydrogenStore);

    // Computed property to validate storage volume
    const isStorageVolumeValid = computed(() => {
      const volume = storageStore.totalH2VolumeFromHydrogenStore;
      return volume !== null && volume !== undefined && volume > 0;
    });

    // Format data to ensure proper mapping
    const formattedRegulations = computed(() =>
      regulationsStore.regulations.map(item => ({
        regulation_name: item.regulation_name || item["﻿regulation_name"], // Handle BOM issue
        regulation_info: item.regulation_info || "N/A",
        storage_gal_min: item.storage_gal_min || "N/A",
      }))
    );

    const formattedDistancesRequirements = computed(() =>
      regulationsStore.distancesRequirements.map(item => ({
        regulation_name: item.regulation_name || item["﻿regulation_name"], // Handle BOM issue
        regulation_info: item.regulation_info || "N/A",
        storage_gal_min: item.storage_gal_min || "N/A",
        storage_gal_max: item.storage_gal_max || "N/A",
        safety_distance_ft: item.safety_distance_ft || "N/A",
      }))
    );

    // Load data on component mount
    onMounted(async () => {
      await regulationsStore.loadRegulations();
      await regulationsStore.loadDistancesRequirements();
    });

    return {
      formattedRegulations,
      formattedDistancesRequirements,
      storageStore,
      isStorageVolumeValid,
    };
  },
};
</script>

<style scoped>
.regulations-view {
  padding: 20px;
}

section {
  margin-bottom: 30px;
}

h2 {
  margin-bottom: 10px;
  font-size: 1.5rem;
  color: #64ffda;
  /* Match the theme color */
}

.table-container {
  overflow-x: auto;
  background: rgba(255, 255, 255, 0.05);
  /* Darker background */
  border: 1px solid #444;
  border-radius: 8px;
  padding: 10px;
  margin-top: 10px;
}

.error {
  color: red;
  font-size: 1rem;
  margin-top: 10px;
}
</style>