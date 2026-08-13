"""MongoDB Atlas connection helper."""
import os

from pymongo import MongoClient


def build_uri():
    """Build a MongoDB connection URI from environment variables."""
    uri = os.getenv("MONGODB_URI")
    if uri:
        return uri
    username = os.getenv("MONGODB_ATLAS_USERNAME")
    password = os.getenv("MONGODB_ATLAS_PASSWORD")
    cluster = os.getenv("MONGODB_ATLAS_CLUSTER")
    if username and password and cluster:
        return (
            f"mongodb+srv://{username}:{password}@{cluster}"
            "?retryWrites=true&w=majority"
        )
    return None


def get_db_name():
    return os.getenv("DATABASE_NAME") or os.getenv("MONGODB_DB_NAME") or "smartcrop"


_client = None


def get_client():
    global _client
    if _client is not None:
        return _client
    uri = build_uri()
    if not uri:
        return None
    try:
        _client = MongoClient(uri, serverSelectionTimeoutMS=4000, connect=False)
        return _client
    except Exception:
        return None
