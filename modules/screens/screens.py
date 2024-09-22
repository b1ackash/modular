# screens.py
from flask import  render_template, session, redirect, url_for


def main_page():
    return render_template('accounts/login.html')

def landing_page():
    if 'username' in session:
        return render_template('home/index.html')
    else:
        return redirect(url_for('screens.main_page'))

# Logout route

def logout():
    # Clear session data (logout)
    session.pop('username', None)
    return redirect(url_for('screens.main_page'))