# File: backend/app/routes/sustainability.py

from flask import Blueprint, request, jsonify, current_app
from app.services.sustainability_service import emissions

# Define the Blueprint
sustainability_bp = Blueprint("sustainability", __name__)

@sustainability_bp.route("/emissions", methods=["POST"])
def get_emissions():
    """Calculate CO2 emissions for hydrogen-jetA and jetA-only fleets."""
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request body"}), 400
        
        # Extract parameters from request
        # Now we expect the three fuel weights (all in lbs)
        jetA_weight = float(data.get("jetA_weight", 0))
        H2_weight = float(data.get("H2_weight", 0))
        Fuel_weight = float(data.get("Fuel_weight", 0))
        
        # Optionally validate that fuel weight values are not negative
        if jetA_weight < 0 or H2_weight < 0 or Fuel_weight < 0:
            return jsonify({
                "error": "Invalid parameter",
                "message": "Fuel weights must be non-negative"
            }), 400
        
        # Calculate emissions using the new emissions function
        jetA_co2, H2_co2, just_jetA_co2 = emissions(jetA_weight, H2_weight, Fuel_weight)

        # Add logging to verify data
        print(f"Calculated emissions: jetA_co2={jetA_co2}, H2_co2={H2_co2}, just_jetA_co2={just_jetA_co2}")
        
        current_app.logger.info("Calculated emissions successfully")
        return jsonify({
            "jetA_co2": jetA_co2,
            "H2_co2": H2_co2,
            "just_jetA_co2": just_jetA_co2
        })
    
    except ValueError as e:
        current_app.logger.warning(f"Validation error in emissions endpoint: {str(e)}")
        return jsonify({
            "error": "Invalid parameter format", 
            "message": "All fuel weights must be numbers"
        }), 400
    
    except Exception as e:
        current_app.logger.error(f"Error calculating emissions: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@sustainability_bp.route("/sustainability", methods=["GET"])
def get_sustainability():
    """Legacy endpoint for backward compatibility."""
    return jsonify({"message": "Sustainability endpoint is working!"})