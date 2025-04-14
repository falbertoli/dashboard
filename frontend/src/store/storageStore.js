// File: frontend/src/store/storageStore.js

import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useHydrogenStore } from "./hydrogenStore";
import { api } from "@/utils/api";
import { STORAGE } from "@/utils/constants";

export const useStorageStore = defineStore("storage", () => {
  const hydrogenStore = useHydrogenStore();

  // Reactive state - using diameter to match backend parameter names
  const tankDiameter = ref(STORAGE.TANK.DIMENSIONS.DIAMETER_FT);
  const tankLength = ref(STORAGE.TANK.DIMENSIONS.LENGTH_FT);
  const constructionCost = ref(STORAGE.COSTS.CONSTRUCTION);
  const insulationCost = ref(STORAGE.COSTS.INSULATION);
  const results = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  // Computed properties aligned with the original Python script
  const usableVolumePerTank = computed(() => {
    // Match Python: Water_cap = 18014/7.48052 #gal->ft3
    const waterCapacityFt3 =
      STORAGE.TANK.DIMENSIONS.WATER_CAPACITY_GAL /
      STORAGE.CONVERSIONS.GALLON_TO_FT3;

    return (
      (waterCapacityFt3 *
        (1 - STORAGE.TANK.EFFICIENCY.ULLAGE) *
        STORAGE.TANK.EFFICIENCY.EVAPORATION_LOSS) /
      100
    );
  });

  const totalH2Volume = computed(() => {
    return parseFloat(hydrogenStore.totalH2Demand * 11 || 0);
  });

  // Raw tank count calculation
  const rawTankCount = computed(() => {
    if (!totalH2Volume.value || !usableVolumePerTank.value) return 0;
    return totalH2Volume.value / usableVolumePerTank.value;
  });

  // Recommended tank count - now using Math.ceil without any limits
  const recommendedTankCount = computed(() => {
    if (!rawTankCount.value) return 1; // Default to 1 tank
    return Math.ceil(rawTankCount.value);
  });

  // Information about the last tank's fill level
  const lastTankFillPercentage = computed(() => {
    if (
      !totalH2Volume.value ||
      !usableVolumePerTank.value ||
      !recommendedTankCount.value
    )
      return 0;

    // Calculate how much of the last tank is filled
    const volumeInFullTanks =
      (recommendedTankCount.value - 1) * usableVolumePerTank.value;
    const volumeInLastTank = totalH2Volume.value - volumeInFullTanks;
    return (volumeInLastTank / usableVolumePerTank.value) * 100;
  });

  // Add total storage capacity
  const totalStorageCapacity = computed(() => {
    return usableVolumePerTank.value * recommendedTankCount.value;
  });

  const totalH2VolumeGallons = computed(() => {
    // Convert from cubic feet to gallons using the conversion factor
    return totalH2Volume.value * STORAGE.CONVERSIONS.FT3_TO_GALLON;
  });

  // Match original Python: area_tank = tank_width*tank_length
  const tankFootprint = computed(() => {
    return tankDiameter.value * tankLength.value;
  });

  // Match original Python: area_tot = area_tank*nbr_tanks
  const totalFootprint = computed(() => {
    if (results.value && results.value.footprint_total) {
      return results.value.footprint_total;
    }
    // Fallback calculation matching Python
    return tankFootprint.value * recommendedTankCount.value;
  });

  // Insulation volume calculation matching the storage cost calculation
  const insulationVolume = computed(() => {
    if (!totalH2Volume.value || recommendedTankCount.value <= 0) return 0;

    // Convert to cubic feet using the storage cost calculation factor
    const totalH2VolumeCuft = totalH2VolumeGallons.value * 0.1337;

    // h_over_d = tank_length_ft / tank_diameter_ft
    const hOverD = tankLength.value / tankDiameter.value;

    // Match storage cost calculation formula exactly
    return (
      Math.PI *
      Math.pow(tankDiameter.value / 2.0, 2) *
      (2.0 * hOverD - 1.0 / 3.0) *
      (totalH2VolumeCuft / recommendedTankCount.value)
    );
  });

  // Calculate insulation cost
  const insulationCostTotal = computed(() => {
    if (results.value && results.value.insulation_cost) {
      return results.value.insulation_cost;
    }
    return insulationVolume.value * insulationCost.value;
  });

  // Calculate construction cost
  const constructionCostTotal = computed(() => {
    if (results.value && results.value.construction_cost) {
      return results.value.construction_cost;
    }
    return totalFootprint.value * constructionCost.value;
  });

  // Calculate total infrastructure cost
  const totalCost = computed(() => {
    if (results.value && results.value.total_infrastructure_cost) {
      return results.value.total_infrastructure_cost;
    }
    return insulationCostTotal.value + constructionCostTotal.value;
  });

  // Actions
  const calculateRequirements = async () => {
    if (!totalH2Volume.value) {
      error.value = "No hydrogen demand data available";
      return;
    }

    console.log("--- Storage Calculation Debug ---");
    console.log("Total H2 Volume (ft³):", totalH2Volume.value);
    console.log("Total H2 Volume (gallons):", totalH2VolumeGallons.value);
    console.log(
      "Water Capacity (ft³):",
      STORAGE.TANK.DIMENSIONS.WATER_CAPACITY_GAL /
        STORAGE.CONVERSIONS.GALLON_TO_FT3
    );
    console.log(
      "After Ullage:",
      (STORAGE.TANK.DIMENSIONS.WATER_CAPACITY_GAL /
        STORAGE.CONVERSIONS.GALLON_TO_FT3) *
        (1 - STORAGE.TANK.EFFICIENCY.ULLAGE)
    );
    console.log(
      "Evaporation Factor:",
      STORAGE.TANK.EFFICIENCY.EVAPORATION_LOSS
    );
    console.log("Usable Volume per Tank (ft³):", usableVolumePerTank.value);
    console.log("Raw Tank Count:", rawTankCount.value);
    console.log(
      "Recommended Tank Count (ceiling):",
      recommendedTankCount.value
    );
    console.log(
      "Last Tank Fill Percentage:",
      lastTankFillPercentage.value.toFixed(2) + "%"
    );
    console.log("Total Storage Capacity (ft³):", totalStorageCapacity.value);
    console.log("Tank Footprint (ft²):", tankFootprint.value);
    console.log("Total Footprint (ft²):", totalFootprint.value);
    console.log("Insulation Volume (ft³):", insulationVolume.value);
    console.log("-------------------------------");

    isLoading.value = true;
    error.value = null;

    try {
      // Call the API to calculate storage requirements
      // Use parameter names that match the storage cost calculation function
      const response = await api.storage.calculate({
        total_h2_volume_gal: totalH2VolumeGallons.value,
        number_of_tanks: recommendedTankCount.value,
        tank_diameter_ft: tankDiameter.value, // Matches storage cost parameter name
        tank_length_ft: tankLength.value,
        cost_per_sqft_construction: constructionCost.value,
        cost_per_cuft_insulation: insulationCost.value,
      });

      results.value = response.data;
      console.log("API Response:", results.value);
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
    totalStorageCapacity,
    totalH2Volume,
    totalH2VolumeGallons,
    tankFootprint,
    totalFootprint,
    insulationVolume,
    insulationCostTotal,
    constructionCostTotal,
    totalCost,
    recommendedTankCount,
    rawTankCount, // New property
    lastTankFillPercentage, // New property

    // Actions
    calculateRequirements,
    reset,
  };
});
