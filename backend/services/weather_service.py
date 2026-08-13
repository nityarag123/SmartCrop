"""Weather service.

Primary source: Open-Meteo (https://open-meteo.com) — free, no API key, real
forecast data with built-in geocoding. Secondary: OpenWeatherMap when a
``WEATHER_API_KEY`` is set (the key never reaches the browser). When neither
works the service returns clearly-labelled demo data and never claims it is
live.
"""
import os
from datetime import datetime, timedelta

import requests

API_KEY = os.getenv("WEATHER_API_KEY")
OWM_BASE = "https://api.openweathermap.org/data/2.5"

OM_GEO = "https://geocoding-api.open-meteo.com/v1/search"
OM_FORECAST = "https://api.open-meteo.com/v1/forecast"

# Open-Meteo WMO weather codes -> (condition, description, icon)
_WMO = {
    0: ("Clear", "clear sky", "01d"),
    1: ("Mainly clear", "mainly clear", "01d"),
    2: ("Partly cloudy", "partly cloudy", "02d"),
    3: ("Overcast", "overcast clouds", "04d"),
    45: ("Fog", "fog", "50d"),
    48: ("Fog", "depositing rime fog", "50d"),
    51: ("Drizzle", "light drizzle", "09d"),
    53: ("Drizzle", "moderate drizzle", "09d"),
    55: ("Drizzle", "dense drizzle", "09d"),
    56: ("Freezing drizzle", "light freezing drizzle", "09d"),
    57: ("Freezing drizzle", "dense freezing drizzle", "09d"),
    61: ("Rain", "slight rain", "10d"),
    63: ("Rain", "moderate rain", "10d"),
    65: ("Rain", "heavy rain", "10d"),
    66: ("Freezing rain", "light freezing rain", "10d"),
    67: ("Freezing rain", "heavy freezing rain", "10d"),
    71: ("Snow", "slight snow fall", "13d"),
    73: ("Snow", "moderate snow fall", "13d"),
    75: ("Snow", "heavy snow fall", "13d"),
    77: ("Snow grains", "snow grains", "13d"),
    80: ("Rain showers", "slight rain showers", "09d"),
    81: ("Rain showers", "moderate rain showers", "09d"),
    82: ("Rain showers", "violent rain showers", "09d"),
    85: ("Snow showers", "slight snow showers", "13d"),
    86: ("Snow showers", "heavy snow showers", "13d"),
    95: ("Thunderstorm", "thunderstorm", "11d"),
    96: ("Thunderstorm", "thunderstorm with slight hail", "11d"),
    99: ("Thunderstorm", "thunderstorm with heavy hail", "11d"),
}


def _wmo(code):
    return _WMO.get(int(code), ("Cloudy", "cloudy", "03d"))


def _demo_current(location):
    return {
        "location": location or "Sample Village",
        "temperature": 29.4,
        "feels_like": 30.2,
        "humidity": 66,
        "wind_speed": 3.1,
        "condition": "Partly cloudy",
        "description": "partly cloudy",
        "rain_probability": 20,
        "rainfall": 120,
        "icon": "02d",
        "demo": True,
    }


def _demo_forecast():
    days = []
    conditions = [
        ("Partly cloudy", "partly cloudy", 20, 29.4, 66, "02d"),
        ("Light rain", "light rain", 70, 27.8, 78, "10d"),
        ("Cloudy", "overcast clouds", 40, 28.9, 72, "04d"),
        ("Sunny", "clear sky", 10, 31.2, 58, "01d"),
        ("Scattered clouds", "scattered clouds", 15, 30.1, 61, "03d"),
    ]
    for index, (condition, description, rain, temp, humidity, icon) in enumerate(conditions):
        days.append({
            "date": (datetime.now() + timedelta(days=index + 1)).strftime("%Y-%m-%d"),
            "condition": condition,
            "description": description,
            "rain_probability": rain,
            "temp_max": temp,
            "temp_min": temp - 4,
            "humidity": humidity,
            "wind_speed": 3.0,
            "icon": icon,
            "demo": True,
        })
    return days


# ---------------------------------------------------------------- Open-Meteo
def _geocode(location):
    """Resolve a place name to (lat, lon, display label)."""
    try:
        response = requests.get(
            OM_GEO, params={"name": location, "count": 1, "language": "en"}, timeout=10
        )
        if response.status_code != 200:
            return None
        results = (response.json() or {}).get("results") or []
        if not results:
            return None
        r = results[0]
        name = r.get("name") or location
        region = r.get("admin1") or ""
        country = r.get("country") or ""
        label = ", ".join(x for x in [name, region, country] if x) or location
        return float(r["latitude"]), float(r["longitude"]), label
    except (requests.RequestException, ValueError, KeyError, TypeError):
        return None


