# File: backend/app/routes/economic.py


from flask import Blueprint, request, jsonify
from app.services.economic_service import calculate_economic_impact, EconomicCalculationError
from app.utils.response import APIResponse
from datetime import datetime  # Import datetime for current year


economic_bp = Blueprint("economic", __name__)


@economic_bp.route("/impact", methods=["POST"])
def get_economic_impact():
    """API endpoint to calculate hydrogen economic impact with user-defined parameters."""
    try:
        data = request.json
        print(f"Received economic impact request data: {data}")


        # Get the current year for validation
        # current_year = datetime.now().year
       
        # Extract and validate parameters
        try:
            # Year validation
            start_year = int(data.get("startYear", 2023))
            end_year = int(data.get("endYear", 2040))
           
            # Other parameters
            total_h2_demand = float(data.get("totalH2Demand", 0))
            fleet_percentage = float(data.get("fleetPercentage", 0))
            growth_rate = float(data.get("growthRate", 0.02))
            extra_turn_time = int(data.get("extraTurnTime", 30))
            turn_time_decrease_rates = data.get("turnTimeDecreaseRates", [0, 1, 2, 3, 4, 5])
            # Extract final_h2_year from request, defaulting to end_year if not provided.
            final_h2_year = int(data.get("finalH2Year", end_year))
               
        except (ValueError, TypeError) as e:
            return APIResponse.error(f"Invalid parameter format: {str(e)}", 400)


        print(f"Validated Parameters: Start Year: {start_year}, End Year: {end_year}, Growth Rate: {growth_rate}")
        print(f"Turn Time Parameters: Initial: {extra_turn_time} min, Decrease Rates: {turn_time_decrease_rates}")


        # Call the economic calculation service
        result = calculate_economic_impact(
            total_h2_demand=total_h2_demand,
            fleet_percentage=fleet_percentage,
            start_year=start_year,
            end_year=end_year,
            growth_rate=growth_rate,
            extra_turn_time=extra_turn_time,
            turn_time_decrease_rates=turn_time_decrease_rates,
            final_h2_year=final_h2_year
        )


        return APIResponse.success(
            data=result,  # Pass the entire result object
            message="Successfully calculated economic impact"
        )
    except EconomicCalculationError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        print(f"Error in economic impact calculation: {str(e)}")  # Add debugging
        return APIResponse.error(
            f"An error occurred while calculating economic impact: {str(e)}", 500
        )

