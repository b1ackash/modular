# customfunc.py
from flask import session,render_template
from sqlmodel import Session as SQLSession, select,and_
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
    
def deactivate_user(user_id: int):
    # Step 1: Fetch the user from the database
    username = session['username']
    with SQLSession(engine) as session_db:
        statement = select(Users).where(and_(Users.id == user_id,Users.username!=username))
        result = session_db.exec(statement)
        user = result.one_or_none()
        
        # Step 2: If user exists, delete it
        if user:
            session_db.delete(user)
            session_db.commit()
            return f"User with ID {user_id} deleted successfully."
        else:
            return f"User with ID {user_id} does not exist."    