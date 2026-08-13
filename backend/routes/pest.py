"""Pest / plant-disease detection API."""
import os

import numpy as np
from flask import Blueprint, request
from PIL import Image

from config import Config
from ..ml.pest_detection import classifier
from ..models.db import get_store
from ..utils.helpers import ok, error, login_required, current_user, validate_image

bp = Blueprint("api_pest", __name__)


@bp.route("/pest/detect", methods=["POST"])
@login_required
def detect():
    file = request.files.get("image")
    filename, error_msg = validate_image(file)
    if error_msg:
        return error(error_msg, 400)

    if not classifier.is_pest_model_available():
        return error(
            "Pest detection model is not trained. "
            "Run `python -m backend.ml.pest_detection.train` and try again.",
            503,
        )

    os.makedirs(Config.UPLOAD_DIR, exist_ok=True)
    filepath = os.path.join(Config.UPLOAD_DIR, filename)
    file.save(filepath)

    try:
        rgb = np.asarray(Image.open(filepath).convert("RGB"), dtype=np.float32)
        if rgb.size == 0:
            return error("Unable to read the uploaded image. Please upload a clearer image.", 400)
        result, confidence = classifier.detect_from_image(rgb)
        result["image"] = filename
    except Exception as exc:
        return error(f"Unable to analyze image. Please upload a clearer image. ({exc})", 500)
    finally:
        try:
            os.remove(filepath)
        except OSError:
            pass

    user = current_user()
    if user:
        get_store().insert("pest_reports", {
            "user_id": user["id"],
            "label": result.get("label"),
            "category": result.get("category"),
            "confidence": result.get("confidence"),
            "engine": result.get("engine"),
        })
    return ok(result)
