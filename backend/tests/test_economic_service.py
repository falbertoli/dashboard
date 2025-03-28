# File: backend/app/tests/test_economic_service.py

import pytest
from unittest.mock import patch, Mock
import pandas as pd
import numpy as np
from app.services.economic_service import (
    calculate_economic_impact,
    load_data,
    validate_data,
    EconomicCalculationError
)

@pytest.fixture
def mock_operational_data():
    return pd.DataFrame({
        "UNIQUE_CARRIER_NAME": ["Delta Air Lines Inc.", "Delta Air Lines Inc."],
        "ORIGIN": ["ATL", "JFK"],
        "DEPARTURES_PERFORMED": [100, 50]
    })

@pytest.fixture
def mock_income_data():
    return pd.DataFrame({
        "OP_REVENUES": [1000000, 2000000]
    })

@pytest.fixture
def mock_utilization_data():
    return pd.DataFrame({
        "REV_ACRFT_HRS_AIRBORNE_610": [1000, 2000]
    })

class TestEconomicService:
    def test_validate_data_valid(self, mock_operational_data, mock_income_data, mock_utilization_data):
        """Test data validation with valid data"""
        data = {
            "operations_data": mock_operational_data,
            "income_data": mock_income_data,
            "uti_data": mock_utilization_data
        }
        validate_data(data)  # Should not raise any exception

    def test_validate_data_missing_dataset(self):
        """Test data validation with missing dataset"""
        data = {}
        with pytest.raises(EconomicCalculationError) as exc:
            validate_data(data)
        assert "Missing required dataset" in str(exc.value)

    def test_calculate_economic_impact_valid(self, mock_operational_data, mock_income_data, mock_utilization_data):
        """Test economic impact calculation with valid data"""
        with patch('app.services.economic_service.load_data') as mock_load:
            mock_load.return_value = {
                "operations_data": mock_operational_data,
                "income_data": mock_income_data,
                "uti_data": mock_utilization_data
            }
            
            result = calculate_economic_impact()
            
            assert isinstance(result, dict)
            assert "hydrogen_utilization" in result
            assert "revenue_drop" in result
            assert "total_tax_credits" in result
            assert isinstance(result["hydrogen_utilization"], float)
            assert isinstance(result["revenue_drop"], float)
            assert isinstance(result["total_tax_credits"], float)

    def test_calculate_economic_impact_no_delta_data(self, mock_income_data, mock_utilization_data):
        """Test economic impact calculation with no Delta Airlines data"""
        empty_delta_data = pd.DataFrame({
            "UNIQUE_CARRIER_NAME": ["Other Airline"],
            "ORIGIN": ["JFK"],
            "DEPARTURES_PERFORMED": [100]
        })
        
        with patch('app.services.economic_service.load_data') as mock_load:
            mock_load.return_value = {
                "operations_data": empty_delta_data,
                "income_data": mock_income_data,
                "uti_data": mock_utilization_data
            }
            
            with pytest.raises(EconomicCalculationError) as exc:
                calculate_economic_impact()
            assert "No Delta Airlines operations data found" in str(exc.value)

    def test_calculate_economic_impact_zero_departures(self, mock_operational_data, mock_income_data, mock_utilization_data):
        """Test economic impact calculation with zero departures"""
        mock_operational_data["DEPARTURES_PERFORMED"] = 0
        
        with patch('app.services.economic_service.load_data') as mock_load:
            mock_load.return_value = {
                "operations_data": mock_operational_data,
                "income_data": mock_income_data,
                "uti_data": mock_utilization_data
            }
            
            with pytest.raises(EconomicCalculationError) as exc:
                calculate_economic_impact()
            assert "Total departures cannot be zero" in str(exc.value)

def test_calculate_economic_impact_integration():
    """
    Integration test for calculate_economic_impact using the actual CSV files.
    This test uses the CSV files in the data folder (renamed to utilization_data.csv,
    operations_data.csv, and income_data.csv) to run the complete calculation.
    """
    # Call the full end-to-end function
    result = calculate_economic_impact()

    # Expected keys
    expected_keys = [
        "hydrogen_utilization",
        "revenue_drop",
        "total_tax_credits",
        "baseline_revenue",
        "new_h2_revenue",
        "percent_revenue_drop"
    ]

    # Check that all expected keys are present
    for key in expected_keys:
        assert key in result, f"Missing key: {key}"
        # Check that the value is a float; optionally ensure non-negativity if it makes sense.
        assert isinstance(result[key], float), f"Value for {key} is not float"

    # Additional checks: for example, baseline revenue should be positive.
    assert result["baseline_revenue"] > 0, "Baseline revenue should be positive"