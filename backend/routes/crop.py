"""Crop recommendation APIs."""
from flask import Blueprint, request

from ..ml.crop_recommendation.model import recommend_crop
from ..models.db import get_store
from ..utils.helpers import ok, error, login_required, current_user

bp = Blueprint("api_crop", __name__)


@bp.route("/crop/recommend", methods=["POST"])
@login_required
def recommend():
    data = request.get_json(silent=True) or {}
    result, status = recommend_crop(data)
    if status != 200:
        return error(result["error"], status)

    user = current_user()
    if user:
        get_store().insert("crop_recommendations", {
            "user_id": user["id"],
            "inputs": result["inputs"],
            "crop": result["crop"],
            "confidence": result["confidence"],
            "engine": result["engine"],
        })
    return ok(result)
