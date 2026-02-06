from flask import Blueprint, render_template, redirect, url_for, flash, request
from sqlalchemy import func
from flask_login import login_user, logout_user, login_required, current_user

from bookmark import db, bcrypt
from bookmark.models import User, Topic, Question
from bookmark.forms import RegisterForm, LoginForm, TopicForm, QuestionForm

routes = Blueprint("routes", __name__)


@routes.route("/")
@login_required
def dashboard():
    total_topics = Topic.query.filter_by(user_id=current_user.id).count()
    total_questions = (
        Question.query.join(Topic)
        .filter(Topic.user_id == current_user.id)
        .count()
    )
    pending_questions = (
        Question.query.join(Topic)
        .filter(Topic.user_id == current_user.id, Question.is_revised.is_(False))
        .count()
    )
    return render_template(
        "dashboard.html",
        total_topics=total_topics,
        total_questions=total_questions,
        pending_questions=pending_questions
    )


@routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("routes.dashboard"))

        flash("Invalid credentials", "danger")

    return render_template("login.html", form=form)


@routes.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("routes.dashboard"))
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf-8")

        user = User(
            email=form.email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash("Account created", "success")
        return redirect(url_for("routes.login"))

    return render_template("register.html", form=form)



@routes.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.login"))


@routes.route("/topics")
@login_required
def topics():
    topics = (
        db.session.query(Topic, func.count(Question.id).label("question_count"))
        .outerjoin(Question, Topic.id == Question.topic_id)
        .filter(Topic.user_id == current_user.id)
        .group_by(Topic.id)
        .all()
    )
    topic_items = []
    for topic, question_count in topics:
        topic.question_count = question_count
        topic_items.append(topic)
    topics = topic_items
    return render_template("topics.html", topics=topics)


@routes.route("/topic/add", methods=["GET", "POST"])
@login_required
def add_topic():
    form = TopicForm()

    if form.validate_on_submit():
        topic = Topic(name=form.name.data, user=current_user)
        db.session.add(topic)
        db.session.commit()
        flash("Topic created successfully.", "success")
        return redirect(url_for("routes.topics"))

    if request.method == "POST":
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "danger")

    return render_template("add_topic.html", form=form)


@routes.route("/topic/<int:topic_id>")
@login_required
def questions(topic_id):
    topic = Topic.query.filter_by(id=topic_id, user_id=current_user.id).first_or_404()
    difficulty = request.args.get("difficulty", "")
    search = request.args.get("search", "")

    questions_query = Question.query.filter_by(topic_id=topic.id)
    if difficulty:
        questions_query = questions_query.filter_by(difficulty=difficulty)
    if search:
        questions_query = questions_query.filter(Question.title.ilike(f"%{search}%"))

    questions = questions_query.order_by(Question.created_at.desc()).all()
    return render_template(
        "questions.html",
        topic=topic,
        questions=questions,
        selected_difficulty=difficulty,
        search_query=search
    )


@routes.route("/question/<int:question_id>/toggle", methods=["POST"])
@login_required
def toggle_question(question_id):
    question = (
        Question.query.join(Topic)
        .filter(Question.id == question_id, Topic.user_id == current_user.id)
        .first_or_404()
    )
    payload = request.get_json(silent=True) or {}
    is_revised = payload.get("is_revised")
    if is_revised is None:
        form_value = request.form.get("is_revised", "")
        is_revised = form_value.lower() in {"true", "1", "yes", "on"}
    question.is_revised = bool(is_revised)
    db.session.commit()
    return ("", 204)


@routes.route("/question/add/<int:topic_id>", methods=["GET", "POST"])
@login_required
def add_question(topic_id):
    form = QuestionForm()
    topic = Topic.query.filter_by(id=topic_id, user_id=current_user.id).first_or_404()

    if form.validate_on_submit():
        q = Question(
            title=form.title.data,
            link=form.link.data,
            difficulty=form.difficulty.data,
            mistake=form.mistake.data,
            takeaway=form.takeaway.data,
            is_revised=form.is_revised.data,
            topic=topic
        )
        db.session.add(q)
        db.session.commit()
        flash("Question added successfully.", "success")
        return redirect(url_for("routes.questions", topic_id=topic.id))

    if request.method == "POST":
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "danger")

    return render_template("add_question.html", form=form)


@routes.route("/question/<int:question_id>/delete", methods=["POST"])
@login_required
def delete_question(question_id):
    question = (
        Question.query.join(Topic)
        .filter(Question.id == question_id, Topic.user_id == current_user.id)
        .first_or_404()
    )
    topic_id = question.topic_id
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted successfully.", "success")
    return redirect(url_for("routes.questions", topic_id=topic_id))


@routes.route("/topic/<int:topic_id>/delete", methods=["POST"])
@login_required
def delete_topic(topic_id):
    topic = Topic.query.filter_by(id=topic_id, user_id=current_user.id).first_or_404()
    db.session.delete(topic)
    db.session.commit()
    flash("Topic deleted successfully.", "success")
    return redirect(url_for("routes.topics"))


@routes.route("/account")
@login_required
def account():
    return render_template("account.html")