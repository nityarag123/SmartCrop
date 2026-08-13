"""Dashboard aggregation API."""
from flask import Blueprint, request

from ..models.db import get_store
from ..models.users import public_user
from ..services.weather_service import get_current, get_forecast, farming_advice
from ..utils.helpers import ok, login_required, current_user

bp = Blueprint("api_dashboard", __name__)


@bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    user = current_user()
    store = get_store()

    location = user.get("location") or ""
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    used_geo = not location and lat is not None and lon is not None

    weather = None
    forecast = []
    weather_advice = []
    if used_geo:
        weather = get_current("", lat=lat, lon=lon)
        forecast = get_forecast("", lat=lat, lon=lon)
        weather_advice = farming_advice(weather, forecast)
    elif location:
        weather = get_current(location)
        forecast = get_forecast(location)
        weather_advice = farming_advice(weather, forecast)

    soil = store.find_one("soil_reports", {"user_id": user["id"]}, sort=[("created_at", -1)])
    crop = store.find_one("crop_recommendations", {"user_id": user["id"]}, sort=[("created_at", -1)])
    pest = store.find_one("pest_reports", {"user_id": user["id"]}, sort=[("created_at", -1)])
    calendar = store.find_one("crop_calendar", {"user_id": user["id"]})

    notifications = []
    if not location and not used_geo:
        notifications.append({"type": "setup", "icon": "📍", "text": "Add your location to get weather-based guidance."})
    else:
        for tip in weather_advice[:2]:
            notifications.append({"type": "weather", "icon": "🌦", "text": tip})
    if not user.get("soil_info"):
        notifications.append({"type": "soil", "icon": "🧪", "text": "Add your soil values to unlock crop recommendations."})
    if not calendar:
        notifications.append({"type": "calendar", "icon": "📅", "text": "Set up your crop calendar to get reminders."})

    return ok({
        "user": public_user(user),
        "weather": weather,
        "weather_advice": weather_advice,
        "used_geo": used_geo,
        "soil": soil,
        "crop": crop,
        "pest": pest,
        "calendar": calendar,
        "notifications": notifications,
    })
