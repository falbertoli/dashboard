# File: backend/scripts/validate_csv.py

import pandas as pd

def validate_csv(file_path):
    """
    Validate the structure and content of the CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
    
    Returns:
        bool: True if the CSV is valid, otherwise False.
    """
    try:
        df = pd.read_csv(file_path)

        # Check for required columns
        required_columns = ["regulation_name", "safety_distance_ft", "storage_gal_min", "storage_gal_max"]
        for col in required_columns:
            if col not in df.columns:
                print(f"❌ Missing column: {col}")
                return False

        # Check for valid data
        if df["safety_distance_ft"].isnull().any():
            print("❌ Missing values in 'safety_distance_ft'")
            return False

        print("✅ CSV file is valid!")
        return True

    except Exception as e:
        print(f"❌ Error validating CSV: {e}")
        return False


if __name__ == "__main__":
    csv_path = "backend/data/distances_requirements.csv"
    if validate_csv(csv_path):
        print("✅ CSV file is valid!")
    else:
        print("❌ CSV file contains errors. Please fix them.")