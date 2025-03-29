# File: backend/app/routes/distances_requirements.py

import os
import csv
from flask import Blueprint, jsonify

distances_requirements_bp = Blueprint("distances_requirements", __name__)

def load_distances_requirements_csv():
    # Build file path relative to this file’s directory
    file_path = os.path.join(os.path.dirname(__file__), "../../data/distances_requirements.csv")
    distances_requirements = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert numeric fields if required.
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
    """
    Return a JSON list of distances requirements items.
    """
    regs = load_distances_requirements_csv()
    if regs:
        return jsonify(regs)
    else:
        return jsonify({"error": "Could not load distances_requirements data"}), 500