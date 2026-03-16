from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    NumberRange,
    URL,
    Optional,
    ValidationError,
)
from bookmark.models import User


# ──────────────────────────────────────────────
# REGISTER FORM
# ──────────────────────────────────────────────
class RegisterForm(FlaskForm):
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Enter a valid email address."),
            Length(max=120, message="Email must be under 120 characters."),
        ],
        description="We'll never share your email with anyone.",
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
            Length(min=8, max=64, message="Password must be between 8 and 64 characters."),
        ],
        description="At least 8 characters.",
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo("password", message="Passwords do not match."),
        ],
    )

    submit = SubmitField("Create Account")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.strip().lower()).first()
        if user:
            raise ValidationError("This email is already registered. Please log in.")

    def validate_password(self, password):
        pw = password.data
        if pw and not any(c.isdigit() for c in pw):
            raise ValidationError("Password must contain at least one number.")
        if pw and not any(c.isalpha() for c in pw):
            raise ValidationError("Password must contain at least one letter.")


# ──────────────────────────────────────────────
# LOGIN FORM
# ──────────────────────────────────────────────
class LoginForm(FlaskForm):
    email = StringField(
        "Email Address",
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Enter a valid email address."),
            Length(max=120),
        ],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
            Length(min=1, max=64),
        ],
    )

    submit = SubmitField("Sign In")


# ──────────────────────────────────────────────
# TOPIC FORM
# ──────────────────────────────────────────────
class TopicForm(FlaskForm):
    name = StringField(
        "Topic Name",
        validators=[
            DataRequired(message="Topic name is required."),
            Length(min=2, max=50, message="Topic name must be between 2 and 50 characters."),
        ],
        description="e.g. Arrays, Graph Algorithms, System Design",
    )

    description = TextAreaField(
        "Description",
        validators=[
            Optional(),
            Length(max=300, message="Description must be under 300 characters."),
        ],
        description="Optional — briefly describe what this topic covers.",
    )

    submit = SubmitField("Save Topic")


# ──────────────────────────────────────────────
# QUESTION FORM
# ──────────────────────────────────────────────
class QuestionForm(FlaskForm):
    title = StringField(
        "Question Title",
        validators=[
            DataRequired(message="Question title is required."),
            Length(min=2, max=200, message="Title must be between 2 and 200 characters."),
        ],
        description="e.g. Two Sum, Longest Substring Without Repeating Characters",
    )

    link = StringField(
        "Problem Link",
        validators=[
            DataRequired(message="Problem link is required."),
            URL(message="Enter a valid URL (include https://)."),
            Length(max=500, message="URL must be under 500 characters."),
        ],
        description="Paste the full LeetCode / GFG / Codeforces URL.",
    )

    difficulty = SelectField(
        "Difficulty",
        choices=[
            ("", "— Select Difficulty —"),
            ("Easy", "Easy"),
            ("Medium", "Medium"),
            ("Hard", "Hard"),
        ],
        validators=[DataRequired(message="Please select a difficulty level.")],
        default="",
    )

    platform = SelectField(
        "Platform",
        choices=[
            ("", "— Select Platform —"),
            ("LeetCode", "LeetCode"),
            ("GeeksforGeeks", "GeeksforGeeks"),
            ("Codeforces", "Codeforces"),
            ("HackerRank", "HackerRank"),
            ("InterviewBit", "InterviewBit"),
            ("Other", "Other"),
        ],
        default="",
        validators=[Optional()],
        description="Where is this problem from?",
    )

    time_complexity = StringField(
        "Time Complexity",
        validators=[
            Optional(),
            Length(max=30, message="Keep it short, e.g. O(n log n)."),
        ],
        description="e.g. O(n), O(n log n), O(n²)",
    )

    space_complexity = StringField(
        "Space Complexity",
        validators=[
            Optional(),
            Length(max=30, message="Keep it short, e.g. O(n)."),
        ],
        description="e.g. O(1), O(n)",
    )

    approach = SelectField(
        "Approach / Pattern",
        choices=[
            ("", "— Select Pattern —"),
            ("Two Pointers", "Two Pointers"),
            ("Sliding Window", "Sliding Window"),
            ("Binary Search", "Binary Search"),
            ("BFS", "BFS"),
            ("DFS", "DFS"),
            ("Dynamic Programming", "Dynamic Programming"),
            ("Greedy", "Greedy"),
            ("Backtracking", "Backtracking"),
            ("HashMap / HashSet", "HashMap / HashSet"),
            ("Stack / Queue", "Stack / Queue"),
            ("Heap / Priority Queue", "Heap / Priority Queue"),
            ("Trie", "Trie"),
            ("Union Find", "Union Find"),
            ("Divide & Conquer", "Divide & Conquer"),
            ("Bit Manipulation", "Bit Manipulation"),
            ("Math", "Math"),
            ("Other", "Other"),
        ],
        default="",
        validators=[Optional()],
        description="What algorithmic pattern does this problem use?",
    )

    mistake = TextAreaField(
        "What I Did Wrong",
        validators=[
            Optional(),
            Length(max=1000, message="Keep this under 1000 characters."),
        ],
        description="Be specific — what tripped you up the first time?",
    )

    takeaway = TextAreaField(
        "Key Takeaway",
        validators=[
            Optional(),
            Length(max=1000, message="Keep this under 1000 characters."),
        ],
        description="The one thing you must remember for next time.",
    )

    revision_count = IntegerField(
        "Revision Count",
        default=0,
        validators=[
            NumberRange(min=0, max=999, message="Revision count must be between 0 and 999."),
        ],
        description="How many times have you revised this problem?",
    )

    submit = SubmitField("Save Question")

    def validate_difficulty(self, difficulty):
        if not difficulty.data:
            raise ValidationError("Please select a difficulty level.")