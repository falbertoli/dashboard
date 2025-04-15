# File: backend/app/services/sustainability_service.py

import matplotlib.pyplot as plt
import numpy as np

# Constants for emissions calculations
JET_A_EMISSION_FACTOR = 9.75  # kg of CO2/gal - https://www.eia.gov/environment/emissions/co2_vol_mass.php
DIESEL_EMISSION_FACTOR = 10.19  # kg of CO2/gal
GASOLINE_EMISSION_FACTOR = 9.46  # kg of CO2/gal
H2_EMISSION_INDEX = 1  # kg/kg H2 for green H2
LB_TO_KG = 0.453592
JETA_DENSITY_LBS_GAL = 6.7  # lbs per gallon of Jet A
GALLON_TO_FT3 = 0.134  # conversion factor from gallons to cubic feet

def emissions(jetA_weight, H2_weight, Fuel_weight):
    """
    Calculate CO2 emissions (in metric tons) for two fleet scenarios:
      1. A hydrogen-jetA combination fleet (combining emissions from the jetA and the hydrogen fuel component).
      2. A pure jetA-only fleet.
      
    Inputs:
      - jetA_weight: Weight of Jet A fuel (in lbs) used in hybrid operations (with hydrogen)
      - H2_weight: Total weight of hydrogen fuel (in lbs) from both aircraft and GSE
      - Fuel_weight: Weight of Jet A fuel (in lbs) that would be used in a conventional scenario

    Returns:
      A tuple (jetA_co2, H2_co2, just_jetA_co2) representing:
        - jetA_co2: CO2 emissions (metric tons) for the reduced jetA portion in hybrid operations
        - H2_co2: CO2 emissions (metric tons) from hydrogen use
        - just_jetA_co2: CO2 emissions (metric tons) if all operations used conventional Jet A
    """

    jetA_emissions = (jetA_weight / JETA_DENSITY_LBS_GAL) * JET_A_EMISSION_FACTOR # vol in gal, kg of CO2 produced
    H2_emissions = H2_weight * H2_EMISSION_INDEX # weight in kg, kg of CO2 produced
    just_jetA_emissions = (Fuel_weight / JETA_DENSITY_LBS_GAL) * JET_A_EMISSION_FACTOR # vol in gal, kg of CO2 produced
    
    # Convert from kg to metric tons
    jetA_co2 = jetA_emissions / 1000
    H2_co2 = H2_emissions / 1000
    just_jetA_co2 = just_jetA_emissions / 1000

    print(f"jetA_co2: {jetA_co2} metric tons")
    print(f"H2_co2: {H2_co2} metric tons")
    print(f"just_jetA_co2: {just_jetA_co2} metric tons")
    
    return jetA_co2, H2_co2, just_jetA_co2