import sqlite3

from flask import current_app, g

DATABASE = ''


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config('DATABASE')
        )

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()