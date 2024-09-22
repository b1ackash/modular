from flask import request, jsonify, session, redirect, url_for
from sqlmodel import select
from modules.models.models import Users, engine  # Import the Users model and engine
from sqlmodel import Session as SQLSession  # Import SQLModel's Session
import hashlib

# Login route
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