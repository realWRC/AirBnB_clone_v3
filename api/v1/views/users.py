#!/usr/bin/python3
"""API views for users objects"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route(
    '/users', methods=['GET'], strict_slashes=False
)
def getUsers():
    """Gets all users in storage"""
    users = []
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route(
    '/users/<string:user_id>', methods=['GET'],
    strict_slashes=False
)
def getUser(user_id):
    """Gets data for specific user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
    '/users', methods=['POST'], strict_slashes=False
)
def postUser():
    """Creates a new user"""
    if not request.get_json():
        return make_response(
            jsonify({'error': 'Not a JSON'}), 400
        )
    if 'email' not in request.get_json():
        return make_response(
            jsonify({'error': 'Missing email'}), 400
        )
    if 'password' not in request.get_json():
        return make_response(
            jsonify({'error': 'Missing password'}), 400
        )
    data = request.get_json()
    user = User(**data)
    user.save()
    return (jsonify(user.to_dict()), 201)


@app_views.route(
    '/users/<string:user_id>', methods=['PUT'],
    strict_slashes=False
)
def putUser(user_id):
    """Updates user data"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(
            jsonify({'error': 'Not a JSON'}), 400
        )
    for attribute, value in request.get_json().items():
        if attribute not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attribute, value)
    user.save()
    return jsonify(user.to_dict())


@app_views.route(
    '/users/<string:user_id>', methods=['DELETE'],
    strict_slashes=False
)
def delete_user(user_id):
    """Deletes a specific user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({}))
