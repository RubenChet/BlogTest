#!/usr/bin/env python3
"""Declare a Flask blueprint to register authentication views.
"""
import flask
from db import get_db
from flask_bcrypt import generate_password_hash, check_password_hash
import uuid

sessions_cookies = {}  # store the session cookies

bp = flask.Blueprint(  # declare new blueprint
    name='auth',
    import_name=__name__,
    template_folder='templates',
    url_prefix='/auth',
)


@bp.route('/register', methods=('POST',))
def register():
    """Register view. Insert new user in db when a POST request occurs.

    Returns (str): JSON response
    """
    data = flask.request.get_json()
    username = data.get('username').lower()
    password = data.get('password')
    db = get_db()
    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    if error is None:
        try:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
        except db.IntegrityError:
            error = f'User {username} is already registered.'

    if error is None:
        response = flask.jsonify(
            {'status': 'success', 'message': 'Successfully registered.'})
    else:
        response = flask.jsonify({'status': 'error', 'message': error})
    return response


@bp.route('/login', methods=('POST',))
def login():
    """Login view. Handle login requests via JSON payload.

    Returns (json): response object with status and message
    """
    data = flask.request.get_json()
    username = data.get('username')
    password = data.get('password')
    db = get_db()
    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    if error is None:
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username or password.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'

    if error is None:
        response = flask.jsonify(
            {'status': 'success', 'message': 'Logged in successfully.'})
        user_cookie = str(uuid.uuid4())

        # SameSite Strict for CSRF protection
        # hhtponly to prevent XSS
        # response.set_cookie('sessionId', user_cookie,
        #                     secure=True, httponly=True, samesite='Strict', max_age=10) exemple de cookie qui expire dans 10 secondes
        response.set_cookie('sessionId', user_cookie,
                            secure=True, httponly=True, samesite='Strict', max_age=86400) # Cookie qui expire dans 24h
        sessions_cookies[user_cookie] = username
    else:
        response = flask.jsonify({'status': 'error', 'message': error})
    return response


@bp.route('/logout', methods=('POST',))
def logout():
    """Logout view. Handle logout requests.

    Returns (json): response object with status and message
    """
    cookie = flask.request.cookies.get('sessionId')
    if cookie and cookie in sessions_cookies:
        del sessions_cookies[cookie]
    response = flask.jsonify(
        {'status': 'success', 'message': 'Logged out successfully.'})
    response.set_cookie('sessionId', '', expires=0)
    return response
