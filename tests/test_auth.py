import pytest
from flask import g, session
from api.db import get_db


def test_register(client, auth, app):
    """Test that a user can register."""
    # Successful registration
    response = client.post(
        '/auth/register', data={'username': 'newuser', 'password': 'newpass', 'role': 'user'})
    assert response.status_code == 200
    assert b"Successfully registered." in response.data

    # Check database state to ensure integrity of data after registration.
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'newuser'",
        ).fetchone() is not None

    # Attempt to register with an existing username
    response = client.post(
        '/auth/register', data={'username': 'newuser', 'password': 'newpass2', 'role': 'user'})
    assert response.status_code == 400
    assert b"User already registered." in response.data

    # Attempt to register user with the test auth fixture
    response = auth.register_user()
    assert response.status_code == 200
    assert b"Successfully registered." in response.data

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'test_user'",
        ).fetchone() is not None
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'test_user' AND role = 'user'").fetchone() is not None
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'test_user' AND role = 'admin'").fetchone() is None

    # Attempt to register admin with the test auth fixture
    response = auth.register_admin()
    assert response.status_code == 200
    assert b"Successfully registered." in response.data

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'test_admin'",
        ).fetchone() is not None
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'test_admin' AND role = 'admin'").fetchone() is not None
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'test_admin' AND role = 'user'").fetchone() is None

    # Attempt to register with incomplete data
    response = client.post(
        '/auth/register', data={'username': 'newuser2', 'password': ''})
    assert response.status_code == 400


def test_login(client, app, auth):
    """Test that a user can login."""

    # Register a user
    response = auth.register_user()

    # Successful login
    response = auth.login_user()
    assert response.status_code == 200
    assert b"Successfully logged in." in response.data

    with client:
        client.get('/users')
        with app.app_context():
            assert session.get('user_id') == 3 # app fixture creates 2 users by default, so any new user in a test will be the 3rd user
            # assert g.user['username'] == 'test_user' #TODO: Fix this test

    # Attempt to login with an invalid username
    response = auth.login_user('invalid', 'test')
    assert response.status_code == 401
    assert b"Invalid username or password." in response.data

    # Attempt to login with an invalid password
    response = auth.login_user('test', 'invalid')
    assert response.status_code == 401
    assert b"Invalid username or password." in response.data

    # Check if user_id is stored in session after successful login
    with client:
        client.post('/auth/login',
                    data={'username': 'testuser', 'password': 'testpass'})
        with app.app_context():
            assert session.get('user_id') is not None


def test_logout(client, auth, app):
    """Test that a user can logout."""
    # Register and login a user
    auth.register_user()
    auth.login_user()

    # Logout a user
    response = auth.logout()
    assert response.status_code == 200
    assert b"Successfully logged out." in response.data

    # Check if user_id is removed from session after successful logout
    with client:
        client.get('/')  # Make a simple request to check session state
        with app.app_context():
            assert session.get('user_id') is None

    # Attempt to logout without logging in
    response = auth.logout()
    assert response.status_code == 401
    assert b"You must be logged in to log out." in response.data


@pytest.mark.parametrize(('username', 'password', 'role', 'message'), (
    ('', '', '', b'Username, password, and role are required.'),
    ('test', '', '', b'Username, password, and role are required.'),
    ('test', 'test', '', b'Username, password, and role are required.'),
))
def test_register_validate_input(client, username, password, role, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password, 'role': role}
    )
    assert message in response.data
