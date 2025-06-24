from flask import Flask
from .config import Config
from .extensions import db, jwt, mail, bcrypt
from .routes.auth import auth_bp
from .routes.client import client_bp
from .routes.ops import ops_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(client_bp, url_prefix="/client")
    app.register_blueprint(ops_bp, url_prefix="/ops")

    with app.app_context():
        db.create_all()

    return app
