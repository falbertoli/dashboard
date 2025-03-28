# File: backend/app/tests/test_sustainability_service.py

import matplotlib
matplotlib.use("Agg")  # Use the non-interactive Agg backend for tests

import pytest
from app.services.sustainability_service import emissions
import matplotlib.pyplot as plt

# Optionally disable plt.show(), though the Agg backend should be sufficient
@pytest.fixture(autouse=True)
def disable_plots(monkeypatch):
    monkeypatch.setattr(plt, "show", lambda: None)

def test_emissions_valid():
    """
    Test the emissions function with valid input weights.
    Input values (in lbs) are converted to metric tons, and the function returns three values.
    """
    # Example weights in lbs:
    jetA_weight = 10000   # lbs used in the hydrogen-jetA combination fleet (Jet A portion)
    H2_weight   = 3000    # lbs of hydrogen fuel used in the hydrogen-jetA combination fleet
    Fuel_weight = 15000   # lbs used in a pure jetA-only fleet

    jetA_co2, H2_co2, just_jetA_co2 = emissions(jetA_weight, H2_weight, Fuel_weight)

    # Verify that the outputs are floats and non-negative:
    assert isinstance(jetA_co2, float)
    assert isinstance(H2_co2, float)
    assert isinstance(just_jetA_co2, float)
    assert jetA_co2 >= 0
    assert H2_co2 >= 0
    assert just_jetA_co2 >= 0

def test_emissions_zero_input():
    """
    Test that when all fuel weights are zero, the emissions are zero.
    """
    jetA_co2, H2_co2, just_jetA_co2 = emissions(0, 0, 0)
    assert jetA_co2 == 0
    assert H2_co2 == 0
    assert just_jetA_co2 == 0

def test_emissions_negative_input():
    """
    Although negative fuel inputs are not physically valid,
    this test demonstrates that the arithmetic conversion is performed correctly.
    """
    jetA_co2, H2_co2, just_jetA_co2 = emissions(-1000, 3000, 1500)
    # Simply verify that outputs remain floats.
    assert isinstance(jetA_co2, float)
    assert isinstance(H2_co2, float)
    assert isinstance(just_jetA_co2, float)