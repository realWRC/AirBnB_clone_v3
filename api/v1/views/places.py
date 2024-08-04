#!/usr/bin/python3
"""places.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
    '/cities/<string:city_id>/places', methods=['GET'],
    strict_slashes=False
)
def getPlaces(city_id):
    """Gets place objects"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route(
    '/places/<string:place_id>', methods=['GET'],
    strict_slashes=False
)
def getPlace(place_id):
    """Gets a specified place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    '/places/<string:place_id>', methods=['DELETE'],
    strict_slashes=False
)
def deletePlace(place_id):
    """deletes a place based on its place_id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}))


@app_views.route(
    '/cities/<string:city_id>/places', methods=['POST'],
    strict_slashes=False
)
def postPlace(city_id):
    """Creates a new place object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    data = request.get_json()
    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    user = storage.get("User", data.user_id)
    if user is None:
        abort(404)
    data.city_id = city_id
    place = Place(**data)
    place.save()
    return (jsonify(place.to_dict()), 201)


@app_views.route(
    '/places/<string:place_id>', methods=['PUT'],
    strict_slashes=False
)
def putPlace(place_id):
    """Updates a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attribute, value in request.get_json().items():
        if attribute not in [
            'id', 'user_id', 'city_id', 'created_at', 'updated_at'
        ]:
            setattr(place, attribute, value)
    place.save()
    return jsonify(place.to_dict())
