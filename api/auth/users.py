from flask import Blueprint, request, abort
from flask.typing import ResponseReturnValue
from sqlite3 import Row, Connection, DatabaseError, Cursor
from schedulr.db import get_db
from schedulr.auth import login_required


def create_users_bp():

    bp = Blueprint(name='users', import_name=__name__, url_prefix='/users')

    @bp.route(rule='/', methods=(['GET']))
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

    @bp.route(rule='/<int:id>', methods=(['GET']))
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
            user_row: Cursor = db.execute(
                'SELECT * FROM user WHERE id = ?', (id,)
            ).fetchone()

            if user_row is None:
                return {'status': 'error', 'message': 'User not found.'}, 404

            # Convert the SQlite Row object to a dictionary, which can be serialized to JSON.
            return {'status': 'success', 'data': dict(user_row)}, 200
        except DatabaseError as e:
            return {'status': 'error', 'message': e.args[0]}, 500

    @bp.route(rule='/', methods=(['PUT']))
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

    @bp.route(rule='/', methods=(['DELETE']))
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
    return bp


users_bp = create_users_bp()
