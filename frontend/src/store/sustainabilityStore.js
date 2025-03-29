// File: frontend/src/store/sustainabilityStore.js

import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useHydrogenStore } from "./hydrogenStore";
import { api } from "@/utils/api";
import { EMISSIONS } from "@/utils/constants";

export const useSustainabilityStore = defineStore("sustainability", () => {
  const hydrogenStore = useHydrogenStore();

  // Reactive state
  const emissionsResults = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  // Computed properties
  const totalJetAEmissions = computed(() => {
    if (!emissionsResults.value) return 0;
    return emissionsResults.value.just_jetA_co2 || 0;
  });

  const totalHydrogenEmissions = computed(() => {
    if (!emissionsResults.value) return 0;
    return (
      (emissionsResults.value.jetA_co2 || 0) +
      (emissionsResults.value.H2_co2 || 0)
    );
  });

  const emissionsReduction = computed(() => {
    return totalJetAEmissions.value - totalHydrogenEmissions.value;
  });

  const emissionsReductionPercentage = computed(() => {
    if (totalJetAEmissions.value === 0) return 0;
    return (emissionsReduction.value / totalJetAEmissions.value) * 100;
  });

  const carbonOffsetEquivalent = computed(() => {
    // Average tree absorbs about 25kg of CO2 per year
    // Over 40 years, that's about 1 metric ton
    const tonsReduction = emissionsReduction.value / 1000; // Convert kg to metric tons
    return Math.round(tonsReduction * 1);
  });

  const vehicleEquivalent = computed(() => {
    // Average car emits about 4.6 metric tons of CO2 per year
    const tonsReduction = emissionsReduction.value / 1000; // Convert kg to metric tons
    return Math.round(tonsReduction / 4.6);
  });

  // Actions
  const calculateEmissions = async () => {
    if (!hydrogenStore.aircraftH2Demand || !hydrogenStore.gseH2Demand) {
      error.value = "Hydrogen demand data is required to calculate emissions";
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      // Extract values from hydrogen store
      const jetAWeight =
        hydrogenStore.aircraftH2Demand.projected_fuel_weight_lb || 0;
      const h2Weight = hydrogenStore.totalH2Demand * 4.43; // Convert ft³ to lb using density

      // GSE fuel weights
      const dieselWeight = hydrogenStore.gseH2Demand.total_diesel_used_lb || 0;
      const gasolineWeight =
        hydrogenStore.gseH2Demand.total_gasoline_used_lb || 0;

      // Baseline fuel weight (if all operations used conventional fuels)
      const fuelWeight = jetAWeight + h2Weight * 2.8; // Convert H2 to Jet A equivalent

      const response = await api.sustainability.calculateEmissions({
        jetA_weight: jetAWeight,
        H2_weight: h2Weight,
        Fuel_weight: fuelWeight,
        diesel_weight: dieselWeight,
        gasoline_weight: gasolineWeight,
      });

      emissionsResults.value = response.data;
    } catch (err) {
      console.error("Error calculating emissions:", err);
      error.value = err.message || "Failed to calculate emissions";
    } finally {
      isLoading.value = false;
    }
  };

  const reset = () => {
    emissionsResults.value = null;
    error.value = null;
  };

  return {
    // State
    emissionsResults,
    isLoading,
    error,

    // Computed properties
    totalJetAEmissions,
    totalHydrogenEmissions,
    emissionsReduction,
    emissionsReductionPercentage,
    carbonOffsetEquivalent,
    vehicleEquivalent,

    // Actions
    calculateEmissions,
    reset,
  };
});
