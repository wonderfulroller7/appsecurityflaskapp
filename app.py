import os
from flask import Flask
from config import Config
from flask_wtf.csrf import CSRFProtect

import database
import login
import spellchecker

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    csrf = CSRFProtect()
    csrf.init_app(app)
    app.config.from_mapping(
        SECRET_KEY = 'babayaga',
        DATABASE = os.path.join(app.instance_path, 'spellchecker.sqlite'),
    )

    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Strict',
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    database.initialise_app(app)
    with app.app_context():
        database.init_db()
    
    app.register_blueprint(login.root_view)
    app.register_blueprint(spellchecker.root_view)

    csrf.exempt(login.root_view)
    
    return app