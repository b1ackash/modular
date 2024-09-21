from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_from_directory
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta
from sqlmodel import SQLModel, Field, create_engine, Session as SQLSession, select
import hashlib
#import os

app = Flask(__name__, static_url_path='/static')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secure secret key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
Session(app)
CORS(app)
# Assets Management
#ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')  
#app.config['ASSETS_ROOT'] = '/static/assets/'
# Define the database model for the Users
class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str  # This will store the hashed password

# Create the database engine
engine = create_engine("sqlite:///database.db")

#icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

#pages
# Route for landing
@app.route('/')
def main_page():
    # Render the main.html template
    return render_template('index.html')
# Route for landing page
@app.route('/landing')
def landing_page():
    # Check if user is authenticated
    if 'username' in session:
        return render_template('landing.html')
    else:
        return redirect(url_for('main_page'))  # Redirect to login page if not authenticated

# Logout route
@app.route('/logout')
def logout():
    # Clear session data (logout)
    session.pop('username', None)
    return redirect(url_for('main_page'))

#endpoints	
# Route for login endpoint
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    # Hash the incoming password to compare with the stored hash
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    with SQLSession(engine) as session_db:
        statement = select(Users).where(Users.username == username, Users.password == hashed_password)
        user = session_db.exec(statement).first()

    if user:
        # Set session to be permanent
        session.permanent = True
        # Set session data upon successful login
        session['username'] = username
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Route for user details endpoint
@app.route('/api/user_details', methods=['GET'])
def get_user_details():
    if 'username' in session:
        username = session['username']

        with SQLSession(engine) as session_db:
            statement = select(Users).where(Users.username == username)
            user = session_db.exec(statement).first()

        if user:
            user_details = {
                'id': user.id,
                'username': user.username,
				'password': user.password
            }
            return jsonify(user_details), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 401

# Route to get user details by username
@app.route('/api/user_details_by_username', methods=['GET'])
def get_user_details_by_username():
    if 'username' in session:
        username = request.args.get('username')

        if not username:
            return jsonify({'message': 'Username parameter is required'}), 400

        with SQLSession(engine) as session_db:
            statement = select(Users).where(Users.username == username)
            user = session_db.exec(statement).first()

        if user:
            user_details = {
                'id': user.id,
                'username': user.username,
				'password': user.password
            }
            return jsonify(user_details), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 401

# Route to create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    if 'username' in session:  # Check if session is active
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Username and password are required'}), 400

        # Hash the password before storing it
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        new_user = Users(username=username, password=hashed_password)

        with SQLSession(engine) as session_db:
            session_db.add(new_user)
            session_db.commit()
            session_db.refresh(new_user)

        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201
    else:
        return jsonify({'message': 'Unauthorized'}), 401  # Return unauthorized if session is not active

# Route to update an existing user
@app.route('/api/userupdate/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if 'username' in session:  # Check if session is active
        data = request.json
        new_username = data.get('username')
        new_password = data.get('password')

        if not new_username and not new_password:
            return jsonify({'message': 'No new data provided for update'}), 400

        with SQLSession(engine) as session_db:
            user = session_db.get(Users, user_id)
            if not user:
                return jsonify({'message': 'User not found'}), 404

            if new_username:
                user.username = new_username
            if new_password:
                user.password = hashlib.sha256(new_password.encode()).hexdigest()

            session_db.add(user)
            session_db.commit()

        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'message': 'Unauthorized'}), 401  # Return unauthorized if session is not active
		

#API to get logout
@app.route('/api/logout')
def logout_api():
    # Clear session data (logout)
	session.pop('username', None)
	return jsonify({'message': 'Aidos'}), 200
	

if __name__ == '__main__':
    app.run(debug=True)
