# File: backend/app/routes/storage.py

from flask import Blueprint, request, jsonify
from app.services.storage_service import calculate_h2_storage_cost
from app.utils.validation import validate_required_params

storage_bp = Blueprint('storage', __name__)

@storage_bp.route('/calculate', methods=['POST'])
def storage_cost():
    """API endpoint to calculate hydrogen storage cost."""
    data = request.get_json()

    try:
        # Validate required parameters
        validate_required_params(data, [
            "total_h2_volume_gal", "number_of_tanks", 
            "tank_diameter_ft", "tank_length_ft", 
            "cost_per_sqft_construction", "cost_per_cuft_insulation"
        ])
        
        # Extract parameters
        total_h2_volume_gal = data.get("total_h2_volume_gal")
        number_of_tanks = data.get("number_of_tanks")
        tank_diameter_ft = data.get("tank_diameter_ft")
        tank_length_ft = data.get("tank_length_ft")
        cost_per_sqft_construction = data.get("cost_per_sqft_construction")
        cost_per_cuft_insulation = data.get("cost_per_cuft_insulation")

        # Call the service function to calculate storage cost
        result = calculate_h2_storage_cost(
            total_h2_volume_gal,
            number_of_tanks,
            tank_diameter_ft,
            tank_length_ft,
            cost_per_sqft_construction,
            cost_per_cuft_insulation
        )
        
        # Return the result as a JSON response
        return jsonify(result), 200

    except ValueError as e:
        # Handle validation error
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        # Handle any other errors
        return jsonify({"error": str(e)}), 500
