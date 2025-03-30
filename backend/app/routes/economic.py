# File: backend/app/routes/economic.py

from flask import Blueprint, request, jsonify
from app.services.economic_service import calculate_economic_impact, EconomicCalculationError
from app.utils.response import APIResponse
from datetime import datetime  # Import datetime for current year

economic_bp = Blueprint("economic", __name__)

@economic_bp.route("/impact", methods=["POST"])
def get_economic_impact():
    """API endpoint to calculate hydrogen economic impact."""
    try:
        data = request.json

        # Dynamically determine the current year as the start year
        current_year = datetime.now().year
        start_year = int(data.get("startYear", current_year))  # Default to current year
        end_year = int(data.get("endYear", 2040))
        total_h2_demand = float(data.get("totalH2Demand", 0))
        fleet_percentage = float(data.get("fleetPercentage", 0))
        growth_rate = float(data.get("growthRate", 0.02))
        extra_turn_time = int(data.get("extraTurnTime", 30))
        turn_time_decrease_rates = data.get("turnTimeDecreaseRates", [0, 1, 2, 3, 4, 5])

        print(f"Received Parameters: Start Year: {start_year}, End Year: {end_year}, Current Year: {current_year}")

        # Call the economic calculation service
        scenario_results = calculate_economic_impact(
            total_h2_demand=total_h2_demand,
            fleet_percentage=fleet_percentage,
            start_year=start_year,
            end_year=end_year,
            growth_rate=growth_rate,
            extra_turn_time=extra_turn_time,
            turn_time_decrease_rates=turn_time_decrease_rates,
        )

        # Serialize the results for the frontend
        serialized_results = {
            rate: df.to_dict(orient="records") for rate, df in scenario_results.items()
        }

        return APIResponse.success(
            data=serialized_results,
            message="Successfully calculated economic impact"
        )
    except EconomicCalculationError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        return APIResponse.error(
            "An error occurred while calculating economic impact", 500
        )