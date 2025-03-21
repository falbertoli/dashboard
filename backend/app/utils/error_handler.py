# File: backend/app/utils/error_handler.py
from flask import jsonify

def register_error_handlers(app):
    """Register error handlers with the Flask app.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({
            "error": "Bad Request", 
            "message": str(error)
        }), 400
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            "error": "Not Found", 
            "message": str(error) or "The requested resource was not found."
        }), 404
    
    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 Internal Server Error."""
        app.logger.error(f"Server error: {error}")
        return jsonify({
            "error": "Internal Server Error", 
            "message": "The server encountered an internal error."
        }), 500
    
    @app.errorhandler(Exception)
    def unhandled_exception(error):
        """Handle any unhandled exceptions."""
        app.logger.error(f"Unhandled exception: {error}", exc_info=True)
        return jsonify({
            "error": "Server Error", 
            "message": "An unexpected error occurred."
        }), 500