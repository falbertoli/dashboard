// frontend/src/store/regulationsStore.js

import { defineStore } from "pinia";
import { ref } from "vue";
import { api } from "@/utils/api";

export const useRegulationsStore = defineStore("regulations", () => {
  const regulations = ref([]);
  const distancesRequirements = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  const loadRegulations = async () => {
    isLoading.value = true;
    try {
      regulations.value = await api.regulations.getAll();
      console.log("✅ Regulations data loaded:", regulations.value);
    } catch (err) {
      console.error("❌ Error loading regulations:", err);
      error.value = err.message;
    } finally {
      isLoading.value = false;
    }
  };

  const loadDistancesRequirements = async () => {
    isLoading.value = true;
    try {
      distancesRequirements.value = await api.distancesRequirements.getAll();
      console.log(
        "✅ Distance requirements loaded:",
        distancesRequirements.value
      );
    } catch (err) {
      console.error("❌ Error loading distance requirements:", err);
      error.value = err.message;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    regulations,
    distancesRequirements,
    loadRegulations,
    loadDistancesRequirements,
    isLoading,
    error,
  };
});
