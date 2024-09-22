# app.py
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta
import os
from modules.models.models import engine, SQLModel
from modules.auth import auth_bp
from modules.api import api_bp
from modules.screens import screens_bp

ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')  
app = Flask(__name__, static_url_path='/static')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['ASSETS_ROOT'] = ASSETS_ROOT
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)



Session(app)
CORS(app)

# Create database tables if not exists
SQLModel.metadata.create_all(engine)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)
app.register_blueprint(screens_bp)

# Favicon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

if __name__ == '__main__':
    app.run(debug=True)
