"""Helpers for reading/writing users via the active store."""
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_store


def public_user(user):
    """Return a safe user dict without password hashes or internal ids."""
    if not user:
        return None
    return {
        "id": user.get("id") or user.get("_id"),
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "phone": user.get("phone", ""),
        "location": user.get("location", ""),
        "state": user.get("state", ""),
        "district": user.get("district", ""),
        "language": user.get("language", "en"),
        "farm_size": user.get("farm_size", ""),
        "soil_info": user.get("soil_info", ""),
        "current_crop": user.get("current_crop", ""),
        "irrigation": user.get("irrigation", ""),
        "role": user.get("role", "farmer"),
        "created_at": user.get("created_at", ""),
    }


def create_user(name, email, password, phone="", location="", language="en",
                state="", district=""):
    store = get_store()
    email = (email or "").strip().lower()
    if store.find_one("users", {"email": email}):
        raise ValueError("An account with this email already exists")
    user = {
        "id": _next_user_id(store),
        "name": (name or "").strip(),
        "email": email,
        "phone": (phone or "").strip(),
        "password_hash": generate_password_hash(password),
        "location": (location or "").strip(),
        "state": (state or "").strip(),
        "district": (district or "").strip(),
        "language": language,
        "role": "farmer",
        "farm_size": "",
        "soil_info": "",
        "current_crop": "",
        "irrigation": "",
    }
    return store.insert("users", user)


def _next_user_id(store):
    ids = [u.get("id", 0) for u in store.find("users")]
    return max(ids, default=0) + 1


def get_user_by_email(email):
    return get_store().find_one("users", {"email": (email or "").strip().lower()})


def get_user_by_id(user_id):
    store = get_store()
    user = store.find_one("users", {"id": user_id})
    if not user:
        user = store.find_one("users", {"_id": user_id})
    return user


def authenticate(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None


def update_user(user_id, **fields):
    allowed = {
        "name", "phone", "location", "state", "district", "language",
        "farm_size", "soil_info", "current_crop", "irrigation",
    }
    payload = {k: v for k, v in fields.items() if k in allowed and v is not None}
    if not payload:
        return None
    get_store().update("users", {"id": user_id}, payload)
    return get_user_by_id(user_id)
