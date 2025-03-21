# File: backend/app/utils/validation.py

from typing import Dict, Any, List, Union

class ValidationError(ValueError):
    """Custom exception for validation errors"""
    pass

def validate_required_params(data: Dict[str, Any], required_params: List[str]) -> None:
    """Validate required parameters exist in data."""
    for param in required_params:
        if param not in data or data[param] is None:
            raise ValidationError(f"Missing required parameter: {param}")

def validate_numeric_range(
    value: Union[int, float], 
    min_value: Union[int, float], 
    max_value: Union[int, float],
    param_name: str
) -> None:
    """Validate numeric value is within specified range."""
    if not isinstance(value, (int, float)):
        raise ValidationError(f"{param_name} must be a number")
    if value < min_value or value > max_value:
        raise ValidationError(
            f"{param_name} must be between {min_value} and {max_value}"
        )

def validate_year(year: int, min_year: int = 2023) -> None:
    """Validate year is valid for projections."""
    if not isinstance(year, int):
        raise ValidationError("Year must be an integer")
    if year < min_year:
        raise ValidationError(f"Year must be {min_year} or later")

def validate_gse_list(gse_list: List[str]) -> None:
    """Validate GSE list."""
    if not isinstance(gse_list, list):
        raise ValidationError("GSE list must be an array")
    if not gse_list:
        raise ValidationError("GSE list cannot be empty")
    if not all(isinstance(item, str) for item in gse_list):
        raise ValidationError("All GSE items must be strings")