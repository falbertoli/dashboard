# File: backend/app/services/economic_service.py

from typing import Dict, Any
import pandas as pd
from app.utils.validation import ValidationError
from app.utils.data_loader import load_operational_hours, load_carrier_operations, load_income_data
from app.constants import HYDROGEN_FLIGHT_FRACTION, EXTRA_TURNAROUND_TIME, TAX_CREDIT_PER_GALLON

class EconomicCalculationError(ValidationError):
    """Custom exception for economic calculation errors."""
    pass

def validate_data(data: Dict[str, pd.DataFrame]) -> None:
    """Validate loaded data for economic calculations."""
    required_keys = ["uti_data", "operations_data", "income_data"]
    for key in required_keys:
        if key not in data:
            raise EconomicCalculationError(f"Missing required dataset: {key}")
        if data[key].empty:
            raise EconomicCalculationError(f"Dataset {key} is empty")

    required_columns = {
        "operations_data": ["UNIQUE_CARRIER_NAME", "ORIGIN", "DEPARTURES_PERFORMED"],
        "income_data": ["OP_REVENUES"],
        "uti_data": ["REV_ACRFT_HRS_AIRBORNE_610"]
    }
    for dataset, columns in required_columns.items():
        missing_cols = [col for col in columns if col not in data[dataset].columns]
        if missing_cols:
            raise EconomicCalculationError(
                f"Missing required columns in {dataset}: {', '.join(missing_cols)}"
            )

def load_data() -> Dict[str, pd.DataFrame]:
    """Load required datasets using centralized data loader."""
    try:
        data = {
            "uti_data": load_operational_hours(),
            "operations_data": load_carrier_operations(),
            "income_data": load_income_data(),
        }
        validate_data(data)
        return data
    except Exception as e:
        raise EconomicCalculationError(f"Error loading data: {str(e)}")

# ------------------------------------------------------------------------
# New Function: hydrogen_uti_rev
# ------------------------------------------------------------------------
def hydrogen_uti_rev(
    fraction_flights_year: float,
    tot_delta_flights_atl: float,
    flights_atl_to_dome: float,
    h2_demand_annual_gal: float,
    extra_turn_time: float,
    total_rev: float,
    baseline_jetA_util: float
):
    """
    Calculates the hydrogen utilization impact and required tax credit per gallon.

    Parameters
    ----------
    fraction_flights_year   : Fraction of flights using H2 in the given year.
    tot_delta_flights_atl   : Total delta flights at ATL.
    flights_atl_to_dome     : Ratio of domestic flights from ATL.
    h2_demand_annual_gal    : Annual hydrogen demand (in gallons).
    extra_turn_time         : Additional turnaround time (minutes).
    total_rev               : Total revenue (in millions USD).
    baseline_jetA_util      : Baseline Jet-A utilization (in flight hours).

    Returns
    -------
    utilization_h2          : Adjusted hydrogen utilization hours.
    revenue_drop_m          : Revenue drop (in millions USD).
    required_tax_crd_per_gal: Required tax credit ($/gal) to offset the revenue drop.
    baseline_revenue_m      : Baseline revenue (in millions USD).
    new_h2_revenue_m        : Revised revenue after H2 adoption (in millions USD).
    pct_drop                : Percentage drop in revenue.
    """
    # Adjusted utilization considering the extra turnaround (applied for both departure and arrival)
    utilization_h2 = baseline_jetA_util - 2 * (
        fraction_flights_year * tot_delta_flights_atl * flights_atl_to_dome * (extra_turn_time / 60.0)
    )

    # Baseline revenue assumes no lost utilization; scaled by the fraction and domestic ratio.
    baseline_revenue_m = fraction_flights_year * flights_atl_to_dome * total_rev

    # New revenue is scaled by how much of baseline utilization remains.
    new_h2_revenue_m = baseline_revenue_m * (utilization_h2 / baseline_jetA_util) if baseline_jetA_util != 0 else 0.0

    # Revenue drop and its percentage
    revenue_drop_m = baseline_revenue_m - new_h2_revenue_m
    pct_drop = 0.0 if baseline_revenue_m == 0 else 100.0 * (revenue_drop_m / baseline_revenue_m)

    # Required tax credit per gallon. Convert revenue drop from millions to dollars.
    if h2_demand_annual_gal > 0:
        required_tax_crd_per_gal = (revenue_drop_m * 1_000_000) / h2_demand_annual_gal
    else:
        required_tax_crd_per_gal = 0.0

    return (
        utilization_h2,
        revenue_drop_m,
        required_tax_crd_per_gal,
        baseline_revenue_m,
        new_h2_revenue_m,
        pct_drop
    )

def calculate_economic_impact() -> Dict[str, float]:
    """Compute revenue changes due to hydrogen fleet transition using the revised logic."""
    try:
        data = load_data()

        # Filter Delta operations data
        total_delta_oper = data["operations_data"][data["operations_data"]["UNIQUE_CARRIER_NAME"] == "Delta Air Lines Inc."]
        if total_delta_oper.empty:
            raise EconomicCalculationError("No Delta Airlines operations data found")

        atl_delta_oper = total_delta_oper[total_delta_oper["ORIGIN"] == "ATL"]
        if atl_delta_oper.empty:
            raise EconomicCalculationError("No Delta Airlines ATL operations data found")

        # Aggregate key metrics from the data
        total_departures = float(total_delta_oper["DEPARTURES_PERFORMED"].sum())
        if total_departures == 0:
            raise EconomicCalculationError("Total departures cannot be zero")

        # Calculate the domestic portion from ATL
        domestic_ratio = float(atl_delta_oper["DEPARTURES_PERFORMED"].sum() / total_departures)
        # Revenue in millions USD
        total_rev = float(data["income_data"]["OP_REVENUES"].sum() / 1_000_000)
        # Baseline Jet-A utilization is scaled by the constant fraction and domestic ratio
        baseline_jetA_util = float(
            HYDROGEN_FLIGHT_FRACTION * domestic_ratio * data["uti_data"]["REV_ACRFT_HRS_AIRBORNE_610"].sum()
        )
        if baseline_jetA_util == 0:
            raise EconomicCalculationError("Baseline Jet-A utilization cannot be zero")

        # For demonstration, define an annual hydrogen demand in gallons.
        # (In practice, this would come from an external demand model.)
        h2_demand_annual_gal = 250000 * 7.48052 * 12  # example conversion factor: month demand * 12

        # Use the extra turnaround time constant from app.constants.
        extra_turn_time = EXTRA_TURNAROUND_TIME

        # Use the constant HYDROGEN_FLIGHT_FRACTION as a proxy of the fraction of flights using hydrogen.
        fraction_flights_year = HYDROGEN_FLIGHT_FRACTION

        (utilization_h2, revenue_drop_m, required_tax_crd_per_gal, baseline_revenue_m, new_h2_revenue_m, pct_drop) = hydrogen_uti_rev(
            fraction_flights_year,
            total_departures,
            domestic_ratio,
            h2_demand_annual_gal,
            extra_turn_time,
            total_rev,
            baseline_jetA_util
        )

        return {
            "hydrogen_utilization": float(utilization_h2),
            "revenue_drop": float(revenue_drop_m),
            "total_tax_credits": float(required_tax_crd_per_gal),
            "baseline_revenue": float(baseline_revenue_m),
            "new_h2_revenue": float(new_h2_revenue_m),
            "percent_revenue_drop": float(pct_drop)
        }

    except EconomicCalculationError:
        raise
    except Exception as e:
        raise EconomicCalculationError(f"Error calculating economic impact: {str(e)}")