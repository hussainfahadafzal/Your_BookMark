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

    # ✅ Connection pool settings — required for Neon (serverless Postgres)
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,       # test connection before using it
        "pool_recycle": 300,         # recycle connections every 5 mins
        "connect_args": {
            "sslmode": "require"     # Neon requires SSL
        }
    }

    # ✅ INIT EXTENSIONS
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # ✅ ROUTES (register before app_context so models are imported)
    from bookmark.routes import routes
    app.register_blueprint(routes)

    with app.app_context():
        db.create_all()                    # ✅ Create tables if they don't exist
        _ensure_revision_count_column()    # ✅ Add revision_count if missing

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