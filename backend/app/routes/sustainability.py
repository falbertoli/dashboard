# File: backend/app/routes/sustainability.py
from flask import Blueprint, request, jsonify, current_app
from app.services.sustainability_service import calculate_sustainability_metrics

# Define the Blueprint
sustainability_bp = Blueprint("sustainability", __name__)

@sustainability_bp.route("/metrics", methods=["POST"])
def get_sustainability_metrics():
    """Calculate sustainability metrics for hydrogen adoption."""
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request body"}), 400
        
        # Extract parameters from request
        jet_fuel_lb = float(data.get("jet_fuel_lb", 0))
        diesel_fuel_lb = float(data.get("diesel_fuel_lb", 0))
        gasoline_fuel_lb = float(data.get("gasoline_fuel_lb", 0))
        hydrogen_adoption_rate = float(data.get("hydrogen_adoption_rate", 0))
        
        # Validate hydrogen_adoption_rate range
        if not 0 <= hydrogen_adoption_rate <= 1:
            return jsonify({
                "error": "Invalid parameter",
                "message": "hydrogen_adoption_rate must be between 0 and 1"
            }), 400
        
        # Calculate metrics
        metrics = calculate_sustainability_metrics(
            jet_fuel_lb,
            diesel_fuel_lb,
            gasoline_fuel_lb,
            hydrogen_adoption_rate
        )
        
        # Log successful request
        current_app.logger.info(
            f"Calculated sustainability metrics with {hydrogen_adoption_rate*100}% "
            f"hydrogen adoption rate"
        )
        
        return jsonify(metrics)
    
    except ValueError as e:
        # Handle type conversion errors
        current_app.logger.warning(f"Validation error in sustainability metrics: {str(e)}")
        return jsonify({
            "error": "Invalid parameter format", 
            "message": "All fuel values and adoption rate must be numbers"
        }), 400
    
    except Exception as e:
        # Log unexpected errors
        current_app.logger.error(f"Error calculating sustainability metrics: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500

@sustainability_bp.route("/sustainability", methods=["GET"])
def get_sustainability():
    """Legacy endpoint for backward compatibility."""
    return jsonify({"message": "Sustainability endpoint is working!"})