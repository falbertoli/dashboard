# File: backend/app/tests/test_storage_service.py
import pytest
from app.services.storage_service import (
    calculate_h2_storage_cost,
    validate_storage_params,
    StorageCalculationError
)

class TestStorageService:
    @pytest.fixture
    def valid_params(self):
        return {
            "total_h2_volume_gal": 1000.0,
            "number_of_tanks": 2,
            "tank_diameter_ft": 10.0,
            "tank_length_ft": 20.0,
            "cost_per_sqft_construction": 100.0,
            "cost_per_cuft_insulation": 50.0
        }

    def test_validate_storage_params_valid(self, valid_params):
        """Test parameter validation with valid inputs"""
        validate_storage_params(**valid_params)  # Should not raise exception

    @pytest.mark.parametrize("param,invalid_value,expected_error", [
        ("total_h2_volume_gal", -100, "Total H2 volume must be positive"),
        ("number_of_tanks", 0, "Number of tanks must be positive"),
        ("tank_diameter_ft", -5, "Tank diameter must be positive"),
        ("tank_length_ft", 0, "Tank length must be positive"),
        ("cost_per_sqft_construction", -10, "Construction cost must be positive"),
        ("cost_per_cuft_insulation", 0, "Insulation cost must be positive"),
    ])
    def test_validate_storage_params_invalid(self, valid_params, param, invalid_value, expected_error):
        """Test parameter validation with invalid inputs"""
        params = valid_params.copy()
        params[param] = invalid_value
        with pytest.raises(StorageCalculationError) as exc:
            validate_storage_params(**params)
        assert expected_error in str(exc.value)

    def test_calculate_h2_storage_cost_valid(self, valid_params):
        """Test storage cost calculation with valid inputs"""
        result = calculate_h2_storage_cost(**valid_params)
        
        assert isinstance(result, dict)
        assert "insulation_volume_total" in result
        assert "insulation_cost" in result
        assert "footprint_total" in result
        assert "construction_cost" in result
        assert "total_infrastructure_cost" in result
        
        assert result["insulation_volume_total"] > 0
        assert result["insulation_cost"] > 0
        assert result["footprint_total"] > 0
        assert result["construction_cost"] > 0
        assert result["total_infrastructure_cost"] > 0

    def test_calculate_h2_storage_cost_type_error(self, valid_params):
        """Test storage cost calculation with invalid type inputs"""
        params = valid_params.copy()
        params["number_of_tanks"] = 2.5  # Should be integer
        
        with pytest.raises(StorageCalculationError) as exc:
            calculate_h2_storage_cost(**params)
        assert "Number of tanks must be an integer" in str(exc.value)

    def test_calculate_h2_storage_cost_zero_division(self, valid_params):
        """Test storage cost calculation with zero division possibility"""
        params = valid_params.copy()
        params["tank_diameter_ft"] = 0  # Would cause division by zero
        
        with pytest.raises(StorageCalculationError) as exc:
            calculate_h2_storage_cost(**params)
        assert "Tank diameter must be positive" in str(exc.value)