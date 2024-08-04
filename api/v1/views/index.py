#!/usr/bin/python3
"""Connects to api"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns API status code"""
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    pass
