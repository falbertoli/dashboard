# File: backend/app/routes/economic.py
from flask import Blueprint, request, jsonify
from app.services.economic_service import calculate_economic_impact

economic_bp = Blueprint("economic", __name__)

@economic_bp.route("/impact", methods=["GET"])
def get_economic_impact():
    """API endpoint to calculate hydrogen economic impact."""
    result = calculate_economic_impact()
    return jsonify(result)
