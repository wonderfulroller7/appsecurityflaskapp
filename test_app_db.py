import pytest
from flask import g, session
import database
import re

def test_admin(client, app):
    client.post('/login', data = {'uname': 'sb', 'pword': 'welcome1', '2fa': '9292197847'})
    response = client.get('/spell_check')
    token = response.data.decode().split("csrf_token")[1].split("value=")[1].split("\"/>")[0].split("TOKEN \"")[0][1:]
    #submitting two responses
    response = client.post('/spell_check',
        data = {'inputtext': 'Wheres the cat at?','csrf_token':token})
    response = client.post('/spell_check',
        data = {'inputtext': 'Today is the day!', 'csrf_token':token})
    client.post('/logout')
    client.post('/login', data = {'uname': 'sb6856', 'pword': 'welcome1', '2fa': '9339752654'})
    response = client.get('/spell_check')
    token = response.data.decode().split("csrf_token")[1].split("value=")[1].split("\"/>")[0].split("TOKEN \"")[0][1:]
    #submitting two responses
    response = client.post('/spell_check',
        data={'inputtext': 'Rick and Morty Season 4 is here finally','csrf_token':token})
    response = client.post('/spell_check',
        data={'inputtext': 'The stone monster is here','csrf_token':token})
    response = client.post('/spell_check',
        data={'inputtext': "Agana exsaka sapulu",'csrf_token':token})
    client.post('/logout')
    client.post('/login', data = {'uname': 'admin', 'pword': 'Administrator@1', '2fa': '12345678901'})
    response = client.get('/history')
    token = response.data.decode().split("csrf_token")[1].split("value=")[1].split("\"/>")[0].split("TOKEN \"")[0][1:]
    with client:
        # token = response.data.decode().split("csrf_token")[1].split("value=")[1].split("\"/>")[0].split("TOKEN \"")[0][1:]
        history_response = client.get('/history')
        #token = history_response.data.decode().split("csrf_token")[1].split("value=")[1].split("\"/>")[0].split("TOKEN \"")[0][1:]
        # 2 queries should be present
        #print(history_response.data.decode())
        assert b"id=\"queryresults\"" in history_response.data
        response = client.post('/history', data = {'userid': 'sb6856', 'csrf_token': token})
        print(response.data.decode())
        print(response.status_code)
        
        #allow admin user to post a username
        assert response.status_code==200
        assert "<h2>Queries Made by sb6856 </h2>" in response.data.decode()