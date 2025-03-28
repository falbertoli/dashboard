# File: backend/app/services/__init__.py

from .hydrogen_service import (
    compute_h2_demand_ac, compute_h2_demand_gse, 
    compute_storage_area, compute_emissions
)
from .economic_service import calculate_economic_impact
from .storage_service import calculate_h2_storage_cost
from .sustainability_service import emissions  # now using the new emissions function

# Export all service functions for easier importing
__all__ = [
    'compute_h2_demand_ac', 'compute_h2_demand_gse', 
    'compute_storage_area', 'compute_emissions',
    'calculate_economic_impact', 'calculate_h2_storage_cost',
    'emissions'
]