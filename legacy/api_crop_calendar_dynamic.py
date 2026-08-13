from flask import Blueprint, jsonify, session, request
import json
from datetime import datetime, timedelta
import calendar
import random
import logging
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('crop_calendar_dynamic_api', __name__)

class SmartCropCalendar:
    def __init__(self):
        # Base crop data with seasonal information
        self.crop_seasons = {
            'kharif': {  # Monsoon season (June-October)
                'months': [6, 7, 8, 9, 10],
                'crops': [
                    'Rice', 'Maize', 'Cotton', 'Soybean', 'Sugarcane',
                    'Groundnut', 'Bajra', 'Jowar', 'Tur', 'Urad'
                ]
            },
            'rabi': {  # Winter season (October-March)
                'months': [10, 11, 12, 1, 2, 3],
                'crops': [
                    'Wheat', 'Barley', 'Mustard', 'Chickpea', 'Lentil',
                    'Potato', 'Onion', 'Garlic', 'Peas', 'Oats'
                ]
            },
            'zaid': {  # Summer season (March-June)
                'months': [3, 4, 5, 6],
                'crops': [
                    'Muskmelon', 'Watermelon', 'Cucumber', 'Bitter gourd',
                    'Bottle gourd', 'Pumpkin', 'Tomato', 'Brinjal', 'Okra'
                ]
            }
        }

        # Weather-based recommendations
        self.weather_recommendations = {
            'high_rainfall': [
                'Rice', 'Jute', 'Sugarcane', 'Banana', 'Coconut'
            ],
            'moderate_rainfall': [
                'Wheat', 'Cotton', 'Soybean', 'Maize', 'Groundnut'
            ],
            'low_rainfall': [
                'Bajra', 'Jowar', 'Mustard', 'Chickpea', 'Barley'
            ],
            'hot_dry': [
                'Cotton', 'Groundnut', 'Sesame', 'Castor', 'Sunflower'
            ],
            'cool_dry': [
                'Wheat', 'Barley', 'Mustard', 'Potato', 'Onion'
            ]
        }

        # Month-wise activity templates
        self.monthly_activities = {
            1: ['Winter crop monitoring', 'Irrigation planning', 'Pest control', 'Soil testing'],
            2: ['Fertilizer application', 'Weed management', 'Disease monitoring', 'Harvesting preparation'],
            3: ['Summer crop sowing', 'Land preparation', 'Seed treatment', 'Irrigation setup'],
            4: ['Pest monitoring', 'Fertilizer application', 'Weed control', 'Growth monitoring'],
            5: ['Water management', 'Disease control', 'Nutrient management', 'Growth assessment'],
            6: ['Monsoon preparation', 'Seed selection', 'Land preparation', 'Pre-sowing irrigation'],
            7: ['Kharif crop sowing', 'Seed treatment', 'Fertilizer application', 'Pest prevention'],
            8: ['Crop monitoring', 'Weed control', 'Disease management', 'Growth tracking'],
            9: ['Fertilizer application', 'Pest control', 'Irrigation management', 'Quality assessment'],
            10: ['Harvesting', 'Post-harvest handling', 'Rabi crop planning', 'Field preparation'],
            11: ['Rabi crop sowing', 'Seed treatment', 'Land preparation', 'Winter crop care'],
            12: ['Crop protection', 'Irrigation', 'Disease monitoring', 'Yield assessment']
        }

    def get_current_season(self, month=None):
        """Determine current agricultural season based on month"""
        if month is None:
            month = datetime.now().month

        if month in [6, 7, 8, 9, 10]:
            return 'kharif'
        elif month in [10, 11, 12, 1, 2, 3]:
            return 'rabi'
        else:
            return 'zaid'

    def get_weather_based_crops(self, weather_condition, temperature=None, rainfall=None):
        """Get crop recommendations based on weather conditions"""
        if weather_condition == 'rainy' or rainfall == 'high':
            return self.weather_recommendations['high_rainfall']
        elif weather_condition == 'dry' and temperature and temperature > 35:
            return self.weather_recommendations['hot_dry']
        elif weather_condition == 'dry' and temperature and temperature < 25:
            return self.weather_recommendations['cool_dry']
        elif rainfall == 'moderate':
            return self.weather_recommendations['moderate_rainfall']
        else:
            return self.weather_recommendations['low_rainfall']

    def get_location_specific_crops(self, state, district=None):
        """Get crops suitable for specific location"""
        # State-wise crop preferences (simplified)
        state_crops = {
            'punjab': ['Wheat', 'Rice', 'Cotton', 'Sugarcane', 'Maize'],
            'haryana': ['Wheat', 'Rice', 'Cotton', 'Mustard', 'Bajra'],
            'uttar_pradesh': ['Wheat', 'Rice', 'Sugarcane', 'Potato', 'Maize'],
            'maharashtra': ['Cotton', 'Soybean', 'Sugarcane', 'Rice', 'Jowar'],
            'gujarat': ['Cotton', 'Groundnut', 'Rice', 'Wheat', 'Bajra'],
            'madhya_pradesh': ['Soybean', 'Wheat', 'Rice', 'Cotton', 'Maize'],
            'rajasthan': ['Bajra', 'Wheat', 'Mustard', 'Cotton', 'Groundnut'],
            'karnataka': ['Rice', 'Cotton', 'Sugarcane', 'Maize', 'Groundnut'],
            'andhra_pradesh': ['Rice', 'Cotton', 'Sugarcane', 'Maize', 'Groundnut'],
            'telangana': ['Rice', 'Cotton', 'Maize', 'Soybean', 'Groundnut'],
            'tamil_nadu': ['Rice', 'Sugarcane', 'Cotton', 'Groundnut', 'Banana'],
            'kerala': ['Rice', 'Coconut', 'Rubber', 'Banana', 'Spices'],
            'west_bengal': ['Rice', 'Jute', 'Potato', 'Sugarcane', 'Wheat'],
            'bihar': ['Rice', 'Wheat', 'Maize', 'Sugarcane', 'Potato']
        }

        # Normalize state name
        state_key = state.lower().replace(' ', '_')
        return state_crops.get(state_key, ['Rice', 'Wheat', 'Cotton', 'Sugarcane', 'Maize'])

    def generate_smart_calendar(self, state=None, district=None, weather_data=None):
        """Generate intelligent crop calendar based on location and conditions"""
        current_month = datetime.now().month
        current_season = self.get_current_season(current_month)

        # Get location-specific crops
        location_crops = self.get_location_specific_crops(state, district) if state else []

        # Get weather-based recommendations
        weather_crops = []
        if weather_data:
            weather_condition = weather_data.get('condition', '').lower()
            temperature = weather_data.get('temperature')
            rainfall = weather_data.get('rainfall', 'moderate')

            if 'rain' in weather_condition or rainfall == 'high':
                weather_crops = self.weather_recommendations['high_rainfall']
            elif 'dry' in weather_condition or rainfall == 'low':
                if temperature and temperature > 35:
                    weather_crops = self.weather_recommendations['hot_dry']
                else:
                    weather_crops = self.weather_recommendations['cool_dry']
            else:
                weather_crops = self.weather_recommendations['moderate_rainfall']

        # Combine and prioritize crops
        recommended_crops = list(set(location_crops + weather_crops))
        if not recommended_crops:
            recommended_crops = self.crop_seasons[current_season]['crops']

        # Generate 12-month calendar
        calendar_data = []

        for month_num in range(1, 13):
            month_name = calendar.month_name[month_num]
            season = self.get_current_season(month_num)

            # Get activities for this month
            activities = self.monthly_activities.get(month_num, ['General crop care'])

            # Get crops suitable for this month
            month_crops = []
            if month_num in self.crop_seasons[season]['months']:
                month_crops = [crop for crop in recommended_crops
                             if crop in self.crop_seasons[season]['crops']]

            # Add seasonal recommendations
            recommendations = []
            if month_num == current_month:
                recommendations.append("Current month - Focus on ongoing crops")
            if month_num in [3, 4, 5]:
                recommendations.append("Summer crop preparation")
            elif month_num in [6, 7, 8]:
                recommendations.append("Monsoon crop management")
            elif month_num in [10, 11, 12]:
                recommendations.append("Winter crop care")

            calendar_data.append({
                'month': month_name,
                'month_number': month_num,
                'season': season,
                'recommended_crops': month_crops[:5],  # Limit to 5 crops
                'activities': activities,
                'recommendations': recommendations,
                'weather_considerations': self.get_weather_considerations(season, month_num)
            })

        return calendar_data

    def get_weather_considerations(self, season, month):
        """Get weather-related considerations for farming activities"""
        considerations = {
            'kharif': [
                "Monitor monsoon patterns",
                "Ensure proper drainage",
                "Watch for waterlogging",
                "Plan for flood-resistant crops"
            ],
            'rabi': [
                "Monitor frost conditions",
                "Ensure adequate irrigation",
                "Watch for winter pests",
                "Plan for cold-resistant varieties"
            ],
            'zaid': [
                "Monitor temperature fluctuations",
                "Ensure water availability",
                "Watch for heat stress",
                "Plan for summer crop varieties"
            ]
        }

        base_considerations = considerations.get(season, [])
        month_specific = []

        if month in [4, 5, 6]:
            month_specific.append("High temperature management required")
        elif month in [7, 8, 9]:
            month_specific.append("Heavy rainfall expected - ensure drainage")
        elif month in [12, 1, 2]:
            month_specific.append("Cold weather protection needed")

        return base_considerations + month_specific

    def get_crop_specific_timeline(self, crop_name, state=None):
        """Get detailed timeline for a specific crop"""
        crop_timelines = {
            'rice': {
                'sowing': 'June-July (Kharif), November-December (Rabi)',
                'growth_period': '90-150 days',
                'harvest': 'September-November (Kharif), March-April (Rabi)',
                'water_requirement': 'High',
                'soil_type': 'Clayey to loamy'
            },
            'wheat': {
                'sowing': 'October-December',
                'growth_period': '120-150 days',
                'harvest': 'March-April',
                'water_requirement': 'Medium',
                'soil_type': 'Well-drained loamy'
            },
            'cotton': {
                'sowing': 'May-June',
                'growth_period': '150-180 days',
                'harvest': 'September-December',
                'water_requirement': 'Medium',
                'soil_type': 'Black cotton soil'
            },
            'sugarcane': {
                'sowing': 'February-March, October-November',
                'growth_period': '10-18 months',
                'harvest': 'December-March',
                'water_requirement': 'Very High',
                'soil_type': 'Well-drained loamy'
            }
        }

        return crop_timelines.get(crop_name.lower(), {
            'sowing': 'Season dependent',
            'growth_period': 'Variable',
            'harvest': 'Season dependent',
            'water_requirement': 'Medium',
            'soil_type': 'Well-drained'
        })

