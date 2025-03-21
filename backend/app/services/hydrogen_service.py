# File: backend/app/services/hydrogen_service.py
import pandas as pd
import numpy as np
import sqlite3
from app.constants import (
    DELTA_PART_FLIGHTS, DELTA_PART_DOMESTIC, CONVERSION_FACTOR_JET_TO_H2, 
    H2_DENSITY_LB_PER_FT3, BUFFER_DAYS, AVG_DAYS_IN_MONTH,
    TANK_WIDTH_FT, TANK_LENGTH_FT, WATER_CAPACITY_GAL, GALLON_TO_FT3,
    TANK_ULLAGE, EVAPORATION_LOSS, 
    JET_A_EMISSION_FACTOR, DIESEL_EMISSION_FACTOR, GASOLINE_EMISSION_FACTOR
)

def get_growth_rate(end_year, gr_data):
    """
    Compute growth rate for Delta flights at ATL.
    
    Parameters:
    - end_year (int): The target year for growth projection.
    - gr_data (dict): Growth rate data containing projected operations per year.
    
    Returns:
    - float: Computed growth factor for Delta flights.
    """
    growth_rate_df = pd.DataFrame(gr_data)
    ops_start = growth_rate_df.loc[growth_rate_df["Year"] == 2023, "Projected Operations"].values[0]
    ops_projected = growth_rate_df.loc[growth_rate_df["Year"] == end_year, "Projected Operations"].values[0]
    growth = (ops_projected - ops_start) / ops_start
    return growth * DELTA_PART_DOMESTIC * DELTA_PART_FLIGHTS

def compute_h2_demand_ac(database_name, slider_perc, end_year, gr_data):
    """
    Calculate Hydrogen demand for aircraft operations.
    
    Parameters:
    - database_name (str): The database file name.
    - slider_perc (float): User-defined percentage of flights converted to hydrogen.
    - end_year (int): Target year for growth projection.
    - gr_data (dict): Growth rate data containing projected operations per year.
    
    Returns:
    - tuple: (Daily hydrogen demand in cubic feet, Projected fuel weight in lbs).
    """
    conn = sqlite3.connect(database_name)
    query = """
    SELECT "AIR_TIME", "FUEL_CONSUMPTION"
    FROM my_table
    WHERE "MONTH" = 7 AND "DATA_SOURCE" = "DU";
    """
    filtered_db = pd.read_sql(query, conn)
    conn.close()

    # Convert data types
    filtered_db["AIR_TIME"] = pd.to_numeric(filtered_db["AIR_TIME"], errors='coerce')
    filtered_db["FUEL_CONSUMPTION"] = pd.to_numeric(filtered_db["FUEL_CONSUMPTION"], errors='coerce')

    # Compute fuel weight
    fuel_weight = sum(filtered_db["FUEL_CONSUMPTION"] * filtered_db["AIR_TIME"] / 60)

    # Apply user slider and projected growth
    fuel_weight_user = slider_perc * fuel_weight
    growth = get_growth_rate(end_year, gr_data)
    fuel_weight_projected = fuel_weight_user * (1 + growth)

    # Convert Jet A fuel mass to Hydrogen mass
    h2_weight = fuel_weight_projected / CONVERSION_FACTOR_JET_TO_H2
    h2_vol = h2_weight / H2_DENSITY_LB_PER_FT3

    # Apply buffer
    buffer = h2_vol / AVG_DAYS_IN_MONTH
    h2_demand_vol = h2_vol + buffer * BUFFER_DAYS

    return h2_demand_vol / AVG_DAYS_IN_MONTH, fuel_weight_projected

def compute_h2_demand_gse(database_name, gse_list, end_year, gr_data):
    """Calculate Hydrogen demand for Ground Support Equipment."""
    conn = sqlite3.connect(database_name)
    placeholders = ', '.join(['?'] * len(gse_list))
    query = f"""
    SELECT "Ground support Equipment", "Fuel used", "Usable Fuel Consumption (ft3/min)", 
           "Operating time - Departure", "Operating Time - Arrival"
    FROM my_table
    WHERE "Ground support Equipment" IN ({placeholders});
    """
    file = pd.read_sql(query, conn, params=gse_list)
    conn.close()

    hydrogen_tot_per_cycle, tot_diesel_used, tot_gasoline_used = 0, 0, 0
    for _, row in file.iterrows():
        fuel_vol = row["Usable Fuel Consumption (ft3/min)"] * (row["Operating time - Departure"] + row["Operating Time - Arrival"])
        if row["Fuel used"] == "Diesel":
            hydrogen_vol = fuel_vol / 2.81
            tot_diesel_used += fuel_vol * 52.28  # Convert ft³ to lb
        elif row["Fuel used"] == "Gasoline":
            hydrogen_vol = fuel_vol / 2.76
            tot_gasoline_used += fuel_vol * 46.38  # Convert ft³ to lb
        hydrogen_tot_per_cycle += hydrogen_vol

    growth = get_growth_rate(end_year, gr_data)
    hydrogen_tot_gse = 33440 * hydrogen_tot_per_cycle * growth
    buffer = hydrogen_tot_gse / AVG_DAYS_IN_MONTH
    h2_demand_vol_gse = hydrogen_tot_gse + buffer * BUFFER_DAYS

    return h2_demand_vol_gse / AVG_DAYS_IN_MONTH, tot_diesel_used, tot_gasoline_used

def compute_storage_area(h2_demand_vol):
    """Calculate required storage area for Hydrogen tanks."""
    water_cap_ft3 = WATER_CAPACITY_GAL / GALLON_TO_FT3
    tank_h2_storage = water_cap_ft3 * (1 - TANK_ULLAGE) * EVAPORATION_LOSS
    nbr_tanks = h2_demand_vol / tank_h2_storage
    return nbr_tanks * (TANK_WIDTH_FT * TANK_LENGTH_FT)

def compute_emissions(tot_jetA, tot_diesel, tot_gasoline):
    """Calculate CO2 emissions for Jet A, Diesel, and Gasoline usage."""
    return (
        tot_jetA * JET_A_EMISSION_FACTOR + 
        tot_diesel * DIESEL_EMISSION_FACTOR + 
        tot_gasoline * GASOLINE_EMISSION_FACTOR
    )
