# File: backend/app/__init__.py

from flask import Flask
from flask_cors import CORS
from app.config import config
from app.utils.data_loader import populate_database, ac_engine, gse_engine, init_db_engines

def create_app(config_name="default"):
    """Application factory function that creates and configures the Flask app.
    
    Args:
        config_name (str): Configuration to use - 'development', 'testing', 'production', or 'default'
        
    Returns:
        Flask: Configured Flask application
    """
    # Create Flask app
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Load configuration based on config_name
    app.config.from_object(config[config_name])
    
    # Enable CORS for API requests
    CORS(app)
    
    # Initialize database engines with app configuration
    with app.app_context():
        init_db_engines(app)
    
    # Populate databases during app initialization
    with app.app_context():
        print(f"Initializing app with {config_name} configuration...")
        
        # Skip database population for testing environment
        if not app.config["TESTING"]:
            print("Populating databases...")
            try:
                populate_database("ac_data.csv", ac_engine, "ac_data")
                populate_database("gse_data.csv", gse_engine, "gse_data")
            except Exception as e:
                print(f"Error populating databases: {e}")
        else:
            print("Skipping database population for testing environment")

    # Import and register blueprints
    from app.routes.economic import economic_bp
    from app.routes.hydrogen import hydrogen_bp
    from app.routes.storage import storage_bp
    from app.routes.sustainability import sustainability_bp

    app.register_blueprint(economic_bp, url_prefix="/api/economic")
    app.register_blueprint(hydrogen_bp, url_prefix="/api/hydrogen")
    app.register_blueprint(storage_bp, url_prefix="/api/storage")
    app.register_blueprint(sustainability_bp, url_prefix="/api/sustainability")
    
    # Register error handlers (if you've created the error_handler.py file)
    try:
        from app.utils.error_handler import register_error_handlers
        register_error_handlers(app)
    except ImportError:
        # If error_handler.py doesn't exist yet, skip this step
        pass

    return app