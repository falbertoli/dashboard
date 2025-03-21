# File: backend/app/routes/hydrogen.py

from flask import Blueprint, request, jsonify
from app.services.hydrogen_service import (
    compute_h2_demand_ac, compute_h2_demand_gse, 
    compute_storage_area, compute_emissions
)
from app.constants import AVG_DAYS_IN_MONTH, growth_rate_data

# Create Blueprint
hydrogen_bp = Blueprint('hydrogen', __name__)

@hydrogen_bp.route('/h2_demand/ac', methods=['POST'])
def h2_demand_ac():
    """API to compute Hydrogen demand for Aircraft Operations."""
    data = request.json
    database_name = data.get("database_name")
    slider_perc = data.get("slider_perc", 1.0)
    end_year = data.get("end_year", 2036)

    if not database_name:
        return jsonify({"error": "Database name is required"}), 400

    try:
        h2_demand_vol_day, fuel_weight_projected = compute_h2_demand_ac(database_name, slider_perc, end_year, growth_rate_data)
        return jsonify({
            "daily_h2_demand_ft3": h2_demand_vol_day,
            "projected_fuel_weight_lb": fuel_weight_projected
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hydrogen_bp.route('/h2_demand/gse', methods=['POST'])
def h2_demand_gse():
    """API to compute Hydrogen demand for Ground Support Equipment."""
    data = request.json
    database_name = data.get("database_name")
    gse_list = data.get("gse_list", [])
    end_year = data.get("end_year", 2036)

    if not database_name or not gse_list:
        return jsonify({"error": "Database name and GSE list are required"}), 400

    try:
        daily_h2_demand_gse, tot_diesel, tot_gasoline = compute_h2_demand_gse(database_name, gse_list, end_year, growth_rate_data)
        return jsonify({
            "daily_h2_demand_ft3": daily_h2_demand_gse,
            "total_diesel_used_lb": tot_diesel,
            "total_gasoline_used_lb": tot_gasoline
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hydrogen_bp.route('/storage_area', methods=['POST'])
def storage_area():
    """API to compute required storage area for Hydrogen tanks."""
    data = request.json
    h2_demand_vol = data.get("h2_demand_vol")

    if h2_demand_vol is None:
        return jsonify({"error": "H2 demand volume is required"}), 400

    try:
        area_required = compute_storage_area(h2_demand_vol)
        return jsonify({"storage_area_ft2": area_required})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@hydrogen_bp.route('/emissions', methods=['POST'])
def emissions():
    """API to compute CO2 emissions from Jet A, Diesel, and Gasoline."""
    data = request.json
    tot_jetA = data.get("tot_jetA", 0)
    tot_diesel = data.get("tot_diesel", 0)
    tot_gasoline = data.get("tot_gasoline", 0)

    try:
        total_emissions = compute_emissions(tot_jetA, tot_diesel, tot_gasoline)
        return jsonify({"total_emissions_kg": total_emissions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
