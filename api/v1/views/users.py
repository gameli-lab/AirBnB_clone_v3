#!/usr/bin/python3
"""
View for all User objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route(
        "/users", methods=["GET"], strict_slashes=False
        )
def all_users():
    """
    Retrieves the list of all User objects
    """
    users = []
    for user in storage.all(User).values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route(
        "/users/<user_id>", methods=["GET"], strict_slashes=False
        )
def user_by_id(user_id):
    """
    Retrieves a User object by id.
    """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    return jsonify(user_obj.to_dict())


@app_views.route(
        "/users/<user_id>", methods=["DELETE"], strict_slashes=False
        )
def remove_user(user_id):
    """
    Deletes a User object by id.
    """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    storage.delete(user_obj)
    storage.save()
    return jsonify({})


@app_views.route(
        "/users", methods=["POST"], strict_slashes=False
        )
def create_user():
    """
    Creates a new user object.
    """
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, description="Not a JSON")
    if "email" not in json_data:
        abort(400, description="Missing email")
    if "password" not in json_data:
        abort(400, description="Missing password")
    new_user_obj = User(**json_data)
    new_user_obj.save()
    return make_response(
            jsonify(new_user_obj.to_dict()), 201
            )


@app_views.route(
        "users/<user_id>", methods=["PUT"], strict_slashes=False
        )
def update_user(user_id):
    """
    Updates User object of a particular id.
    """
    user_obj = storage.get(User, user_id)
    if not user_obj:
        abort(404)
    json_data = request.get_json(silent=True)
    if not json_data:
        abort(400, description="Not a JSON")
    for key, value in json_data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user_obj, key, value)
    storage.save()
    return make_response(
            jsonify(user_obj.to_dict()), 200
            )
