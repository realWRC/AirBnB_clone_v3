#!/usr/bin/python3
"""API file for reviews"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
    '/places/<string:place_id>/reviews', methods=['GET'],
    strict_slashes=False
)
def getReviews(place_id):
    """Gets reviews form specified place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return (jsonify(reviews))


@app_views.route(
    '/reviews/<string:review_id>', methods=['GET'],
    strict_slashes=False
)
def getReview(review_id):
    """Gets review using id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    '/reviews/<string:review_id>', methods=['DELETE'],
    strict_slashes=False
)
def deleteReview(review_id):
    """Deletes a review using id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({}))


@app_views.route(
    '/places/<string:place_id>/reviews', methods=['POST'],
    strict_slashes=False
)
def postReview(place_id):
    """Create a review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(
            jsonify({'error': 'Not a JSON'}), 400
        )

    data = request.get_json()
    if 'user_id' not in data:
        return make_response(
            jsonify({'error': 'Missing user_id'}), 400
        )
    if 'text' not in data:
        return make_response(
            jsonify({'error': 'Missing text'}), 400
        )

    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route(
    '/reviews/<string:review_id>', methods=['PUT'],
    strict_slashes=False
)
def putReview(review_id):
    """Updates a review" data"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attribute, value in request.get_json().items():
        if attribute not in [
            'id', 'user_id', 'place_id', 'created_at', 'updated_at'
        ]:
            setattr(review, attribute, value)
    review.save()
    return jsonify(review.to_dict())
