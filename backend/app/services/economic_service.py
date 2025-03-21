# File: backend/app/services/economic_service.py
import pandas as pd
from app.constants import HYDROGEN_FLIGHT_FRACTION, EXTRA_TURNAROUND_TIME, TAX_CREDIT_PER_GALLON, DATA_PATHS

def load_data():
    """Load CSV data into Pandas DataFrames"""
    return {
        "uti_data": pd.read_csv(DATA_PATHS["uti_data"]),
        "operations_data": pd.read_csv(DATA_PATHS["operations_data"]),
        "income_data": pd.read_csv(DATA_PATHS["income_data"]),
    }

def calculate_economic_impact():
    """Compute revenue changes due to hydrogen fleet transition."""
    data = load_data()

    # Extract relevant data
    total_delta_oper = data["operations_data"][
        data["operations_data"]["UNIQUE_CARRIER_NAME"] == "Delta Air Lines Inc."
    ]
    atl_delta_oper = total_delta_oper[total_delta_oper["ORIGIN"] == "ATL"]

    # Define Constants
    B = total_delta_oper["DEPARTURES_PERFORMED"].sum()
    C = atl_delta_oper["DEPARTURES_PERFORMED"].sum() / B
    F = data["income_data"]["OP_REVENUES"].sum() / 1_000_000
    baseline_jetA_util = HYDROGEN_FLIGHT_FRACTION * C * data["uti_data"]["REV_ACRFT_HRS_AIRBORNE_610"].sum()

    # Compute Revenue Changes
    utilization_h2 = baseline_jetA_util - (HYDROGEN_FLIGHT_FRACTION * B * (EXTRA_TURNAROUND_TIME / 60.0))
    baseline_revenue = HYDROGEN_FLIGHT_FRACTION * C * F
    new_h2_revenue = baseline_revenue * (utilization_h2 / baseline_jetA_util)
    total_tax_credits = TAX_CREDIT_PER_GALLON * 2752285.804321897 * 7.48052 * 12 / 1_000_000
    revenue_drop = baseline_revenue - new_h2_revenue
    pct_drop = 100 * (revenue_drop / baseline_revenue)

    return {
        "hydrogen_utilization": utilization_h2,
        "revenue_drop": revenue_drop,
        "total_tax_credits": total_tax_credits,
        "baseline_revenue": baseline_revenue,
        "new_h2_revenue": new_h2_revenue,
        "percent_revenue_drop": pct_drop
    }