# Global crop calendar instance
crop_calendar_manager = SmartCropCalendar()

@bp.route('/crop-calendar', methods=['GET'])
def get_smart_crop_calendar():
    """Get intelligent crop calendar based on location and conditions"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401

        # Get query parameters
        state = request.args.get('state')
        district = request.args.get('district')
        weather_condition = request.args.get('weather_condition')
        temperature = request.args.get('temperature')
        rainfall = request.args.get('rainfall')

        logger.info(f"Crop calendar request - State: {state}, District: {district}")

        # Prepare weather data if provided
        weather_data = None
        if weather_condition or temperature or rainfall:
            weather_data = {
                'condition': weather_condition or 'moderate',
                'temperature': float(temperature) if temperature else None,
                'rainfall': rainfall or 'moderate'
            }

        # Generate smart calendar
        calendar_data = crop_calendar_manager.generate_smart_calendar(
            state, district, weather_data
        )

        # Get current season info
        current_month = datetime.now().month
        current_season = crop_calendar_manager.get_current_season(current_month)

        response = {
            'success': True,
            'calendar': calendar_data,
            'current_season': current_season,
            'current_month': calendar.month_name[current_month],
            'filters_applied': {
                'state': state,
                'district': district,
                'weather_condition': weather_condition
            },
            'generated_at': datetime.now().isoformat()
        }

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in crop calendar API: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@bp.route('/crop-calendar/crop/<crop_name>', methods=['GET'])
def get_crop_timeline(crop_name):
    """Get detailed timeline for a specific crop"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401

        state = request.args.get('state')

        timeline = crop_calendar_manager.get_crop_specific_timeline(crop_name, state)

        return jsonify({
            'success': True,
            'crop': crop_name,
            'timeline': timeline,
            'state_specific': state is not None
        })

    except Exception as e:
        logger.error(f"Error getting crop timeline: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@bp.route('/crop-calendar/seasons', methods=['GET'])
def get_season_info():
    """Get information about agricultural seasons"""
    try:
        seasons = {
            'kharif': {
                'name': 'Kharif Season',
                'months': 'June to October',
                'description': 'Monsoon crops grown during rainy season',
                'major_crops': ['Rice', 'Cotton', 'Soybean', 'Maize', 'Sugarcane']
            },
            'rabi': {
                'name': 'Rabi Season',
                'months': 'October to March',
                'description': 'Winter crops grown during dry season',
                'major_crops': ['Wheat', 'Barley', 'Mustard', 'Chickpea', 'Potato']
            },
            'zaid': {
                'name': 'Zaid Season',
                'months': 'March to June',
                'description': 'Summer crops grown during hot season',
                'major_crops': ['Muskmelon', 'Watermelon', 'Cucumber', 'Tomato', 'Okra']
            }
        }

        return jsonify({
            'success': True,
            'seasons': seasons,
            'current_season': crop_calendar_manager.get_current_season()
        })

    except Exception as e:
        logger.error(f"Error getting season info: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500
