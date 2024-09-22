from flask import Blueprint
from .auth import login  # Import the functions from auth.py

auth_bp = Blueprint('auth', __name__)

# Register the login route
auth_bp.add_url_rule('/login', view_func=login, methods=['POST'])