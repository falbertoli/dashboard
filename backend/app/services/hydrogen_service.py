# File: backend/app/services/hydrogen_service.py
import pandas as pd
import numpy as np
from app.utils.validation import ValidationError
from app.utils.data_loader import load_data_from_db
from app.constants import (
    DELTA_PART_FLIGHTS, DELTA_PART_DOMESTIC, CONVERSION_FACTOR_JET_TO_H2,
    H2_DENSITY_LB_PER_FT3, BUFFER_DAYS, AVG_DAYS_IN_MONTH,
    TANK_WIDTH_FT, TANK_LENGTH_FT, WATER_CAPACITY_GAL, GALLON_TO_FT3,
    TANK_ULLAGE, EVAPORATION_LOSS, JET_A_EMISSION_FACTOR,
    DIESEL_EMISSION_FACTOR, GASOLINE_EMISSION_FACTOR, growth_rate_data
)
from typing import Tuple, List, Union

def validate_year(end_year: Union[int, None]) -> None:
    """Validate the year parameter."""
    if end_year is None:
        raise ValidationError("Year cannot be None")
    if not isinstance(end_year, int):
        raise ValidationError("Year must be an integer")
    if end_year < 2023:
        raise ValidationError("Year must be 2023 or later")

def validate_slider_perc(slider_perc: Union[float, None]) -> None:
    """Validate the slider percentage parameter."""
    if slider_perc is None:
        raise ValidationError("slider_perc cannot be None")
    if not isinstance(slider_perc, (int, float)):
        raise ValidationError("slider_perc must be a number")
    if slider_perc < 0 or slider_perc > 1:
        raise ValidationError("slider_perc must be between 0 and 1")  # Changed error message
    
def validate_gse_list(gse_list: Union[List[str], None]) -> None:
    """Validate the GSE list parameter."""
    if gse_list is None:
        raise ValidationError("GSE list cannot be None")
    if not isinstance(gse_list, list):
        raise ValidationError("GSE list must be an array")
    if not gse_list:
        raise ValidationError("GSE list cannot be empty")
    if not all(isinstance(item, str) for item in gse_list):
        raise ValidationError("All GSE items must be strings")
    
def validate_h2_demand_vol(h2_demand_vol: Union[float, None]) -> None:
    """Validate the hydrogen demand volume parameter."""
    if h2_demand_vol is None:
        raise ValidationError("H2 demand volume cannot be None")
    if not isinstance(h2_demand_vol, (int, float)):
        raise ValidationError("H2 demand volume must be a number")
    if h2_demand_vol <= 0:
        raise ValidationError("H2 demand volume must be positive")

def validate_fuel_amount(amount: Union[float, None], fuel_type: str) -> None:
    """Validate a fuel amount parameter."""
    if amount is None:
        raise ValidationError(f"{fuel_type} amount cannot be None")
    if not isinstance(amount, (int, float)):
        raise ValidationError(f"{fuel_type} amount must be a number")
    if amount < 0:
        raise ValidationError(f"{fuel_type} amount cannot be negative")
    
def get_growth_rate(end_year: int) -> float:
    """Compute growth rate for Delta flights at ATL."""
    try:
        validate_year(end_year)
        
        growth_rate_df = pd.DataFrame(growth_rate_data)
        
        if end_year not in growth_rate_df["Year"].values:
            raise ValidationError(f"No projection data available for year {end_year}")
            
        ops_start = growth_rate_df.loc[growth_rate_df["Year"] == 2023, "Projected Operations"].values[0]
        ops_projected = growth_rate_df.loc[growth_rate_df["Year"] == end_year, "Projected Operations"].values[0]
        
        growth = (ops_projected - ops_start) / ops_start
        return float(growth * DELTA_PART_DOMESTIC * DELTA_PART_FLIGHTS)
    except IndexError:
        raise ValidationError(f"Failed to calculate growth rate for year {end_year}")


def compute_h2_demand_ac(slider_perc: float, end_year: int) -> Tuple[float, float]:
    """Calculate Hydrogen demand for aircraft operations."""
    validate_slider_perc(slider_perc)
    validate_year(end_year)
    
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

    return float(h2_demand_vol / AVG_DAYS_IN_MONTH), float(fuel_weight_projected)


def compute_h2_demand_gse(gse_list: List[str], end_year: int) -> Tuple[float, float, float]:
    """Calculate Hydrogen demand for Ground Support Equipment."""
    validate_gse_list(gse_list)
    validate_year(end_year)
    
    # Load GSE data from the database
    file = load_data_from_db("gse_data", filters={"Ground support Equipment": gse_list})
    
    if file.empty:
        raise ValidationError(f"No data found for GSE equipment: {', '.join(gse_list)}")

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

    return (
        float(h2_demand_vol_gse / AVG_DAYS_IN_MONTH), 
        float(tot_diesel_used), 
        float(tot_gasoline_used)
    )


def compute_storage_area(h2_demand_vol: float) -> float:
    """
    Calculate required storage area for Hydrogen tanks.

    Parameters:
    - h2_demand_vol (float): Hydrogen demand in cubic feet.

    Returns:
    - float: Total storage area in square feet.
    """
    validate_h2_demand_vol(h2_demand_vol)
    
    water_cap_ft3 = WATER_CAPACITY_GAL / GALLON_TO_FT3
    tank_h2_storage = water_cap_ft3 * (1 - TANK_ULLAGE) * EVAPORATION_LOSS
    nbr_tanks = h2_demand_vol / tank_h2_storage
    return float(nbr_tanks * (TANK_WIDTH_FT * TANK_LENGTH_FT))


def compute_emissions(tot_jetA: float, tot_diesel: float, tot_gasoline: float) -> float:
    """Calculate CO2 emissions for Jet A, Diesel, and Gasoline usage."""
    """
    Calculate CO2 emissions for Jet A, Diesel, and Gasoline usage.

    Parameters:
    - tot_jetA (float): Total Jet A fuel in lbs.
    - tot_diesel (float): Total diesel fuel in lbs.
    - tot_gasoline (float): Total gasoline fuel in lbs.

    Returns:
    - float: Total emissions in kilograms.
    """
    # Validate all fuel amounts
    validate_fuel_amount(tot_jetA, "Jet A")
    validate_fuel_amount(tot_diesel, "Diesel")
    validate_fuel_amount(tot_gasoline, "Gasoline")
    
    return float(
        tot_jetA * JET_A_EMISSION_FACTOR
        + tot_diesel * DIESEL_EMISSION_FACTOR
        + tot_gasoline * GASOLINE_EMISSION_FACTOR
    )