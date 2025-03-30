# File: backend/app/services/economic_service.py

from typing import Dict, Any
import pandas as pd
from app.utils.validation import ValidationError
from app.utils.data_loader import load_operational_hours, load_carrier_operations, load_income_data
from typing import Dict, Any
from datetime import datetime
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

def calculate_economic_impact(
    total_h2_demand: float,
    fleet_percentage: float,
    start_year: int,
    end_year: int,
    growth_rate: float,
    extra_turn_time: int,
    turn_time_decrease_rates: list,
) -> Dict[str, Any]:
    """
    Compute revenue changes for hydrogen fleet transition across multiple years and scenarios.

    Parameters:
    ----------
    total_h2_demand         : Annual hydrogen demand in gallons for the current year.
    fleet_percentage        : Percentage of flights using hydrogen in the current year.
    start_year              : Current year (set dynamically if not provided).
    end_year                : Final year for hydrogen adoption.
    growth_rate             : Annual growth rate for scaling demand, revenue, and utilization.
    extra_turn_time         : Initial extra turnaround time in minutes for hydrogen flights.
    turn_time_decrease_rates: List of annual reduction rates for turnaround time (in minutes/year).

    Returns:
    -------
    Dict[str, Any]: Dictionary containing scenario results and summary metrics.
    """
    try:
        print(f"Economic calculation parameters: {total_h2_demand=}, {fleet_percentage=}, {start_year=}, {end_year=}, {growth_rate=}, {extra_turn_time=}, {turn_time_decrease_rates=}")
        data = load_data()

        # Filter Delta operations data
        total_delta_oper = data["operations_data"][data["operations_data"]["UNIQUE_CARRIER_NAME"] == "Delta Air Lines Inc."]
        atl_delta_oper = total_delta_oper[total_delta_oper["ORIGIN"] == "ATL"]
        tot_delta_flights_atl = float(total_delta_oper["DEPARTURES_PERFORMED"].sum())
        flights_atl_to_dome = float(atl_delta_oper["DEPARTURES_PERFORMED"].sum() / tot_delta_flights_atl)

        total_rev = float(data["income_data"]["OP_REVENUES"].sum() / 1_000_000)
        baseline_jetA_util = float(
            fleet_percentage
            * flights_atl_to_dome
            * data["uti_data"]["REV_ACRFT_HRS_AIRBORNE_610"].sum()
        )

        # Load growth rate data
        growth_rate_data = pd.DataFrame({
            "Year": list(range(2023, 2051)),
            "Projected Operations": [
                755856, 784123, 815016, 834644, 853350, 872286, 890251, 
                907846, 925298, 942989, 960976, 979187, 997398, 1016764, 
                1036063, 1055234, 1074792, 1094786, 1114237, 1134615, 1155514, 
                1176625, 1197973, 1219542, 1241334, 1263264, 1285643, 1308659
            ]
        })

        # Get baseline operations for the start year
        baseline_operations = growth_rate_data.loc[growth_rate_data["Year"] == start_year, "Projected Operations"].values[0]

        years = range(start_year, end_year + 1)
        slope = (1 - fleet_percentage) / (end_year - start_year)  # Linear growth slope for hydrogen adoption.

        # Store results for each scenario
        scenario_results = {}

        for rate in turn_time_decrease_rates:
            all_results = []
            for year in years:
                years_elapsed = year - start_year
                fraction_flights_year = fleet_percentage + slope * years_elapsed
                this_year_turn_time = max(0, extra_turn_time - (rate * years_elapsed))

                # Scale up using the growth rate data
                projected_operations = growth_rate_data.loc[growth_rate_data["Year"] == year, "Projected Operations"].values[0]
                factor = projected_operations / baseline_operations

                h2_demand_annual_scaled_gal = total_h2_demand * factor
                total_rev_scaled_m = total_rev * factor
                baseline_jetA_util_scaled = baseline_jetA_util * factor

                (
                    utilization_h2,
                    revenue_drop_m,
                    required_tax_crd_per_gal,
                    baseline_revenue_m,
                    new_h2_revenue_m,
                    pct_drop,
                ) = hydrogen_uti_rev(
                    fraction_flights_year,
                    tot_delta_flights_atl,
                    flights_atl_to_dome,
                    h2_demand_annual_scaled_gal,
                    this_year_turn_time,
                    total_rev_scaled_m,
                    baseline_jetA_util_scaled,
                )

                all_results.append({
                    "Year": year,
                    "Growth_Factor": factor,
                    "Turn_Time_min": this_year_turn_time,
                    "Fraction_Flights_H2": fraction_flights_year,
                    "H2_Demand_annual_gal": h2_demand_annual_scaled_gal,
                    "Hydrogen_Utilization": utilization_h2,
                    "Baseline_Revenue_M": baseline_revenue_m,
                    "Hydrogen_Revenue_M": new_h2_revenue_m,
                    "Revenue_Drop_M": revenue_drop_m,
                    "Pct_Drop": pct_drop,
                    "Req_Tax_Credit_per_gal": required_tax_crd_per_gal
                })

            scenario_results[rate] = pd.DataFrame(all_results)

        # Calculate summary metrics for each scenario
        summary_metrics = {}
        for rate, df in scenario_results.items():
            summary_metrics[rate] = {
                "max_tax_credit": float(df["Req_Tax_Credit_per_gal"].max()),
                "max_revenue_drop_pct": float(df["Pct_Drop"].max()),
                "avg_revenue_drop_pct": float(df["Pct_Drop"].mean()),
                "final_year_tax_credit": float(df.iloc[-1]["Req_Tax_Credit_per_gal"]),
                "final_year_revenue_drop": float(df.iloc[-1]["Pct_Drop"])
            }

        # Return both scenario data and summary metrics
        return {
            "scenarios": {k: v.to_dict(orient="records") for k, v in scenario_results.items()},
            "summary": summary_metrics
        }

    except EconomicCalculationError as e:
        raise
    except Exception as e:
        raise EconomicCalculationError(f"Error calculating economic impact: {str(e)}")