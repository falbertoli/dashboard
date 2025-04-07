// src/store/hydrogenStore.js
import { defineStore } from "pinia";
import { computed, watch } from "vue";

import {
  fetchAircraftH2Demand,
  fetchGSEH2Demand,
  fetchGseOptions,
} from "../utils/api";

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
    async loadGSEOptions() {
      this.gseOptions = await fetchGseOptions();
    },
    async loadAircraftH2Demand() {
      try {
        this.aircraftH2Demand = await fetchAircraftH2Demand(
          this.fleetPercentage,
          this.year
        );
      } catch (error) {
        console.error("Error fetching aircraft H2 demand:", error);
        this.aircraftH2Demand = null; // Clear data on error
      }
    },
    async loadGSEH2Demand() {
      try {
        this.gseH2Demand = await fetchGSEH2Demand(this.gseList, this.year);
      } catch (error) {
        console.error("Error fetching GSE H2 demand:", error);
        this.gseH2Demand = null; // Clear data on error
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
