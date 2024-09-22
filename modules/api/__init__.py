from flask import Blueprint
from .api import get_user_details, create_user,get_user_details_by_username,update_user,logout_api

api_bp = Blueprint('api', __name__)

api_bp.add_url_rule('/api/user_details', view_func=get_user_details, methods=['GET'])

api_bp.add_url_rule('/api/users', view_func=create_user, methods=['POST'])

api_bp.add_url_rule('/api/user_details_by_username', view_func=get_user_details_by_username, methods=['GET'])

api_bp.add_url_rule('/api/userupdate/<int:user_id>', view_func=update_user, methods=['PUT'])

api_bp.add_url_rule('/api/logout', view_func=logout_api)