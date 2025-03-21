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

    # Validate required columns
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

def calculate_economic_impact() -> Dict[str, float]:
    """Compute revenue changes due to hydrogen fleet transition."""
    try:
        data = load_data()

        # Extract relevant data
        total_delta_oper = data["operations_data"][
            data["operations_data"]["UNIQUE_CARRIER_NAME"] == "Delta Air Lines Inc."
        ]
        
        if total_delta_oper.empty:
            raise EconomicCalculationError("No Delta Airlines operations data found")
            
        atl_delta_oper = total_delta_oper[total_delta_oper["ORIGIN"] == "ATL"]
        
        if atl_delta_oper.empty:
            raise EconomicCalculationError("No Delta Airlines ATL operations data found")

        # Calculate metrics
        B = float(total_delta_oper["DEPARTURES_PERFORMED"].sum())
        if B == 0:
            raise EconomicCalculationError("Total departures cannot be zero")
            
        C = float(atl_delta_oper["DEPARTURES_PERFORMED"].sum() / B)
        F = float(data["income_data"]["OP_REVENUES"].sum() / 1_000_000)
        baseline_jetA_util = float(
            HYDROGEN_FLIGHT_FRACTION * C * data["uti_data"]["REV_ACRFT_HRS_AIRBORNE_610"].sum()
        )

        if baseline_jetA_util == 0:
            raise EconomicCalculationError("Baseline Jet-A utilization cannot be zero")

        # Compute Revenue Changes
        utilization_h2 = baseline_jetA_util - (HYDROGEN_FLIGHT_FRACTION * B * (EXTRA_TURNAROUND_TIME / 60.0))
        baseline_revenue = HYDROGEN_FLIGHT_FRACTION * C * F
        new_h2_revenue = baseline_revenue * (utilization_h2 / baseline_jetA_util)
        total_tax_credits = TAX_CREDIT_PER_GALLON * 2752285.804321897 * 7.48052 * 12 / 1_000_000
        revenue_drop = baseline_revenue - new_h2_revenue
        pct_drop = 100 * (revenue_drop / baseline_revenue)

        return {
            "hydrogen_utilization": float(utilization_h2),
            "revenue_drop": float(revenue_drop),
            "total_tax_credits": float(total_tax_credits),
            "baseline_revenue": float(baseline_revenue),
            "new_h2_revenue": float(new_h2_revenue),
            "percent_revenue_drop": float(pct_drop)
        }

    except EconomicCalculationError:
        raise
    except Exception as e:
        raise EconomicCalculationError(f"Error calculating economic impact: {str(e)}")