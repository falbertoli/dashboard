# File: backend/app/constants.py
import os
import pandas as pd

# ===========================
# 📌 HYDROGEN UTILIZATION CONSTANTS
# ===========================
DELTA_PART_FLIGHTS = 0.67  # Percentage of flights departed from ATL that are operated by Delta
DELTA_PART_DOMESTIC = 0.89 # Percentage of flights operated by Delta from ATl that are domestic
HYDROGEN_FLIGHT_FRACTION = 0.3  # Fraction of flights converted to H2
EXTRA_TURNAROUND_TIME = 30  # Extra minutes per flight
CONVERSION_FACTOR_JET_TO_H2 = 2.8  # LHV(H2) / LHV(JetA)
H2_DENSITY_LB_PER_FT3 = 4.43  # lbs/ft³ (Dept of Energy for LH2)
BUFFER_DAYS = 11  # Buffer storage in days
AVG_DAYS_IN_MONTH = 31  # Used for monthly calculations

# ===========================
# 📌 TAX CREDITS & REVENUE
# ===========================
TAX_CREDIT_PER_GALLON = 0.1  # USD per gallon
JET_A_REVENUE_YEARLY = 1_000_000  # Placeholder, dynamically calculated

# ===========================
# 📌 GROWTH RATE DATA (TAF Projections)
# ===========================
growth_rate_data = pd.DataFrame({
    "Year": list(range(2023, 2051)),
    "Projected Operations": [
        755856, 784123, 815016, 834644, 853350, 872286, 890251, 
        907846, 925298, 942989, 960976, 979187, 997398, 1016764, 
        1036063, 1055234, 1074792, 1094786, 1114237, 1134615, 1155514, 
        1176625, 1197973, 1219542, 1241334, 1263264, 1285643, 1308659
    ]
})

# ===========================
# 📌 STORAGE TANK CONSTANTS
# ===========================
TANK_WIDTH_FT = 10.1667
TANK_LENGTH_FT = 56.5
WATER_CAPACITY_GAL = 18014
TANK_ULLAGE = 0.05  # % of volume taken by gas form of H2
EVAPORATION_LOSS = 0.9925  # % of LH2 lost per day

# Conversions
GALLON_TO_CUBIC_FEET = 0.1337  # Conversion factor from gallons to cubic feet
GALLON_TO_FT3 = 7.48052  # Gallons to ft³ conversion

# ===========================
# 📌 CONSTRUCTION & INSULATION COSTS
# ===========================
DEFAULT_TANK_DIAMETER_FT = 10
DEFAULT_TANK_LENGTH_FT = 40
DEFAULT_COST_PER_SQFT_CONSTRUCTION = 580  # $ per square foot
DEFAULT_COST_PER_CUFT_INSULATION = 15  # $ per cubic foot

# ===========================
# 📌 EMISSIONS FACTORS (EPA Estimates)
# ===========================
JET_A_EMISSION_FACTOR = 9.57  # kg CO2/lb Jet A
DIESEL_EMISSION_FACTOR = 22.38  # kg CO2/lb Diesel
GASOLINE_EMISSION_FACTOR = 19.64  # kg CO2/lb Gasoline
