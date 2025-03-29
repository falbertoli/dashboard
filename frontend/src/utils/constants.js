// File: frontend/src/utils/constants.js

/**
 * 🚀 HYDROGEN INFRASTRUCTURE CONSTANTS
 * Organized by domain with clear hierarchy
 * Mirrors backend values with frontend-friendly structure
 */

// ========================
// 🏗️  STORAGE
// ========================
export const STORAGE = {
  TANK: {
    DIMENSIONS: {
      WIDTH_FT: 10.1667,
      LENGTH_FT: 56.5,
      DIAMETER_FT: 10,
      WATER_CAPACITY_GAL: 18014,
    },
    EFFICIENCY: {
      ULLAGE: 0.05, // % volume for gas form
      EVAPORATION_LOSS: 99.25, // Daily LH2 loss
    },
  },
  COSTS: {
    CONSTRUCTION: 580, // $/ft²
    INSULATION: 15, // $/ft³
  },
  CONVERSIONS: {
    GALLON_TO_FT3: 7.48052,
    FT3_TO_GALLON: 0.1337,
  },
};

// ========================
// ✈️  AVIATION
// ========================
export const AVIATION = {
  AIRLINE: {
    DELTA: {
      FLIGHT_SHARE: 0.67, // ATL departures
      DOMESTIC_SHARE: 0.89, // Domestic flights
    },
  },
  HYDROGEN: {
    PHYSICAL: {
      CONVERSION_FACTOR: 2.8, // LHV(H₂)/LHV(JetA)
      DENSITY_LB_PER_FT3: 4.43,
    },
    OPERATIONAL: {
      TURNAROUND_TIME_MIN: 30,
      FLEET_FRACTION: 0.3,
    },
  },
};

// ========================
// 🌱  EMISSIONS
// ========================
export const EMISSIONS = {
  FACTORS: {
    JET_A: 9.57, // kg CO₂/lb
    DIESEL: 22.38, // kg CO₂/lb
    GASOLINE: 19.64, // kg CO₂/lb
  },
  BASELINES: {
    JET_A_YEARLY_KG: 1_000_000,
  },
};

// ========================
// 💰  ECONOMICS
// ========================
export const ECONOMICS = {
  INCENTIVES: {
    TAX_CREDIT_PER_GAL: 0.1, // USD
  },
  REVENUE: {
    JET_A_YEARLY_USD: 1_000_000,
  },
};

// ========================
// ⏱️  OPERATIONS
// ========================
export const OPERATIONS = {
  PLANNING: {
    BUFFER_DAYS: 11,
    AVG_MONTH_DAYS: 31,
  },
  GROWTH: {
    2023: 755856,
    2024: 784123,
    // ... other years
    2050: 1308659,
  },
};

// ========================
// 🛠️  UTILITIES
// ========================
export const UNIT_CONVERSIONS = {
  LB_TO_KG: 0.453592,
  KG_TO_LB: 2.20462,
};
