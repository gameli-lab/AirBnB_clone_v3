#!/usr/bin/python3
"""A module for a flask application."""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
import os


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def close_conn(exception):
    """closes connection to storage

    Args:
        exception(Exception): exception that occurs.
    """
    storage.close()


@app.errorhandler(404)
def page_not_found():
    """Handles 404 error."""
    content = jsonify({
        "error": "Not found"
        })
    return make_response(content, 404)


if __name__ == "__main__":
    """runs the application with the specified config"""
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True)
