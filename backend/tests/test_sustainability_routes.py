# File: backend/tests/test_sustainability_routes.py
import json
import pytest

def test_emissions_endpoint(client):
    """Test the emissions endpoint for calculating CO2 emissions."""
    # Test data using the new expected parameters (all weights in lbs)
    test_data = {
        "jetA_weight": 10000,   # lbs used in the hydrogen-jetA combination fleet (Jet A portion)
        "H2_weight": 3000,      # lbs of hydrogen fuel used in the hydrogen-jetA combination fleet
        "Fuel_weight": 15000    # lbs used in a Jet A-only fleet
    }
    
    # Make request to the new emissions endpoint
    response = client.post(
        "/api/sustainability/emissions",
        data=json.dumps(test_data),
        content_type="application/json"
    )
    
    # Check response
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"
    data = json.loads(response.data)
    
    # Verify that the response JSON contains the three expected keys: 
    # jetA_co2, H2_co2, and just_jetA_co2.
    expected_keys = ["jetA_co2", "H2_co2", "just_jetA_co2"]
    for key in expected_keys:
        assert key in data, f"Missing expected key: {key}"

    # Optionally, you could add additional tests to check that the values are numbers
    for key in expected_keys:
        assert isinstance(data[key], (int, float)), f"{key} should be numeric"

def test_emissions_endpoint_invalid_values(client):
    """Test the emissions endpoint with invalid (non-numeric) fuel input."""
    invalid_data = {
        "jetA_weight": "not-a-number",
        "H2_weight": 3000,
        "Fuel_weight": 15000
    }
    
    response = client.post(
        "/api/sustainability/emissions",
        data=json.dumps(invalid_data),
        content_type="application/json"
    )
    
    # As the conversion to float should fail, we expect a 400 response.
    assert response.status_code == 400

def test_sustainability_get_endpoint(client):
    """Test the basic legacy sustainability GET endpoint for backward compatibility."""
    response = client.get("/api/sustainability/sustainability")
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"
    data = json.loads(response.data)
    assert "message" in data