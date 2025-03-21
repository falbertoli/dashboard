# File: backend/app/routes/hydrogen.py

from flask import Blueprint, request
from app.services.hydrogen_service import (
    compute_h2_demand_ac, compute_h2_demand_gse,
    compute_storage_area, compute_emissions
)
from app.utils.response import APIResponse
from app.utils.validation import (
    validate_required_params, validate_numeric_range,
    validate_year, validate_gse_list, ValidationError
)
from typing import Dict, Any

hydrogen_bp = Blueprint('hydrogen', __name__)

def validate_h2_demand_ac_params(data: Dict[str, Any]) -> None:
    """Validate parameters for aircraft hydrogen demand calculation."""
    try:
        # Check required parameters
        validate_required_params(data, ["slider_perc", "end_year"])
        
        # Validate slider percentage
        slider_perc = data.get("slider_perc")
        validate_numeric_range(
            slider_perc, 0, 1, "slider_perc"
        )
        
        # Validate end year
        end_year = data.get("end_year")
        validate_year(end_year)

    except ValidationError as e:
        raise ValidationError(f"Invalid parameters: {str(e)}")

@hydrogen_bp.route('/h2_demand/ac', methods=['POST'])
def h2_demand_ac():
    """API to compute Hydrogen demand for Aircraft Operations."""
    try:
        data = request.json
        if not data:
            return APIResponse.error("No data provided", 400)

        # Validate input parameters
        validate_h2_demand_ac_params(data)
        
        # Compute hydrogen demand
        h2_demand_vol_day, fuel_weight_projected = compute_h2_demand_ac(
            slider_perc=data["slider_perc"],
            end_year=data["end_year"]
        )
        
        return APIResponse.success(
            data={
                "daily_h2_demand_ft3": h2_demand_vol_day,
                "projected_fuel_weight_lb": fuel_weight_projected
            },
            message="Successfully calculated aircraft hydrogen demand"
        )
    
    except ValidationError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        # Log the error here if you have logging set up
        return APIResponse.error(
            "An error occurred while calculating hydrogen demand", 
            500
        )

def validate_h2_demand_gse_params(data: Dict[str, Any]) -> None:
    """Validate parameters for GSE hydrogen demand calculation."""
    try:
        # Check required parameters
        validate_required_params(data, ["gse_list", "end_year"])
        
        # Validate GSE list
        validate_gse_list(data["gse_list"])
        
        # Validate end year
        validate_year(data["end_year"])

    except ValidationError as e:
        raise ValidationError(f"Invalid parameters: {str(e)}")

@hydrogen_bp.route('/h2_demand/gse', methods=['POST'])
def h2_demand_gse():
    """API to compute Hydrogen demand for Ground Support Equipment."""
    try:
        data = request.json
        if not data:
            return APIResponse.error("No data provided", 400)

        # Validate input parameters
        validate_h2_demand_gse_params(data)
        
        # Compute hydrogen demand
        daily_h2_demand_gse, tot_diesel, tot_gasoline = compute_h2_demand_gse(
            gse_list=data["gse_list"],
            end_year=data["end_year"]
        )
        
        return APIResponse.success(
            data={
                "daily_h2_demand_ft3": daily_h2_demand_gse,
                "total_diesel_used_lb": tot_diesel,
                "total_gasoline_used_lb": tot_gasoline
            },
            message="Successfully calculated GSE hydrogen demand"
        )
    
    except ValidationError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        # Log the error here if you have logging set up
        return APIResponse.error(
            "An error occurred while calculating GSE hydrogen demand", 
            500
        )

def validate_storage_area_params(data: Dict[str, Any]) -> None:
    """Validate parameters for storage area calculation."""
    try:
        # Check required parameters
        validate_required_params(data, ["h2_demand_vol"])
        
        # Validate h2_demand_vol is positive
        h2_demand_vol = data.get("h2_demand_vol")
        validate_numeric_range(
            h2_demand_vol, 
            min_value=0, 
            max_value=float('inf'), 
            param_name="h2_demand_vol"
        )

    except ValidationError as e:
        raise ValidationError(f"Invalid parameters: {str(e)}")
    
@hydrogen_bp.route('/storage_area', methods=['POST'])
def storage_area():
    """API to compute required storage area for Hydrogen tanks."""
    try:
        data = request.json
        if not data:
            return APIResponse.error("No data provided", 400)

        # Validate input parameters
        validate_storage_area_params(data)
        
        # Compute storage area
        area_required = compute_storage_area(data["h2_demand_vol"])
        
        return APIResponse.success(
            data={
                "storage_area_ft2": area_required
            },
            message="Successfully calculated storage area"
        )
    
    except ValidationError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        # Log the error here if you have logging set up
        return APIResponse.error(
            "An error occurred while calculating storage area", 
            500
        )

def validate_emissions_params(data: Dict[str, Any]) -> None:
    """Validate parameters for emissions calculation."""
    try:
        # Check required parameters exist (with defaults)
        for param in ["tot_jetA", "tot_diesel", "tot_gasoline"]:
            if param not in data:
                data[param] = 0
        
        # Validate all fuel values are non-negative
        for param in ["tot_jetA", "tot_diesel", "tot_gasoline"]:
            value = data.get(param, 0)
            validate_numeric_range(
                value,
                min_value=0,
                max_value=float('inf'),
                param_name=param
            )

        # Ensure at least one fuel value is provided
        if all(data.get(param, 0) == 0 for param in ["tot_jetA", "tot_diesel", "tot_gasoline"]):
            raise ValidationError("At least one fuel value must be greater than 0")

    except ValidationError as e:
        raise ValidationError(f"Invalid parameters: {str(e)}")

@hydrogen_bp.route('/emissions', methods=['POST'])
def emissions():
    """API to compute CO2 emissions from Jet A, Diesel, and Gasoline."""
    try:
        data = request.json
        if not data:
            return APIResponse.error("No data provided", 400)

        # Validate input parameters
        validate_emissions_params(data)
        
        # Compute emissions
        total_emissions = compute_emissions(
            tot_jetA=data.get("tot_jetA", 0),
            tot_diesel=data.get("tot_diesel", 0),
            tot_gasoline=data.get("tot_gasoline", 0)
        )
        
        return APIResponse.success(
            data={
                "total_emissions_kg": total_emissions
            },
            message="Successfully calculated emissions"
        )
    
    except ValidationError as e:
        return APIResponse.error(str(e), 400)
    except Exception as e:
        # Log the error here if you have logging set up
        return APIResponse.error(
            "An error occurred while calculating emissions", 
            500
        )