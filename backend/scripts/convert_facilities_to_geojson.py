import csv
import json
import math

def compute_bounding_box(lat, lng, sq_ft):
    # Convert square footage to square kilometers
    sq_km = sq_ft / 10763910.417

    # Calculate the side length of the bounding box based on the area
    side_length_in_km = math.sqrt(sq_km)

    # Convert the side length from kilometers to degrees
    side_length_in_degrees = side_length_in_km / 111  # 111 km per degree

    # Compute the bounding box
    bounding_box = {
        "top_left": [lng - side_length_in_degrees / 2, lat + side_length_in_degrees / 2],
        "top_right": [lng + side_length_in_degrees / 2, lat + side_length_in_degrees / 2],
        "bottom_right": [lng + side_length_in_degrees / 2, lat - side_length_in_degrees / 2],
        "bottom_left": [lng - side_length_in_degrees / 2, lat - side_length_in_degrees / 2],
    }

    # Compute the vertices
    coordinates = [
        bounding_box["top_left"],
        bounding_box["top_right"],
        bounding_box["bottom_right"],
        bounding_box["bottom_left"],
        bounding_box["top_left"],  # Close the polygon
    ]

    return coordinates

def convert_csv_to_geojson(input_csv, output_geojson):
    features = []
    with open(input_csv, mode="r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                latitude = float(row["Latitude"])
                longitude = float(row["Longitude"])
                sq_ft = int(row["Sq. Ft."].replace(",", ""))  # Remove commas
                coordinates = compute_bounding_box(latitude, longitude, sq_ft)
                feature = {
                    "type": "Feature",
                    "properties": {
                        "name": row["Facility Name"],
                        "function": row["Building Function"],
                        "sq_ft": row["Sq. Ft."],
                        "address": row["Address"],
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [coordinates],
                    },
                }
                features.append(feature)
            except Exception as e:
                print(f"Error processing row: {row}, error: {e}")

    geojson_data = {"type": "FeatureCollection", "features": features}
    with open(output_geojson, mode="w", encoding="utf-8") as geojsonfile:
        json.dump(geojson_data, geojsonfile, indent=2)

if __name__ == "__main__":
    input_csv = r"c:\Users\alber\flask-vue-app\hydrogen\backend\data\facilities_with_coordinates.csv"
    output_geojson = r"c:\Users\alber\flask-vue-app\hydrogen\backend\data\geojson\facilities.geojson"
    convert_csv_to_geojson(input_csv, output_geojson)