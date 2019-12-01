import os
import subprocess
from flask import Blueprint, render_template, redirect, g, url_for, request, session

import database
from login import isLoggedIn

root_view = Blueprint('spellchecker', __name__)

@root_view.route('/spell_check', methods=['GET', 'POST'])
@isLoggedIn
def spell_check():
    if request.method == 'POST':
        
        # print(request.headers.get['origin'])

        string_to_be_checked = request.form['inputtext']

        input_file = str(session.get('session-id')) + '.txt'
        print(string_to_be_checked)
        f = open(input_file, 'w')
        f.write(string_to_be_checked)
        f.close()
        arguments = ("./spell_check", str(input_file), "dictionary.txt")
        try:
            shell_process = subprocess.Popen(arguments, stdout=subprocess.PIPE)
            shell_process.wait()
            shell_output = shell_process.stdout.read()
            shell_output = shell_output.decode().replace("\n",",")
            print("Misspelled words : ", shell_output)
        except subprocess.CalledProcessError as e:
            print('Error :', e)

        insert_query = 'INSERT INTO logs(uname, request, result) VALUES (?, ?, ?)'
        db_connection = database.get_db()
        uname = g.user['uname']
        db_connection.execute(insert_query,(uname, string_to_be_checked, shell_output,))
        db_connection.commit()        

        return render_template('/spellreview.html', string_query=string_to_be_checked, misspelled=shell_output)
    else:
        return render_template('/spellchecker.html')

@root_view.route('/history', methods=['GET', 'POST'])
@isLoggedIn
def get_queries():
    if request.method == 'GET':
        db_connection = database.get_db()
        db_cursor = db_connection.cursor()
        query_list = []
        if g.user['uname'] != 'admin':
            select_query = 'SELECT * FROM logs WHERE uname = ?'
            uname = g.user['uname']    
            queries = db_cursor.execute(select_query,(uname,))
            for row in queries:
                query_list.append({
                "queryid": str(row[0]),
                "username": str(row[1]),
                "querytext": str(row[2]),
                "queryresults": str(row[3])
                })
            print(query_list)
        else:
            select_query = 'SELECT * FROM logs'
            queries = db_cursor.execute(select_query)
            for row in queries:
                query_list.append({
                "queryid": str(row[0]),
                "username": str(row[1]),
                "querytext": str(row[2]),
                "queryresults": str(row[3])
                })
            print(query_list)
        return render_template('/history.html', list=query_list)
    else:
        db_connection = database.get_db()
        db_cursor = db_connection.cursor()
        query_list = []
        username = request.form['userquery']
        select_query = 'SELECT * FROM logs WHERE uname = ?'
        queries = db_cursor.execute(select_query,(username,))
        for row in queries:
            query_list.append({
                "queryid": str(row[0]),
                "username": str(row[1]),
                "querytext": str(row[2]),
                "queryresults": str(row[3])
                })
        print(query_list)
        return render_template('/history.html', list=query_list)


@root_view.route('/history/query<queryId>', methods=['GET',])
@isLoggedIn
def get_individual_query(queryId):
    query_list = []
    username = g.user['uname']
    db_connection = database.get_db()
    db_cursor = db_connection.cursor()
    if username != 'admin':
        select_query = 'SELECT * FROM logs WHERE uname = ? and id = ?'
        if str(queryId).isdigit():
            queries = db_cursor.execute(select_query, (username, queryId,))
            for row in queries:
                query_list.append({
                "queryid": str(row[0]),
                "username": str(row[1]),
                "querytext": str(row[2]),
                "queryresults": str(row[3])
                })
            print(query_list)
    else:
        select_query = 'SELECT * FROM logs WHERE id = ?'
        if str(queryId).isdigit():
            queries = db_cursor.execute(select_query, (username,))
            for row in queries:
                query_list.append({
                "queryid": str(row[0]),
                "username": str(row[1]),
                "querytext": str(row[2]),
                "queryresults": str(row[3])
                })
        print(query_list)
    return render_template('/individual_history.html', list=query_list)
        

@root_view.route('/login_history', methods=['GET', 'POST'])
@isLoggedIn
def get_login_history():
    if g.user['uname'] != 'admin':
        return render_template('/spellchecker.html')
    if request.method == 'GET':
        return render_template('/login_history_search.html')
    if request.method == 'POST':
        userid = request.form['userid']
        select_query = 'SELECT * FROM logins WHERE uname = ?'
        db_connection = database.get_db()
        db_cursor = db_connection.cursor()
        queries = db_cursor.execute(select_query,(userid,))
        request_list = []
        for row in queries:
            request_list.append({
                "id": str(row[0]),
                "username": str(row[1]),
                "action": str(row[2]) + str(row[0]) + '_' + str(row[3])
            })    
        print(request_list)
        return render_template('/login_history.html', list=request_list)


@root_view.after_request
def cache(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response