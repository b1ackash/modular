# api.py
from flask import Blueprint, request, jsonify, session
from sqlmodel import Session as SQLSession, select
from hashlib import sha256
from modules.models.models import Users, engine
import hashlib
api_bp = Blueprint('api', __name__)

@api_bp.route('/api/user_details', methods=['GET'])
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

@api_bp.route('/api/users', methods=['POST'])
def create_user():
    if 'username' in session:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        hashed_password = sha256(password.encode()).hexdigest()
        new_user = Users(username=username, password=hashed_password)

        with SQLSession(engine) as session_db:
            session_db.add(new_user)
            session_db.commit()
            session_db.refresh(new_user)

        return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201
    else:
        return jsonify({'message': 'Unauthorized'}), 401


# Route to get user details by username
@api_bp.route('/api/user_details_by_username', methods=['GET'])
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

# Route to update an existing user
@api_bp.route('/api/userupdate/<int:user_id>', methods=['PUT'])
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
@api_bp.route('/api/logout')
def logout_api():
    # Clear session data (logout)
	session.pop('username', None)
	return jsonify({'message': 'Aidos'}), 200
	