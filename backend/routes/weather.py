"""Weather APIs."""
from flask import Blueprint, request

from ..services.weather_service import get_current, get_forecast, farming_advice
from ..utils.helpers import ok, error

bp = Blueprint("api_weather", __name__)


def _params():
    """Return (location, lat, lon). Location may be empty when lat/lon are given."""
    location = (request.args.get("location") or "").strip()
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    has_coords = lat is not None and lon is not None
    if not location and not has_coords:
        return None, None, None
    return location, lat, lon


@bp.route("/weather", methods=["GET"])
def weather():
    location, lat, lon = _params()
    if location is None:
        return error("Location is required (state, district or city name)", 400)
    current = get_current(location, lat=lat, lon=lon)
    return ok(current)


@bp.route("/weather/forecast", methods=["GET"])
def forecast():
    location, lat, lon = _params()
    if location is None:
        return error("Location is required (state, district or city name)", 400)
    days = get_forecast(location, lat=lat, lon=lon)
    return ok({"location": location, "days": days, "demo": any(d.get("demo") for d in days)})


@bp.route("/weather/advice", methods=["GET"])
def advice():
    location, lat, lon = _params()
    if location is None:
        return error("Location is required", 400)
    current = get_current(location, lat=lat, lon=lon)
    days = get_forecast(location, lat=lat, lon=lon)
    return ok({
        "location": location,
        "demo": current.get("demo", False),
        "advice": farming_advice(current, days),
    })
