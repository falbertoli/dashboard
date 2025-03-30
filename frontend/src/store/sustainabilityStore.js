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
    // A mature tree absorbs approximately 22 kg of CO₂ per year
    // It takes about 45 years for a tree to absorb 1 metric ton of CO₂
    // Our emissions values are already in metric tons, so no division needed
    return Math.round(emissionsReduction.value);
  });

  const vehicleEquivalent = computed(() => {
    // Average passenger vehicle emits about 4.6 metric tons of CO₂ per year
    // Our emissions values are already in metric tons, so no division needed
    return Math.round(emissionsReduction.value / 4.6);
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
      const jetAWeight =
        hydrogenStore.aircraftH2Demand.projected_fuel_weight_lb || 0;
      const h2Weight = hydrogenStore.totalH2Demand * 4.43; // Convert ft³ to lb using density

      // GSE fuel weights (not used by the current backend implementation)
      const dieselWeight = hydrogenStore.gseH2Demand.total_diesel_used_lb || 0;
      const gasolineWeight =
        hydrogenStore.gseH2Demand.total_gasoline_used_lb || 0;

      // Baseline fuel weight (if all operations used conventional fuels)
      const fuelWeight = jetAWeight + h2Weight * 2.8; // Convert H2 to Jet A equivalent

      console.log("📊 Emissions calculation request:", {
        jetA_weight: jetAWeight,
        H2_weight: h2Weight,
        Fuel_weight: fuelWeight,
      });

      // Only send the parameters the backend expects
      const response = await api.sustainability.calculateEmissions({
        jetA_weight: jetAWeight,
        H2_weight: h2Weight,
        Fuel_weight: fuelWeight,
      });

      // Debug code from Step 1
      console.log("🔍 API Response Type:", typeof response);
      console.log("🔍 API Response Keys:", Object.keys(response));

      if (response.data) {
        console.log("🔍 Response.data Type:", typeof response.data);
        console.log("🔍 Response.data Keys:", Object.keys(response.data));
      } else {
        console.log("🔍 Response has no 'data' property");
      }

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

      // ADD THIS CODE RIGHT HERE - STEP 2: Debug Computed Properties
      if (emissionsResults.value) {
        // Log raw values from emissionsResults
        console.log("🔢 Raw emissions values:", {
          jetA_co2: emissionsResults.value.jetA_co2,
          H2_co2: emissionsResults.value.H2_co2,
          just_jetA_co2: emissionsResults.value.just_jetA_co2,
        });

        // Test computed properties directly
        const jetA = emissionsResults.value.just_jetA_co2 || 0;
        const h2Combined =
          (emissionsResults.value.jetA_co2 || 0) +
          (emissionsResults.value.H2_co2 || 0);
        const reduction = jetA - h2Combined;
        const percentage = jetA > 0 ? (reduction / jetA) * 100 : 0;

        console.log("🧮 Manual calculation check:", {
          manualJetA: jetA,
          manualH2Combined: h2Combined,
          manualReduction: reduction,
          manualPercentage: percentage,

          // Compare with computed properties
          computedJetA: totalJetAEmissions.value,
          computedH2Combined: totalHydrogenEmissions.value,
          computedReduction: emissionsReduction.value,
          computedPercentage: emissionsReductionPercentage.value,
        });

        // Check for discrepancies
        if (
          Math.abs(jetA - totalJetAEmissions.value) > 0.001 ||
          Math.abs(h2Combined - totalHydrogenEmissions.value) > 0.001 ||
          Math.abs(reduction - emissionsReduction.value) > 0.001
        ) {
          console.warn(
            "⚠️ Discrepancy detected between manual calculations and computed properties"
          );
        } else {
          console.log("✅ Manual calculations match computed properties");
        }
      }
      // END OF STEP 2 CODE

      console.log("📈 Calculated emissions metrics:", {
        totalJetAEmissions: totalJetAEmissions.value,
        totalHydrogenEmissions: totalHydrogenEmissions.value,
        emissionsReduction: emissionsReduction.value,
        emissionsReductionPercentage: emissionsReductionPercentage.value,
      });
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
    vehicleEquivalent,

    // Actions
    calculateEmissions,
    reset,
  };
});
