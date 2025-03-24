// File: frontend/src/utils/api.js
import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api";

export async function fetchGseOptions() {
  try {
    const response = await fetch(
      "http://localhost:5000/api/hydrogen/gse_options"
    );
    return await response.json();
  } catch (error) {
    console.error("❌ Error fetching GSE options:", error);
    return { data: [] }; // Return an empty array if API fails
  }
}

export const fetchAircraftH2Demand = async (fleetPercentage, year) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/hydrogen/h2_demand/ac`, {
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
    const response = await axios.post(
      `${API_BASE_URL}/hydrogen/h2_demand/gse`,
      {
        gse_list: gseList.length ? gseList : [], // Send empty array if no GSE selected
        end_year: year,
      }
    );

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
