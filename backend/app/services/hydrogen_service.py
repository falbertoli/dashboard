# File: backend/app/services/hydrogen_service.py
import pandas as pd
import numpy as np
from app.utils.data_loader import load_data_from_db
from app.constants import (
    DELTA_PART_FLIGHTS, DELTA_PART_DOMESTIC, CONVERSION_FACTOR_JET_TO_H2,
    H2_DENSITY_LB_PER_FT3, BUFFER_DAYS, AVG_DAYS_IN_MONTH,
    TANK_WIDTH_FT, TANK_LENGTH_FT, WATER_CAPACITY_GAL, GALLON_TO_FT3,
    TANK_ULLAGE, EVAPORATION_LOSS, JET_A_EMISSION_FACTOR,
    DIESEL_EMISSION_FACTOR, GASOLINE_EMISSION_FACTOR, growth_rate_data
)

def get_growth_rate(end_year):
    """
    Compute growth rate for Delta flights at ATL.

    Parameters:
    - end_year (int): The target year for growth projection.

    Returns:
    - float: Computed growth factor for Delta flights.
    """
    # Convert growth_rate_data from constants into a DataFrame
    growth_rate_df = pd.DataFrame(growth_rate_data)

    # Get operations for starting year (2023) and target year
    ops_start = growth_rate_df.loc[growth_rate_df["Year"] == 2023, "Projected Operations"].values[0]
    ops_projected = growth_rate_df.loc[growth_rate_df["Year"] == end_year, "Projected Operations"].values[0]

    # Calculate growth percentage and adjust for Delta domestic flights
    growth = (ops_projected - ops_start) / ops_start
    return growth * DELTA_PART_DOMESTIC * DELTA_PART_FLIGHTS


def compute_h2_demand_ac(slider_perc, end_year):
    """
    Calculate Hydrogen demand for aircraft operations.

    Parameters:
    - slider_perc (float): User-defined percentage of flights converted to hydrogen.
    - end_year (int): Target year for growth projection.

    Returns:
    - tuple: (Daily hydrogen demand in cubic feet, Projected fuel weight in lbs).
    """
    # Load aircraft data from the database
    filtered_db = load_data_from_db("ac_data", filters={"MONTH": 7, "DATA_SOURCE": "DU"})

    # Convert data types
    filtered_db["AIR_TIME"] = pd.to_numeric(filtered_db["AIR_TIME"], errors='coerce')
    filtered_db["FUEL_CONSUMPTION"] = pd.to_numeric(filtered_db["FUEL_CONSUMPTION"], errors='coerce')

    # Compute fuel weight
    fuel_weight = sum(filtered_db["FUEL_CONSUMPTION"] * filtered_db["AIR_TIME"] / 60)

    # Apply user slider and projected growth
    fuel_weight_user = slider_perc * fuel_weight
    growth = get_growth_rate(end_year)
    fuel_weight_projected = fuel_weight_user * (1 + growth)

    # Convert Jet A fuel mass to Hydrogen mass
    h2_weight = fuel_weight_projected / CONVERSION_FACTOR_JET_TO_H2
    h2_vol = h2_weight / H2_DENSITY_LB_PER_FT3

    # Apply buffer
    buffer = h2_vol / AVG_DAYS_IN_MONTH
    h2_demand_vol = h2_vol + buffer * BUFFER_DAYS

    return h2_demand_vol / AVG_DAYS_IN_MONTH, fuel_weight_projected


def compute_h2_demand_gse(gse_list, end_year):
    """
    Calculate Hydrogen demand for Ground Support Equipment.

    Parameters:
    - gse_list (list): List of ground support equipment to filter.
    - end_year (int): Target year for growth projection.

    Returns:
    - tuple: (Daily hydrogen demand in cubic feet, Total diesel used in lbs, Total gasoline used in lbs).
    """
    # Load GSE data from the database
    file = load_data_from_db("gse_data", filters={"Ground support Equipment": gse_list})

    hydrogen_tot_per_cycle, tot_diesel_used, tot_gasoline_used = 0, 0, 0
    for _, row in file.iterrows():
        fuel_vol = row["Usable Fuel Consumption (ft3/min)"] * (
            row["Operating time - Departure"] + row["Operating Time - Arrival"]
        )
        if row["Fuel used"] == "Diesel":
            hydrogen_vol = fuel_vol / 2.81
            tot_diesel_used += fuel_vol * 52.28  # Convert ft³ to lb
        elif row["Fuel used"] == "Gasoline":
            hydrogen_vol = fuel_vol / 2.76
            tot_gasoline_used += fuel_vol * 46.38  # Convert ft³ to lb
        hydrogen_tot_per_cycle += hydrogen_vol

    growth = get_growth_rate(end_year)
    hydrogen_tot_gse = 33440 * hydrogen_tot_per_cycle * growth
    buffer = hydrogen_tot_gse / AVG_DAYS_IN_MONTH
    h2_demand_vol_gse = hydrogen_tot_gse + buffer * BUFFER_DAYS

    return h2_demand_vol_gse / AVG_DAYS_IN_MONTH, tot_diesel_used, tot_gasoline_used


def compute_storage_area(h2_demand_vol):
    """
    Calculate required storage area for Hydrogen tanks.

    Parameters:
    - h2_demand_vol (float): Hydrogen demand in cubic feet.

    Returns:
    - float: Total storage area in square feet.
    """
    water_cap_ft3 = WATER_CAPACITY_GAL / GALLON_TO_FT3
    tank_h2_storage = water_cap_ft3 * (1 - TANK_ULLAGE) * EVAPORATION_LOSS
    nbr_tanks = h2_demand_vol / tank_h2_storage
    return nbr_tanks * (TANK_WIDTH_FT * TANK_LENGTH_FT)


def compute_emissions(tot_jetA, tot_diesel, tot_gasoline):
    """
    Calculate CO2 emissions for Jet A, Diesel, and Gasoline usage.

    Parameters:
    - tot_jetA (float): Total Jet A fuel in lbs.
    - tot_diesel (float): Total diesel fuel in lbs.
    - tot_gasoline (float): Total gasoline fuel in lbs.

    Returns:
    - float: Total emissions in kilograms.
    """
    return (
        tot_jetA * JET_A_EMISSION_FACTOR
        + tot_diesel * DIESEL_EMISSION_FACTOR
        + tot_gasoline * GASOLINE_EMISSION_FACTOR
    )