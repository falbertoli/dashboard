import { defineStore } from "pinia";
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
    year: new Date().getFullYear(),
    aircraftH2Demand: null,
    gseH2Demand: null,
  }),
  actions: {
    async loadGSEOptions() {
      this.gseOptions = await fetchGseOptions();
    },
    async loadAircraftH2Demand() {
      this.aircraftH2Demand = await fetchAircraftH2Demand(
        this.fleetPercentage,
        this.year
      );
    },
    async loadGSEH2Demand() {
      this.gseH2Demand = await fetchGSEH2Demand(this.gseList, this.year);
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
