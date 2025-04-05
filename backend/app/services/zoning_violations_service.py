# File: backend/app/services/zoning_violations_service.py
import pandas as pd
import geopandas as gpd
from shapely.geometry import shape
from shapely.ops import transform
from pyproj import CRS, Transformer
from flask import current_app
import os
import json

def check_safety_violations(amenity_filter=None):
    """
    Detect safety zoning violations between hydrogen storage areas and other facilities.

    Args:
        amenity_filter (str, optional): Filter facilities by amenity type (e.g., "Free Space", "Deicing"). Defaults to None.

    Returns:
        list: A list of violation details.
    """
    try:
        # Load data
        facilities_geojson = load_facilities_data()
        requirements_df = load_distances_requirements_data()

        # Create GeoDataFrames
        facilities = gpd.GeoDataFrame.from_features(facilities_geojson['features'], crs="EPSG:4326")

        # Filter hydrogen storage areas
        storage_areas = facilities[facilities['amenity'].isin(["Free Space", "Deicing"])]

        # Reproject to a local metric CRS (e.g., EPSG:2240 for Georgia)
        local_crs = "EPSG:2240"
        facilities = facilities.to_crs(local_crs)
        storage_areas = storage_areas.to_crs(local_crs)

        violations = []

        # Iterate over hydrogen storage areas
        for _, storage_area in storage_areas.iterrows():
            # Iterate over other facilities
            for _, facility in facilities.iterrows():
                if storage_area.name == facility.name:  # Skip comparison with itself
                    continue

                # Match safety regulations based on the target facility's properties
                matched_regulations = match_regulations(facility, requirements_df)

                # Calculate edge-to-edge distance
                distance_m = storage_area.geometry.distance(facility.geometry)

                # Check for violations
                for regulation in matched_regulations:
                    if distance_m < regulation['safety_distance_ft'] * 0.3048:  # Convert ft to meters
                        violation = {
                            "source_name": storage_area.name,
                            "target_name": facility.name,
                            "regulation_name": regulation['regulation_name'],
                            "required_distance_ft": regulation['safety_distance_ft'],
                            "actual_distance_m": distance_m,
                            "source_geometry": storage_area.geometry.__geo_interface__,
                            "target_geometry": facility.geometry.__geo_interface__
                        }
                        violations.append(violation)

        return violations

    except Exception as e:
        current_app.logger.error(f"Error checking safety violations: {str(e)}")
        raise

def load_facilities_data():
    """Load facilities data from the GeoJSON file."""
    file_path = os.path.join(os.path.dirname(__file__), "../../data/geojson/facilities.geojson")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Facilities GeoJSON file not found.")
    except json.JSONDecodeError:
        raise ValueError("Invalid GeoJSON format in facilities file.")

def load_distances_requirements_data():
    """Load distances requirements data from the CSV file."""
    file_path = os.path.join(os.path.dirname(__file__), "../../data/distances_requirements.csv")
    try:
        df = pd.read_csv(file_path)
        return df.to_dict('records')
    except FileNotFoundError:
        raise FileNotFoundError("Distances requirements CSV file not found.")
    except pd.errors.EmptyDataError:
        raise ValueError("Distances requirements CSV file is empty.")

def match_regulations(facility, regulations):
    """Match safety regulations based on facility properties."""
    matched_regulations = []
    # In a GeoDataFrame loaded via from_features, the attributes from GeoJSON
    # become top-level columns. 
    # Retrieve the 'distance_requirements' column from the facility object.
    dr = facility.get("distance_requirements")
    if not isinstance(dr, dict):
        # Sometimes the 'distance_requirements' column may be stored as a string.
        try:
            import json
            dr = json.loads(dr)
        except Exception:
            dr = {}

    for regulation in regulations:
        regulation_info = regulation['regulation_info'].lower()
        if "people" in regulation_info and dr.get('contains_people', False):
            matched_regulations.append(regulation)
        if "flammable liquids" in regulation_info and dr.get('contains_flammable_liquids', False):
            matched_regulations.append(regulation)
        if "open fire" in regulation_info and dr.get('contains_open_fire', False):
            matched_regulations.append(regulation)

    return matched_regulations