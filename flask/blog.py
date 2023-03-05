#!/usr/bin/env python3
"""Declare a Flask blueprint to register blog views.
"""
import flask
from werkzeug.exceptions import abort
from db import get_db
from flask import jsonify

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
        'SELECT p.post_id, title, body, created, p.user_id, username'
        ' FROM post p JOIN user u ON p.user_id = u.user_id'
        ' ORDER BY created DESC'
    ).fetchall()
    return jsonify(posts=[dict(post) for post in posts])

@bp.route('/create', methods=('POST',))
def create_post():
    """Insert new post in db when a POST request occurs and return user to index
    page if everything went right, otherwise to the same view.

    Returns (json): response in JSON format
    """
    data = flask.request.get_json()
    title = data.get('title')
    body = data.get('body')
    cookie = data.get('cookie')
    error = None
    if not title:
        error = 'Title is required.'

    if error is not None:
        response = {'status': 'error', 'message': error}
    else:
        db = get_db()
        db.execute(
            'INSERT INTO post (title, body, user_id)'
            f' VALUES ("{title}", "{body}", "{cookie}")'
        )
        db.commit()
        response = {'status': 'success', 'message': 'Post successfully created.'}

    return flask.jsonify(response)

def get_post(post_id):
    """Return a blog post from the database from its id.
    If check_author is True, check if the current logged-in user is
    the owner of the post, raising HTTP 403 Forbidden error if they are not.

    Args:
        post_id: the post id to fetch
        check_author (bool): If True, check ownership of the post.
            Default to True.

    Returns: result from the queryset

    Raises:
        werkzeug.exceptions.NotFound: if the post id is not found
        werkzeug.exceptions.Forbidden: if check_author is True and current
            logged-in user is not author of the post
    """
    post = get_db().execute(
        'SELECT post_id, title, body, created, user_id'
        ' FROM post'
        f' WHERE post_id = {post_id}'
    ).fetchone()

    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")

    # if check_author and post['author_id'] != flask.g.user['id']:
    #     abort(403)

    return post

@bp.route('/update/<int:post_id>', methods=['PUT'])
def update(post_id):
    """Blog post update view. Display update form in the same way as the
    creation form. Answer POST update with an update in the database.

    Args:
        post_id: the id of the post to update

    Returns: update view or a redirect to the index page
    """
    data = flask.request.get_json()
    title = data.get('title')
    body = data.get('body')
    error = None
    if error is not None:
        response = {'status': 'error', 'message': error}
    else:
        db = get_db()
        db.execute(
            f'UPDATE post SET title = "{title}", body = "{body}"'
            f' WHERE post_id = {post_id}'
        )
        db.commit()
        response = {'status': 'success', 'message': 'Post successfully Updated.'}
    return jsonify(response)

@bp.route('/delete/<int:post_id>',  methods=['DELETE'])
def delete(post_id):
    """POST method to delete a post by its id. Silently fails.

    Args:
        post_id: the post id to delete

    Returns: redirect to the index view
    """
    get_post(post_id)
    db = get_db()
    db.execute(f'DELETE FROM post WHERE post_id = {post_id}')
    db.commit()
    response = {'message': 'Post has been deleted'}
    return jsonify(response)

@bp.route('/detail/<int:post_id>')
def detail(post_id):
    """Post detail view. Display the blog post alone in a page.

    Args:
        post_id: the post id to display

    Returns: the view of the detailed post

    Raises:
        werkzeug.exceptions.NotFound: if the post id is not found
    """
    post = get_post(post_id)
    return jsonify(post=dict(post))
