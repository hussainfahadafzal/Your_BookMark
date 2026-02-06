from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField,
    BooleanField
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from bookmark.models import User


# ---------------------------
# REGISTER FORM
# ---------------------------
class RegisterForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match.")
        ]
    )

    submit = SubmitField("Create Account")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already registered.")


# ---------------------------
# LOGIN FORM
# ---------------------------
class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")


# ---------------------------
# TOPIC FORM
# ---------------------------
class TopicForm(FlaskForm):
    name = StringField(
        "Topic Name",
        validators=[DataRequired()]
    )

    submit = SubmitField("Save Topic")


# ---------------------------
# QUESTION FORM
# ---------------------------
class QuestionForm(FlaskForm):
    title = StringField(
        "Question Title",
        validators=[DataRequired()]
    )

    link = StringField(
        "Problem Link",
        validators=[DataRequired()]
    )

    difficulty = SelectField(
        "Difficulty",
        choices=[
            ("Easy", "Easy"),
            ("Medium", "Medium"),
            ("Hard", "Hard")
        ],
        validators=[DataRequired()]
    )

    mistake = TextAreaField("What I did wrong")
    takeaway = TextAreaField("What to remember next time")

    is_revised = BooleanField("Mark as revised")

    submit = SubmitField("Save Question")
