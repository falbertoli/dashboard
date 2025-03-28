# File: backend/app/routes/economic.py

from flask import Blueprint, request, jsonify
from app.services.economic_service import calculate_economic_impact, EconomicCalculationError
from app.utils.response import APIResponse

economic_bp = Blueprint("economic", __name__)

@economic_bp.route("/impact", methods=["GET"])
def get_economic_impact():
    """API endpoint to calculate hydrogen economic impact."""
    try:
        result = calculate_economic_impact()
        return APIResponse.success(
            data=result,
            message="Successfully calculated economic impact"
        )
    except EconomicCalculationError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error(
            "An error occurred while calculating economic impact", 500
        )