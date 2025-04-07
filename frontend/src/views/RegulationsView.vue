<!-- File: frontend/src/views/RegulationsView.vue -->
<template>

  <div class="regulations-view">
    <div class="page-header">
      <h1><i class="fas fa-gavel"></i>Regulations and Compliance</h1>
      <p class="description">
        This section provides an overview of the regulations and compliance requirements for hydrogen storage systems.
        It includes a list of regulations, their minimum storage requirements, and distance requirements for various
        storage scenarios.
        <br />
        <strong>Disclaimer:</strong> The information provided in this section is for informational purposes only and
        should not be considered legal advice. Always consult with a qualified professional or regulatory authority for
        specific compliance requirements.
        <br />
        <strong>Note:</strong> Ensure that your storage system complies with all applicable regulations and safety
        standards.
        <br />
      </p>
    </div>


    <section>
      <h2><i class="fas fa-book-open"></i>List of regulations and their minimum storage requirements</h2>
      <div class="table-container">
        <RegulationsTable :items="formattedRegulations" />
      </div>
    </section>

    <section>
      <h2><i class="fas fa-ruler"></i>Distance requirements for various storage scenarios</h2>
      <div class="table-container">
        <RegulationsTable :items="formattedDistancesRequirements" />
      </div>
    </section>

    <section>
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

h1 {
  color: #64ffda;
  font-size: 1.8rem;
  margin-bottom: 25px;
}

h2 {
  color: #64ffda;
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

h2 i {
  opacity: 0.8;
  width: 20px;
}

.table-container {
  overflow-x: auto;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 20px;
  margin-top: 10px;
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}

.error {
  color: #ff6b6b;
  font-size: 1rem;
  margin-top: 10px;
  padding: 10px;
  background: rgba(255, 107, 107, 0.1);
  border-radius: 4px;
}
</style>