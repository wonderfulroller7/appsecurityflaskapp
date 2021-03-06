# Library imports
from flask import Blueprint, render_template, redirect, g, url_for, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import functools
import datetime

# Local file imports
from database import get_db

root_view = Blueprint('login', __name__, url_prefix='')

@root_view.route('/', methods=['GET'])
def basepath():
    return render_template('/spellchecker.html')

@root_view.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        select_query = 'SELECT id FROM user WHERE uname = ?'
        insert_query = 'INSERT INTO user(uname, phone_number, password) VALUES (?, ?, ?)'
        user = request.form['uname']
        password = request.form['pword']
        phone = request.form['2fa']
        db_connection = get_db()
        error = None
        if not user:
            error = 1
        elif not password:
            error = 1
        elif db_connection.execute(select_query, (user,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(user)
        # print(error)
        if error is not None:
            return render_template('/failure.html')
        else:
            db_connection.execute(insert_query,(user, phone, password))
            db_connection.commit()
            # print(user, generate_password_hash(password), generate_password_hash(phone))
            return render_template('/success.html')

    return render_template('/register.html')

@root_view.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        uname = g.user
        if uname is not None:
            return redirect(url_for('login.basepath'))
        return render_template('/login.html')
    else:
        uname = g.user
        if uname is not None:
            return redirect(url_for(login.basepath))
        uname = request.form['uname']
        pword = request.form['pword']
        dualauth = request.form['2fa']
        select_query = 'SELECT * FROM user WHERE uname = ?'
        db_connection = get_db()
        error = None

        cur_user = db_connection.execute(select_query, (uname,)).fetchone()
        # print(uname + ' ' + dualauth + ' ' + pword)
        # print(cur_user['uname'] + ' ' + cur_user['phone_number'] + ' ' + cur_user['password'])
        if cur_user is None:
            error = 'Incorrect'
        elif cur_user['uname'] != uname:
            error = 'Incorrect'
        elif cur_user['password'] != pword:
            error = 'Incorrect'
        elif cur_user['phone_number'] != dualauth:
            error = 'Failure in Two-factor authentication'

        if error is None:
            session.clear()
            session['session_id'] = cur_user['id']
            session.permanent = True
            login_query = 'INSERT INTO logins(uname, request, access_time) VALUES (?, ?, ?)'
            db_connection.execute(login_query,(uname, 'login', datetime.datetime.now()))
            db_connection.commit()
        
        return redirect(url_for('login.loginresult', result=error))

@root_view.route('/login_success')
def loginresult():
    return render_template('/login_success.html',result=request.args.get('result'))

@root_view.route('/logout')
def logout():
    print(request.headers)
    db_connection = get_db()
    login_query = 'INSERT INTO logins(uname, request, access_time) VALUES (?, ?, ?)'
    db_connection.execute(login_query,(g.user['uname'], 'logout', datetime.datetime.now()))
    db_connection.commit()
    session.clear()
    g.user = None
    return redirect(url_for('login.basepath'))

@root_view.before_app_request
def check_if_user_isLoggedIn():
    user_session_id = session.get('session_id')
    print(user_session_id)
    select_query = 'SELECT * FROM user WHERE id = ?'
    if user_session_id is None:
        g.user = None
    else:
        g.user = get_db().execute(select_query, (user_session_id,)).fetchone()
    
def isLoggedIn(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login.login'))
        return view(**kwargs)
    return wrapped_view

@root_view.after_request
def cache(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response