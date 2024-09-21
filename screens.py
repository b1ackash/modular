# screens.py
from flask import Blueprint, render_template, session, redirect, url_for

screens_bp = Blueprint('screens', __name__)

@screens_bp.route('/')
def main_page():
    return render_template('index.html')

@screens_bp.route('/landing')
def landing_page():
    if 'username' in session:
        return render_template('landing.html')
    else:
        return redirect(url_for('screens.main_page'))

# Logout route
@screens_bp.route('/logout')
def logout():
    # Clear session data (logout)
    session.pop('username', None)
    return redirect(url_for('screens.main_page'))