#!/usr/bin/python3
"""Views file for city objects"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    '/states/<string:state_id>/cities',
    methods=['GET'], strict_slashes=False
)
def getCities(state_id):
    """Gets cities in a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    allCities = []
    for city in state.cities:
        allCities.append(city.to_dict())
    return jsonify(allCities)


@app_views.route(
    '/cities/<string:city_id>', methods=['GET'],
    strict_slashes=False
)
def getCity(city_id):
    """Get Specified City"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
    '/cities/<string:city_id>', methods=['DELETE'],
    strict_slashes=False
)
def deleteCity(city_id):
    """Deletes a city by city_id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route(
    '/states/<string:state_id>/cities/',
    methods=['POST'], strict_slashes=False
)
def postCity(state_id):
    """Creates city in a given state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    data = request.get_json()
    city = City(**data)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route(
    '/cities/<string:city_id>', methods=['PUT'],
    strict_slashes=False
)
def putCity(city_id):
    """Updates a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attribute, value in request.get_json().items():
        if attribute not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, attribute, value)
    city.save()
    return jsonify(city.to_dict())
