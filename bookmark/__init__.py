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

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        "d0782e15d02562e8c563941487976982645ae44644e687a3881503c468f17709",
    )

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "connect_args": {"sslmode": "require"},
    }

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from bookmark.routes import routes
    app.register_blueprint(routes)

    with app.app_context():
        db.create_all()
        _migrate_columns()

    return app


def _migrate_columns():
    """Add any missing columns introduced in new versions — safe to run repeatedly."""
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    # ── questions table ────────────────────────────────────────
    if "questions" in tables:
        existing = {col["name"] for col in inspector.get_columns("questions")}

        migrations = [
            # (column_name, DDL_type, default_expression)
            ("revision_count",  "INTEGER NOT NULL DEFAULT 0",    None),
            ("platform",        "VARCHAR(30) NOT NULL DEFAULT ''", None),
            ("approach",        "VARCHAR(50) NOT NULL DEFAULT ''", None),
            ("time_complexity",  "VARCHAR(30) NOT NULL DEFAULT ''", None),
            ("space_complexity", "VARCHAR(30) NOT NULL DEFAULT ''", None),
        ]

        for col, ddl, _ in migrations:
            if col not in existing:
                db.session.execute(
                    text(f"ALTER TABLE questions ADD COLUMN {col} {ddl}")
                )

        # Back-fill revision_count from is_revised if needed
        if "revision_count" not in existing and "is_revised" in existing:
            db.session.execute(
                text(
                    "UPDATE questions SET revision_count = "
                    "CASE WHEN is_revised THEN 1 ELSE 0 END"
                )
            )

        db.session.commit()

    # ── topics table ───────────────────────────────────────────
    if "topics" in tables:
        existing = {col["name"] for col in inspector.get_columns("topics")}

        if "description" not in existing:
            db.session.execute(
                text("ALTER TABLE topics ADD COLUMN description VARCHAR(300) NOT NULL DEFAULT ''")
            )
            db.session.commit()