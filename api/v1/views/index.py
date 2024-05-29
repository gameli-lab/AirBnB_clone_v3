#!/usr/bin/python3
"""
Contains routes for app_views blueprint.
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False)
def stat():
    """
    returns the status of the page in json format
    """
    return jsonify({
        "status": "OK"
        })


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def objects():
    """
    counts the number of objects
    """
    objs = {}
    classes = {
            "amenities": "amenities",
            "cities": "cities",
            "places": "places",
            "reviews": "reviews",
            "states": "states",
            "users": "users"
            }

    for class_name, class_property in classes.items():
        count = storage.count(class_name)
        objs[class_property] = count

    return jsonify(objs)


@app_views.route("/nop", strict_slashes=False)
def nop():
    """
    Handles 404 error
    """
    return jsonify({
        "error": "Not found"
        })
