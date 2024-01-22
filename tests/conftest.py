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
        'DATABASE': db_path, # could also do 'sqlite:///:memory:'
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

# TO DO: Add authentication headers fixture for testing authenticated endpoints
# @pytest.fixture(scope='module')
# def auth_headers(client):
#     """Get authentication headers."""
#     response = client.post('/auth/login', data={
#         'username': 'admin',
#         'password': 'admin'
#     })
#     assert response.status_code == 200
#     assert isinstance(response.json, dict)
#     assert 'access_token' in response.json
#     assert 'refresh_token' in response.json
#     return {
#         'Authorization': 'Bearer {}'.format(response.json['access_token'])
#     }