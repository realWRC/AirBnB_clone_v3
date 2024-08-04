#!/usr/bin/python3
"""States API portion"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def getState():
    """Gets all states in storage"""
    allStates = []
    for state in storage.all("State").values():
        allStates.append(state.to_dict())
    return jsonify(allStates)


@app_views.route(
    '/states/<string:state_id>',
    methods=['GET'], strict_slashes=False
)
def getStateId(state_id):
    """Gets a specific object from storage"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<string:state_id>',
    methods=['DELETE'], strict_slashes=False
)
def deleteState(state_id):
    """Deletes a state object"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route(
    '/states/',
    methods=['POST'], strict_slashes=False
)
def postState():
    """Deletes a state object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    data = request.get_json()
    state = State(**data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route(
    '/states/<string:state_id>',
    methods=['PUT'], strict_slashes=False
)
def putState(state_id):
    """Update a state object"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())
