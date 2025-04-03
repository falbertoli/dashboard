# File: backend/app/services/distances_requirements_services.py
from geopy.distance import geodesic

def calculate_min_distance(area_coords, hazard_coords_list):
    """
    Calculate minimum distance between an area and multiple hazard points.
    - area_coords: Tuple (lat, lng) of the area centroid.
    - hazard_coords_list: List of tuples [(lat, lng), ...] hazards.
    """
    distances = [geodesic(area_coords, hazard_coords).feet for hazard_coords in hazard_coords_list]
    return min(distances) if distances else None

def calculate_area_centroid(polygon_coords):
    """Calculate centroid of a polygon area explicitly."""
    lat_sum = sum(coord[1] for coord in polygon_coords[0])
    lng_sum = sum(coord[0] for coord in polygon_coords[0])
    num_points = len(polygon_coords[0])
    return (lat_sum / num_points, lng_sum / num_points)