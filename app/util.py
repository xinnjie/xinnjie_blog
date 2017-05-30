import sqlite3

from flask import g

from .blog_app import app


def get_db():
	db = getattr(g, '_databse', None)
	if db is None:
		db = g._databse = sqlite3.connect(app.config['DB_URL'])
	return db


@app.teardown_appcontext
def close_db_connection(e):  # TODO e?
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()
