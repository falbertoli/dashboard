# File: backend/app/routes/distances_requirements.py

import os
import csv
from flask import Blueprint, jsonify, request
from app.services.distances_requirements_services import calculate_min_distance, calculate_area_centroid

distances_requirements_bp = Blueprint("distances_requirements", __name__)

def load_distances_requirements_csv():
    file_path = os.path.join(os.path.dirname(__file__), "../../data/distances_requirements.csv")
    distances_requirements = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["storage_gal_min"] = float(row["storage_gal_min"]) if row["storage_gal_min"] else None
                row["storage_gal_max"] = float(row["storage_gal_max"]) if row["storage_gal_max"] else None
                row["safety_distance_ft"] = float(row["safety_distance_ft"]) if row["safety_distance_ft"] else None
                distances_requirements.append(row)
        return distances_requirements
    except Exception as e:
        print("Error loading distances_requirements:", e)
        return []

@distances_requirements_bp.route("/all", methods=["GET"])
def get_all_distances_requirements():
    regs = load_distances_requirements_csv()
    if regs:
        return jsonify(regs)
    else:
        return jsonify({"error": "Could not load distances_requirements data"}), 500

@distances_requirements_bp.route("/check_area_compliance", methods=["GET"])
def check_area_compliance():
    try:
        storage_volume_gal = float(request.args.get("storage_volume_gal"))
        area_id = int(request.args.get("area_id"))

        distances_requirements = load_distances_requirements_csv()
        if not distances_requirements:
            return jsonify({"error": "Distances requirements data is empty"}), 500

        required_distance = None
        for req in distances_requirements:
            min_vol = req["storage_gal_min"] or 0
            max_vol = req["storage_gal_max"] or float('inf')
            if min_vol <= storage_volume_gal <= max_vol:
                required_distance = req["safety_distance_ft"]
                break

        if required_distance is None:
            return jsonify({"is_compliant": False, "reason": "No matching regulation found for given volume"}), 400

        return jsonify({
            "area_id": area_id,
            "storage_volume_gal": storage_volume_gal,
            "required_safety_distance_ft": required_distance,
            "is_compliant": True,
            "reason": "Fully compliant"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400