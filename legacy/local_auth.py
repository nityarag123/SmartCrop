import json
from pathlib import Path


LOCAL_USERS_PATH = Path(__file__).resolve().parent / "instance" / "local_users.json"


def _ensure_store():
    LOCAL_USERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not LOCAL_USERS_PATH.exists():
        LOCAL_USERS_PATH.write_text("[]", encoding="utf-8")


def _load_users():
    _ensure_store()
    with LOCAL_USERS_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def _save_users(users):
    _ensure_store()
    with LOCAL_USERS_PATH.open("w", encoding="utf-8") as file:
        json.dump(users, file, indent=2)


def create_user(name, email, password_hash, role="farmer", language="en"):
    users = _load_users()
    normalized_email = email.strip().lower()

    if any(user["email"] == normalized_email for user in users):
        raise ValueError("Email already registered")

    next_id = max((user["id"] for user in users), default=0) + 1
    user = {
        "id": next_id,
        "name": name or "",
        "email": normalized_email,
        "password_hash": password_hash,
        "role": role,
        "language": language,
    }
    users.append(user)
    _save_users(users)
    return user


def get_user_by_email(email):
    normalized_email = (email or "").strip().lower()
    return next((user for user in _load_users() if user["email"] == normalized_email), None)


def get_user_by_id(user_id):
    return next((user for user in _load_users() if user["id"] == user_id), None)


def update_user(user_id, **fields):
    users = _load_users()
    for user in users:
        if user["id"] == user_id:
            user.update(fields)
            _save_users(users)
            return user
    return None
