import csv
import requests
import json

# Replace with your OpenCage Geocoder API key
API_KEY = "c8fd43091fbd4be5885817571bb7bd16"
GEOCODING_URL = "https://api.opencagedata.com/geocode/v1/json"

def get_coordinates(address):
    """Fetch latitude and longitude for a given address using OpenCage Geocoder API."""
    params = {"q": address, "key": API_KEY}
    try:
        response = requests.get(GEOCODING_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data["results"]:
            location = data["results"][0]["geometry"]
            print(f" Geocoded {address}: {location}")
            return location["lat"], location["lng"]
        else:
            print(f" No results for address: {address}")
    except requests.exceptions.RequestException as e:
        print(f" Geocoding failed for {address}: {e}")
    return None, None

def is_valid_address(address):
    """Check if the address is valid for geocoding."""
    if not address:  # Check if address is None or empty
        return False
    # A valid address should not be purely numeric or contain only square footage
    return not address.replace(",", "").replace(".", "").isdigit()

def update_facilities_with_coordinates(input_file, output_file):
    """Read facilities CSV, fetch coordinates, and write updated CSV."""
    with open(input_file, mode="r", encoding="utf-8") as infile, open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["Latitude", "Longitude"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            address = row["Address"]
            if is_valid_address(address):
                lat, lng = get_coordinates(address)
            else:
                lat, lng = None, None  # Skip invalid addresses
            row["Latitude"] = lat if lat is not None else ""
            row["Longitude"] = lng if lng is not None else ""
            writer.writerow(row)
            print(f"Processed: {address} -> {lat}, {lng}")

def compute_bounding_box(lat, lng, offset=0.01):
    """Compute a simple bounding box around a given latitude and longitude."""
    if lat is None or lng is None:
        return None
    bounding_box = {
        "top_left": (lat + offset, lng - offset),
        "top_right": (lat + offset, lng + offset),
        "bottom_left": (lat - offset, lng - offset),
        "bottom_right": (lat - offset, lng + offset),
    }
    print(f" Bounding box for ({lat}, {lng}): {bounding_box}")
    return bounding_box

def add_building_vertices(input_file, output_file):
    """Read facilities CSV, compute building vertices, and write updated CSV."""
    with open(input_file, mode="r", encoding="utf-8") as infile, open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["TopLeft", "TopRight", "BottomLeft", "BottomRight"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            lat = row.get("Latitude")
            lng = row.get("Longitude")
            if lat and lng:
                try:
                    lat, lng = float(lat), float(lng)
                    bounding_box = compute_bounding_box(lat, lng)
                    if bounding_box:
                        row["TopLeft"] = str(bounding_box["top_left"])
                        row["TopRight"] = str(bounding_box["top_right"])
                        row["BottomLeft"] = str(bounding_box["bottom_left"])
                        row["BottomRight"] = str(bounding_box["bottom_right"])
                    else:
                        row["TopLeft"] = row["TopRight"] = row["BottomLeft"] = row["BottomRight"] = ""
                except ValueError:
                    row["TopLeft"] = row["TopRight"] = row["BottomLeft"] = row["BottomRight"] = ""
            else:
                row["TopLeft"] = row["TopRight"] = row["BottomLeft"] = row["BottomRight"] = ""
            writer.writerow(row)
            print(f"Processed bounding box for: {row.get('Address')}")

if __name__ == "__main__":
    # Uncomment the following lines to run the respective functions
    input_csv = r"c:\Users\alber\flask-vue-app\hydrogen\backend\data\facilities.csv"
    output_csv = r"c:\Users\alber\flask-vue-app\hydrogen\backend\data\facilities_with_coordinates.csv"
    update_facilities_with_coordinates(input_csv, output_csv)

    input_csv = r"c:\Users\alber\flask-vue-app\hydrogen\backend\data\facilities_with_coordinates.csv"
    output_csv = r"c:\Users\alber\flask-vue-app\hydrogen\backend\data\facilities_with_vertices.csv"
    add_building_vertices(input_csv, output_csv)