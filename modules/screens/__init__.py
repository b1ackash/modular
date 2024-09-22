from flask import Blueprint
from .screens import main_page,landing_page,logout

screens_bp = Blueprint('screens', __name__)

screens_bp.add_url_rule('/',view_func=main_page)

screens_bp.add_url_rule('/landing',view_func=landing_page)

screens_bp.add_url_rule('/logout',view_func=logout)