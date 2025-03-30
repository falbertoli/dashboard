# app/routes/regulations.py
import os
import csv
from flask import Blueprint, jsonify, request
from app.services.regulations_service import is_compliant_distance, check_other_regulations

regulations_bp = Blueprint("regulations", __name__)

def load_regulations_csv():
    # Build file path relative to this file’s directory
    file_path = os.path.join(os.path.dirname(__file__), "../../data/regulations.csv")
    regulations = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert numeric fields if required.
                row["storage_gal_min"] = float(row["storage_gal_min"]) if row["storage_gal_min"] else None
                regulations.append(row)
        return regulations
    except Exception as e:
        print("Error loading regulations:", e)
        return []

@regulations_bp.route("/all", methods=["GET"])
def get_all_regulations():
    """
    Return a JSON list of regulation items.
    """
    regs = load_regulations_csv()
    if regs:
        return jsonify(regs)
    else:
        return jsonify({"error": "Could not load regulations data"}), 500

@regulations_bp.route("/compliant_distance", methods=["GET"])
def check_compliant_distance():
    """
    API endpoint to check if a given distance is compliant with regulations.
    """
    try:
        storage_volume = float(request.args.get("storage_volume"))
        feature_type = request.args.get("feature_type")
        distance = float(request.args.get("distance"))

        is_compliant = is_compliant_distance(storage_volume, feature_type, distance)
        return jsonify({"is_compliant": is_compliant}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400