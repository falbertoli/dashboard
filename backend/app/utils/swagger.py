# File: backend/app/utils/swagger.py

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can be a local file or url)

def setup_swagger(app):
    """Configure Swagger UI for the application.
    
    Args:
        app: Flask application instance
    """
    # Create Swagger UI blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Hydrogen Dashboard API"
        }
    )
    
    # Register blueprint
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    # Create a route to serve the OpenAPI spec
    @app.route('/static/swagger.json')
    def serve_swagger_spec():
        return app.send_static_file('swagger.json')