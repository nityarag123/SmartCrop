from flask import Blueprint, request, jsonify
import requests
from config import Config

bp = Blueprint('api_weather', __name__)

OPENWEATHER_API_KEY = Config.WEATHER_API_KEY  # Corrected attribute name from Config

@bp.route('/weather/current')
def get_current_weather():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location parameter is required'}), 400

    if not OPENWEATHER_API_KEY or OPENWEATHER_API_KEY == 'your_openweather_key':
        return jsonify({'error': 'Weather API key is not configured'}), 500

    url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHER_API_KEY}&units=metric'
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch weather data'}), response.status_code

    data = response.json()
    result = {
        'location': data.get('name'),
        'temperature': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
        'condition': data['weather'][0]['main'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon']
    }
    return jsonify(result)

@bp.route('/weather/forecast')
def get_weather_forecast():
    location = request.args.get('location')
    if not location:
        return jsonify({'error': 'Location parameter is required'}), 400

    url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={OPENWEATHER_API_KEY}&units=metric'
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch forecast data'}), response.status_code

    data = response.json()
    daily_forecasts = []
    processed_dates = set()
    for item in data.get('list', []):
        date = item['dt_txt'].split(' ')[0]
        if date not in processed_dates:
            processed_dates.add(date)
            daily_forecasts.append({
                'date': item['dt'],
                'temp_day': item['main']['temp_max'],
                'temp_night': item['main']['temp_min'],
                'condition': item['weather'][0]['main'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon']
            })
        if len(daily_forecasts) >= 7:
            break

    return jsonify({'daily_forecasts': daily_forecasts})
