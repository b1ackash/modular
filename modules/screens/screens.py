# screens.py
from flask import  render_template, session, redirect, url_for 
from ..config import Config
from ..functions.customffunc import get_user_details,deactivate_user,log_user_action

title =Config.TITLE

def main_page():
    if 'username' in session:
        log_user_action(' opened Main page', session['username'])        
        return render_template('home/landing.html',title=title)
    else:
        return render_template('accounts/login.html',title=title)

def landing_page():
    if 'username' in session:
        log_user_action(' opened landing_page ', session['username'])        
        return render_template('home/landing.html',title=title)
    else:
        return redirect(url_for('screens.main_page'))

def register():
    if 'username' in session:
        log_user_action(' opened Register_page', session['username'])        
        return render_template('home/register.html',title=title)
    else:
        return redirect(url_for('screens.main_page'))
def profile():
    if 'username' in session:
        log_user_action(' opened Profile_page ', session['username'])        
        return render_template('home/profile.html',title=title)
    else:
        return redirect(url_for('screens.main_page'))

def viewusers():
    if 'username' in session:
        log_user_action(' opened View_users_page', session['username'])        
        return render_template('home/viewusers.html',title=title)
    else:
        return redirect(url_for('screens.main_page'))
    
def viewuser(user_id):
    if 'username' in session:
        log_user_action(' opened View_user_page', session['username'])                            
        return render_template('home/viewuser.html',user=get_user_details(user_id),title=title)
    else:
        return redirect(url_for('screens.main_page'))

def deactivateuser(user_id):
    if 'username' in session:
             log_user_action(' opened deactivate_user_page ', session['username'])                            
             deactivate_user(user_id)        
             return render_template('home/viewusers.html',title=title)
    else:
        return redirect(url_for('screens.main_page'))


def page_blank():
    if 'username' in session:
        return render_template('home/page-blank.html',title=title)
    else:
        return redirect(url_for('screens.main_page'))


# Logout route

def logout():
    # Clear session data (logout)
    log_user_action('  Logouted  ', session['username'])                            
    session.pop('username', None)
    return redirect(url_for('screens.main_page'))