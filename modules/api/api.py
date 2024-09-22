# api.py
from flask import  request, jsonify, session
from sqlmodel import Session as SQLSession, select
from sqlalchemy import func
from hashlib import sha256
from modules.models.models import Users, engine


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

def get_all_users():
    if 'username' in session:
        with SQLSession(engine) as session_db:
            statement = select(Users)
            users = session_db.exec(statement).all()

        if users:
            all_users = []
            for user in users:
                user_details = {
                    'id': user.id,
                    'username': user.username
                }
                all_users.append(user_details)
            return jsonify(all_users), 200
        else:
            return jsonify({'message': 'No users found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 401
    
def get_all_users_page():
    if 'username' in session:
        # Get pagination parameters
        page = request.args.get('page', default=1, type=int)
        limit = request.args.get('limit', default=10, type=int)

        # Calculate offset (how many rows to skip)
        offset = (page - 1) * limit

        with SQLSession(engine) as session_db:
            # Fetch limited users based on pagination
            statement = select(Users).offset(offset).limit(limit)
            users = session_db.exec(statement).all()

            # Fetch the total number of users for pagination metadata
            statementcount = select(Users)
            results = session_db.exec(statementcount).all()  # Get all records
            total_users = len(results) #session_db.exec(select(func.count(Users.id))).first()[0]  # Use first() and access the count
        if users:
            all_users = []
            for user in users:
                user_details = {
                    'id': user.id,
                    'username': user.username,
                    'password': user.password  # Avoid returning passwords in real-world scenarios
                }
                all_users.append(user_details)
            
            # Pagination metadata
            pagination_info = {
                'total': total_users,
                'page': page,
                'limit': limit,
                'total_pages': (total_users + limit - 1) // limit  # Calculate total pages
            }

            return jsonify({'users': all_users, 'pagination': pagination_info}), 200
        else:
            return jsonify({'message': 'No users found'}), 404
    else:
        return jsonify({'message': 'Unauthorized'}), 401
    
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
def logout_api():
    # Clear session data (logout)
	session.pop('username', None)
	return jsonify({'message': 'Aidos'}), 200
	