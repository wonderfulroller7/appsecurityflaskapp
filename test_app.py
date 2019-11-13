import pytest
from flask import g, session
import database

def test_registration_get(client, app):
    assert client.get('/register').status_code == 200

def test_registration_post(client, app):
    client.post('/register', data = {'uname': 'sourbose', 'pword': 'test123', '2fa': '9292197847'})
    with app.app_context():
        assert database.get_db().execute(
            "SELECT * FROM user WHERE uname = 'sourbose'"
        ).fetchone() is not None

def test_login_get(client, app):
    assert client.get('/login').status_code == 200

def test_login_post(client, app):
    client.post('/register', data = {'uname': 'sourbose', 'pword': 'test123', '2fa': '9292197847'})
    client.post('/login', data = {'uname': 'sourbose', 'pword': 'test123', '2fa': '9292197847'})
    with client:
        assert client.get('/login').status_code == 302
        assert client.get('/spell_check').status_code == 200
        assert g.user['uname'] == 'sourbose'
        
def test_csrf(client, app):
    client.post('/register', data = {'uname': 'sourbose', 'pword': 'test123', '2fa': '9292197847'})
    client.post('/login', data = {'uname': 'sourbose', 'pword': 'test123', '2fa': '9292197847'})
    with client:
        response = client.get('/spell_check')
        print(response.data)