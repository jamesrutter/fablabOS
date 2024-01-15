import functools
from flask import (
    Blueprint, g, request, session
)
from werkzeug.security import check_password_hash, generate_password_hash
from schedulr.db import get_db

bp = Blueprint(name='auth', import_name=__name__, url_prefix='/auth')


@bp.route(rule='/register', methods=(['POST']))
def register():
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    if not username or not password or not role:
        return {
            "message": "Username, password and role are required.",
            "status": 400
        }

    db = get_db()

    try:
        db.execute(
            "INSERT INTO user (username, password, role) VALUES (?, ?, ?)",
            (username, generate_password_hash(password=password), role),
        )
        db.commit()
    except db.IntegrityError:
        return {
            "message": f'User {username} is already registered.',
            "status": 400
        }
    return {
        "message": f'{username} successfully registered.',
        "status": 200
    }


@bp.route(rule='/login', methods=(['POST']))
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()

    if user is None or not check_password_hash(pwhash=user['password'], password=password):
        return {
            "message": "Incorrect username or password.",
            "status": 401
        }
    session.clear()
    if user:
        session['user_id'] = user['id']
    return {
        "message": f'{username} successfully logged in.',
        "status": 200
    }


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
    return {
        "message": "Successfully logged out.",
        "status": 200
    }


def login_required(view):
    @functools.wraps(wrapped=view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return {
                "message": "You must be logged in to access this page.",
                "status": 401
            }

        return view(**kwargs)

    return wrapped_view