def _om_fetch(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,rain,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
        "timezone": "auto",
        "forecast_days": "7",
    }
    response = requests.get(OM_FORECAST, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def _om_current(data, label):
    c = data.get("current") or {}
    daily = data.get("daily") or {}
    condition, description, icon = _wmo(c.get("weather_code"))
    precip = daily.get("precipitation_probability_max")
    rain_prob = int(precip[0]) if precip and precip[0] is not None else 0
    return {
        "location": label,
        "temperature": c.get("temperature_2m"),
        "feels_like": c.get("apparent_temperature"),
        "humidity": c.get("relative_humidity_2m"),
        "wind_speed": c.get("wind_speed_10m"),
        "condition": condition,
        "description": description,
        "rain_probability": rain_prob,
        "rainfall": c.get("rain") or 0,
        "icon": icon,
        "demo": False,
        "source": "Open-Meteo",
    }


def _om_forecast(data, label):
    daily = data.get("daily") or {}
    times = daily.get("time") or []
    days = []
    codes = daily.get("weather_code") or []
    for i in range(len(times)):
        condition, description, icon = _wmo(codes[i] if i < len(codes) else 0)
        precip = daily.get("precipitation_probability_max") or []
        rain_prob = int(precip[i]) if i < len(precip) and precip[i] is not None else 0
        days.append({
            "date": times[i],
            "condition": condition,
            "description": description,
            "rain_probability": rain_prob,
            "temp_max": (daily.get("temperature_2m_max") or [None])[i],
            "temp_min": (daily.get("temperature_2m_min") or [None])[i],
            "humidity": None,
            "wind_speed": None,
            "icon": icon,
            "demo": False,
        })
    return days


def _resolve(location, lat, lon):
    """Return (lat, lon, label) using coords or geocoded location."""
    if lat is not None and lon is not None:
        return float(lat), float(lon), location or "Your location"
    if location:
        resolved = _geocode(location)
        if resolved:
            return resolved[0], resolved[1], resolved[2]
    return None


# --------------------------------------------------------------- OpenWeatherMap
def _owm_current(location, lat, lon):
    params = {"appid": API_KEY, "units": "metric"}
    if lat is not None and lon is not None:
        params["lat"] = float(lat)
        params["lon"] = float(lon)
    else:
        params["q"] = location
    response = requests.get(f"{OWM_BASE}/weather", params=params, timeout=8)
    if response.status_code != 200:
        return None
    data = response.json()
    rain = 0
    if data.get("rain") and isinstance(data["rain"], dict):
        rain = round(data["rain"].get("1h", 0) / 10, 0)
    elif "clouds" in data:
        rain = max(0, round((data["clouds"].get("all", 0) - 60) * 0.5))
    return {
        "location": data.get("name", location or "Your location"),
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "rain_probability": min(100, int(rain)),
        "rainfall": round(float(rain), 1),
        "icon": data["weather"][0]["icon"],
        "demo": False,
        "source": "OpenWeatherMap",
    }


def _owm_forecast(location, lat, lon):
    params = {"appid": API_KEY, "units": "metric"}
    if lat is not None and lon is not None:
        params["lat"] = float(lat)
        params["lon"] = float(lon)
    else:
        params["q"] = location
    response = requests.get(f"{OWM_BASE}/forecast", params=params, timeout=8)
    if response.status_code != 200:
        return None
    data = response.json()
    days = []
    seen = set()
    for item in data.get("list", []):
        day = item["dt_txt"][:10]
        if day in seen:
            continue
        seen.add(day)
        rain = 0
        if item.get("rain") and isinstance(item["rain"], dict):
            rain = item["rain"].get("3h", 0) / 10
        days.append({
            "date": day,
            "condition": item["weather"][0]["main"],
            "description": item["weather"][0]["description"],
            "rain_probability": min(100, int(rain * 100 / 8) if rain else 0),
            "temp_max": item["main"]["temp_max"],
            "temp_min": item["main"]["temp_min"],
            "humidity": item["main"]["humidity"],
            "wind_speed": item["wind"]["speed"],
            "icon": item["weather"][0]["icon"],
            "demo": False,
        })
        if len(days) >= 5:
            break
    return days


def get_current(location, lat=None, lon=None):
    resolved = _resolve(location, lat, lon)
    if resolved:
        rlat, rlon, label = resolved
        try:
            return _om_current(_om_fetch(rlat, rlon), label)
        except (requests.RequestException, ValueError, KeyError, TypeError):
            pass
        if API_KEY:
            try:
                current = _owm_current(location, lat, lon)
                if current:
                    return current
            except (requests.RequestException, ValueError, KeyError, TypeError):
                pass
    return _demo_current(location or "Your location")


def get_forecast(location, lat=None, lon=None):
    resolved = _resolve(location, lat, lon)
    if resolved:
        rlat, rlon, label = resolved
        try:
            return _om_forecast(_om_fetch(rlat, rlon), label)
        except (requests.RequestException, ValueError, KeyError, TypeError):
            pass
        if API_KEY:
            try:
                days = _owm_forecast(location, lat, lon)
                if days:
                    return days
            except (requests.RequestException, ValueError, KeyError, TypeError):
                pass
    return _demo_forecast()


def farming_advice(current, forecast):
    """Simple, clearly-worded guidance derived from weather. Not predictions of fact."""
    advice = []
    condition = (current.get("condition") or "").lower()
    temp = current.get("temperature") or 0
    humidity = current.get("humidity") or 0

    if any(k in condition for k in ("rain", "drizzle", "thunderstorm")):
        advice.append("Rain is happening or expected soon — irrigation may not be required today.")
    if temp >= 38:
        advice.append("Very high temperature expected — consider extra irrigation and shade for young plants.")
    elif temp >= 33:
        advice.append("High temperature — keep an eye on moisture; consider additional irrigation for sensitive crops.")
    if humidity >= 80:
        advice.append("High humidity — watch for fungal diseases; improve air circulation where possible.")
    if humidity <= 30:
        advice.append("Low humidity — be alert to drying; plan irrigation early in the day.")

    for day in forecast[:3]:
        if day.get("rain_probability", 0) >= 60:
            advice.append(
                f"{day['date']}: high chance of rain — plan irrigation around it and consider harvesting mature crops before heavy rain."
            )
    if not advice:
        advice.append("Weather is broadly favourable — follow your normal crop schedule and check back tomorrow.")
    return advice
