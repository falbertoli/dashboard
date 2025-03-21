import pytest
from unittest.mock import patch
import pandas as pd
from app.services.hydrogen_service import (
    get_growth_rate, compute_h2_demand_ac, compute_h2_demand_gse
)
from app.constants import growth_rate_data

def test_get_growth_rate():
    # Test the growth rate calculation for 2030
    growth = get_growth_rate(2030)
    assert growth > 0, "Growth rate should be greater than 0"
    assert isinstance(growth, float), "Growth rate should be a float"

@patch("app.utils.data_loader.load_data_from_db")
def test_compute_h2_demand_ac(mock_load_data_from_db):
    # Mock the aircraft data returned from the database
    mock_load_data_from_db.return_value = pd.DataFrame({
        "AIR_TIME": [60, 120, 180],
        "FUEL_CONSUMPTION": [500, 1000, 1500]
    })

    # Run the function with test parameters
    slider_perc = 0.5
    end_year = 2030
    h2_demand_ac, fuel_weight = compute_h2_demand_ac(slider_perc, end_year)

    # Check outputs
    assert h2_demand_ac > 0, "Daily H2 demand should be greater than 0"
    assert fuel_weight > 0, "Projected fuel weight should be greater than 0"

@patch("app.utils.data_loader.load_data_from_db")
def test_compute_h2_demand_gse(mock_load_data_from_db):
    # Mock the GSE data returned from the database
    mock_load_data_from_db.return_value = pd.DataFrame({
        "Ground support Equipment": ["F250", "FMC Commander 15"],
        "Fuel used": ["Diesel", "Gasoline"],
        "Usable Fuel Consumption (ft3/min)": [0.002, 0.003],
        "Operating time - Departure": [10, 15],
        "Operating Time - Arrival": [5, 10]
    })

    # Run the function with test parameters
    gse_list = ["F250", "FMC Commander 15"]
    end_year = 2030
    h2_demand_gse, tot_diesel, tot_gasoline = compute_h2_demand_gse(gse_list, end_year)

    assert h2_demand_gse > 0, "Daily hydrogen demand for GSE should be greater than 0."
    assert tot_diesel > 0, "Total diesel usage should be greater than 0."
    assert tot_gasoline > 0, "Total gasoline usage should be greater than 0."