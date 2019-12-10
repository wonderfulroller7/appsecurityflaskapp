import os
from app import create_app
import pytest
import database

class Authentication(object):

    def __init__(self, client):
        self._client = client

    def login(self, username='sourbose', password='potato123', tfa='9292197847'):
        return self._client.post('/login',
                data={'uname': username, 'pword': password, '2fa': tfa},
                follow_redirects=True)

    def login_admin(self, username='admin', password='Administrator@1', tfa='12345678901'):
        return self._client.post('/login',
                data={'uname': username, 'pword': password, '2fa': tfa},
                follow_redirects=True)

    def logout(self):
        return self._client.get('/logout')

@pytest.fixture
def app():
    
    app = create_app()

    with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'rb') as f:
        _data_sql = f.read().decode('utf8')

    with app.app_context():
        database.init_db()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()