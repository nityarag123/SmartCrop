"""Farmer profile / farm management APIs."""
from flask import Blueprint, request

from ..models import users
from ..utils.helpers import ok, error, login_required, current_user

bp = Blueprint("api_profile", __name__)


@bp.route("/profile", methods=["GET"])
@login_required
def get_profile():
    user = current_user()
    if not user:
        return error("User not found", 404)
    return ok({"user": users.public_user(user)})


@bp.route("/profile", methods=["PUT"])
@login_required
def update_profile():
    data = request.get_json(silent=True) or {}
    user = current_user()
    if not user:
        return error("User not found", 404)

    updated = users.update_user(
        user["id"],
        name=data.get("name"),
        phone=data.get("phone"),
        location=data.get("location"),
        state=data.get("state"),
        district=data.get("district"),
        language=data.get("language"),
        farm_size=data.get("farm_size"),
        soil_info=data.get("soil_info"),
        current_crop=data.get("current_crop"),
        irrigation=data.get("irrigation"),
    )
    if updated is None:
        updated = user
    return ok({"message": "Profile updated successfully.", "user": users.public_user(updated)})
