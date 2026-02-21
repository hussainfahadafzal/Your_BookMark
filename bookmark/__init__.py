import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from sqlalchemy import inspect, text

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "routes.login"
login_manager.login_message_category = "info"


def create_app():
    app = Flask(__name__)

    # ✅ SECRET KEY
    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "d0782e15d02562e8c563941487976982645ae44644e687a3881503c468f17709"
    )

    # ✅ DATABASE URL (PostgreSQL)
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ INIT EXTENSIONS
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        _ensure_revision_count_column()

    # ✅ ROUTES
    from bookmark.routes import routes
    app.register_blueprint(routes)

    return app


def _ensure_revision_count_column():
    inspector = inspect(db.engine)
    if "questions" not in inspector.get_table_names():
        return

    columns = {col["name"] for col in inspector.get_columns("questions")}
    if "revision_count" in columns:
        return

    db.session.execute(
        text("ALTER TABLE questions ADD COLUMN revision_count INTEGER NOT NULL DEFAULT 0")
    )
    db.session.execute(
        text("UPDATE questions SET revision_count = CASE WHEN is_revised THEN 1 ELSE 0 END")
    )
    db.session.commit()
