# backend/app/services/regulations_service.py

from geopy.distance import geodesic  # You might need to install this: pip install geopy
from app.constants import *  # Import constants, including distances/requirements
from app.utils.data_loader import load_distances_requirements, load_regulations
import pandas as pd

def calculate_distance(coord1, coord2):
    """Calculates the distance between two coordinates using the geodesic distance."""
    return geodesic(coord1, coord2).feet  # Return distance in feet

def is_compliant_distance(storage_volume, feature_type, distance):
    """Checks if the distance meets the minimum safety distance requirement."""
    # TO-DO: Implement distances loading on utils/data_loader
    df = load_distances_requirements()
    if df.empty:
        raise ValueError("Distances Requirements data is empty")

    distances_requirements = df.to_dict('records')

    # Iterate through each row in the distances_requirements DataFrame
    for req in distances_requirements:
        min_volume = req['storage_gal_min'] or 0  # Minimum storage volume, default to 0 if None
        max_volume = req['storage_gal_max'] or float('inf')  # Maximum storage volume, default to infinity if None
        safety_distance = req['safety_distance_ft']

        # Check if the storage volume falls within the range specified in the current row
        if min_volume <= storage_volume <= max_volume:
            # Check if the actual distance is greater than or equal to the required safety distance
            if distance >= safety_distance:
                return True  # Compliant: distance is sufficient
            else:
                return False  # Non-compliant: distance is insufficient
    return False

def check_other_regulations(storage_volume, regulation_data):
    """Check compliance against other regulations in the `regulations.csv` data."""

    df = load_regulations()
    if df.empty:
        raise ValueError("Regulations data is empty")

    df_filtered = df[df['storage_gal_min'] <= storage_volume]
    is_compliant = not df_filtered.empty

    return is_compliant  # Placeholder: Replace with actual logic