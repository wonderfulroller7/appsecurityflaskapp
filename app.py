import os
from flask import Flask
from config import Config

import database

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = 'babayaga',
        DATABASE = os.path.join(app.instance_path, 'spellchecker.sqlite'),
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    database.initialise_app(app)
    with app.app_context():
        database.init_db()
        
    return app