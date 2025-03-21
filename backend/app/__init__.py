# File: backend/app/__init__.py
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for API requests

    # Import and register blueprints
    from app.routes.economic import economic_bp
    from app.routes.hydrogen import hydrogen_bp
    from app.routes.storage import storage_bp
    from app.routes.sustainability import sustainability_bp

    app.register_blueprint(economic_bp, url_prefix="/api/economic")
    app.register_blueprint(hydrogen_bp, url_prefix="/api/hydrogen")
    app.register_blueprint(storage_bp, url_prefix="/api/storage")
    app.register_blueprint(sustainability_bp, url_prefix="/api/sustainability")

    return app
