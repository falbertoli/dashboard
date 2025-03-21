# File: backend/app/routes/sustainability.py

from flask import Blueprint

# Define the Blueprint
sustainability_bp = Blueprint("sustainability", __name__)

# Define a route for the Blueprint
@sustainability_bp.route("/sustainability", methods=["GET"])
def get_sustainability():
    return {"message": "Sustainability endpoint is working!"}