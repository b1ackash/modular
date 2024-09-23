# customfunc.py
from flask import session,render_template
from sqlmodel import Session as SQLSession, select
from modules.models.models import Users, engine




def get_user_details(user_id):
    if 'username' in session:

        with SQLSession(engine) as session_db:
            statement = select(Users).where(Users.id == user_id)
            user = session_db.exec(statement).first()

        if user:
            user_details = {
                'id': user.id,
                'username': user.username,
				'password': user.password
            }
            return user_details
        else:
             return render_template('home/page-404.html')
    else:
         return render_template('home/page-404.html')