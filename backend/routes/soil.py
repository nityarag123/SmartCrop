"""Soil analysis APIs."""
import os

import numpy as np
from flask import Blueprint, request
from PIL import Image

from config import Config
from ..ml.soil_analysis.analyzer import analyze, visual_classification
from ..models.db import get_store
from ..utils.helpers import ok, error, login_required, current_user, validate_image

bp = Blueprint("api_soil", __name__)


@bp.route("/soil/analyze", methods=["POST"])
@login_required
def analyze_soil():
    data = request.get_json(silent=True) or {}
    result, status = analyze(data)
    if status != 200:
        return error(result["error"], status)

    user = current_user()
    if user:
        get_store().insert("soil_reports", {
            "user_id": user["id"],
            "engine": result["engine"],
            "overall": result["overall"],
            "ph": result["ph"],
            "nitrogen": result["nitrogen"],
            "phosphorus": result["phosphorus"],
            "potassium": result["potassium"],
        })
    return ok(result)


@bp.route("/soil/image", methods=["POST"])
@login_required
def analyze_soil_image():
    file = request.files.get("image")
    filename, error_msg = validate_image(file)
    if error_msg:
        return error(error_msg, 400)

    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
    filepath = os.path.join(Config.UPLOAD_DIR, filename)
    file.save(filepath)

    try:
        rgb = np.asarray(Image.open(filepath).convert("RGB"), dtype=np.float32)
        if rgb.size == 0:
            return error("Unable to read the uploaded image. Please upload a clearer photo.", 400)
        result = visual_classification(rgb, filename)
    except Exception as exc:
        return error(f"Unable to analyze the photo. Please upload a clear photo of soil. ({exc})", 500)
    finally:
        try:
            os.remove(filepath)
        except OSError:
            pass

    return ok(result)
