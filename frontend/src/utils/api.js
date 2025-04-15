// frontend/src/utils/api.js

import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api";

// Create an axios instance for consistent configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Individual export functions (legacy approach)
export async function fetchGseOptions() {
  try {
    const response = await fetch(`${API_BASE_URL}/hydrogen/gse_options`);
    return await response.json();
  } catch (error) {
    console.error("❌ Error fetching GSE options:", error);
    return { data: [] }; // Return an empty array if API fails
  }
}

export const fetchAircraftH2Demand = async (fleetPercentage, year) => {
  try {
    const response = await apiClient.post(`/hydrogen/h2_demand/ac`, {
      slider_perc: fleetPercentage / 100, // Convert percentage to fraction
      end_year: year,
    });
    return response.data.data;
  } catch (error) {
    console.error("Error fetching aircraft hydrogen demand:", error);
    throw error;
  }
};

export const fetchGSEH2Demand = async (gseList, year) => {
  try {
    console.log("🚀 Sending GSE Demand Request:", {
      gse_list: gseList,
      end_year: year,
    });

    // Ensure an empty list is sent correctly
    const response = await apiClient.post(`/hydrogen/h2_demand/gse`, {
      gse_list: gseList.length ? gseList : [], // Send empty array if no GSE selected
      end_year: year,
    });

    console.log("✅ GSE Demand Response:", response.data);
    return response.data.data;
  } catch (error) {
    console.error(
      "❌ Error fetching GSE hydrogen demand:",
      error.response?.data || error
    );
    throw error;
  }
};

// New organized API object
export const api = {
  hydrogen: {
    getGseOptions: fetchGseOptions,
    calculateAircraftDemand: fetchAircraftH2Demand,
    calculateGseDemand: fetchGSEH2Demand,

    // Calculate storage area
    calculateStorageArea: async (h2DemandVol) => {
      try {
        const response = await apiClient.post("/hydrogen/storage_area", {
          h2_demand_vol: h2DemandVol,
        });
        return response.data;
      } catch (error) {
        console.error("Storage area calculation error:", error);
        throw error;
      }
    },
  },

  storage: {
    // Calculate storage costs and requirements
    calculate: async (params) => {
      try {
        const response = await apiClient.post("/storage/calculate", params);
        return response.data;
      } catch (error) {
        console.error("Storage calculation error:", error);
        throw error;
      }
    },
  },

  sustainability: {
    calculateEmissions: async (params) => {
      try {
        console.log("📊 Sending emissions calculation request:", params);
        const response = await apiClient.post(
          "/sustainability/emissions",
          params
        );
        console.log("✅ Emissions calculation response:", response.data);
        return response.data;
      } catch (error) {
        console.error("❌ Error calculating emissions:", error);
        throw error;
      }
    },
  },

  economics: {
    calculateEconomicImpact: async (params) => {
      try {
        console.log(
          "Sending economic impact calculation request with params:",
          params
        );
        // Use apiClient instead of axios directly
        const response = await apiClient.post("/economic/impact", params);
        return response.data;
      } catch (error) {
        console.error("Error calculating economic impact:", error);
        throw error;
      }
    },
  },

  regulations: {
    getAll: async () => {
      try {
        const response = await apiClient.get("/regulations/all");
        return response.data;
      } catch (error) {
        console.error("Error fetching regulations:", error);
        throw error;
      }
    },
    getCompliantDistance: async (params) => {
      try {
        const response = await apiClient.get(
          "/regulations/compliant_distance",
          { params }
        );
        return response.data;
      } catch (error) {
        console.error("Error checking compliant distance:", error);
        throw error;
      }
    },
  },
  distancesRequirements: {
    getAll: async () => {
      try {
        const response = await apiClient.get("/distances_requirements/all");
        return response.data;
      } catch (error) {
        console.error("Error fetching distances requirements:", error);
        throw error;
      }
    },
    checkAreaCompliance: async (storage_volume_gal, area_id) => {
      try {
        const response = await apiClient.get(
          "/distances_requirements/check_area_compliance",
          {
            params: { storage_volume_gal, area_id },
          }
        );
        return response.data;
      } catch (error) {
        console.error("Error checking area compliance:", error);
        throw error;
      }
    },
  },
  map: {
    getFacilities: async () => {
      try {
        console.log("🚀 Fetching facilities data...");
        const response = await apiClient.get("/map/facilities");
        console.log("✅ Facilities data fetched:", response.data);
        return response.data;
      } catch (error) {
        console.error(
          "❌ Error fetching facilities data:",
          error.message || error
        );
        throw error;
      }
    },
  },
  buffer_zones: {
    getBuffers: async () => {
      try {
        const response = await apiClient.get("/buffer_zones/buffers");
        if (response.status === 200 && response.data?.features) {
          console.log("✅ Buffer Zones Loaded:", response.data);
          return response.data;
        } else {
          console.error("❌ Unexpected buffer zone response:", response.data);
          throw new Error("Invalid buffer zones data received.");
        }
      } catch (error) {
        console.error(
          "🚨 Buffer Zones Fetch Failed:",
          error.message,
          error.response?.data
        );
        throw error;
      }
    },
    analyzeStorageAreas: async (storageVolumeGal = null) => {
      try {
        const params = storageVolumeGal
          ? { storage_volume_gal: storageVolumeGal }
          : {};
        const response = await apiClient.get(
          "/buffer_zones/storage-area-analysis",
          { params }
        );
        console.log("✅ Storage area analysis complete:", response.data);
        return response.data;
      } catch (error) {
        console.error("🚨 Storage Area Analysis Failed:", error.message);
        throw error;
      }
    },
  },
};
