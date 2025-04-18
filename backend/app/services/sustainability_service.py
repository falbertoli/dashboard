# File: backend/app/services/sustainability_service.py

import matplotlib.pyplot as plt
import numpy as np

# Constants for emissions calculations
JET_A_EMISSION_FACTOR = 9.75  # kg of CO2/gal - https://www.eia.gov/environment/emissions/co2_vol_mass.php
DIESEL_EMISSION_FACTOR = 10.19  # kg of CO2/gal
GASOLINE_EMISSION_FACTOR = 9.46  # kg of CO2/gal
LB_TO_KG = 0.453592
JETA_DENSITY_LBS_GAL = 6.7  # lbs per gallon of Jet A
GALLON_TO_FT3 = 0.134  # conversion factor from gallons to cubic feet

# Year-based H2 emission factors (kg CO2/kg H2)
# These values represent the carbon intensity of hydrogen production over time
# as the grid becomes cleaner and hydrogen production technology improves
H2_EMISSION_FACTORS = {
    2026: 17.5,
    2027: 15.0,
    2028: 12.5,
    2029: 10.0,
    2030: 7.5,
    2031: 6.0,
    2032: 5.0,
    2033: 4.0,
    2034: 3.0,
    2035: 2.0,
    2036: 1.0,  # Default year set in hydrogenStore uses 1.0
    2037: 0.8,
    2038: 0.6,
    2039: 0.4,
    2040: 0.2,
    2041: 0.1,
    2042: 0.1,
    2043: 0.1,
    2044: 0.1,
    2045: 0.1,
    2046: 0.1,
    2047: 0.1,
    2048: 0.1,
    2049: 0.1,
    2050: 0.1
}

def get_h2_emission_factor(year):
    """
    Get the hydrogen emission factor for a given year.
    Falls back to the closest available year if the exact year isn't found.
    """
    if year in H2_EMISSION_FACTORS:
        return H2_EMISSION_FACTORS[year]
    
    # If year is outside our range, use the closest boundary
    if year < min(H2_EMISSION_FACTORS.keys()):
        return H2_EMISSION_FACTORS[min(H2_EMISSION_FACTORS.keys())]
    if year > max(H2_EMISSION_FACTORS.keys()):
        return H2_EMISSION_FACTORS[max(H2_EMISSION_FACTORS.keys())]
    
    # This should never happen with our current implementation
    return 1.0  # Default fallback

def emissions(jetA_weight, H2_weight, Fuel_weight, year=2036):
    """
    Calculate CO2 emissions (in metric tons) for two fleet scenarios:
      1. A hydrogen-jetA combination fleet (combining emissions from the jetA and the hydrogen fuel component).
      2. A pure jetA-only fleet.
      
    Inputs:
      - jetA_weight: Weight of Jet A fuel (in lbs) used in hybrid operations (with hydrogen)
      - H2_weight: Total weight of hydrogen fuel (in lbs) from both aircraft and GSE
      - Fuel_weight: Weight of Jet A fuel (in lbs) that would be used in a conventional scenario
      - year: Year for which to calculate emissions (affects H2 emission factor)

    Returns:
      A tuple (jetA_co2, H2_co2, just_jetA_co2) representing:
        - jetA_co2: CO2 emissions (metric tons) for the reduced jetA portion in hybrid operations
        - H2_co2: CO2 emissions (metric tons) from hydrogen use
        - just_jetA_co2: CO2 emissions (metric tons) if all operations used conventional Jet A
    """
    # Get the year-specific H2 emission factor
    h2_emission_index = get_h2_emission_factor(year)
    
    # Convert H2_weight from lbs to kg
    h2_weight_kg = H2_weight * LB_TO_KG

    jetA_emissions = (jetA_weight / JETA_DENSITY_LBS_GAL) * JET_A_EMISSION_FACTOR # vol in gal, kg of CO2 produced
    H2_emissions = h2_weight_kg * h2_emission_index # weight in kg, kg of CO2 produced
    just_jetA_emissions = (Fuel_weight / JETA_DENSITY_LBS_GAL) * JET_A_EMISSION_FACTOR # vol in gal, kg of CO2 produced
    
    # Convert from kg to metric tons
    jetA_co2 = jetA_emissions / 1000
    H2_co2 = H2_emissions / 1000
    just_jetA_co2 = just_jetA_emissions / 1000

    print(f"Year: {year}, H2 Emission Factor: {h2_emission_index} kg CO2/kg H2")
    print(f"jetA_co2: {jetA_co2} metric tons")
    print(f"H2_co2: {H2_co2} metric tons")
    print(f"just_jetA_co2: {just_jetA_co2} metric tons")
    
    return jetA_co2, H2_co2, just_jetA_co2