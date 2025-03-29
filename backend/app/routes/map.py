# File: backend/app/routes/map.py
import os
import json
from flask import Blueprint, jsonify

map_bp = Blueprint('map', __name__)

@map_bp.route("/available-areas", methods=["GET"])
def get_available_areas():
    """
    Serve the GeoJSON file containing hydrogen storage area compliance data.
    """
    try:
        # Build the file path relative to this file’s directory
        file_path = os.path.join(os.path.dirname(__file__), "../../data/geojson/atl_areas.geojson")
        with open(file_path, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
        return jsonify(geojson_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500