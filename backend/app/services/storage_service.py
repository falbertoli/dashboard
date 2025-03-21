# File: backend/app/services/storage_service.py
import numpy as np
from app.constants import GALLON_TO_CUBIC_FEET

def calculate_h2_storage_cost(
    total_h2_volume_gal,
    number_of_tanks,
    tank_diameter_ft,
    tank_length_ft,
    cost_per_sqft_construction,
    cost_per_cuft_insulation
):
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

    # Convert total hydrogen volume from gallons to cubic feet
    total_h2_volume_cuft = total_h2_volume_gal * GALLON_TO_CUBIC_FEET

    # Compute insulation volume
    h_over_d = tank_length_ft / tank_diameter_ft
    insulation_volume_total = (
        np.pi
        * (tank_diameter_ft / 2.0) ** 2
        * (2.0 * h_over_d - 1.0 / 3.0)
        * (total_h2_volume_cuft / number_of_tanks)
    )

    # Compute insulation cost
    insulation_cost = insulation_volume_total * cost_per_cuft_insulation

    # Compute footprint
    footprint_per_tank_sqft = tank_diameter_ft * tank_length_ft
    footprint_total = footprint_per_tank_sqft * number_of_tanks

    # Compute construction cost
    construction_cost = footprint_total * cost_per_sqft_construction

    # Compute total infrastructure cost
    total_infrastructure_cost = insulation_cost + construction_cost

    return {
        "insulation_volume_total": insulation_volume_total,
        "insulation_cost": insulation_cost,
        "footprint_total": footprint_total,
        "construction_cost": construction_cost,
        "total_infrastructure_cost": total_infrastructure_cost
    }
