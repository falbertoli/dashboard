# File: backend/app/tests/test_hydrogen_service.py

import pytest
from unittest.mock import patch, Mock
import pandas as pd
from app.services.hydrogen_service import (
    get_growth_rate, compute_h2_demand_ac, compute_h2_demand_gse, compute_storage_area, compute_emissions
)
from app.utils.data_loader import load_data_from_db
from app.utils.validation import ValidationError
from app.constants import growth_rate_data

class TestGrowthRate:
    def test_get_growth_rate_valid(self):
        """Test growth rate calculation with valid year"""
        growth = get_growth_rate(2030)
        assert growth > 0, "Growth rate should be greater than 0"
        assert isinstance(growth, float), "Growth rate should be a float"
    
    def test_get_growth_rate_invalid_year(self):
        """Test growth rate calculation with invalid year"""
        with pytest.raises(ValidationError) as exc:
            get_growth_rate(2020)
        assert "Year must be 2023 or later" in str(exc.value)

class TestH2DemandAC:
    @pytest.mark.usefixtures("setup_test_databases")
    def test_compute_h2_demand_ac_valid(self):
        """Test computing hydrogen demand for aircraft with valid inputs"""
        slider_perc = 0.5  # Changed from 1.5 to 0.5 (valid range 0-1)
        end_year = 2030
        
        h2_demand_ac, fuel_weight = compute_h2_demand_ac(slider_perc, end_year)
        
        assert h2_demand_ac > 0, "Daily H2 demand should be greater than 0"
        assert fuel_weight > 0, "Fuel weight should be greater than 0"
        assert isinstance(h2_demand_ac, float), "H2 demand should be a float"
        assert isinstance(fuel_weight, float), "Fuel weight should be a float"

    def test_compute_h2_demand_ac_invalid_slider(self):
        """Test with invalid slider percentage"""
        with pytest.raises(ValidationError) as exc:
            compute_h2_demand_ac(1.5, 2030)
        assert "slider_perc must be between 0 and 1" in str(exc.value)

    def test_compute_h2_demand_ac_invalid_year(self):
        """Test with invalid year"""
        with pytest.raises(ValidationError) as exc:
            compute_h2_demand_ac(0.5, 2020)
        assert "Year must be 2023 or later" in str(exc.value)

    @pytest.mark.parametrize("slider_perc,end_year", [
        (None, 2030),
        (0.5, None),
        ("0.5", 2030),
        (0.5, "2030"),
    ])
    def test_compute_h2_demand_ac_invalid_types(self, slider_perc, end_year):
        """Test with invalid parameter types"""
        with pytest.raises((ValidationError, TypeError)):
            compute_h2_demand_ac(slider_perc, end_year)

class TestH2DemandGSE:
    @pytest.fixture
    def mock_gse_data(self):
        """Fixture for mocked GSE data"""
        return pd.DataFrame({
            "Ground support Equipment": ["F250", "FMC Commander 15"],
            "Operating time - Departure": [1.0, 1.5],
            "Operating Time - Arrival": [1.0, 1.5],
            "Usable Fuel Consumption (ft3/min)": [2.0, 2.5],
            "Fuel used": ["Diesel", "Diesel"]
        })

    def test_compute_h2_demand_gse_valid(self, mock_gse_data):
        """Test computing hydrogen demand for GSE with valid inputs"""
        with patch('app.services.hydrogen_service.load_data_from_db', return_value=mock_gse_data):
            gse_list = ["F250", "FMC Commander 15"]
            end_year = 2030
            
            h2_demand_gse, tot_diesel, tot_gasoline = compute_h2_demand_gse(gse_list, end_year)
            
            assert h2_demand_gse > 0, "H2 demand should be greater than 0"
            assert tot_diesel > 0, "Total diesel should be greater than 0"
            assert tot_gasoline == 0, "Total gasoline should be 0 for these equipment"
            
            # Test specific calculations
            assert isinstance(h2_demand_gse, float), "H2 demand should be a float"
            assert isinstance(tot_diesel, float), "Diesel total should be a float"
            assert isinstance(tot_gasoline, float), "Gasoline total should be a float"

    def test_compute_h2_demand_gse_empty_list(self):
        """Test with empty GSE list"""
        with pytest.raises(ValidationError) as exc:
            compute_h2_demand_gse([], 2030)
        assert "GSE list cannot be empty" in str(exc.value)

    def test_compute_h2_demand_gse_invalid_year(self):
        """Test with invalid year"""
        with pytest.raises(ValidationError) as exc:
            compute_h2_demand_gse(["F250"], 2020)
        assert "Year must be 2023 or later" in str(exc.value)

    def test_compute_h2_demand_gse_invalid_gse_type(self):
        """Test with invalid GSE list type"""
        with pytest.raises(ValidationError) as exc:
            compute_h2_demand_gse("F250", 2030)  # String instead of list
        assert "GSE list must be an array" in str(exc.value)

    @pytest.mark.integration
    def test_compute_h2_demand_gse_integration(self):
        """Integration test using actual database"""
        test_data = load_data_from_db(
            "gse_data", 
            filters={"Ground support Equipment": ["F250", "FMC Commander 15"]},
            db="gse"
        )
        assert not test_data.empty, "Should be able to load test data"
        assert len(test_data) == 2, "Should find both test equipment"
        
        gse_list = ["F250", "FMC Commander 15"]
        end_year = 2030
        
        h2_demand_gse, tot_diesel, tot_gasoline = compute_h2_demand_gse(gse_list, end_year)
        
        # Print detailed test results for debugging
        print(f"\nIntegration Test Results:")
        print(f"H2 Demand: {h2_demand_gse:.2f} ft³/day")
        print(f"Total Diesel: {tot_diesel:.2f} lb")
        print(f"Total Gasoline: {tot_gasoline:.2f} lb")
        
        for gse in gse_list:
            equipment_data = test_data[test_data["Ground support Equipment"] == gse]
            operating_hours = equipment_data[
                ["Operating time - Departure", "Operating Time - Arrival"]
            ].iloc[0].sum()
            print(f"{gse} Operating Hours: {operating_hours:.2f}")


class TestStorageArea:
    def test_storage_area_valid(self):
        """Test storage area calculation with valid input"""
        result = compute_storage_area(1000.0)
        assert isinstance(result, float)
        assert result > 0

    def test_storage_area_invalid(self):
        """Test storage area calculation with invalid input"""
        with pytest.raises(ValidationError):
            compute_storage_area(-100)

class TestEmissions:
    def test_emissions_valid(self):
        """Test emissions calculation with valid inputs"""
        result = compute_emissions(1000.0, 500.0, 200.0)
        assert isinstance(result, float)
        assert result > 0

    def test_emissions_zero_inputs(self):
        """Test emissions calculation with all zero inputs"""
        result = compute_emissions(0, 0, 0)
        assert result == 0
        assert isinstance(result, float)

    def test_emissions_negative_input(self):
        """Test emissions calculation with negative input"""
        with pytest.raises(ValidationError):
            compute_emissions(-100, 0, 0)