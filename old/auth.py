# auth.py
from flask import Blueprint, request, jsonify, session, redirect, url_for
from sqlmodel import Session as SQLSession, select
from hashlib import sha256
from models import Users, engine

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    hashed_password = sha256(password.encode()).hexdigest()

    with SQLSession(engine) as session_db:
        statement = select(Users).where(Users.username == username, Users.password == hashed_password)
        user = session_db.exec(statement).first()

    if user:
        session.permanent = True
        session['username'] = username
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

""" @auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully'}), 200 """
