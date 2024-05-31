#!/usr/bin/python3
"""
View for Amenity objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route(
        "/amenities", methods=["GET"], strict_slashes=False
        )
def all_amenity():
    """
    Retrieves the list of all Amenity objects.
    """
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route(
        "/amenities/<amenity_id>", methods=["GET"], strict_slashes=False
        )
def amenity_by_id(amenity_id):
    """
    Retrieves a Amenity object.
    """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    return jsonify(amenity_obj.to_dict())


@app_views.route(
        "/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False
        )
def remove_amenity(amenity_id):
    """
    Deletes a Amenity object.
    """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    storage.delete(amenity_obj)
    storage.save()
    return jsonify({})


@app_views.route(
        "/amenities", methods=["POST"], strict_slashes=False
        )
def create_amenity():
    """
    Creates a Amenity object.
    """
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, description="Not a JSON")
    if "name" not in json_data:
        abort(400, description="Missing name")
    new_amenity_obj = Amenity(**json_data)
    new_amenity_obj.save()
    return make_response(
            jsonify(new_amenity_obj.to_dict()), 201
            )


@app_views.route(
        "/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False
        )
def update_amenity(amenity_id):
    """
    Updates an Amenity object
    """
    amenity_obj = storage.get(Amenity, amenity_id)
    if not amenity_obj:
        abort(404)
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, description="Not a JSON")
    for key, value in json_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity_obj, key, value)
    storage.save()
    return make_response(
            jsonify(amenity_obj.to_dict()), 200
            )
