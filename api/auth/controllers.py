from flask import current_app, Request
from sqlalchemy.orm import joinedload
from sqlalchemy import select, ScalarResult
from sqlalchemy.exc import SQLAlchemyError
from api.models import User
from api.database import db_session
from typing import Sequence
from api.models import User, UserRole, Role
from werkzeug.security import generate_password_hash


#############################
## USER CRUD FUNCTIONS ##
#############################

def get_users() -> Sequence[UserRole]:
    """Fetch all complete user records from the database.

    Returns:
        Sequence[UserRole]: A list of UserRole objects which contains Users and Roles. 
    """
    stmt = select(UserRole)
    try:
        users = db_session.execute(stmt).scalars().all()
        return users
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error fetching users: {e}")
        return []


def get_user(id: int) -> UserRole | None:
    """Fetch a single user from the database by id.

    Args:
        id (int): The id of the user to fetch.

    Returns:
        User | None: A UserRole object which contains a User and a Role.
    """
    stmt = select(UserRole).where(UserRole.id == id)
    try:
        user = db_session.execute(stmt).scalar()
        return user
    except SQLAlchemyError as e:
        current_app.logger.error(f"Error fetching user: {e}")
        return None


def create_user(request: Request) -> tuple[UserRole | None, str | None]:
    error = None
    # Extract data from request
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    role = request.form.get('role', 'user')

    # Check if user already exists
    stmt = select(User).where(User.username == username)
    if db_session.execute(stmt).one_or_none():
        error = "User already registered. Please specify a different username."
        return None, error

    # Check that username and password are not empty
    if not password or not username:
        error = "A username and password are required!"
        return None, error

    # Hash password
    hashed_password = generate_password_hash(password)

    # Create user and add to database session
    user = User(username=username, password=hashed_password, email=email)
    role = db_session.execute(select(Role).where(Role.id == role)).scalar_one()
    u = UserRole(user=user, role=role)
    db_session.add(u)

    # Commit changes to database
    db_session.commit()

    return u, None


def update_user(id: int, request) -> tuple[User | None, str | None]:
    error = None
    try:
        # Fetch the user to be updated (u)
        u = db_session.execute(select(UserRole).filter_by(id=id)).scalar_one()

        if u is None:
            error = "User not found."
            return None, error

        # Get current user data
        current_username = u.user.username
        current_email = u.user.email
        current_role = u.role.id

        # Update user details with partial data from the request
        updated_username = request.form.get('username', current_username)
        updated_email = request.form.get('email', current_email)
        updated_role = request.form.get('role', current_role)

        # Update the user model with the new data
        u.user.username = updated_username
        u.user.email = updated_email
        u.role.id = updated_role

        # Commit changes to database
        db_session.commit()

        return u, None

    except SQLAlchemyError as e:
        db_session.rollback()
        current_app.logger.error(f"Error updating user: {e}")
        return None, str(e)


def delete_user(id: int):
    try:
        # Fetch the user to be deleted
        stmt = select(User).where(User.id == id)
        u = db_session.execute(stmt).scalar()

        if u is None:
            return False, "User not found."

        # Delete the user
        db_session.delete(u)
        db_session.commit()

        return True, None
    except SQLAlchemyError as e:
        db_session.rollback()
        current_app.logger.error(f"Error deleting user: {e}")
        return False, str(e)
