# File: backend/app/services/buffer_zone_service.py
import os
import json
import pandas as pd
import geopandas as gpd
from flask import current_app
from pyproj import CRS
from shapely.geometry import shape, mapping
from shapely.ops import transform
from pyproj import Transformer
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


def calculate_available_storage_areas(storage_volume_gal=None):
    """
    Calculate available areas for hydrogen storage considering safety buffer overlaps.
    
    Args:
        storage_volume_gal: Optional hydrogen storage volume in gallons to check compliance
        
    Returns:
        List of dictionaries containing available storage areas and compliance status
    """
    # Step 1: Load necessary data
    buffer_zones = load_buffer_zones()
    potential_storage_areas = load_potential_storage_areas()
    
    results = []
    
    # Step 2: Process each potential storage area
    for area in potential_storage_areas:
        area_geom = area["geometry"]
        area_props = area["properties"]
        area_id = area_props["id"]
        area_name = area_props.get("name", area_props.get("id"))
        original_area_sqft = calculate_area_sqft(area_geom)
        
        # Initialize with full area
        available_area_geom = area_geom
        available_area_sqft = original_area_sqft
        overlapping_buffers = []
        
        # Step 3: Check for overlaps with each buffer zone
        for buffer in buffer_zones:
            buffer_props = buffer["properties"]
            buffer_geom = buffer["geometry"]
            
            # Skip if this buffer belongs to the current area
            if buffer_props["facility_name"] == area_name:
                continue
            
            # Check if buffer intersects with the area
            if geometries_intersect(buffer_geom, area_geom):
                # Calculate intersection (overlap)
                overlap_geom = geometry_intersection(buffer_geom, area_geom)
                overlap_area_sqft = calculate_area_sqft(overlap_geom)
                
                # Subtract overlap from available area
                available_area_geom = geometry_difference(available_area_geom, buffer_geom)
                available_area_sqft = calculate_area_sqft(available_area_geom)
                
                # Record the overlapping buffer
                overlapping_buffers.append({
                    "buffer_id": buffer_props["facility_name"],
                    "hazard_type": buffer_props["hazard_categories"][0],
                    "overlap_area_sqft": overlap_area_sqft
                })
        
        # Step 4: Determine compliance status
        compliance_status = "compliant"
        compliance_details = "No safety buffer overlaps"
        
        if len(overlapping_buffers) > 0:
            # Area has some overlaps
            if available_area_sqft == 0:
                compliance_status = "non-compliant"
                compliance_details = "Area completely covered by safety buffers"
            else:
                # Check if remaining area meets minimum requirements
                if storage_volume_gal:
                    required_area_sqft = calculate_required_area(storage_volume_gal)
                    if available_area_sqft < required_area_sqft:
                        compliance_status = "non-compliant"
                        compliance_details = f"Available area ({available_area_sqft} sq ft) is less than required ({required_area_sqft} sq ft)"
                    else:
                        compliance_details = f"Available area ({available_area_sqft} sq ft) is sufficient for storage"
        
        # Step 5: Prepare result for this area
        area_result = {
            "area_id": area_id,
            "area_name": area_props.get("name", f"Area {area_id}"),
            "area_type": area_props.get("amenity", "Unknown"),
            "original_area_sqft": original_area_sqft,
            "available_area_sqft": available_area_sqft,
            "area_reduction_percent": ((original_area_sqft - available_area_sqft) / original_area_sqft * 100) if original_area_sqft > 0 else 0,
            "overlapping_buffers": overlapping_buffers,
            "compliance_status": compliance_status,
            "compliance_details": compliance_details,
            "original_geometry": area_geom,
            "available_geometry": available_area_geom
        }
        
        results.append(area_result)
    
    return results

def load_potential_storage_areas():
    """Load potential hydrogen storage areas (free space and deicing areas)"""
    facilities_geojson = load_facilities_data()
    
    # Filter for free space and deicing areas
    storage_areas = [
        feature for feature in facilities_geojson["features"]
        if feature["properties"].get("amenity") in ["Free Space", "Deicing"]
    ]
    
    return storage_areas

def calculate_area_sqft(geometry):
    """Calculate area in square feet from a GeoJSON geometry"""
    # Convert to shapely geometry
    shape_geom = shape(geometry)
    
    # Ensure we're working in a projected CRS for accurate area calculation
    # Transform to a local CRS (e.g., EPSG:2240 for Georgia)
    proj_geom = transform_to_local_crs(shape_geom)
    
    # Calculate area
    return proj_geom.area

def calculate_required_area(storage_volume_gal):
    """Calculate required area in square feet for given storage volume"""
    # Implementation based on storage requirements formula
    # This would use the same logic as in storage_service.py
    from app.constants import TANK_WIDTH_FT, TANK_LENGTH_FT, WATER_CAPACITY_GAL, GALLON_TO_FT3, TANK_ULLAGE, EVAPORATION_LOSS
    
    water_cap_ft3 = WATER_CAPACITY_GAL / GALLON_TO_FT3
    tank_h2_storage = water_cap_ft3 * (1 - TANK_ULLAGE) * EVAPORATION_LOSS
    nbr_tanks = storage_volume_gal * GALLON_TO_FT3 / tank_h2_storage
    return nbr_tanks * (TANK_WIDTH_FT * TANK_LENGTH_FT)

def geometries_intersect(geom1, geom2):
    """Check if two GeoJSON geometries intersect"""
    return shape(geom1).intersects(shape(geom2))

def geometry_intersection(geom1, geom2):
    """Get the intersection of two GeoJSON geometries"""
    intersection = shape(geom1).intersection(shape(geom2))
    return mapping(intersection)

def geometry_difference(geom1, geom2):
    """Get the difference between two GeoJSON geometries (geom1 - geom2)"""
    difference = shape(geom1).difference(shape(geom2))
    return mapping(difference)

def transform_to_local_crs(geom):
    """Transform geometry from WGS84 to a local projected CRS"""
    # Create transformer from WGS84 to local CRS (e.g., Georgia State Plane)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2240", always_xy=True)
    
    # Apply transformation
    return transform(lambda x, y: transformer.transform(x, y), geom)

def load_buffer_zones():
    """Load buffer zones data from the GeoJSON file."""
    file_path = os.path.join(os.path.dirname(__file__), "../../data/geojson/buffer_zones.geojson")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("Buffer zones GeoJSON file not found.")
    except json.JSONDecodeError:
        raise ValueError("Invalid GeoJSON format in buffer zones file.")