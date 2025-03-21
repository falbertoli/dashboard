# backend/app/utils/response.py
from flask import jsonify

class APIResponse:
    @staticmethod
    def success(data=None, message=None):
        return jsonify({
            "status": "success",
            "data": data,
            "message": message
        })
    
    @staticmethod
    def error(message, status_code=400):
        return jsonify({
            "status": "error",
            "message": message
        }), status_code