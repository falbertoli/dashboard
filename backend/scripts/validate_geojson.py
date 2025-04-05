import json
from shapely.geometry import shape
import os

def fix_and_validate_geojson(file_path, output_path=None):
    """
    Validate and fix the GeoJSON file structure.
    - Add missing required properties with default values.
    - Close unclosed polygons.
    - Report other geometry validation errors (unfixed).
    
    Args:
        file_path (str): Path to the input GeoJSON file.
        output_path (str, optional): Path to write the fixed GeoJSON. 
            Defaults to <original_filename>_fixed.geojson in the same directory.
    
    Returns:
        tuple: (is_valid, fixed_data)
            - is_valid (bool): True if all fixable issues were resolved, False otherwise.
            - fixed_data (dict): The modified GeoJSON data.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    is_valid = True
    modified = False

    required_props = {
        "name": "Unknown",
        "amenity": "Unspecified",
        "distance_requirements": None
    }

    for feature in data.get("features", []):
        # Fix missing required properties
        properties = feature.setdefault("properties", {})
        for prop, default_value in required_props.items():
            if prop not in properties:
                print(f"⚠️  Adding missing property '{prop}' to feature: {properties.get('name', 'Unknown')}")
                properties[prop] = default_value
                modified = True

        # Validate and fix geometry
        geometry = feature.get("geometry")
        if not geometry or geometry["type"] != "Polygon":
            print(f"❌ Invalid geometry in feature: {properties.get('name', 'Unknown')}. Cannot fix automatically.")
            is_valid = False
        else:
            # Fix unclosed polygons
            coords = geometry["coordinates"][0]  # Exterior ring coordinates
            if coords[0] != coords[-1]:  
                print(f"⚠️  Closing unclosed polygon in feature: {properties.get('name', 'Unknown')}")
                geometry["coordinates"][0].append(coords[0])  # Append first point to end
                modified = True
            
            # Validate fixed geometry with Shapely (report errors, don't fix)
            try:
                shape(geometry)  
            except Exception as e:
                print(f"❌ Geometry validation error (cannot fix automatically): {e} in feature: {properties.get('name', 'Unknown')}")
                is_valid = False

    # Determine output path if not specified
    if output_path is None:
        base, ext = os.path.splitext(file_path)
        output_path = f"{base}_fixed{ext}"

    # Write fixed GeoJSON only if modifications were made
    if modified:
        print(f"Writing fixed GeoJSON to: {output_path}")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    else:
        print("No modifications needed. Input file is already valid/fixed.")

    return is_valid, data


if __name__ == "__main__":
    geojson_path = "backend/data/geojson/facilities.geojson"
    is_valid, _ = fix_and_validate_geojson(geojson_path)
    if is_valid:
        print("✅ All fixable issues resolved. Fixed GeoJSON written.")
    else:
        print("⚠️  GeoJSON file contains errors that require manual fixing.")