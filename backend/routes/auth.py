"""Authentication APIs."""
from flask import Blueprint, jsonify, request, session

from ..models import users
from ..utils.helpers import ok, error, current_user

bp = Blueprint("api_auth", __name__)


@bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    location = (data.get("location") or "").strip()
    state = (data.get("state") or "").strip()
    district = (data.get("district") or "").strip()
    language = data.get("language") or "en"

    if not name:
        return error("Please enter your full name", 400)
    if not email or "@" not in email:
        return error("Please enter a valid email address", 400)
    if len(password) < 6:
        return error("Password must be at least 6 characters", 400)

    try:
        user = users.create_user(name, email, password, location=location,
                                 language=language, state=state, district=district)
    except ValueError as exc:
        return error(str(exc), 409)

    session.clear()
    session["user_id"] = user["id"]
    return ok({
        "message": "Account created. Welcome to SmartCrop!",
        "created": True,
        "logged_in": True,
        "user": users.public_user(user),
    }, 201)


@bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if not email or not password:
        return error("Email and password are required", 400)

    user = users.authenticate(email, password)
    if not user:
        return error("Invalid email or password", 401)

    session.clear()
    session["user_id"] = user["id"]
    return ok({"message": "Welcome back!", "logged_in": True, "user": users.public_user(user)})


@bp.route("/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return ok({"message": "You have been signed out."})


@bp.route("/auth/me", methods=["GET"])
def me():
    user = current_user()
    if not user:
        return error("Not logged in", 401)
    return ok({"user": users.public_user(user)})


@bp.route("/auth/status", methods=["GET"])
def status():
    user = current_user()
    if not user:
        return ok({"logged_in": False})
    return ok({"logged_in": True, "user": users.public_user(user)})
