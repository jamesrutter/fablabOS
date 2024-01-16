import functools
from flask import Blueprint, g, request, session, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import BadRequestKeyError
from schedulr.db import get_db

bp = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')


@bp.route(rule='/register', methods=(['POST']))
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
    except db.IntegrityError:
        return make_response(
            {"error": "User already registered. Please specify a different username."}, 400)
    return make_response({"message": "Successfully registered."}, 200)


@bp.route(rule='/login', methods=(['POST']))
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None or not check_password_hash(pwhash=user['password'], password=password):
        return make_response({"error": "Invalid username or password."}, 401)
    session.clear()
    if user:
        session['user_id'] = user['id']
    return make_response({"message": "Successfully logged in."}, 200)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()


@bp.route(rule='/logout')
def logout():
    session.clear()
    return make_response({"message": "Successfully logged out."}, 200)


def login_required(view):
    @functools.wraps(wrapped=view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return make_response(
                {"error": "You must be logged in to access this page."}, 401)

        return view(**kwargs)

    return wrapped_view
