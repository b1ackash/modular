# screens.py
from flask import  render_template, session, redirect, url_for , current_app
from .config import Config

title =Config.TITLE

def main_page():
    return render_template('accounts/login.html',title=title)

def landing_page():
    if 'username' in session:
        return render_template('home/index.html',title=title)
    else:
        return redirect(url_for('screens.main_page'))

# Logout route

def logout():
    # Clear session data (logout)
    session.pop('username', None)
    return redirect(url_for('screens.main_page'))