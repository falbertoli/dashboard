# File: backend/app/services/storage_service.py
from typing import Dict, Union
import numpy as np
from app.constants import GALLON_TO_CUBIC_FEET
from app.utils.validation import ValidationError

class StorageCalculationError(ValidationError):
    """Custom exception for storage calculation errors."""
    pass

def validate_storage_params(
    total_h2_volume_gal: float,
    number_of_tanks: int,
    tank_diameter_ft: float,
    tank_length_ft: float,
    cost_per_sqft_construction: float,
    cost_per_cuft_insulation: float
) -> None:
    """Validate storage calculation parameters."""
    # Validate types
    if not isinstance(total_h2_volume_gal, (int, float)):
        raise StorageCalculationError("Total H2 volume must be a number")
    if not isinstance(number_of_tanks, int):
        raise StorageCalculationError("Number of tanks must be an integer")
    if not isinstance(tank_diameter_ft, (int, float)):
        raise StorageCalculationError("Tank diameter must be a number")
    if not isinstance(tank_length_ft, (int, float)):
        raise StorageCalculationError("Tank length must be a number")
    if not isinstance(cost_per_sqft_construction, (int, float)):
        raise StorageCalculationError("Construction cost per square foot must be a number")
    if not isinstance(cost_per_cuft_insulation, (int, float)):
        raise StorageCalculationError("Insulation cost per cubic foot must be a number")

    # Validate ranges
    if total_h2_volume_gal <= 0:
        raise StorageCalculationError("Total H2 volume must be positive")
    if number_of_tanks <= 0:
        raise StorageCalculationError("Number of tanks must be positive")
    if tank_diameter_ft <= 0:
        raise StorageCalculationError("Tank diameter must be positive")
    if tank_length_ft <= 0:
        raise StorageCalculationError("Tank length must be positive")
    if cost_per_sqft_construction <= 0:
        raise StorageCalculationError("Construction cost must be positive")
    if cost_per_cuft_insulation <= 0:
        raise StorageCalculationError("Insulation cost must be positive")

def calculate_h2_storage_cost(
    total_h2_volume_gal: float,
    number_of_tanks: int,
    tank_diameter_ft: float,
    tank_length_ft: float,
    cost_per_sqft_construction: float,
    cost_per_cuft_insulation: float
) -> Dict[str, float]:
    """Compute cost estimates for hydrogen storage infrastructure."""
    """
    Computes cost estimates for hydrogen storage infrastructure.
    
    Parameters:
    - total_h2_volume_gal (float): Total hydrogen volume required in gallons.
    - number_of_tanks (int): Number of storage tanks required.
    - tank_diameter_ft (float): Diameter of each storage tank in feet.
    - tank_length_ft (float): Length of each storage tank in feet.
    - cost_per_sqft_construction (float): Cost per square foot for tank construction.
    - cost_per_cuft_insulation (float): Cost per cubic foot for tank insulation.
    
    Returns:
    - dict: Dictionary containing insulation volume, insulation cost, footprint, construction cost, and total infrastructure cost.
    
    Notes:
    - `h_over_d` represents the ratio of tank length to diameter, which helps determine insulation volume based on tank geometry.
    """
    try:
        # Validate input parameters
        validate_storage_params(
            total_h2_volume_gal,
            number_of_tanks,
            tank_diameter_ft,
            tank_length_ft,
            cost_per_sqft_construction,
            cost_per_cuft_insulation
        )

        # Convert total hydrogen volume from gallons to cubic feet
        total_h2_volume_cuft = total_h2_volume_gal * GALLON_TO_CUBIC_FEET

        # Compute insulation volume
        h_over_d = tank_length_ft / tank_diameter_ft
        insulation_volume_total = float(
            np.pi
            * (tank_diameter_ft / 2.0) ** 2
            * (2.0 * h_over_d - 1.0 / 3.0)
            * (total_h2_volume_cuft / number_of_tanks)
        )

        # Compute costs
        insulation_cost = float(insulation_volume_total * cost_per_cuft_insulation)
        footprint_per_tank_sqft = float(tank_diameter_ft * tank_length_ft)
        footprint_total = float(footprint_per_tank_sqft * number_of_tanks)
        construction_cost = float(footprint_total * cost_per_sqft_construction)
        total_infrastructure_cost = float(insulation_cost + construction_cost)

        return {
            "insulation_volume_total": insulation_volume_total,
            "insulation_cost": insulation_cost,
            "footprint_total": footprint_total,
            "construction_cost": construction_cost,
            "total_infrastructure_cost": total_infrastructure_cost
        }

    except StorageCalculationError:
        raise
    except Exception as e:
        raise StorageCalculationError(f"Error calculating storage cost: {str(e)}")