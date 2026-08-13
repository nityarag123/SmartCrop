"""Crop calendar APIs.

GET /api/calendar returns the knowledge-base timeline for a crop+season.
POST /api/calendar saves a farmer's chosen crop + season and returns a reminder
timeline with week numbers.
"""
from flask import Blueprint, request

from ..seed import CROP_CALENDAR_KB
from ..models.db import get_store
from ..utils.helpers import ok, error, login_required, current_user

bp = Blueprint("api_calendar", __name__)


def _canonical_crop(name):
    if not name:
        return None
    target = name.strip().lower()
    for key in CROP_CALENDAR_KB:
        if key in target or target in key:
            return key
    return None


@bp.route("/calendar", methods=["GET"])
@login_required
def get_calendar():
    crop = request.args.get("crop", "").strip().lower()
    season = request.args.get("season", "").strip().lower()

    user = current_user()
    saved = None
    if user:
        saved = get_store().find_one("crop_calendar", {"user_id": user["id"]})

    key = _canonical_crop(crop) or (saved or {}).get("crop") or "rice"
    season = season or (saved or {}).get("season") or "kharif"
    entry = CROP_CALENDAR_KB.get(key)

    if not entry:
        return error("Crop calendar not available for that crop.", 404)

    seasons = entry.get("seasons", [])
    if season not in seasons:
        season = seasons[0]

    return ok({
        "crop": key,
        "display_name": key.title(),
        "season": season,
        "seasons": seasons,
        "soil": entry.get("soil", ""),
        "phases": entry.get("phases", []),
        "saved": saved,
        "knowledge_base": True,
    })


@bp.route("/calendar", methods=["POST"])
@login_required
def save_calendar():
    data = request.get_json(silent=True) or {}
    crop = _canonical_crop(data.get("crop"))
    season = (data.get("season") or "kharif").strip().lower()
    if not crop:
        return error("Please choose a valid crop.", 400)
    entry = CROP_CALENDAR_KB.get(crop)
    if not entry:
        return error("Crop calendar not available for that crop.", 404)
    if season not in entry["seasons"]:
        season = entry["seasons"][0]

    user = current_user()
    get_store().update(
        "crop_calendar",
        {"user_id": user["id"]},
        {"crop": crop, "season": season},
        upsert=True,
    )
    return ok({"message": "Calendar saved. We will show reminders for your crop schedule.", "crop": crop, "season": season})
