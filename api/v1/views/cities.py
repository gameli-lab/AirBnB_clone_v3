#!/usr/bin/python3
"""View for city objects"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route(
        "/states/<state_id>/cities", methods=["GET"], strict_slashes=False
        )
def all_cities(state_id):
    """
    Retrieves list of all city objects of a states

    Args:
        state_id(City): id of state in city model
    """
    cityList = []
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    for city_obj in state_obj.cities:
        cityList.append(city_obj.to_dict())
    return jsonify(cityList)


@app_views.route(
        "/cities/<city_id>", methods=["GET"], strict_slashes=False
        )
def city_by_id(city_id):
    """
    Retrieves a city object

    Args:
        city_id(City): id of city object
    """

    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route(
        "/cities/<city_id>", methods=["DELETE"], strict_slashes=False
        )
def remove_city(city_id):
    """
    Deletes a city object

    Args:
        city_id(City): id of city object
    """
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({})


@app_views.route(
        "/states/<state_id>/cities", methods=["POST"], strict_slashes=False
        )
def create_city(state_id):
    """
    Creates a city object

    Args:
        state_id(State): id of city object
    """
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    city_json_obj = request.get_json()
    if not city_json_obj:
        abort(400, description="Not a JSON")
    if 'name' not in city_json_obj:
        abort(400, description="Missing name")

    new_obj = City(**city_json_obj)
    new_obj.state_id = state_id
    new_obj.save()
    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route(
        "/cities/<city_id>", methods=["PUT"], strict_slashes=False
        )
def update_city(city_id):
    """
    Updates a city object

    Args:
        city_id(City): id of city object
    """
    city_json_obj = request.get_json()
    if city_json_obj is None:
        abort(400, description="Not a JSON")
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)
    for key, value in city_json_obj.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict())
