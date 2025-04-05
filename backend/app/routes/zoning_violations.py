# File: backend/app/routes/zoning_violations.py
from flask import Blueprint, jsonify, request
from app.services.zoning_violations_service import check_safety_violations
from app.utils.response import APIResponse

zoning_violations_bp = Blueprint("zoning_violations", __name__)

@zoning_violations_bp.route("/violations", methods=["GET"])
def get_zoning_violations():
    """API endpoint to retrieve safety zoning violations."""
    try:
        # Get optional filters from request arguments
        amenity_filter = request.args.get("amenity", None)

        violations = check_safety_violations(amenity_filter)

        return APIResponse.success(
            data=violations, message="Successfully retrieved zoning violations"
        )
    except Exception as e:
        return APIResponse.error(f"Error retrieving zoning violations: {str(e)}", 500)