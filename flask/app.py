#!/usr/bin/env python3
"""app.py
Main entry point of the blog web app.
"""
import pathlib

import flask  # import the flask library
from flask_cors import CORS

import db
import auth
import blog


app_dir = pathlib.Path(__file__).resolve().parent

app = flask.Flask(__name__)  # instantiate a minimal webserver

app.config['DATABASE'] = app_dir / 'db.sqlite'  # path to the db file
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'some_random_value'

cors = CORS(app, resources={r"/*": {"origins": "*"}})

db.register_db_methods(app)  # register db management methods

app.register_blueprint(auth.bp)  # add auth views to application
app.register_blueprint(blog.bp)  # add blog views to application

app.add_url_rule('/', endpoint='index')  # map the 'index' endpoint with /


if __name__ == '__main__':
    app.run()  # start web server
