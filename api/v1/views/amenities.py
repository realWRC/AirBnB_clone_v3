#!/usr/bin/python3
"""Views for amenities"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route(
    '/amenities', methods=['GET'],
    strict_slashes=False
)
def getAmenities():
    """Get amenities from storage"""
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return (jsonify(amenities))


@app_views.route(
    '/amenities/<string:amenity_id>', methods=['GET'],
    strict_slashes=False
)
def getAmenity(amenity_id):
    """get amenity information for specified amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return (jsonify(amenity.to_dict()))


@app_views.route(
    '/amenities', methods=['POST'], strict_slashes=False
)
def postAmenity():
    """Creates a new amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    date = request.get_json()
    amenity = Amenity(**data)
    amenity.save()
    return (jsonify(amenity.to_dict()), 201)


@app_views.route(
    '/amenities/<string:amenity_id>', methods=['PUT'],
    strict_slashes=False
)
def putAmenity(amenity_id):
    """Updates an amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    for attribute, value in request.get_json().items():
        if attribute not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attribute, value)
    amenity.save()
    return jsonify(amenity.to_dict())


@app_views.route(
    '/amenities/<string:amenity_id>', methods=['DELETE'],
    strict_slashes=False
)
def delete_amenity(amenity_id):
    """deletes an amenity based on its amenity_id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}))
