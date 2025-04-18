// File: frontend/src/store/sustainabilityStore.js

import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useHydrogenStore } from "./hydrogenStore";
import { api } from "@/utils/api";
import { AVIATION } from "../utils/constants";

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
    // A mature tree absorbs approximately 22 kg of CO₂ per year
    // It takes about 45 years for a tree to absorb 1 metric ton of CO₂
    // Our emissions values are already in metric tons, so no division needed
    return Math.round(emissionsReduction.value);
  });

  const conventionalTreeEquivalent = computed(() => {
    // Using the same calculation logic as carbonOffsetEquivalent but for conventional operations
    return Math.round(totalJetAEmissions.value);
  });

  const vehicleEquivalent = computed(() => {
    // Average passenger vehicle emits about 4.6 metric tons of CO₂ per year
    // Our emissions values are already in metric tons, so no division needed
    return Math.round(emissionsReduction.value / 4.6);
  });

  const conventionalVehicleEquivalent = computed(() => {
    // Average passenger vehicle emits about 4.6 metric tons of CO₂ per year
    // Our emissions values are already in metric tons, so no division needed
    return Math.round(totalJetAEmissions.value / 4.6);
  });

  // Actions
  const calculateEmissions = async () => {
    if (!hydrogenStore.aircraftH2Demand || !hydrogenStore.gseH2Demand) {
      console.error("Missing hydrogen demand data:", {
        aircraftH2Demand: hydrogenStore.aircraftH2Demand,
        gseH2Demand: hydrogenStore.gseH2Demand,
      });
      error.value = "Hydrogen demand data is required to calculate emissions";
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      // Extract values from hydrogen store
      // Total fuel weight for conventional operations
      const sliderPercentage = hydrogenStore.fleetPercentage / 100; // Convert percentage to decimal
      const currentYear = hydrogenStore.year; // Get the selected year from hydrogen store

      const totalFuelWeight =
        hydrogenStore.aircraftH2Demand.projected_fuel_weight_lb /
          sliderPercentage || 0;

      // Jet A weight for hybrid operations (reduced by hydrogen percentage)
      const jetAWeight =
        (hydrogenStore.aircraftH2Demand.projected_fuel_weight_lb /
          sliderPercentage) *
          (1 - sliderPercentage) || 0;

      // Total H2 weight from both aircraft and ground vehicles (in lbs)
      const aircraftH2Weight =
        hydrogenStore.aircraftH2Demand.projected_fuel_weight_lb /
          AVIATION.HYDROGEN.PHYSICAL.CONVERSION_FACTOR || 0;
      const gseH2Weight = hydrogenStore.gseH2Demand.total_h2_weight_lb || 0;
      const totalH2Weight = aircraftH2Weight + gseH2Weight;

      console.log("📊 Emissions calculation request:", {
        sliderPercentage: sliderPercentage,
        year: currentYear,
        aircraftH2Weight: aircraftH2Weight,
        gseH2Weight: gseH2Weight,
        jetA_weight: jetAWeight,
        H2_weight: totalH2Weight,
        Fuel_weight: totalFuelWeight,
      });

      // Send parameters exactly as the backend expects them
      const response = await api.sustainability.calculateEmissions({
        jetA_weight: jetAWeight,
        H2_weight: totalH2Weight,
        Fuel_weight: totalFuelWeight,
        year: currentYear, // Add the year parameter
      });

      console.log("✅ Emissions calculation response:", response);

      // Store results based on response structure
      if (response && typeof response === "object") {
        if (
          response.data &&
          typeof response.data === "object" &&
          "jetA_co2" in response.data
        ) {
          console.log("📊 Using response.data for emissions");
          emissionsResults.value = response.data;
        } else if ("jetA_co2" in response) {
          console.log("📊 Using response directly for emissions");
          emissionsResults.value = response;
        } else {
          console.error("❌ Unexpected response format:", response);
          error.value = "Received an unexpected data format from the server";
        }
      } else {
        console.error("❌ Invalid response type:", typeof response);
        error.value = "Received an invalid response from the server";
      }

      console.log("📊 Stored emissionsResults:", emissionsResults.value);

      // Debug - Print the emissions values
      if (emissionsResults.value) {
        console.log(
          `Remaining Jet A Emissions: ${emissionsResults.value.jetA_co2} metric tons CO2`
        );
        console.log(
          `H2 Emissions: ${emissionsResults.value.H2_co2} metric tons CO2`
        );
        console.log(
          `Just Jet A Emissions: ${emissionsResults.value.just_jetA_co2} metric tons CO2`
        );

        // Log computed properties
        console.log("📈 Calculated emissions metrics:", {
          totalJetAEmissions: totalJetAEmissions.value,
          totalHydrogenEmissions: totalHydrogenEmissions.value,
          emissionsReduction: emissionsReduction.value,
          emissionsReductionPercentage: emissionsReductionPercentage.value,
        });
      }
    } catch (err) {
      console.error("❌ Error calculating emissions:", err);
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
    conventionalTreeEquivalent,
    conventionalVehicleEquivalent,
    vehicleEquivalent,

    // Actions
    calculateEmissions,
    reset,
  };
});
