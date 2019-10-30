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

def login_test_get(client, app):
    assert client.get('/login').status_code == 200

def login_test_post(client, app):
    client.post('/login', data = {'uname': 'sourbose', 'pword': 'test123', '2fa': '9292197847'})
    with client:
        assert client.get('/spell_check').status_code == 200
        assert g.user['uname'] == 'sourbose'

