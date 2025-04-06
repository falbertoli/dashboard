// File: frontend/src/store/bufferAnalysisStore.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from "@/utils/api";
import { useHydrogenStore } from "./hydrogenStore";

export const useBufferAnalysisStore = defineStore("bufferAnalysis", () => {
  const hydrogenStore = useHydrogenStore();

  // State
  const analysisResults = ref(null);
  const selectedAreaId = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  // Computed properties
  const totalAreas = computed(() => analysisResults.value?.total_areas || 0);

  const compliantAreas = computed(
    () => analysisResults.value?.compliant_areas || 0
  );

  const compliancePercentage = computed(() =>
    totalAreas.value > 0
      ? ((compliantAreas.value / totalAreas.value) * 100).toFixed(1)
      : 0
  );

  const selectedArea = computed(() => {
    if (!analysisResults.value || !selectedAreaId.value) return null;
    return analysisResults.value.results.find(
      (area) => area.area_id === selectedAreaId.value
    );
  });

  const sortedAreas = computed(() => {
    if (!analysisResults.value) return [];

    // Sort areas by available area (largest first)
    return [...analysisResults.value.results].sort(
      (a, b) => b.available_area_sqft - a.available_area_sqft
    );
  });

  // Actions
  const analyzeStorageAreas = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      // Get hydrogen volume in gallons from hydrogen store
      const h2VolumeGallons = hydrogenStore.totalH2VolumeGallons;

      // Call API
      analysisResults.value = await api.buffer_zones.analyzeStorageAreas(
        h2VolumeGallons
      );

      // Auto-select the first compliant area if any exist
      const firstCompliantArea = analysisResults.value.results.find(
        (area) => area.compliance_status === "compliant"
      );

      if (firstCompliantArea) {
        selectedAreaId.value = firstCompliantArea.area_id;
      } else if (analysisResults.value.results.length > 0) {
        // Otherwise select the first area
        selectedAreaId.value = analysisResults.value.results[0].area_id;
      }
    } catch (err) {
      console.error("Error analyzing storage areas:", err);
      error.value = err.message || "Failed to analyze storage areas";
    } finally {
      isLoading.value = false;
    }
  };

  const selectArea = (areaId) => {
    selectedAreaId.value = areaId;
  };

  const reset = () => {
    analysisResults.value = null;
    selectedAreaId.value = null;
    error.value = null;
  };

  return {
    // State
    analysisResults,
    selectedAreaId,
    isLoading,
    error,

    // Computed
    totalAreas,
    compliantAreas,
    compliancePercentage,
    selectedArea,
    sortedAreas,

    // Actions
    analyzeStorageAreas,
    selectArea,
    reset,
  };
});
