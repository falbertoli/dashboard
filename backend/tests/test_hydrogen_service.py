import pytest
from unittest.mock import patch
import pandas as pd
from app.services.hydrogen_service import (
    get_growth_rate, compute_h2_demand_ac, compute_h2_demand_gse
)
from app.utils.data_loader import load_data_from_db
from app.constants import growth_rate_data

def test_get_growth_rate():
    # Test the growth rate calculation for 2030
    growth = get_growth_rate(2030)
    assert growth > 0, "Growth rate should be greater than 0"
    assert isinstance(growth, float), "Growth rate should be a float"

@pytest.mark.usefixtures("setup_test_databases")
def test_compute_h2_demand_ac():
    """Test computing hydrogen demand for aircraft"""
    slider_perc = 0.5
    end_year = 2030
    
    # Run the function with actual data
    h2_demand_ac, fuel_weight = compute_h2_demand_ac(slider_perc, end_year)
    
    assert h2_demand_ac > 0, "Daily H2 demand should be greater than 0"
    assert fuel_weight > 0, "Fuel weight should be greater than 0"

def test_compute_h2_demand_gse():
    """Test computing hydrogen demand for GSE with actual database"""
    # First verify we can load the test data
    test_data = load_data_from_db(
        "gse_data", 
        filters={"Ground support Equipment": ["F250", "FMC Commander 15"]},
        db="gse"
    )
    assert not test_data.empty, "Should be able to load test data"
    assert len(test_data) == 2, "Should find both test equipment"
    
    # Now test the actual computation
    gse_list = ["F250", "FMC Commander 15"]
    end_year = 2030
    
    h2_demand_gse, tot_diesel, tot_gasoline = compute_h2_demand_gse(gse_list, end_year)
    
    # Verify results based on actual data
    assert h2_demand_gse > 0, "H2 demand should be greater than 0"
    assert tot_diesel > 0, "Total diesel should be greater than 0"
    assert tot_gasoline == 0, "Total gasoline should be 0 for these equipment"
    
    # Calculate expected values based on your business logic
    operating_hours_f250 = test_data[test_data["Ground support Equipment"] == "F250"][
        ["Operating time - Departure", "Operating Time - Arrival"]
    ].iloc[0].sum()
    
    operating_hours_fmc = test_data[test_data["Ground support Equipment"] == "FMC Commander 15"][
        ["Operating time - Departure", "Operating Time - Arrival"]
    ].iloc[0].sum()
    
    # Add specific assertions based on your calculation logic
    print(f"\nTest Results:")
    print(f"H2 Demand: {h2_demand_gse}")
    print(f"Total Diesel: {tot_diesel}")
    print(f"Total Gasoline: {tot_gasoline}")
    print(f"Operating Hours F250: {operating_hours_f250}")
    print(f"Operating Hours FMC: {operating_hours_fmc}")