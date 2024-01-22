from flask import g, request, session, make_response, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import BadRequestKeyError
from api.db import get_db
from . import auth


@auth.post('/register')
def register():
    try:
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
    except BadRequestKeyError as e:
        return make_response(
            {"error": f"{e.description}",
                "hint": f"Check the following parameter: {e.args[0]}"}, 400)

    if not username or not password or not role:
        return make_response(
            {"error": "Username, password, and role are required."}, 400)

    db = get_db()

    try:
        db.execute(
            "INSERT INTO user (username, password, role) VALUES (?, ?, ?)",
            (username, generate_password_hash(password=password), role),
        )
        db.commit()
        current_app.logger.info(
            f"User {username} successfully registered.")
    except db.IntegrityError:
        current_app.logger.error(
            f"User {username} attempted to register with a username that already exists.")
        return make_response(
            {"error": "User already registered. Please specify a different username."}, 400)
    return make_response({"message": "Successfully registered."}, 200)


@auth.post('/login')
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None or not check_password_hash(pwhash=user['password'], password=password):
        current_app.logger.error(
            f"User {username} attempted to log in with an invalid username or password.")
        return make_response({"error": "Invalid username or password."}, 401)
    session.clear()
    if user:
        session['user_id'] = user['id']
        current_app.logger.info(
            f"User: {username} successfully logged in.")
    return make_response({"message": "Successfully logged in."}, 200)


@auth.before_app_request
def load_logged_in_user():
    current_app.logger.info('NEW REQUEST')
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()


@auth.after_app_request
def log_session_data(response):
    current_app.logger.info(
        f"Active User: {session.get('user_id')}")
    current_app.logger.info(
        f"Session Modified?: {session.modified}")
    return response


@auth.post(rule='/logout')
def logout():
    if g.user is None:
        current_app.logger.error(
            f"User attempted to log out without logging in.")
        return make_response({"error": "You must be logged in to log out."}, 401)
    session.clear()
    current_app.logger.info(
        f"User logged out.")
    return make_response({"message": "Successfully logged out."}, 200)

