# File: backend/app/services/sustainability_service.py

from app.services.hydrogen_service import compute_emissions
from app.utils.data_loader import load_data_from_db
from app.constants import (
    JET_A_EMISSION_FACTOR, DIESEL_EMISSION_FACTOR, GASOLINE_EMISSION_FACTOR,
    CONVERSION_FACTOR_JET_TO_H2
)

def calculate_emissions_reduction(jet_fuel_lb, diesel_fuel_lb, gasoline_fuel_lb, hydrogen_adoption_rate):
    """
    Calculate the emissions reduction from switching to hydrogen fuel.
    
    Parameters:
    - jet_fuel_lb (float): Current jet fuel consumption in lbs
    - diesel_fuel_lb (float): Current diesel fuel consumption in lbs
    - gasoline_fuel_lb (float): Current gasoline fuel consumption in lbs
    - hydrogen_adoption_rate (float): Percentage of fleet converted to hydrogen (0-1)
    
    Returns:
    - dict: Dictionary containing emissions data and reduction metrics
    """
    # Calculate baseline emissions using existing function
    baseline_emissions = compute_emissions(
        jet_fuel_lb, 
        diesel_fuel_lb, 
        gasoline_fuel_lb
    )
    
    # Calculate remaining emissions after hydrogen adoption
    remaining_jet_fuel = jet_fuel_lb * (1 - hydrogen_adoption_rate)
    remaining_emissions = compute_emissions(
        remaining_jet_fuel,
        diesel_fuel_lb * (1 - hydrogen_adoption_rate),
        gasoline_fuel_lb * (1 - hydrogen_adoption_rate)
    )
    
    # Calculate hydrogen production emissions (assuming green hydrogen)
    # For green hydrogen production: ~0.4 kg CO2 per kg H2
    h2_weight = (jet_fuel_lb * hydrogen_adoption_rate) / CONVERSION_FACTOR_JET_TO_H2
    h2_production_emissions = h2_weight * 0.4  # Green hydrogen emissions factor
    
    # Calculate total new emissions
    total_new_emissions = remaining_emissions + h2_production_emissions
    
    # Calculate emissions reduction
    emissions_reduction = baseline_emissions - total_new_emissions
    percent_reduction = (emissions_reduction / baseline_emissions) * 100 if baseline_emissions > 0 else 0
    
    return {
        "baseline_emissions_kg": baseline_emissions,
        "remaining_emissions_kg": remaining_emissions,
        "h2_production_emissions_kg": h2_production_emissions,
        "total_new_emissions_kg": total_new_emissions,
        "emissions_reduction_kg": emissions_reduction,
        "percent_reduction": percent_reduction
    }

def calculate_water_usage(h2_weight_kg):
    """
    Calculate water usage for hydrogen production.
    
    Parameters:
    - h2_weight_kg (float): Amount of hydrogen in kg
    
    Returns:
    - float: Water usage in gallons
    """
    # Water electrolysis requires ~9 kg water per 1 kg H2
    water_kg = h2_weight_kg * 9
    
    # Convert kg to gallons (1 kg water = 0.264172 gallons)
    water_gallons = water_kg * 0.264172
    
    return water_gallons

def calculate_sustainability_metrics(jet_fuel_lb, diesel_fuel_lb, gasoline_fuel_lb, hydrogen_adoption_rate):
    """
    Calculate comprehensive sustainability metrics for hydrogen adoption.
    
    Parameters:
    - jet_fuel_lb (float): Current jet fuel consumption in lbs
    - diesel_fuel_lb (float): Current diesel fuel consumption in lbs
    - gasoline_fuel_lb (float): Current gasoline fuel consumption in lbs
    - hydrogen_adoption_rate (float): Percentage of fleet converted to hydrogen (0-1)
    
    Returns:
    - dict: Dictionary containing comprehensive sustainability metrics
    """
    # Get emissions data
    emissions_data = calculate_emissions_reduction(
        jet_fuel_lb, 
        diesel_fuel_lb, 
        gasoline_fuel_lb, 
        hydrogen_adoption_rate
    )
    
    # Calculate hydrogen weight
    h2_weight_kg = (jet_fuel_lb * hydrogen_adoption_rate) / CONVERSION_FACTOR_JET_TO_H2
    
    # Calculate water usage
    water_usage = calculate_water_usage(h2_weight_kg)
    
    # Calculate renewable energy requirements
    # Assuming ~55 kWh per kg H2 for electrolysis
    energy_required_kwh = h2_weight_kg * 55
    
    # Calculate land use for solar (if using green hydrogen)
    # Assuming solar power: ~8 acres per MW, and ~55 kWh per kg H2
    # Converting to annual power requirement (kWh / 365 days / 24 hours = average kW)
    avg_power_kw = energy_required_kwh / (365 * 24)
    solar_land_acres = (avg_power_kw / 1000) * 8  # 8 acres per MW
    
    return {
        **emissions_data,
        "hydrogen_weight_kg": h2_weight_kg,
        "water_usage_gallons": water_usage,
        "energy_required_kwh": energy_required_kwh,
        "renewable_energy_land_acres": solar_land_acres
    }