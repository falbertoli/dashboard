# File: backend/app/services/economic_service.py


from typing import Dict, Any
import pandas as pd
from app.utils.validation import ValidationError
from app.utils.data_loader import load_operational_hours, load_carrier_operations, load_income_data
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
    print(f"--------------------------------------------------------------------------------Input parameters: fraction_flights_year={fraction_flights_year}, extra_turn_time={extra_turn_time}, flights_atl_to_dome={flights_atl_to_dome}, total_rev={total_rev}")
   
    # Calculate utilization for hydrogen flights, accounting for extra turnaround time
    utilization_h2 = baseline_jetA_util - 2 * (
        fraction_flights_year *
        tot_delta_flights_atl *
        flights_atl_to_dome *
        (extra_turn_time / 60.0)
    )


    # Baseline revenue (if all flights at fraction_flights_year had no extra turnaround delay)
    baseline_revenue_m = fraction_flights_year * flights_atl_to_dome * total_rev
    print(f" fraction_flights_year * flights_atl_to_dome * total_rev:  {fraction_flights_year} * {flights_atl_to_dome} * {total_rev}")
    print(f"baseline_revenue_m {baseline_revenue_m}")


    # New H2 revenue after losing some utilization
    if baseline_jetA_util != 0.0:
        new_h2_revenue_m = baseline_revenue_m * (utilization_h2 / baseline_jetA_util)
    else:
        new_h2_revenue_m = 0.0
   
    print(f"new_h2_revenue_m = baseline_revenue_m * (utilization_h2 / baseline_jetA_util): {new_h2_revenue_m} = {baseline_revenue_m} * ({utilization_h2} / {baseline_jetA_util})")


    # Revenue drop and percentage drop
    revenue_drop_m = baseline_revenue_m - new_h2_revenue_m
    print(f"revenue_drop_m = baseline_revenue_m - new_h2_revenue_m: {revenue_drop_m} = {baseline_revenue_m} - {new_h2_revenue_m}")
    pct_drop = 0.0 if baseline_revenue_m == 0.0 else 100.0 * (revenue_drop_m / baseline_revenue_m)
    print(f"pct_drop = 0.0 if baseline_revenue_m == 0.0 else 100.0 * (revenue_drop_m / baseline_revenue_m): {pct_drop} = 0.0 if {baseline_revenue_m} == 0.0 else 100.0 * ({revenue_drop_m} / {baseline_revenue_m})")


    # Required tax credit per gallon (convert revenue drop from million dollars to dollars)
    if h2_demand_annual_gal > 0:
        required_tax_crd_per_gal = (revenue_drop_m * 1_000_000) / h2_demand_annual_gal
    else:
        required_tax_crd_per_gal = 0.0


    print(f"utilization_h2={utilization_h2}, baseline_jetA_util={baseline_jetA_util}")
    print(f"baseline_revenue_m={baseline_revenue_m}, new_h2_revenue_m={new_h2_revenue_m}")
    print(f"revenue_drop_m={revenue_drop_m}, pct_drop={pct_drop}")


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
    final_h2_year: int  
) -> Dict[str, Any]:
    """
    Compute revenue changes for hydrogen fleet transition across multiple years and scenarios.
    Uses a simple compound growth rate model consistent with the original implementation.
    """
    try:
        print(f"Economic calculation parameters: total_h2_demand={total_h2_demand}, fleet_percentage={fleet_percentage}, start_year={start_year}, end_year={end_year}, growth_rate={growth_rate}, extra_turn_time={extra_turn_time}, turn_time_decrease_rates={turn_time_decrease_rates}, final_h2_year={final_h2_year}")
       
        # -------- Load and validate data --------
        data = load_data()


        # -------- Apply EXACT filtering logic from turn_time_impact.py --------
        # 1. Filter uti_data for Delta domestic flights ('DL' and REGION == 'D')
        total_delta_uti = data["uti_data"][
            (data["uti_data"]['UNIQUE_CARRIER'] == 'DL') &
            (data["uti_data"]['REGION'] == 'D')
        ]
        if total_delta_uti.empty:
            raise EconomicCalculationError("No Delta domestic flights found in utilization data")


        # 2. Filter operations_data for Delta flights departing from ATL
        atl_delta_oper = data["operations_data"][
            (data["operations_data"]['UNIQUE_CARRIER_NAME'] == 'Delta Air Lines Inc.') &
            (data["operations_data"]['ORIGIN'] == 'ATL')
        ]
        if atl_delta_oper.empty:
            raise EconomicCalculationError("No Delta flights departing from ATL found")


        # 3. Filter operations_data for ALL Delta flights
        total_delta_oper = data["operations_data"][
            (data["operations_data"]['UNIQUE_CARRIER_NAME'] == 'Delta Air Lines Inc.')
        ]
        if total_delta_oper.empty:
            raise EconomicCalculationError("No Delta flights found in operations data")


        # 4. Filter income_data for Delta domestic revenue
        total_revenue = data["income_data"][
            (data["income_data"]['UNIQUE_CARRIER_NAME'] == 'Delta Air Lines Inc.') &
            (data["income_data"]['REGION'] == 'D')
        ]
        if total_revenue.empty:
            raise EconomicCalculationError("No Delta domestic revenue found in income data")


        # -------- Compute baseline inputs --------
        tot_delta_flights_atl = float(total_delta_oper['DEPARTURES_PERFORMED'].sum())
        if tot_delta_flights_atl == 0:
            raise EconomicCalculationError("Total Delta flights at ATL cannot be zero")
       
        flights_atl_to_dome = float(
            atl_delta_oper['DEPARTURES_PERFORMED'].sum() / tot_delta_flights_atl
        )


        total_rev = float(total_revenue['OP_REVENUES'].sum() / 1_000_000)
        baseline_jetA_util = float(
            fleet_percentage * flights_atl_to_dome * total_delta_uti['REV_ACRFT_HRS_AIRBORNE_610'].sum()
        )


        # -------- Rest of the function remains the same --------
        # Option 1: Use the user-supplied fleet_percentage as the initial fraction.
        fraction_flights_2023 = fleet_percentage
        target_fraction = fleet_percentage  
        slope = (target_fraction - fraction_flights_2023) / (final_h2_year - start_year)


        years = range(start_year, end_year + 1)
        scenario_results = {}


        for rate in turn_time_decrease_rates:
            all_results = []
            for year in years:
                years_elapsed = year - start_year


                # 1) H2 fraction grows linearly until final_h2_year.
                if year <= final_h2_year:
                    fraction_flights_year = fraction_flights_2023 + slope * years_elapsed
                else:
                    fraction_flights_year = target_fraction


                # 2) Calculate turnaround time for the current year.
                this_year_turn_time = max(0, extra_turn_time - (rate * years_elapsed))


                # 3) Compute a compound growth factor.
                factor = (1 + growth_rate) ** years_elapsed
                print(f"Year {year}: Using growth factor {factor:.4f} (growth_rate={growth_rate})")


                # Scale up key variables using the growth factor.
                h2_demand_annual_scaled_gal = total_h2_demand * factor
                total_rev_scaled_m = total_rev * factor
                baseline_jetA_util_scaled = baseline_jetA_util * factor


                # 4) Compute the economic metrics for the current year.
                (
                    utilization_h2,
                    revenue_drop_m,
                    required_tax_crd_per_gal,
                    baseline_revenue_m,
                    new_h2_revenue_m,
                    pct_drop
                ) = hydrogen_uti_rev(
                    fraction_flights_year,
                    tot_delta_flights_atl,
                    flights_atl_to_dome,
                    h2_demand_annual_scaled_gal,
                    this_year_turn_time,
                    total_rev_scaled_m,
                    baseline_jetA_util_scaled
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


        # -------- Compute Summary Metrics --------
        summary_metrics = {}
        for rate, df in scenario_results.items():
            summary_metrics[rate] = {
                "max_tax_credit": float(df["Req_Tax_Credit_per_gal"].max()),
                "max_revenue_drop_pct": float(df["Pct_Drop"].max()),
                "avg_revenue_drop_pct": float(df["Pct_Drop"].mean()),
                "final_year_tax_credit": float(df.iloc[-1]["Req_Tax_Credit_per_gal"]),
                "final_year_revenue_drop": float(df.iloc[-1]["Pct_Drop"])
            }


        # Return results
        return {
            "scenarios": {k: v.to_dict(orient="records") for k, v in scenario_results.items()},
            "summary": summary_metrics
        }


    except EconomicCalculationError as e:
        raise
    except Exception as e:
        raise EconomicCalculationError(f"Error calculating economic impact: {str(e)}")

