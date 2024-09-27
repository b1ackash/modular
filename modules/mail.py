from flask_mail import Mail

# Create Mail object
mail = Mail()

def init_mail(app):
    """
    Initialize Flask-Mail with the given app instance.
    """
    mail.init_app(app)
