# File: backend/app/routes/__init__.py

from .hydrogen import hydrogen_bp
from .economic import economic_bp
from .storage import storage_bp
from .sustainability import sustainability_bp

# Export all blueprints for easier importing
__all__ = ['hydrogen_bp', 'economic_bp', 'storage_bp', 'sustainability_bp']