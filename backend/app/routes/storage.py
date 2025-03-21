# File: backend/app/routes/storage.py
from flask import Blueprint, request
from app.services.storage_service import calculate_h2_storage_cost, StorageCalculationError
from app.utils.validation import validate_required_params
from app.utils.response import APIResponse

storage_bp = Blueprint('storage', __name__)

@storage_bp.route('/calculate', methods=['POST'])
def storage_cost():
    """API endpoint to calculate hydrogen storage cost."""
    try:
        data = request.get_json()
        if not data:
            return APIResponse.error("No data provided", 400)

        # Validate required parameters
        validate_required_params(data, [
            "total_h2_volume_gal", "number_of_tanks", 
            "tank_diameter_ft", "tank_length_ft", 
            "cost_per_sqft_construction", "cost_per_cuft_insulation"
        ])
        
        # Calculate storage cost
        result = calculate_h2_storage_cost(
            total_h2_volume_gal=float(data["total_h2_volume_gal"]),
            number_of_tanks=int(data["number_of_tanks"]),
            tank_diameter_ft=float(data["tank_diameter_ft"]),
            tank_length_ft=float(data["tank_length_ft"]),
            cost_per_sqft_construction=float(data["cost_per_sqft_construction"]),
            cost_per_cuft_insulation=float(data["cost_per_cuft_insulation"])
        )
        
        return APIResponse.success(
            data=result,
            message="Successfully calculated storage costs"
        )

    except (ValueError, StorageCalculationError) as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error("An error occurred while calculating storage costs", 500)