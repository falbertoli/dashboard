# File: tests/test_data_loader.py

import os
import pytest
import pandas as pd
from app.utils.data_loader import (
    load_utilization_data,
    load_operations_data,
    load_income_data,
    load_regulations,
    load_distances_requirements,
    load_ac_data,
    load_gse_data,
    load_csv,
    DATA_PATH
)

# Test for utilization_data.csv
def test_load_utilization_data():
    """Test loading of utilization_data.csv"""
    df = load_utilization_data() 
    assert not df.empty, "utilization_data.csv should not be empty"
    # Expected column for utilization data:
    assert "REV_ACRFT_HRS_AIRBORNE_610" in df.columns, \
        "Missing 'REV_ACRFT_HRS_AIRBORNE_610' in utilization_data.csv"

# Test for operations_data.csv
def test_load_operations_data():
    """Test loading of operations_data.csv."""
    df = load_operations_data()
    assert not df.empty, "operations_data.csv should not be empty"
    # Expected columns in operations data:
    for col in ["UNIQUE_CARRIER_NAME", "ORIGIN", "DEPARTURES_PERFORMED"]:
        assert col in df.columns, f"Missing '{col}' in operations_data.csv"

# Test for income_data.csv
def test_load_income_data():
    """Test loading of income_data.csv."""
    df = load_income_data()
    assert not df.empty, "income_data.csv should not be empty"
    # Expected column for income data:
    assert "OP_REVENUES" in df.columns, "Missing 'OP_REVENUES' in income_data.csv"

# Test for regulations.csv
def test_load_regulations():
    """Test loading of regulations.csv."""
    df = load_regulations()
    assert not df.empty, "regulations.csv should not be empty"
    # Expected columns in regulations.csv:
    for col in ["regulation_id", "regulation_name", "regulation_info", "storage_gal_min"]:
        assert col in df.columns, f"Missing '{col}' in regulations.csv"

# Test for distances_requirements.csv
def test_load_distances_requirements():
    """Test loading of distances_requirements.csv."""
    df = load_distances_requirements()
    assert not df.empty, "distances_requirements.csv should not be empty"
    # Expected columns in distances_requirements.csv:
    for col in ["regulation_id", "regulation_name", "regulation_info", "storage_gal_min", "storage_gal_max", "safety_distance_ft"]:
        assert col in df.columns, f"Missing '{col}' in distances_requirements.csv"

# Test for ac_data.csv
def test_load_ac_data():
    """Test loading of ac_data.csv."""
    df = load_ac_data()
    assert not df.empty, "ac_data.csv should not be empty"
    # Expected columns for aircraft data:
    for col in ["AIR_TIME", "FUEL_CONSUMPTION", "MONTH", "DATA_SOURCE"]:
        assert col in df.columns, f"Missing '{col}' in ac_data.csv"

# Test for gse_data.csv
def test_load_gse_data():
    """Test loading of gse_data.csv."""
    df = load_gse_data()
    assert not df.empty, "gse_data.csv should not be empty"
    # Expected columns in gse_data.csv:
    for col in ["Ground support Equipment", "Usable Fuel Consumption (ft3/min)",
                "Operating time - Departure", "Operating Time - Arrival", "Fuel used"]:
        assert col in df.columns, f"Missing '{col}' in gse_data.csv"

# A generic test that uses load_csv to load every file and checks for an expected column.
# Adjusted our expected columns to the actual CSV header naming.
@pytest.mark.parametrize("file_name,expected_column", [
    ("utilization_data.csv", "REV_ACRFT_HRS_AIRBORNE_610"),
    ("operations_data.csv", "UNIQUE_CARRIER_NAME"),
    ("income_data.csv", "OP_REVENUES"),
    ("regulations.csv", "regulation_id"),
    ("distances_requirements.csv", "safety_distance_ft"),
    ("ac_data.csv", "AIR_TIME"),
    ("gse_data.csv", "Ground support Equipment")
])
def test_load_csv_generic(file_name, expected_column):
    file_path = os.path.join(DATA_PATH, file_name)
    df = load_csv(file_name)
    assert os.path.exists(file_path), f"File {file_path} does not exist."
    assert not df.empty, f"{file_name} is empty."
    assert expected_column in df.columns, \
        f"Missing expected column '{expected_column}' in {file_name}"

if __name__ == "__main__":
    test_load_utilization_data()
    test_load_operations_data()
    test_load_income_data()
    test_load_regulations()
    test_load_distances_requirements()
    test_load_ac_data()
    test_load_gse_data()