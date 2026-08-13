"""Shared helpers: auth decorators, safe filenames, upload validation."""
import functools
import os
import re
import uuid

from flask import jsonify, session

from config import Config
from ..models.users import public_user, get_user_by_id


def login_required(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "Authentication required. Please log in."}), 401
        return fn(*args, **kwargs)
    return wrapper


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return get_user_by_id(user_id)


def api_current_user():
    user = current_user()
    if not user:
        return None
    return public_user(user)


def safe_filename(filename):
    name = os.path.basename(filename or "")
    name = re.sub(r"[^a-zA-Z0-9._-]", "_", name)
    if not name:
        name = "upload"
    return f"{uuid.uuid4().hex[:8]}_{name}"


def validate_image(file_storage):
    """Return (filename, error). Validates extension and that it is an image."""
    if file_storage is None or not file_storage.filename:
        return None, "No file provided"
    extension = file_storage.filename.rsplit(".", 1)[-1].lower() if "." in file_storage.filename else ""
    if extension not in Config.ALLOWED_IMAGE_EXTENSIONS:
        return None, "Only PNG, JPG, JPEG, WEBP or BMP images are allowed"
    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    if size > Config.MAX_CONTENT_LENGTH:
        return None, "Image is too large (max 10 MB)"
    if size == 0:
        return None, "The uploaded file is empty"
    return safe_filename(file_storage.filename), None


def ok(data, status=200):
    return jsonify(data), status


def error(message, status=400, code=None):
    body = {"error": message}
    if code:
        body["code"] = code
    return jsonify(body), status
