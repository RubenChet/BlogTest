#!/usr/bin/env python3
"""Declare a Flask blueprint to register blog views.
"""
import flask
from werkzeug.exceptions import abort
from db import get_db
from flask import jsonify
from auth import sessions_cookies


bp = flask.Blueprint(  # declare new blueprint
    name='blog',
    import_name=__name__,
    template_folder='templates',
    url_prefix='/',
)


@bp.route('/')
def index():
    """Index view of the blog, fetch all blog posts and display them from
    newest to oldest.

    Returns:
        JSON data containing a list of blog post objects
    """
    db = get_db()
    posts = db.execute(
        'SELECT *'
        ' FROM post '
        ' ORDER BY created DESC'
    ).fetchall()
    return jsonify(posts=[dict(post) for post in posts])


@bp.route('/create', methods=('POST',))
def create_post():
    """Insert new post in db when a POST request occurs and return user to index
    page if everything went right, otherwise to the same view.

    Returns (json): response in JSON format
    """
    # verify if the user is logged in
    username = is_user_logged_in()
    if username == False:
        return flask.jsonify({'status': 'error', 'message': 'Veuillez vous connecter pour pouvoir créer un post'})

    # get the data from the request
    data = flask.request.get_json()
    title = data.get('title')
    body = data.get('body')

    # check if the data is valid
    error = None
    if not title:
        error = 'Title is required.'
    elif not body:
        error = 'Body is required.'
    if error is not None:
        return flask.jsonify({'status': 'error', 'message': error})

    # if the data is valid, insert it in the database
    try:
        db = get_db()
        db.execute(
            'INSERT INTO post (title, body, username)'
            ' VALUES (?, ?, ?)',
            (title, body, username)
        )
        db.commit()
    except:
        return flask.jsonify({'status': 'error', 'message': 'Error inserting post into database'})

    return flask.jsonify({'status': 'success', 'message': 'Post successfully created.'})


@bp.route('/update/<int:post_id>', methods=['PUT'])
def update(post_id):
    """Blog post update view. Display update form in the same way as the
    creation form. Answer POST update with an update in the database.

    Args:
        post_id: the id of the post to update

    Returns: update view or a redirect to the index page
    """

    # verify if the user is logged in
    username = is_user_logged_in()
    if username == False:
        return flask.jsonify({'status': 'error', 'message': 'Veuillez vous connecter'})

    # verify if the user is the owner of the post
    check_user = is_user_owner_of_post(post_id, username)
    if check_user == False:
        return flask.jsonify({'status': 'error', 'message': 'Le post ne vous appartient pas'})

    # get the data from the request
    data = flask.request.get_json()
    title = data.get('title')
    body = data.get('body')

    # check if the data is valid
    error = None
    if not title:
        error = 'Title is required.'
    elif not body:
        error = 'Body is required.'
    if error is not None:
        return jsonify({'status': 'error', 'message': error})

    # if the data is valid, update it in the database
    db = get_db()
    db.execute(
        'UPDATE post SET title = ?, body = ? WHERE post_id = ?',
        (title, body, post_id)
    )
    db.commit()

    return jsonify({'status': 'success', 'message': 'Post successfully updated.'})


@bp.route('/delete/<int:post_id>',  methods=['DELETE'])
def delete(post_id):
    """POST method to delete a post by its id. Silently fails.

    Args:
        post_id: the post id to delete

    Returns: redirect to the index view
    """
    # verify if the user is logged in
    username = is_user_logged_in()
    if username == False:
        return flask.jsonify({'status': 'error', 'message': 'Veuillez vous connecter'})

    # verify if the user is the owner of the post
    check_user = is_user_owner_of_post(post_id, username)
    if check_user == False:
        return flask.jsonify("Vous ne pouvez pas supprimer un post qui ne vous appartient pas")

    # delete the post
    db = get_db()
    db.execute('DELETE FROM post WHERE post_id = ?', (post_id,))
    db.commit()
    return jsonify({'status': 'success', 'message': 'Post has been deleted'})


@bp.route('/detail/<int:post_id>')
def detail(post_id):
    """Post detail view. Display the blog post alone in a page.

    Args:
        post_id: the post id to display

    Returns: the view of the detailed post

    Raises:
        werkzeug.exceptions.NotFound: if the post id is not found
    """

    # get the post from the database
    post = get_db().execute(
        'SELECT *'
        ' FROM post'
        ' WHERE post_id = ?',
        (post_id,)
    ).fetchone()
    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")

    return jsonify(post=dict(post))


@bp.route('/check_id_and_user', methods=['POST'])
def check_id_and_user():
    """
    """
    data = flask.request.get_json()
    id = data.get('id')
    username = is_user_logged_in()
    if username == False:
        return flask.jsonify({'status': 'error', 'message': 'Veuillez vous connecter'})
    check_user = is_user_owner_of_post(id, username)
    if check_user == False:
        return flask.jsonify({'status': 'error'})
    return jsonify({'status': 'success'})

# Function checking if the user is connected


def is_user_logged_in():
    """Check if the user is logged in by verifying if the sessionId cookie is
    present and valid.

    Returns:
        Username if the user is logged in, False otherwise
    """
    cookie = flask.request.cookies.get('sessionId')
    if cookie in sessions_cookies:
        username = sessions_cookies[cookie]
        return username
    return False

# Function checking if the user is the owner of the post


def is_user_owner_of_post(post_id, username):
    """Check if the user is the owner of the post with the given post_id.

    Args:
        post_id: the id of the post to check ownership
        username: the username of the user to check

    Returns:
        True if the user is the owner of the post, False otherwise
    """
    # check if the user is the owner of the post
    db = get_db()
    try:
        result = db.execute(
            'SELECT * FROM post WHERE post_id = ?',
            (post_id,)
        ).fetchone()
    except:
        return False
    if result and result['username'] == username:
        return True
    else:
        return False
