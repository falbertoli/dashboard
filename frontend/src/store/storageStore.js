// File: frontend/src/store/storageStore.js

import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useHydrogenStore } from "./hydrogenStore";
import { api } from "@/utils/api";
import { STORAGE } from "@/utils/constants";

export const useStorageStore = defineStore("storage", () => {
  const hydrogenStore = useHydrogenStore();

  // Reactive state
  const tankDiameter = ref(STORAGE.TANK.DIMENSIONS.DIAMETER_FT);
  const tankLength = ref(STORAGE.TANK.DIMENSIONS.LENGTH_FT);
  const constructionCost = ref(STORAGE.COSTS.CONSTRUCTION);
  const insulationCost = ref(STORAGE.COSTS.INSULATION);
  const results = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  // Computed properties
  const usableVolumePerTank = computed(() => {
    const waterCapacityFt3 =
      STORAGE.TANK.DIMENSIONS.WATER_CAPACITY_GAL *
      STORAGE.CONVERSIONS.GALLON_TO_FT3;

    return (
      waterCapacityFt3 *
      (1 - STORAGE.TANK.EFFICIENCY.ULLAGE) *
      STORAGE.TANK.EFFICIENCY.EVAPORATION_LOSS
    );
  });

  const totalH2Volume = computed(() => {
    return parseFloat(hydrogenStore.totalH2Demand || 0);
  });

  // Add recommended tank count calculation
  const recommendedTankCount = computed(() => {
    if (!totalH2Volume.value || !usableVolumePerTank.value) return 4; // Default

    // Add buffer factor (10% extra capacity for safety)
    const bufferFactor = 1.1;

    // Calculate how many tanks needed to store the total hydrogen volume
    const calculatedCount = Math.ceil(
      (totalH2Volume.value * bufferFactor) / usableVolumePerTank.value
    );

    // Apply min/max constraints
    return Math.max(1, Math.min(20, calculatedCount));
  });

  const totalH2VolumeGallons = computed(() => {
    return totalH2Volume.value * STORAGE.CONVERSIONS.FT3_TO_GALLON;
  });

  const totalFootprint = computed(() => {
    if (!results.value) return 0;
    return results.value.footprint_total || 0;
  });

  const totalCost = computed(() => {
    if (!results.value) return 0;
    return results.value.total_infrastructure_cost || 0;
  });

  // Actions
  const calculateRequirements = async () => {
    if (!totalH2Volume.value) {
      error.value = "No hydrogen demand data available";
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      // Call the API to calculate storage requirements
      const response = await api.storage.calculate({
        total_h2_volume_gal: totalH2VolumeGallons.value,
        number_of_tanks: recommendedTankCount.value, // Use the computed value
        tank_diameter_ft: tankDiameter.value,
        tank_length_ft: tankLength.value,
        cost_per_sqft_construction: constructionCost.value,
        cost_per_cuft_insulation: insulationCost.value,
      });

      results.value = response.data;
    } catch (err) {
      console.error("Storage calculation error:", err);
      error.value = err.message || "Failed to calculate storage requirements";
    } finally {
      isLoading.value = false;
    }
  };

  const reset = () => {
    tankDiameter.value = STORAGE.TANK.DIMENSIONS.DIAMETER_FT;
    tankLength.value = STORAGE.TANK.DIMENSIONS.LENGTH_FT;
    constructionCost.value = STORAGE.COSTS.CONSTRUCTION;
    insulationCost.value = STORAGE.COSTS.INSULATION;
    results.value = null;
    error.value = null;
  };

  return {
    // State
    tankDiameter,
    tankLength,
    constructionCost,
    insulationCost,
    results,
    isLoading,
    error,

    // Computed
    usableVolumePerTank,
    totalH2Volume,
    totalH2VolumeGallons,
    totalFootprint,
    totalCost,
    recommendedTankCount, // Export the computed property

    // Actions
    calculateRequirements,
    reset,
  };
});
