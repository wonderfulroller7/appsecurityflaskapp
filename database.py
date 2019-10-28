import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

DATABASE = ''


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    
    db = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def close_db(e=None):

    db = g.pop('db', None)

    if db is not None:
        db.close()



@click.command('init-db')
@with_appcontext
def initialise_db():
    init_db()
    click.echo('Initialised the database')

def initialise_app(app):

    app.teardown_appcontext(close_db)
    app.cli.add_command(initialise_db)
