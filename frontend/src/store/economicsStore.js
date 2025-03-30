// File: frontend/src/useEconomicsStore.js

import { defineStore } from "pinia";
import { api } from "@/utils/api";
import { useHydrogenStore } from "@/store/hydrogenStore"; // Import the Hydrogen Store

export const useEconomicsStore = defineStore("economics", {
  state: () => ({
    results: null, // Store results for each scenario
    isLoading: false, // Loading state
    error: null, // Error state
  }),
  actions: {
    async fetchEconomicImpact(paramsOverride = {}) {
      this.isLoading = true;
      this.error = null;

      try {
        // Access hydrogen phase values from the Hydrogen Store
        const hydrogenStore = useHydrogenStore();
        const totalH2Demand = parseFloat(hydrogenStore.totalH2Demand || 0);
        const fleetPercentage = hydrogenStore.fleetPercentage || 0.1; // Default to 10%
        const year = hydrogenStore.year || 2036; // Default to 2036

        console.log("Hydrogen Phase Values:", {
          totalH2Demand,
          fleetPercentage,
          year,
        });

        // Define default parameters for the economic impact calculation
        const defaultParams = {
          totalH2Demand, // Hydrogen demand
          fleetPercentage, // Hydrogen fleet percentage
          startYear: 2023, // Current year
          endYear: year, // Target year for hydrogen adoption
          growthRate: 0.02, // 2% annual growth rate
          extraTurnTime: 30, // Initial extra turnaround time (minutes)
          turnTimeDecreaseRates: [0, 1, 2, 3, 4, 5], // Turnaround time reduction scenarios
        };

        // Merge default parameters with any overrides provided by the caller
        const params = { ...defaultParams, ...paramsOverride };

        // Call the API to calculate economic impact
        const response = await api.economics.calculateEconomicImpact(params);

        // Store results for visualization
        this.results = response;
        console.log("Economic Impact Results:", this.results);
      } catch (err) {
        console.error("Error fetching economic impact data:", err);
        this.error = err.message || "Failed to fetch economic impact data.";
      } finally {
        this.isLoading = false;
      }
    },
  },
});
