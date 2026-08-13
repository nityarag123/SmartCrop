import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()


def _build_mongodb_uri():
    uri = os.getenv("MONGODB_URI")
    if uri:
        return uri

    username = os.getenv("MONGODB_ATLAS_USERNAME")
    password = os.getenv("MONGODB_ATLAS_PASSWORD")
    cluster = os.getenv("MONGODB_ATLAS_CLUSTER")
    database = os.getenv("MONGODB_DB_NAME", "smartcrop")

    if username and password and cluster:
        return (
            f"mongodb+srv://{username}:{password}@{cluster}/{database}"
            "?retryWrites=true&w=majority"
        )

    return None


def is_configured():
    return _build_mongodb_uri() is not None


def _get_collection():
    uri = _build_mongodb_uri()
    if not uri:
        raise RuntimeError("MongoDB Atlas is not configured")

    database_name = os.getenv("MONGODB_DB_NAME", "smartcrop")
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    return client, client[database_name]["users"]


def create_user(name, email, password_hash, role="farmer", language="en"):
    client, collection = _get_collection()
    try:
        normalized_email = (email or "").strip().lower()
        if collection.find_one({"email": normalized_email}):
            raise ValueError("Email already registered")

        next_user = collection.find_one(sort=[("id", -1)])
        next_id = (next_user or {}).get("id", 0) + 1
        user = {
            "id": next_id,
            "name": name or "",
            "email": normalized_email,
            "password_hash": password_hash,
            "role": role,
            "language": language,
        }
        collection.insert_one(user)
        return user
    except PyMongoError as exc:
        raise RuntimeError(f"MongoDB operation failed: {exc}") from exc
    finally:
        client.close()


def get_user_by_email(email):
    client, collection = _get_collection()
    try:
        return collection.find_one({"email": (email or "").strip().lower()}, {"_id": 0})
    except PyMongoError as exc:
        raise RuntimeError(f"MongoDB operation failed: {exc}") from exc
    finally:
        client.close()


def get_user_by_id(user_id):
    client, collection = _get_collection()
    try:
        return collection.find_one({"id": user_id}, {"_id": 0})
    except PyMongoError as exc:
        raise RuntimeError(f"MongoDB operation failed: {exc}") from exc
    finally:
        client.close()


def update_user(user_id, **fields):
    client, collection = _get_collection()
    try:
        if "email" in fields and fields["email"]:
            fields["email"] = fields["email"].strip().lower()

        update_result = collection.update_one({"id": user_id}, {"$set": fields})
        if not update_result.matched_count:
            return None
        return collection.find_one({"id": user_id}, {"_id": 0})
    except PyMongoError as exc:
        raise RuntimeError(f"MongoDB operation failed: {exc}") from exc
    finally:
        client.close()
