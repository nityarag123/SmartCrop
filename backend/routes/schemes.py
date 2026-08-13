"""Government schemes API (Kisan Mitra)."""
from flask import Blueprint, request

from ..models.db import get_store
from ..utils.helpers import ok, error

bp = Blueprint("api_schemes", __name__)


@bp.route("/schemes", methods=["GET"])
def schemes():
    category = request.args.get("category", "").strip().lower()
    query = request.args.get("q", "").strip().lower()

    rows = get_store().find("government_schemes", sort=[("name", 1)])
    if category:
        rows = [r for r in rows if (r.get("category") or "").lower() == category]
    if query:
        rows = [
            r for r in rows
            if query in (r.get("name") or "").lower()
            or query in (r.get("summary") or "").lower()
            or query in (r.get("benefits") or "").lower()
        ]
    if not rows:
        return error("No schemes found for those filters.", 404)
    return ok({"schemes": rows})


@bp.route("/schemes/<code>", methods=["GET"])
def scheme_detail(code):
    row = get_store().find_one("government_schemes", {"code": code})
    if not row:
        return error("Scheme not found.", 404)
    return ok({"scheme": row})
