#!/usr/bin/env python3
"""Declare a Flask blueprint to register authentication views.
"""
import flask
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

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
    username = data.get('username')
    password = data.get('password')
    user_id = secrets.token_hex(16)
    db = get_db()
    error = None

    if not username:
        error = 'Username is required.'
    elif not password:
        error = 'Password is required.'

    if error is None:
        try:
            db.execute(
                'INSERT INTO user (user_id, username, password) VALUES (?, ?, ?)',
                (user_id, username, generate_password_hash(password))
            )
            db.commit()
        except db.IntegrityError:  # catch this specific exception
            error = f'User {username} is already registered.'
        else:  # if no exception happened
            return flask.jsonify({'message': 'Successfully registered'})

    return flask.jsonify({'error': error})

@bp.route('/login', methods=('POST',))
def login():
    """Login view. Handle login requests via JSON payload.

    Returns (json): response object with status and message
    """
    data = flask.request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return flask.jsonify({'status': 'error', 'message': 'Username and password are required.'})

    db = get_db()
    user = db.execute(
        f'SELECT * FROM user WHERE username = "{username}"'
    ).fetchone()

    if user is None:
        return flask.jsonify({'status': 'error', 'message': 'Incorrect username or password.'})
    elif not check_password_hash(user['password'], password):
        return flask.jsonify({'status': 'error', 'message': 'Incorrect username or password.'})

    response = flask.jsonify({'status': 'success', 'message': 'Logged in successfully.', 'cookie' : user['user_id']})
    return response