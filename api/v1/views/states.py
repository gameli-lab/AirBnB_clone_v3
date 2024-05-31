#!/usr/bin/python3
"""
View for State objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """
    Gets all states.
    """
    objs = []
    for state in storage.all(State).values():
        objs.append(state.to_dict())
    return jsonify(objs)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    Gets a state by id.
    """
    for state in storage.all(State).values():
        if state_id == state.id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route(
        "/states/<state_id>", methods=["DELETE"], strict_slashes=False
        )
def del_state(state_id):
    """
    Deletes a particular state.
    """
    for state in storage.all(State).values():
        if state_id == state.id:
            storage.delete(state)
            storage.save()
            return jsonify({})
    abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Creates a new state.
    """
    state_json_obj = request.get_json(silent=True)
    if not state_json_obj:
        abort(400, description="Not a JSON")
    if "name" not in state_json_obj:
        abort(400, description="Missing name")
    new_state = State(**state_json_obj)
    new_state.save()
    return make_response(
            jsonify(new_state.to_dict()), 201
            )


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    Updates an already existing state.
    """
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    state_json_obj = request.get_json(silent=True)
    if not state_json_obj:
        abort(400, description="Not a JSON")
    for key, value in state_json_obj.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, value)
    storage.save()
    return make_response(
            jsonify(state_obj.to_dict()), 200
            )
