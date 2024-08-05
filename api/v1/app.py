#!/usr/bin/python3
"""Flask api app"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
from os import getenv
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tearDown(program):
    """Tears down the app context"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Loads a 404 page"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=int(getenv('HBNB_API_PORT', default=5000))
    )
