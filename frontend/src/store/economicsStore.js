// File: frontend/src/store/economicsStore.js

import { defineStore } from "pinia";
import { api } from "@/utils/api";
import { useHydrogenStore } from "@/store/hydrogenStore";

export const useEconomicsStore = defineStore("economics", {
  state: () => ({
    results: null, // Will store both scenarios and summary data
    isLoading: false,
    error: null,
    // Store the last used parameters for reference
    lastParams: null,
    lastCalculationTime: null,
    autoRecalculate: false,
  }),

  getters: {
    // Get scenario summary metrics
    scenarioSummary() {
      if (!this.results || !this.results.summary) return {};
      return this.results.summary;
    },

    // Get max tax credit for each scenario
    maxTaxCredits() {
      if (!this.results || !this.results.scenarios) return {};

      const maxCredits = {};
      Object.entries(this.results.scenarios).forEach(([rate, data]) => {
        const maxCredit = Math.max(
          ...data.map((item) => item.Req_Tax_Credit_per_gal || 0)
        );
        maxCredits[rate] = maxCredit.toFixed(2);
      });

      return maxCredits;
    },

    // Get max revenue drop for each scenario
    maxRevenueDrops() {
      if (!this.results || !this.results.scenarios) return {};

      const maxDrops = {};
      Object.entries(this.results.scenarios).forEach(([rate, data]) => {
        const maxDrop = Math.max(...data.map((item) => item.Pct_Drop || 0));
        maxDrops[rate] = maxDrop.toFixed(2);
      });

      return maxDrops;
    },

    // Get final year tax credit for each scenario
    finalYearTaxCredits() {
      if (!this.results || !this.results.scenarios) return {};

      const finalCredits = {};
      Object.entries(this.results.scenarios).forEach(([rate, data]) => {
        if (data.length > 0) {
          const finalCredit = data[data.length - 1].Req_Tax_Credit_per_gal || 0;
          finalCredits[rate] = finalCredit.toFixed(2);
        }
      });

      return finalCredits;
    },

    // Get comparison data for all scenarios
    scenarioComparison() {
      if (!this.results || !this.results.scenarios) return [];

      return Object.keys(this.results.scenarios).map((rate) => {
        return {
          rate: parseInt(rate),
          maxTaxCredit: `$${this.maxTaxCredits[rate]}/gal`,
          maxRevenueDrop: `${this.maxRevenueDrops[rate]}%`,
          finalYearTaxCredit: `$${this.finalYearTaxCredits[rate]}/gal`,
        };
      });
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

        // Define default parameters
        const defaultParams = {
          totalH2Demand,
          fleetPercentage,
          startYear: 2023,
          endYear: year,
          finalH2Year: year,
          growthRate: 0.02,
          extraTurnTime: 30,
          turnTimeDecreaseRates: [0, 1, 2, 3, 4, 5],
        };

        // Merge parameters (overrides from UI)
        const params = { ...defaultParams, ...paramsOverride };

        // Store the parameters for reference
        this.lastParams = { ...params };

        console.log("Economic calculation parameters:", params);

        // Call the API
        const response = await api.economics.calculateEconomicImpact(params);

        // Store the response
        this.results = response.data;
        this.lastCalculationTime = new Date();
        console.log("Economic Impact Results:", this.results);
      } catch (err) {
        console.error("Error fetching economic impact data:", err);
        this.error = err.message || "Failed to fetch economic impact data.";
      } finally {
        this.isLoading = false;
      }
    },

    // Method to reset calculation results
    resetResults() {
      this.results = null;
    },

    // Method to export scenario data as CSV
    exportScenarioData(scenarioRate) {
      if (
        !this.results ||
        !this.results.scenarios ||
        !this.results.scenarios[scenarioRate]
      ) {
        throw new Error("No scenario data available to export");
      }

      const scenarioData = this.results.scenarios[scenarioRate];
      const headers = Object.keys(scenarioData[0]).join(",");
      const rows = scenarioData.map((row) => Object.values(row).join(","));

      return [headers, ...rows].join("\n");
    },

    setAutoRecalculate(value) {
      this.autoRecalculate = value;
    },
  },
});
