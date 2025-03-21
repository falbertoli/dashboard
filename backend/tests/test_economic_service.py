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