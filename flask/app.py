#!/usr/bin/env python3
"""app.py
Main entry point of the blog web app.
"""
import pathlib
import flask  # import the flask library
from flask import request, session # import the request object
from flask_cors import CORS  # import CORS library
from flask_bcrypt import Bcrypt

from flask_limiter import Limiter  # import the limiter library
# import the get_remote_address function
from flask_limiter.util import get_remote_address

import db  # import db management methods
import auth  # import auth views
import blog  # import blog views

from auth import sessions_cookies

app_dir = pathlib.Path(__file__).resolve().parent

app = flask.Flask(__name__)  # instantiate a minimal webserver
bcrypt = Bcrypt(app)

CORS(app, supports_credentials=True)  # enable CORS

app.config['DATABASE'] = app_dir / 'db.sqlite'  # path to the db file
app.config['DEBUG'] = True  # enable debug mode
# secret key for the session
app.config['SECRET_KEY'] = 'ty4425hk54a21eee5719b9s9df7sdfklx'


db.register_db_methods(app)  # register db management methods

app.register_blueprint(auth.bp)  # add auth views to application
app.register_blueprint(blog.bp)  # add blog views to application

app.add_url_rule('/', endpoint='index')  # map the 'index' endpoint with /

# instantiate the limiter object
limiter = Limiter(
    get_remote_address,
    default_limits=["10 per second"],
    storage_uri="memory://",
)

limiter.init_app(app)
limiter.request_filter(lambda: request.method.upper() == 'OPTIONS')
limiter.limit("5 per hour")(auth.bp)  # limit blog views
limiter.exempt(blog.bp)  # initialize the limiter object


@app.route('/is_logged_in', methods=('GET',))
@limiter.exempt
def is_logged_in():
    """Check if the user is logged in.

    Returns (json): response object with status and message
    """
    cookie = flask.request.cookies.get('sessionId')
    if cookie and cookie in sessions_cookies:
        username = sessions_cookies[cookie]
        return flask.jsonify({'status': 'success', 'message': 'You are logged in.', 'username': username})
    else:
        return flask.jsonify({'status': 'error', 'message': 'You are not logged in.'})

if __name__ == '__main__':
    app.run()  # start web server
