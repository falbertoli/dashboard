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
        jetA_weight = float(data.get("jetA_weight", 0))
        H2_weight = float(data.get("H2_weight", 0))
        Fuel_weight = float(data.get("Fuel_weight", 0))
        year = int(data.get("year", 2036))  # Default to 2036 if not provided
        
        # Validate input parameters
        if jetA_weight < 0 or H2_weight < 0 or Fuel_weight < 0:
            return jsonify({
                "error": "Invalid parameter",
                "message": "Fuel weights must be non-negative"
            }), 400
        
        if year < 2026 or year > 2050:
            return jsonify({
                "error": "Invalid parameter",
                "message": "Year must be between 2026 and 2050"
            }), 400
        
        # Calculate emissions using the updated emissions function that takes year
        jetA_co2, H2_co2, just_jetA_co2 = emissions(jetA_weight, H2_weight, Fuel_weight, year)

        # Add logging to verify data
        print(f"Calculated emissions for year {year}: jetA_co2={jetA_co2}, H2_co2={H2_co2}, just_jetA_co2={just_jetA_co2}")
        
        current_app.logger.info(f"Calculated emissions successfully for year {year}")
        return jsonify({
            "jetA_co2": jetA_co2,
            "H2_co2": H2_co2,
            "just_jetA_co2": just_jetA_co2
        })
    
    except ValueError as e:
        current_app.logger.warning(f"Validation error in emissions endpoint: {str(e)}")
        return jsonify({
            "error": "Invalid parameter format", 
            "message": "Fuel weights must be numbers and year must be an integer"
        }), 400
    
    except Exception as e:
        current_app.logger.error(f"Error calculating emissions: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@sustainability_bp.route("/sustainability", methods=["GET"])
def get_sustainability():
    """Legacy endpoint for backward compatibility."""
    return jsonify({"message": "Sustainability endpoint is working!"})