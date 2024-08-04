#!/usr/bin/python3
"""Connects to api"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns API status code"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    objs = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    statistics = {}
    for key, value in objs.items():
        statistics[key] = storage.count(value)
    return jsonify(statistics)


if __name__ == "__main__":
    pass
