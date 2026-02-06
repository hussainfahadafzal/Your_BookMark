from datetime import datetime
from bookmark import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    topics = db.relationship("Topic", backref="user", lazy=True)


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    questions = db.relationship(
        "Question",
        backref="topic",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(300), nullable=False)

    difficulty = db.Column(db.String(10), nullable=False)
    mistake = db.Column(db.Text)
    takeaway = db.Column(db.Text)

    is_revised = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id"), nullable=False)