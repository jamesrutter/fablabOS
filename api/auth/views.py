from flask import g, request, session, make_response, current_app
from flask.typing import ResponseReturnValue
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import BadRequestKeyError
from sqlite3 import Row, Connection, DatabaseError
from api.db import get_db
from api.auth.decorators import login_required
from . import auth

################################
### Authentication Endpoints ###
################################

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
        current_app.logger.debug(
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
            f"AUTH >> User {username} attempted to log in with an invalid username or password.")
        return make_response({"error": "Invalid username or password."}, 401)
    session.clear()
    if user:
        session['user_id'] = user['id']
        current_app.logger.debug(
            f"AUTH >> User: {username} successfully logged in.")
    return make_response({"message": "Successfully logged in."}, 200)


@auth.post(rule='/logout')
def logout():
    if g.user is None:
        current_app.logger.error(
            f"User attempted to log out without logging in.")
        return make_response({"error": "You must be logged in to log out."}, 401)
    session.clear()
    current_app.logger.debug(
        f"User logged out.")
    return make_response({"message": "Successfully logged out."}, 200)


@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()


@auth.after_app_request
def log_session_data(response):
    current_app.logger.debug(
        f"AUTH >> Active User: {session.get('user_id')}")
    current_app.logger.debug(
        f"AUTH >> Session Modified?: {session.modified}")
    return response


###########################
### User CRUD Endpoints ###
###########################

@auth.get('/users')
@login_required
def get_users() -> ResponseReturnValue:
    """
    Retrieve a list of all users from the database.

    This endpoint fetches all user records from the database and returns them 
    as a list of JSON objects. Each object represents a user with all their details.

    Returns:
        Response: A JSON list of all users. Each user is a dictionary 
        containing user details. If no users are found, an empty list is returned.
    """
    try:
        db: Connection = get_db()

        # Select all users from the database, returns as a list of SQlite Row objects.
        user_rows: list[Row] = db.execute(
            'SELECT * FROM user').fetchall()

        # Convert the list of SQlite Row objects to a list of dictionaries, which can be serialized to JSON.
        return {'status': 'success', 'data': [dict(row) for row in user_rows]}, 200
    except DatabaseError as e:
        return {'status': 'error', 'message': e.args[0]}, 500


@auth.get('/users/<int:id>')
@login_required
def user_detail() -> ResponseReturnValue:
    """
    Retrieve a single user from the database.

    This endpoint fetches a single user record from the database and returns it 
    as a JSON object. The object represents a user with all their details.

    Args:
        id (int): The ID of the user to retrieve.

    Returns:
        Response: A JSON object representing the user. If no user is found, 
        an error message with a 404 status code is returned.
    """
    try:
        db: Connection = get_db()

        # Select the user from the database, returns as a SQlite Row object.
        user_row: Row = db.execute(
            'SELECT * FROM user WHERE id = ?', (id,)
        ).fetchone()

        if user_row is None:
            return {'status': 'error', 'message': 'User not found.'}, 404

        # Convert the SQlite Row object to a dictionary, which can be serialized to JSON.
        return {'status': 'success', 'data': dict(user_row)}, 200
    except DatabaseError as e:
        return {'status': 'error', 'message': e.args[0]}, 500


@auth.post('/users')
@login_required
def update_user(id: int, **kwargs) -> ResponseReturnValue:
    """
    Update a single user in the database.

    This endpoint updates a single user record in the database and returns it 
    as a JSON object. The object represents a user with all their details.

    Args:
        id (int): The ID of the user to update.
        username (str): The username of the user.
        password (str): The password of the user.
        role (str): The role of the user.

    Returns:
        Response: A JSON object representing the user. If no user is found, 
        an error message with a 404 status code is returned.
    """
    try:
        db: Connection = get_db()

        # Select the user from the database, returns as a SQlite Row object.
        user_row: Row = db.execute(
            'SELECT * FROM user WHERE id = ?', (id,)
        ).fetchone()

        if user_row is None:
            return {'status': 'error', 'message': 'User not found.'}, 404

        # Convert the SQlite Row object to a dictionary, which can be serialized to JSON.
        return {'status': 'success', 'data': dict(user_row)}, 200
    except DatabaseError as e:
        return {'status': 'error', 'message': e.args[0]}, 500


@auth.delete('/users/<int:id>')
@login_required
def delete_user(id: int):
    """
    Delete a single user from the database.

    This endpoint deletes a single user record from the database and returns it 
    as a JSON object. The object represents a user with all their details.

    Args:
        id (int): The ID of the user to delete.

    Returns:
        Response: A JSON object representing the user. If no user is found, 
        an error message with a 404 status code is returned.
    """
    try:
        db: Connection = get_db()

        # Select the user from the database, returns as a SQlite Row object.
        user_row: Row = db.execute(
            'SELECT * FROM user WHERE id = ?', (id,)
        ).fetchone()

        if user_row is None:
            return {'status': 'error', 'message': 'User not found.'}, 404

        # Convert the SQlite Row object to a dictionary, which can be serialized to JSON.
        return {'status': 'success', 'data': dict(user_row)}, 200
    except DatabaseError as e:
        return {'status': 'error', 'message': e.args[0]}, 500
