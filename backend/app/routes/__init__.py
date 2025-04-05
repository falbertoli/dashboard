# File: backend/app/routes/__init__.py

from .hydrogen import hydrogen_bp
from .economic import economic_bp
from .storage import storage_bp
from .sustainability import sustainability_bp
from .map import map_bp
from .distances_requirements import distances_requirements_bp
from .regulations import regulations_bp
from .zoning_violations import zoning_violations_bp

# Export all blueprints for easier importing
__all__ = ['hydrogen_bp', 'economic_bp', 'storage_bp', 'sustainability_bp', 'map_bp', 'distances_requirements_bp', 'regulations_bp', 'zoning_violations_bp']