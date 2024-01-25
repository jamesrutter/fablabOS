import functools
from flask import g, make_response, abort, current_app
from api.database import db_session
from api.models import Reservation
from sqlalchemy import select


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
    """Check if the user making a request is the owner of the reservation they are trying to modify."""
    @functools.wraps(wrapped=view)
    def wrapped_view(**kwargs):
        reservation_id = kwargs.get('id')
        stmt = select(Reservation).where(Reservation.id == reservation_id)
        result = db_session.execute(stmt).scalar()

        if result is None:
            current_app.logger.error(f"User {g.user.username} attempted to modify a reservation that does not exist.")
            abort(404, description="Reservation not found.")

        # Assuming user_id is stored in g after authentication
        user_id = g.user.id

        if result.user_id != user_id:
            current_app.logger.error(f"User {g.user.username} attempted to modify a reservation they do not own.")
            abort(401, description='You must be the owner of a reservation to modify it.')

        return view(**kwargs)

    return wrapped_view

def admin_required(view):
    """Check if the user making a request is an admin."""
    @functools.wraps(wrapped=view)
    def wrapped_view(**kwargs):
        # Assuming role is a direct attribute of g.user, and g.user is an instance of User
        if 'admin' not in [role.name for role in g.user.roles]:
            current_app.logger.error(f"User {g.user.username} attempted to access admin resource.")
            abort(401, description='You must be an admin to access this resource.')

        return view(**kwargs)

    return wrapped_view