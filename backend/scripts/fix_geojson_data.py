import geopandas as gpd
from shapely.geometry import shape, Polygon
import json

def fix_unclosed_polygons_in_geojson(geojson_file):
    """
    Preprocesses a GeoJSON file to fix unclosed polygons by closing their rings.
    Returns the fixed GeoJSON data as a dictionary.
    """
    # Load GeoJSON file as a Python dictionary
    with open(geojson_file, 'r') as f:
        geojson_data = json.load(f)

    def close_ring(coords):
        """Closes a ring by appending the first coordinate to the end if necessary."""
        if coords[0] != coords[-1]:
            coords.append(coords[0])
        return coords

    def fix_geometry(geometry):
        """Fixes unclosed polygons in a GeoJSON geometry."""
        if geometry['type'] == 'Polygon':
            # Fix the exterior ring
            geometry['coordinates'][0] = close_ring(geometry['coordinates'][0])
            # Fix any interior rings (holes)
            for i in range(1, len(geometry['coordinates'])):
                geometry['coordinates'][i] = close_ring(geometry['coordinates'][i])
        elif geometry['type'] == 'MultiPolygon':
            # Fix each polygon in the MultiPolygon
            for polygon in geometry['coordinates']:
                polygon[0] = close_ring(polygon[0])  # Fix exterior ring
                for i in range(1, len(polygon)):
                    polygon[i] = close_ring(polygon[i])  # Fix interior rings
        return geometry

    # Process all features in the GeoJSON
    for feature in geojson_data.get('features', []):
        geometry = feature.get('geometry')
        if geometry:
            feature['geometry'] = fix_geometry(geometry)

    return geojson_data


def fix_geojson_geometries(geojson_file, output_file):
    """
    Loads a GeoJSON file, validates geometries, closes unclosed polygons,
    and saves the corrected GeoJSON to a new file.
    """
    # Step 1: Preprocess the GeoJSON to fix unclosed polygons
    fixed_geojson_data = fix_unclosed_polygons_in_geojson(geojson_file)

    # Step 2: Load the fixed GeoJSON into GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(fixed_geojson_data)

    # Step 3: Apply buffer(0) to fix self-touching or invalid geometries
    gdf['geometry'] = gdf['geometry'].buffer(0)

    # Step 4: Save the corrected GeoDataFrame to a new GeoJSON file
    gdf.to_file(output_file, driver='GeoJSON')

if __name__ == '__main__':
    input_file = "backend/data/geojson/facilities_unverify.geojson"
    output_file = "backend/data/geojson/facilities.geojson"
    fix_geojson_geometries(input_file, output_file)
    print(f"Fixed geometries and saved to {output_file}")