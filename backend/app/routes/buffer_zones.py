# File: backend/app/routes/buffer_zones.py
from flask import Blueprint, jsonify, request, current_app
from app.services.buffer_zone_service import generate_buffer_zones, calculate_available_storage_areas
from app.utils.response import APIResponse

buffer_zones_bp = Blueprint("buffer_zones", __name__)

@buffer_zones_bp.route("/buffers", methods=["GET"])
def get_buffer_zones():
    """
    API endpoint to retrieve buffer zones around hazardous facilities.
    Returns a GeoJSON FeatureCollection of buffer zones.
    """
    try:
        buffer_geojson = generate_buffer_zones()
        if not buffer_geojson or "features" not in buffer_geojson:
            raise ValueError("Invalid buffer zones data generated.")
        return jsonify(buffer_geojson)  # Return the GeoJSON directly
    except Exception as e:
        current_app.logger.error(f"Error in get_buffer_zones: {str(e)}")
        return APIResponse.error(f"Error retrieving buffer zones: {str(e)}", 500)
    
@buffer_zones_bp.route("/storage-area-analysis", methods=["GET"])
def analyze_storage_areas():
    """
    API endpoint to analyze potential storage areas against safety buffers.
    
    Query parameters:
        storage_volume_gal: Optional hydrogen storage volume in gallons
    """
    try:
        # Get storage volume from query params if provided
        storage_volume_gal = request.args.get("storage_volume_gal", type=float)
        
        # Calculate available areas
        results = calculate_available_storage_areas(storage_volume_gal)
        
        return jsonify({
            "total_areas": len(results),
            "compliant_areas": sum(1 for r in results if r["compliance_status"] == "compliant"),
            "results": results
        })
    
    except Exception as e:
        current_app.logger.error(f"Error in storage area analysis: {str(e)}")
        return APIResponse.error(f"Error analyzing storage areas: {str(e)}", 500)