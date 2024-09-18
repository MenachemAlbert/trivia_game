from dataclasses import asdict

from flask import Blueprint, jsonify, abort, request

from models.User import User
from repository.user_repository import find_all_users, find_user_by_id, create_user, delete_user, update_user

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/", methods=['GET'])
def get_all():
    users = list(map(asdict, find_all_users()))
    return jsonify(users), 200


@user_blueprint.route("/<int:id_user>", methods=['GET'])
def get_user(id_user):
    user = find_user_by_id(id_user)
    if user:
        return jsonify(asdict(user)), 200
    else:
        return abort(404, description="User not found")


@user_blueprint.route("/", methods=['POST'])
def create_new_user():
    data = request.json
    if not data or not all(k in data for k in ("first", "last", "email")):
        return abort(400, description="Invalid data")
    user = User(first=data["first"], last=data["last"], email=data["email"])
    new_id = create_user(user)
    return jsonify({"id": new_id}), 201


@user_blueprint.route("/<int:id_user>", methods=['DELETE'])
def delete_existing_user(id_user):
    user = find_user_by_id(id_user)
    if not user:
        return abort(404, description="User not found")
    delete_user(id_user)
    return '', 204


@user_blueprint.route("/<int:id_user>", methods=['PUT'])
def update_existing_user(id_user):
    user = find_user_by_id(id_user)
    if not user:
        return abort(404, description="User not found")
    data = request.json
    if not data or not all(k in data for k in ("first", "last", "email")):
        return abort(400, description="Invalid data")
    user.first = data["first"]
    user.last = data["last"]
    user.email = data["email"]
    updated_user = update_user(user)
    return jsonify(asdict(updated_user)), 200
