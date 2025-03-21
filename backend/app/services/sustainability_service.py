# File: backend/app/services/sustainability_service.py

from typing import Dict, Union
from app.services.hydrogen_service import compute_emissions
from app.utils.validation import ValidationError
from app.constants import (
    JET_A_EMISSION_FACTOR, DIESEL_EMISSION_FACTOR, GASOLINE_EMISSION_FACTOR,
    CONVERSION_FACTOR_JET_TO_H2
)

class SustainabilityCalculationError(ValidationError):
    """Custom exception for sustainability calculation errors."""
    pass

def validate_fuel_inputs(
    jet_fuel_lb: float,
    diesel_fuel_lb: float,
    gasoline_fuel_lb: float,
    hydrogen_adoption_rate: float
) -> None:
    """Validate fuel and adoption rate inputs."""
    # Validate types
    for name, value in [
        ("Jet fuel", jet_fuel_lb),
        ("Diesel fuel", diesel_fuel_lb),
        ("Gasoline fuel", gasoline_fuel_lb)
    ]:
        if not isinstance(value, (int, float)):
            raise SustainabilityCalculationError(f"{name} amount must be a number")
        if value < 0:
            raise SustainabilityCalculationError(f"{name} amount cannot be negative")

    if not isinstance(hydrogen_adoption_rate, (int, float)):
        raise SustainabilityCalculationError("Hydrogen adoption rate must be a number")
    if not 0 <= hydrogen_adoption_rate <= 1:
        raise SustainabilityCalculationError("Hydrogen adoption rate must be between 0 and 1")

def calculate_emissions_reduction(
    jet_fuel_lb: float,
    diesel_fuel_lb: float,
    gasoline_fuel_lb: float,
    hydrogen_adoption_rate: float
) -> Dict[str, float]:
    """Calculate the emissions reduction from switching to hydrogen fuel."""
    try:
        validate_fuel_inputs(
            jet_fuel_lb,
            diesel_fuel_lb,
            gasoline_fuel_lb,
            hydrogen_adoption_rate
        )
        
        # Handle zero fuel case
        if jet_fuel_lb == 0 and diesel_fuel_lb == 0 and gasoline_fuel_lb == 0:
            return {
                "baseline_emissions_kg": 0.0,
                "remaining_emissions_kg": 0.0,
                "h2_production_emissions_kg": 0.0,
                "total_new_emissions_kg": 0.0,
                "emissions_reduction_kg": 0.0,
                "percent_reduction": 0.0
            }

        
        # Calculate baseline emissions
        baseline_emissions = compute_emissions(
            jet_fuel_lb, 
            diesel_fuel_lb, 
            gasoline_fuel_lb
        )
        
        # Calculate remaining emissions
        remaining_jet_fuel = jet_fuel_lb * (1 - hydrogen_adoption_rate)
        remaining_emissions = compute_emissions(
            remaining_jet_fuel,
            diesel_fuel_lb * (1 - hydrogen_adoption_rate),
            gasoline_fuel_lb * (1 - hydrogen_adoption_rate)
        )
        
        # Calculate H2 production emissions
        h2_weight = (jet_fuel_lb * hydrogen_adoption_rate) / CONVERSION_FACTOR_JET_TO_H2
        h2_production_emissions = float(h2_weight * 0.4)
        
        # Calculate totals
        total_new_emissions = remaining_emissions + h2_production_emissions
        emissions_reduction = baseline_emissions - total_new_emissions
        percent_reduction = float(
            (emissions_reduction / baseline_emissions) * 100 if baseline_emissions > 0 else 0
        )
        
        return {
            "baseline_emissions_kg": float(baseline_emissions),
            "remaining_emissions_kg": float(remaining_emissions),
            "h2_production_emissions_kg": h2_production_emissions,
            "total_new_emissions_kg": float(total_new_emissions),
            "emissions_reduction_kg": float(emissions_reduction),
            "percent_reduction": percent_reduction
        }
    
    except SustainabilityCalculationError:
        raise
    except Exception as e:
        raise SustainabilityCalculationError(f"Error calculating emissions reduction: {str(e)}")

def validate_h2_weight(h2_weight_kg: float) -> None:
    """Validate hydrogen weight input."""
    if not isinstance(h2_weight_kg, (int, float)):
        raise SustainabilityCalculationError("Hydrogen weight must be a number")
    # Allow zero weight (removed the positive check)

def calculate_water_usage(h2_weight_kg: float) -> float:
    """Calculate water usage for hydrogen production."""
    try:
        validate_h2_weight(h2_weight_kg)
        
        # Zero hydrogen means zero water usage
        if h2_weight_kg == 0:
            return 0.0
            
        water_kg = h2_weight_kg * 9
        return float(water_kg * 0.264172)
    except SustainabilityCalculationError:
        raise
    except Exception as e:
        raise SustainabilityCalculationError(f"Error calculating water usage: {str(e)}")

def calculate_sustainability_metrics(
    jet_fuel_lb: float,
    diesel_fuel_lb: float,
    gasoline_fuel_lb: float,
    hydrogen_adoption_rate: float
) -> Dict[str, float]:
    """Calculate comprehensive sustainability metrics."""
    try:
        # Validate inputs
        validate_fuel_inputs(
            jet_fuel_lb,
            diesel_fuel_lb,
            gasoline_fuel_lb,
            hydrogen_adoption_rate
        )
        
        # Handle zero fuel case
        if jet_fuel_lb == 0 and diesel_fuel_lb == 0 and gasoline_fuel_lb == 0:
            return {
                "baseline_emissions_kg": 0.0,
                "remaining_emissions_kg": 0.0,
                "h2_production_emissions_kg": 0.0,
                "total_new_emissions_kg": 0.0,
                "emissions_reduction_kg": 0.0,
                "percent_reduction": 0.0,
                "hydrogen_weight_kg": 0.0,
                "water_usage_gallons": 0.0,
                "energy_required_kwh": 0.0,
                "renewable_energy_land_acres": 0.0
            }
        # Get emissions data
        emissions_data = calculate_emissions_reduction(
            jet_fuel_lb, 
            diesel_fuel_lb, 
            gasoline_fuel_lb, 
            hydrogen_adoption_rate
        )
        
        # Calculate hydrogen weight
        h2_weight_kg = float(
            (jet_fuel_lb * hydrogen_adoption_rate) / CONVERSION_FACTOR_JET_TO_H2
        )
        
        # Calculate metrics
        water_usage = calculate_water_usage(h2_weight_kg)
        energy_required_kwh = float(h2_weight_kg * 55)
        avg_power_kw = float(energy_required_kwh / (365 * 24))
        solar_land_acres = float((avg_power_kw / 1000) * 8)
        
        return {
            **emissions_data,
            "hydrogen_weight_kg": h2_weight_kg,
            "water_usage_gallons": water_usage,
            "energy_required_kwh": energy_required_kwh,
            "renewable_energy_land_acres": solar_land_acres
        }
    
    except SustainabilityCalculationError:
        raise
    except Exception as e:
        raise SustainabilityCalculationError(
            f"Error calculating sustainability metrics: {str(e)}"
        )