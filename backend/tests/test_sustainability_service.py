# File: backend/app/tests/test_sustainability_service.py

import pytest
from app.services.sustainability_service import (
    calculate_emissions_reduction,
    calculate_water_usage,
    calculate_sustainability_metrics,
    SustainabilityCalculationError,
    validate_fuel_inputs,
    validate_h2_weight
)

class TestSustainabilityService:
    @pytest.fixture
    def valid_fuel_params(self):
        return {
            "jet_fuel_lb": 100000.0,
            "diesel_fuel_lb": 5000.0,
            "gasoline_fuel_lb": 3000.0,
            "hydrogen_adoption_rate": 0.3
        }

    def test_validate_fuel_inputs_valid(self, valid_fuel_params):
        """Test fuel input validation with valid parameters"""
        validate_fuel_inputs(**valid_fuel_params)  # Should not raise exception

    @pytest.mark.parametrize("param,invalid_value,expected_error", [
        ("jet_fuel_lb", -100, "Jet fuel amount cannot be negative"),
        ("diesel_fuel_lb", -50, "Diesel fuel amount cannot be negative"),
        ("gasoline_fuel_lb", -30, "Gasoline fuel amount cannot be negative"),
        ("hydrogen_adoption_rate", 1.5, "Hydrogen adoption rate must be between 0 and 1"),
        ("hydrogen_adoption_rate", -0.1, "Hydrogen adoption rate must be between 0 and 1"),
    ])
    def test_validate_fuel_inputs_invalid(self, valid_fuel_params, param, invalid_value, expected_error):
        """Test fuel input validation with invalid parameters"""
        params = valid_fuel_params.copy()
        params[param] = invalid_value
        with pytest.raises(SustainabilityCalculationError) as exc:
            validate_fuel_inputs(**params)
        assert expected_error in str(exc.value)

    def test_calculate_emissions_reduction_valid(self, valid_fuel_params):
        """Test emissions reduction calculation with valid inputs"""
        result = calculate_emissions_reduction(**valid_fuel_params)
        
        assert isinstance(result, dict)
        assert all(isinstance(v, float) for v in result.values())
        assert result["baseline_emissions_kg"] > 0
        assert result["percent_reduction"] >= 0
        assert result["percent_reduction"] <= 100

    def test_calculate_water_usage_valid(self):
        """Test water usage calculation with valid input"""
        result = calculate_water_usage(100.0)
        assert isinstance(result, float)
        assert result > 0

    def test_calculate_water_usage_invalid(self):
        """Test water usage calculation with invalid input"""
        with pytest.raises(SustainabilityCalculationError) as exc:
            calculate_water_usage(-100)
        assert "Hydrogen weight must be positive" in str(exc.value)

    def test_calculate_sustainability_metrics_valid(self, valid_fuel_params):
        """Test sustainability metrics calculation with valid inputs"""
        result = calculate_sustainability_metrics(**valid_fuel_params)
        
        expected_keys = {
            "baseline_emissions_kg",
            "remaining_emissions_kg",
            "h2_production_emissions_kg",
            "total_new_emissions_kg",
            "emissions_reduction_kg",
            "percent_reduction",
            "hydrogen_weight_kg",
            "water_usage_gallons",
            "energy_required_kwh",
            "renewable_energy_land_acres"
        }
        
        assert isinstance(result, dict)
        assert set(result.keys()) == expected_keys
        assert all(isinstance(v, float) for v in result.values())
        assert all(v >= 0 for v in result.values())

    def test_calculate_sustainability_metrics_zero_fuel(self):
        """Test sustainability metrics calculation with zero fuel inputs"""
        params = {
            "jet_fuel_lb": 0,
            "diesel_fuel_lb": 0,
            "gasoline_fuel_lb": 0,
            "hydrogen_adoption_rate": 0.3
        }
        
        result = calculate_sustainability_metrics(**params)
        assert result["baseline_emissions_kg"] == 0
        assert result["percent_reduction"] == 0