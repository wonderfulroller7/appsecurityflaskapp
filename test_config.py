import os
import pytest
import database

class Authentication(object):

    def __init__(self, client):
        self._client = client

    def login():
        return self._client.post('/login',
                data={'uname': username, 'pword': password, '2fa': twofa},
                follow_redirects=True)

    def logout():
        return self._client.get('/logout')

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def app():
    
    app = create_app({
        'TEST': True
    })

    with app.app_context():
        init_db()

    yield app

    os.close()
    os.unlink()


