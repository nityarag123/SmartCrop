"""SmartCrop database layer.

MongoDB Atlas is the primary store. When MongoDB is not configured or is
unreachable, SmartCrop transparently falls back to a local JSON file so every
feature keeps working for demos, tests and development.

Collections: users, farms, chat_history, soil_reports, crop_recommendations,
pest_reports, crop_calendar, government_schemes, notifications.
"""
import json
import os
import threading
import uuid
from datetime import datetime

from . import mongo

_JSON_LOCK = threading.Lock()

COLLECTIONS = (
    "users",
    "farms",
    "chat_history",
    "soil_reports",
    "crop_recommendations",
    "pest_reports",
    "crop_calendar",
    "government_schemes",
    "notifications",
)


def _utcnow():
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _new_id():
    return str(uuid.uuid4())


class FileStore:
    """A small JSON-backed store with a MongoDB-like API."""

    def __init__(self, path):
        self.path = path
        self._ensure()

    def _ensure(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with _JSON_LOCK:
                if not os.path.exists(self.path):
                    with open(self.path, "w", encoding="utf-8") as fh:
                        json.dump({c: [] for c in COLLECTIONS}, fh)

    def _load(self):
        with _JSON_LOCK:
            with open(self.path, "r", encoding="utf-8") as fh:
                return json.load(fh)

    def _save(self, data):
        with _JSON_LOCK:
            with open(self.path, "w", encoding="utf-8") as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)

    def insert(self, collection, document):
        data = self._load()
        doc = dict(document)
        doc.setdefault("_id", _new_id())
        doc.setdefault("created_at", _utcnow())
        data.setdefault(collection, []).append(doc)
        self._save(data)
        return doc

    def find(self, collection, query=None, sort=None, limit=0):
        query = query or {}
        data = self._load().get(collection, [])
        rows = []
        for doc in data:
            if all(_matches(doc, key, value) for key, value in query.items()):
                rows.append(dict(doc))
        if sort:
            for key, direction in reversed(list(sort)):
                rows.sort(key=lambda r: _sort_key(r, key), reverse=(direction == -1))
        if limit:
            rows = rows[:limit]
        return rows

    def find_one(self, collection, query=None, sort=None):
        rows = self.find(collection, query, sort=sort, limit=1)
        return rows[0] if rows else None

    def update(self, collection, query, update, upsert=False):
        data = self._load()
        docs = data.setdefault(collection, [])
        updated = 0
        for doc in docs:
            if all(_matches(doc, key, value) for key, value in query.items()):
                doc.update(update)
                doc.setdefault("updated_at", _utcnow())
                updated += 1
        if updated == 0 and upsert:
            doc = dict(query)
            doc.update(update)
            doc.setdefault("_id", _new_id())
            doc.setdefault("created_at", _utcnow())
            docs.append(doc)
            updated = 1
        self._save(data)
        return updated

    def delete(self, collection, query):
        data = self._load()
        docs = data.setdefault(collection, [])
        remaining = [
            doc for doc in docs
            if not all(_matches(doc, key, value) for key, value in query.items())
        ]
        deleted = len(docs) - len(remaining)
        data[collection] = remaining
        self._save(data)
        return deleted

    def insert_many(self, collection, documents):
        inserted = [self.insert(collection, doc) for doc in documents]
        return inserted

    def replace(self, collection, query, document):
        self.delete(collection, query)
        return self.insert(collection, document)


def _matches(doc, key, value):
    if key not in doc:
        return False
    if isinstance(value, dict) and set(value.keys()) == {"$ne"}:
        return doc[key] != value["$ne"]
    return doc[key] == value


def _sort_key(doc, key):
    value = doc.get(key)
    if isinstance(value, (int, float)):
        return value
    return str(value or "")


class MongoStore:
    """Real MongoDB Atlas store."""

    def __init__(self, client, db_name):
        self.db = client[db_name]

    def insert(self, collection, document):
        doc = dict(document)
        doc.setdefault("_id", _new_id())
        doc.setdefault("created_at", _utcnow())
        self.db[collection].insert_one(doc)
        return doc

    def find(self, collection, query=None, sort=None, limit=0):
        query = query or {}
        cursor = self.db[collection].find(query, {"_id": 0})
        if sort:
            cursor = cursor.sort([(key, direction) for key, direction in sort])
        if limit:
            cursor = cursor.limit(limit)
        return [dict(item) for item in cursor]

    def find_one(self, collection, query=None, sort=None):
        query = query or {}
        cursor = self.db[collection].find(query, {"_id": 0})
        if sort:
            cursor = cursor.sort([(key, direction) for key, direction in sort])
        item = cursor.limit(1).next() if cursor.count() else None
        return dict(item) if item else None

    def update(self, collection, query, update, upsert=False):
        result = self.db[collection].update_many(query, {"$set": update}, upsert=upsert)
        if result.upserted_id is not None:
            return 1
        return result.modified_count

    def delete(self, collection, query):
        return self.db[collection].delete_many(query).deleted_count

    def insert_many(self, collection, documents):
        docs = [dict(d) for d in documents]
        for doc in docs:
            doc.setdefault("_id", _new_id())
            doc.setdefault("created_at", _utcnow())
        self.db[collection].insert_many(docs)
        return docs

    def replace(self, collection, query, document):
        self.db[collection].replace_one(query, document, upsert=True)
        return document


_store = None
_available = False


def init_store(use_fallback=True, store_path=None):
    """Build the active store. Prefers MongoDB Atlas when reachable."""
    global _store, _available
    client = mongo.get_client()
    if client is not None:
        try:
            client.admin.command("ping")
            _store = MongoStore(client, mongo.get_db_name())
            _available = True
            return _store
        except Exception:
            pass
    if not use_fallback:
        raise RuntimeError("MongoDB Atlas is not reachable and local fallback is disabled")
    _store = FileStore(store_path)
    _available = False
    return _store


def get_store():
    if _store is None:
        from config import Config
        init_store(Config.USE_LOCAL_FALLBACK, Config.LOCAL_STORE_PATH)
    return _store


def is_mongodb():
    return _available


def get_storage_label():
    if is_mongodb():
        return "MongoDB Atlas"
    return "local storage (MongoDB not connected)"
