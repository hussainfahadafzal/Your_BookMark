from datetime import datetime
from bookmark import db, login_manager
from flask_login import UserMixin


# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =======================
# User Model
# =======================
class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    topics = db.relationship(
        "Topic",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


# =======================
# Topic Model
# =======================
class Topic(db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    questions = db.relationship(
        "Question",
        backref="topic",
        lazy=True,
        cascade="all, delete-orphan"
    )


# =======================
# Question Model
# =======================
class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(300), nullable=False)

    difficulty = db.Column(db.String(10), nullable=False)
    mistake = db.Column(db.Text)
    takeaway = db.Column(db.Text)

    is_revised = db.Column(db.Boolean, default=False)
    revision_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    topic_id = db.Column(
        db.Integer,
        db.ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False
    )
