import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "routes.login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "d0782e15d02562e8c563941487976982645ae44644e687a3881503c468f17709"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///bookmark.db"
)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from bookmark.routes import routes
    app.register_blueprint(routes)

    return app
