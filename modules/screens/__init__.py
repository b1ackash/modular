from flask import Blueprint
from .screens import main_page,landing_page,logout,register,profile,page_blank,viewusers

screens_bp = Blueprint('screens', __name__)

screens_bp.add_url_rule('/',view_func=main_page)

screens_bp.add_url_rule('/landing',view_func=landing_page)

screens_bp.add_url_rule('/register',view_func=register)

screens_bp.add_url_rule('/profile',view_func=profile)

screens_bp.add_url_rule('/viewusers',view_func=viewusers)

screens_bp.add_url_rule('/page_blank',view_func=page_blank)


screens_bp.add_url_rule('/logout',view_func=logout)