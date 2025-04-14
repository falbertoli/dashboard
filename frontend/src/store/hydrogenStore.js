// File: frontend/src/store/hydrogenStore.js

import { defineStore } from "pinia";
import { computed, watch } from "vue";

import {
  fetchAircraftH2Demand,
  fetchGSEH2Demand,
  fetchGseOptions,
} from "../utils/api";

// Import the storage store to reset it when needed
import { useStorageStore } from "./storageStore";
import { useSustainabilityStore } from "./sustainabilityStore";

export const useHydrogenStore = defineStore("hydrogen", {
  state: () => ({
    fleetPercentage: 10,
    gseList: [],
    gseOptions: [],
    year: 2036, // Set default year to 2036
    aircraftH2Demand: null,
    gseH2Demand: null,
  }),
  getters: {
    totalH2Demand: (state) => {
      const aircraftDemand = state.aircraftH2Demand?.daily_h2_demand_ft3 || 0;
      const gseDemand = state.gseH2Demand?.daily_h2_demand_ft3 || 0;
      return (aircraftDemand + gseDemand).toFixed(2);
    },
  },
  actions: {
    // Helper method to reset storage calculations
    resetStorageCalculations() {
      const storageStore = useStorageStore();
      if (storageStore.results) {
        console.log(
          "Resetting storage calculations due to hydrogen demand change"
        );
        storageStore.reset();
      }
    },

    resetEmissionsCalculations() {
      const sustainabilityStore = useSustainabilityStore();
      if (sustainabilityStore.emissionsResults) {
        console.log(
          "Resetting sustainabilty calculations due to hydrogen demand change"
        );
        sustainabilityStore.reset();
      }
    },

    async loadGSEOptions() {
      this.gseOptions = await fetchGseOptions();
    },

    async loadAircraftH2Demand() {
      try {
        const oldDemand = this.aircraftH2Demand?.daily_h2_demand_ft3 || 0;
        this.aircraftH2Demand = await fetchAircraftH2Demand(
          this.fleetPercentage,
          this.year
        );
        const newDemand = this.aircraftH2Demand?.daily_h2_demand_ft3 || 0;

        // Reset storage calculations if demand changed
        if (oldDemand !== newDemand) {
          this.resetStorageCalculations();
          this.resetEmissionsCalculations();
        }
      } catch (error) {
        console.error("Error fetching aircraft H2 demand:", error);
        this.aircraftH2Demand = null; // Clear data on error
        this.resetStorageCalculations(); // Reset storage on error too
      }
    },

    async loadGSEH2Demand() {
      try {
        const oldDemand = this.gseH2Demand?.daily_h2_demand_ft3 || 0;
        this.gseH2Demand = await fetchGSEH2Demand(this.gseList, this.year);
        const newDemand = this.gseH2Demand?.daily_h2_demand_ft3 || 0;

        // Reset storage calculations if demand changed
        if (oldDemand !== newDemand) {
          this.resetStorageCalculations();
          this.resetEmissionsCalculations();
        }
      } catch (error) {
        console.error("Error fetching GSE H2 demand:", error);
        this.gseH2Demand = null; // Clear data on error
        this.resetStorageCalculations(); // Reset storage on error too
      }
    },

    setFleetPercentage(value) {
      this.fleetPercentage = value;
      this.loadAircraftH2Demand();
    },

    setGseList(list) {
      console.log("✅ Setting GSE List in Store:", list);
      this.gseList = list;
      this.loadGSEH2Demand();
    },

    setYear(year) {
      this.year = year;
      this.loadAircraftH2Demand();
      this.loadGSEH2Demand();
    },
  },
});
