import functools
from flask import g, make_response, abort, current_app
from api.db import get_db


def login_required(view):
    """This decorator checks if a user is logged in before allowing them to access a view."""
    @functools.wraps(wrapped=view)
    def wrapped_view(**kwargs):
        if g.user is None:
            current_app.logger.error(
                f"User attempted to access a protected resource without logging in.")
            return make_response(
                {"error": "You must be logged in to access this page."}, 401)

        return view(**kwargs)

    return wrapped_view


def owner_required(view):
    """This decorator checks if the user making a request is the owner of the reservation
    they are trying to modify. If the user is not the owner, a 401 error is returned."""
    @functools.wraps(wrapped=view)
    def wrapped_view(**kwargs):
        db = get_db()
        reservation_id = kwargs.get('id')
        reservation = db.execute(
            "SELECT * FROM reservation WHERE id = ?", (reservation_id,)).fetchone()
        if reservation is None:
            current_app.logger.error(
                f"User {g.user['username']} attempted to modify a reservation that does not exist.")
            abort(404, description="Reservation not found.")

        # Assuming user_id is stored in g after authentication
        user_id = g.user['id']

        if reservation['user_id'] != user_id:
            current_app.logger.error(
                f"User {g.user['username']} attempted to modify a reservation they do not own.")
            abort(401, description='You must be the owner of a reservation to modify it.')

        return view(**kwargs)

    return wrapped_view


def admin_required(view):
    """This decorator checks if the user making a request is an admin. If the user is not an admin,
    a 401 error is returned."""
    @functools.wraps(wrapped=view)
    def wrapped_view(**kwargs):
        if g.user['role'] != 'admin':
            current_app.logger.error(
                f"User {g.user['username']} attempted to access admin resource.")
            abort(401, description='You must be an admin to access this resource.')

        return view(**kwargs)

    return wrapped_view
