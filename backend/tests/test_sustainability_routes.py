# File: backend/tests/test_sustainability_routes.py
import json
import pytest

def test_sustainability_metrics_endpoint(client):
    """Test the sustainability metrics endpoint."""
    # Test data
    test_data = {
        "jet_fuel_lb": 100000,
        "diesel_fuel_lb": 5000,
        "gasoline_fuel_lb": 3000,
        "hydrogen_adoption_rate": 0.3
    }
    
    # Make request to the endpoint
    response = client.post(
        "/api/sustainability/metrics",
        data=json.dumps(test_data),
        content_type="application/json"
    )
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Verify response contains expected keys
    expected_keys = [
        "baseline_emissions_kg", "remaining_emissions_kg", 
        "h2_production_emissions_kg", "total_new_emissions_kg",
        "emissions_reduction_kg", "percent_reduction",
        "hydrogen_weight_kg", "water_usage_gallons",
        "energy_required_kwh", "renewable_energy_land_acres"
    ]
    
    for key in expected_keys:
        assert key in data
    
    # Test with invalid adoption rate
    invalid_data = {
        "jet_fuel_lb": 100000,
        "diesel_fuel_lb": 5000,
        "gasoline_fuel_lb": 3000,
        "hydrogen_adoption_rate": 1.5  # Invalid - should be 0-1
    }
    
    response = client.post(
        "/api/sustainability/metrics",
        data=json.dumps(invalid_data),
        content_type="application/json"
    )
    
    assert response.status_code == 400
    
    # Test with non-numeric values
    invalid_type_data = {
        "jet_fuel_lb": "not-a-number",
        "diesel_fuel_lb": 5000,
        "gasoline_fuel_lb": 3000,
        "hydrogen_adoption_rate": 0.3
    }
    
    response = client.post(
        "/api/sustainability/metrics",
        data=json.dumps(invalid_type_data),
        content_type="application/json"
    )
    
    assert response.status_code == 400

def test_sustainability_get_endpoint(client):
    """Test the basic sustainability GET endpoint."""
    response = client.get("/api/sustainability/sustainability")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data