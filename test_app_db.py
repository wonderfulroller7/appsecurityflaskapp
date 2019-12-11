import pytest
from flask import g, session
import database
import re

def test_admin(client, app):
    client.post('/login', data = {'uname': 'sb', 'pword': 'welcome1', '2fa': '9292197847'})
    client.get('/spell_check')
    token=response.data.decode().split("csrf_token")[1].split("value=")[1].split("\"/>")[0].split("TOKEN \"")[0][1:]
    #submitting two responses
    response = client.post('/spell_check',
        data={'inputtext': 'Wheres the cat at?','csrf_token':token)
    response = client.post('/spell_check',
        data={'inputtext': 'Today is the day!', csrf_token':token})
    client.post('/logout')
    client.post('/login', data = {'uname': 'sb6856', 'pword': 'welcome1', '2fa': '9339752654'})
    client.get('/spell_check')
    token=response.data.decode().split("csrf_token")[1].split("value=")[1].split("\"/>")[0].split("TOKEN \"")[0][1:]
    #submitting two responses
    response = client.post('/spell_check',
        data={'inputtext': 'Rick and Morty Season 4 is here finally','csrf_token':token)
    response = client.post('/spell_check',
        data={'inputtext': 'The stone monster is here','csrf_token':token})
    response = client.post('/spell_check',
        data={'inputtext': "Agana exsaka sapulu",'csrf_token':token})
    client.post('/logout')
    response = auth.login_admin()
    with client:
        token=response.data.decode().split("csrf_token")[1].split("value=")[1].split("\"/>")[0].split("TOKEN \"")[0][1:]
        history_response = client.get('/history')
        # 2 queries should be present
        #print(history_response.data.decode())
        assert b"id=\"userquery\"" in history_response.data
        user_response = client.post('/history',
            data={'userid': 'sb6856','csrf_token':token}
        )
        print(user_response.data.decode())
        print(user_response.status_code)
        
        #allow admin user to post a username
        assert user_response.status_code==200
        assert "<h2>Queries Made by sb6856 </h2>" in user_response.data.decode()