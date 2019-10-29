from flask import Blueprint, render_template, redirect, g, url_for, request
from database import get_db

root_view = Blueprint('login', __name__, url_prefix='')

@root_view.route('/', methods=['GET'])
def basepath():
    return render_template('/login.html')

@root_view.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        return render_template('/registrationFailure.html')
    return render_template('/register.html')

@root_view.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        uid = g.user
        if uid is not None:
            return redirect(url_for('login.basepath'))
    else:
        return redirect(url_for('login.basepath'))