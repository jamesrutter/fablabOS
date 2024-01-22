import os
import tempfile
import pytest
from api import create_app
from api.db import get_db, init_db
from flask.testing import FlaskClient

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,  # could also do 'sqlite:///:memory:'
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def register_user(self, username='test_user', password='test', role='user'):
        return self._client.post(
            '/auth/register',
            data={'username': username, 'password': password, 'role': role}
        )
    def register_admin(self, username='test_admin', password='test', role='admin'):
        return self._client.post(
            '/auth/register',
            data={'username': username, 'password': password, 'role': role}
        )

    def login_user(self, username='test_user', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )
    
    def login_admin(self, username='test_admin', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.post('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)

