# File: backend/app/services/buffer_zone_service.py
import os
import json
import pandas as pd
import geopandas as gpd
from flask import current_app
from pyproj import CRS
from shapely.geometry import shape, mapping
import shapely
import pyproj

from app.services.zoning_violations_service import load_facilities_data, load_distances_requirements_data

def save_buffer_zones(geojson_data, filename="buffer_zones.geojson"):
    """
    Save the buffer zones GeoJSON to a file in the geojson data directory.
    
    Args:
        geojson_data (dict): The GeoJSON data to save
        filename (str): The name of the file to save
    """
    output_dir = os.path.join(current_app.root_path, '..', 'data', 'geojson')
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        json.dump(geojson_data, f, indent=2)
    
    current_app.logger.info(f"Buffer zones saved to: {filepath}")
    return filepath

def generate_buffer_zones():
    """
    Generate buffer zones around hazardous facilities with a separate buffer for each hazard category
    (people, flammable liquids, open fire).
    The calculation is performed in EPSG:2240 (feet) and the result is transformed to EPSG:4326 (degrees).
    
    Returns:
        dict: A GeoJSON FeatureCollection with buffer zones in EPSG:4326.
    """
    try:
        facilities_geojson = load_facilities_data()
        gdf = gpd.GeoDataFrame.from_features(facilities_geojson['features'], crs="EPSG:4326")
        gdf = gdf.to_crs("EPSG:2240")

        if gdf.empty:
            raise ValueError("Facilities data is empty or invalid.")

        requirements = load_distances_requirements_data()
        max_required = {"contains_people": 0, "contains_flammable_liquids": 0, "contains_open_fire": 0}
        for req in requirements:
            info = req['regulation_info'].lower()
            rd_ft = req['safety_distance_ft']
            if "people" in info:
                max_required["contains_people"] = max(max_required["contains_people"], rd_ft)
            if "flammable liquids" in info:
                max_required["contains_flammable_liquids"] = max(max_required["contains_flammable_liquids"], rd_ft)
            if "open fire" in info:
                max_required["contains_open_fire"] = max(max_required["contains_open_fire"], rd_ft)

        buffer_features = []
        seen = set()  # To prevent duplicates

        def create_buffer_feature(row, hazard_key, buffer_distance_ft):
            buffer_geom = row.geometry.buffer(buffer_distance_ft)
            buffer_geom = buffer_geom.simplify(0.1)
            buffer_geom_4326 = gpd.GeoSeries([buffer_geom], crs="EPSG:2240").to_crs("EPSG:4326").iloc[0]
            return {
                "type": "Feature",
                "properties": {
                    "facility_name": row.get("name") or row.get("id"),
                    "hazard_categories": [hazard_key],
                    "buffer_distance_ft": buffer_distance_ft
                },
                "geometry": buffer_geom_4326.__geo_interface__
            }

        for idx, row in gdf.iterrows():
            raw_dr = row.get("distance_requirements")
            if isinstance(raw_dr, str):
                try:
                    dr = json.loads(raw_dr)
                except Exception:
                    dr = {}
            elif isinstance(raw_dr, dict):
                dr = raw_dr
            else:
                dr = {}

            facility_name = row.get("name") or row.get("id")
            print(f"\n📍 Processing facility: {facility_name}")
            print(f"↪ Distance requirements: {dr}")

            for hazard_key, buffer_distance_ft in max_required.items():
                if dr.get(hazard_key) is True and buffer_distance_ft > 0:
                    buffer_id = f"{facility_name}_{hazard_key}"
                    if buffer_id not in seen:
                        print(f"  ➕ Adding buffer for: {hazard_key} at {buffer_distance_ft} ft")
                        feature = create_buffer_feature(row, hazard_key, buffer_distance_ft)
                        buffer_features.append(feature)
                        seen.add(buffer_id)
                    else:
                        print(f"  ⚠️ Duplicate detected for: {hazard_key} — skipping")

        if not buffer_features:
            raise ValueError("No buffer zones could be generated.")

        result = {"type": "FeatureCollection", "features": buffer_features}
        filepath = save_buffer_zones(result)
        current_app.logger.info(f"Buffer zones saved to file: {filepath}")
        return result

    except Exception as e:
        current_app.logger.error(f"Error generating buffer zones: {str(e)}")
        raise