# Library imports
from flask import Blueprint, render_template, redirect, g, url_for, request
from werkzeug import generate_password_hash

# Local file imports
from database import get_db

root_view = Blueprint('login', __name__, url_prefix='')

@root_view.route('/', methods=['GET'])
def basepath():
    return render_template('/login.html')

@root_view.route('/register', methods=['GET', 'POST'])
def register():
    print(request.method)
    if request.method == 'POST':
        select_query = 'SELECT id FROM user WHERE name = ?'
        insert_query = 'INSERT INTO user(user, password, phone) VALUES (?, ?, ?)'
        user = request.form['uid']
        password = request.form['password']
        phone = request.form['doublefactor']
        db_connection = get_db()
        print(user, password, phone)
        error = None
        if not user:
            error = 1
        elif not password:
            error = 1
        elif db_connection.execute(select_query, (user,)).fetchone() is not None:
            error = 'User {} is already registered.'.format(user)
        print(error)
        if error is not None:
            db_connection.execute(insert_query,(user, generate_password_hash(password), generate_password_hash(phone)))
            db_connection.commit()
            print(user, generate_password_hash(password), generate_password_hash(phone))
            return render_template('/success.html')
        else:
            return render_template('/failure.html')

    return render_template('/register.html')

@root_view.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        uid = g.user
        if uid is not None:
            return redirect(url_for('login.basepath'))
    else:
        return redirect(url_for('login.basepath'))