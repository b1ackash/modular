from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_session import Session
from datetime import timedelta
import os
from flask_mail import Mail, Message  # Import Flask-Mail
from modules.models.models import engine, SQLModel
from modules.auth import auth_bp
from modules.api import api_bp
from modules.screens import screens_bp

ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')  
app = Flask(__name__, static_url_path='/static')

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['ASSETS_ROOT'] = ASSETS_ROOT
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'osbornepotani@gmail.com'
app.config['MAIL_PASSWORD'] = 'pvfq ftpp umyf svrj'
app.config['MAIL_DEFAULT_SENDER'] = 'osbornepotani@gmail.com'

# Initialize Flask extensions
Session(app)
CORS(app)
mail = Mail(app)  # Initialize Flask-Mail

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

# Email sending route
@app.route('/send-email')
def send_email():
    try:
        msg = Message('Hello from Flask',
                      recipients=['osbornepotani@live.com'])
        msg.body = 'This is a test email sent from your Flask app!'
        mail.send(msg)
        return "Email sent!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
