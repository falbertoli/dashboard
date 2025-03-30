// File: frontend/src/store/economicsStore.js

import { defineStore } from "pinia";
import { api } from "@/utils/api";
import { useHydrogenStore } from "@/store/hydrogenStore";

export const useEconomicsStore = defineStore("economics", {
  state: () => ({
    results: null, // Will store both scenarios and summary
    isLoading: false,
    error: null,
    // Store the last used parameters for reference
    lastParams: null,
  }),

  getters: {
    // Get scenario summary metrics
    scenarioSummary() {
      if (!this.results || !this.results.summary) return {};
      return this.results.summary;
    },
  },

  actions: {
    async fetchEconomicImpact(paramsOverride = {}) {
      this.isLoading = true;
      this.error = null;

      try {
        // Access hydrogen phase values from the Hydrogen Store
        const hydrogenStore = useHydrogenStore();
        const totalH2Demand = parseFloat(hydrogenStore.totalH2Demand || 0);
        const fleetPercentage = hydrogenStore.fleetPercentage / 100 || 0.1; // Convert from percentage to decimal
        const year = hydrogenStore.year || 2036;
        const currentYear = new Date().getFullYear();

        // Define default parameters. Note the added finalH2Year parameter.
        const defaultParams = {
          totalH2Demand,
          fleetPercentage,
          startYear: currentYear,
          endYear: year,
          finalH2Year: year, // <-- Added new parameter; defaulting to 'year'
          growthRate: 0.02,
          extraTurnTime: 30,
          turnTimeDecreaseRates: [0, 1, 2, 3, 4, 5],
        };

        // Merge parameters (overrides from UI, for example)
        const params = { ...defaultParams, ...paramsOverride };

        // Store the parameters for reference
        this.lastParams = { ...params };

        console.log("Economic calculation parameters:", params);

        // Call the API
        const response = await api.economics.calculateEconomicImpact(params);

        // Store the updated response format
        this.results = response.data;
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
