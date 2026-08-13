from flask import Blueprint, jsonify, session, request
import requests
import json
import time
from datetime import datetime, timedelta
import logging
from config import Config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('market_prices_dynamic_api', __name__)

# Cache for market data
market_data_cache = {}
CACHE_DURATION = 300  # 5 minutes cache

class MarketDataManager:
    def __init__(self):
        self.api_sources = {
            'agmarknet': {
                'base_url': 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070',
                'api_key': Config.AGMARKNET_API_KEY if hasattr(Config, 'AGMARKNET_API_KEY') else None,
                'params': {
                    'api-key': Config.AGMARKNET_API_KEY if hasattr(Config, 'AGMARKNET_API_KEY') else '579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b',
                    'format': 'json',
                    'limit': 100
                }
            },
            'mock': {  # Fallback mock data
                'crops': [
                    {'name': 'Wheat', 'min_price': 2200, 'max_price': 2800, 'unit': 'per quintal'},
                    {'name': 'Rice', 'min_price': 1800, 'max_price': 2200, 'unit': 'per quintal'},
                    {'name': 'Corn', 'min_price': 1400, 'max_price': 1800, 'unit': 'per quintal'},
                    {'name': 'Soybean', 'min_price': 3500, 'max_price': 4200, 'unit': 'per quintal'},
                    {'name': 'Cotton', 'min_price': 5500, 'max_price': 6500, 'unit': 'per quintal'},
                    {'name': 'Sugarcane', 'min_price': 280, 'max_price': 320, 'unit': 'per quintal'},
                    {'name': 'Tomato', 'min_price': 800, 'max_price': 1500, 'unit': 'per quintal'},
                    {'name': 'Potato', 'min_price': 1200, 'max_price': 1800, 'unit': 'per quintal'},
                    {'name': 'Onion', 'min_price': 600, 'max_price': 1200, 'unit': 'per quintal'},
                    {'name': 'Banana', 'min_price': 800, 'max_price': 1400, 'unit': 'per quintal'}
                ]
            }
        }

    def get_cached_data(self, cache_key):
        """Get data from cache if available and not expired"""
        if cache_key in market_data_cache:
            cache_entry = market_data_cache[cache_key]
            if time.time() - cache_entry['timestamp'] < CACHE_DURATION:
                return cache_entry['data']
            else:
                # Remove expired cache entry
                del market_data_cache[cache_key]
        return None

    def set_cached_data(self, cache_key, data):
        """Store data in cache with timestamp"""
        market_data_cache[cache_key] = {
            'data': data,
            'timestamp': time.time()
        }

    def fetch_from_agmarknet(self, state=None, district=None):
        """Fetch real-time data from Agmarknet API"""
        try:
            params = self.api_sources['agmarknet']['params'].copy()

            if state:
                params['filters[state]'] = state
            if district:
                params['filters[district]'] = district

            response = requests.get(
                self.api_sources['agmarknet']['base_url'],
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if 'records' in data:
                    return self.process_agmarknet_data(data['records'])
                else:
                    logger.warning("No records found in Agmarknet response")
                    return []
            else:
                logger.error(f"Agmarknet API error: {response.status_code}")
                return []

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching from Agmarknet: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in Agmarknet fetch: {str(e)}")
            return []

    def process_agmarknet_data(self, records):
        """Process raw Agmarknet data into standardized format"""
        processed_data = []

        for record in records[:20]:  # Limit to 20 records for performance
            try:
                # Map Agmarknet fields to our format
                crop_name = record.get('commodity', 'Unknown')
                price = record.get('modal_price', 0)

                if price and price > 0:
                    processed_data.append({
                        'crop': crop_name,
                        'price': float(price),
                        'unit': 'per quintal',
                        'change': self.calculate_price_change(crop_name, float(price)),
                        'state': record.get('state', ''),
                        'district': record.get('district', ''),
                        'market': record.get('market', ''),
                        'arrival_date': record.get('arrival_date', ''),
                        'source': 'Agmarknet'
                    })
            except (ValueError, KeyError) as e:
                logger.warning(f"Error processing record: {str(e)}")
                continue

        return processed_data

    def calculate_price_change(self, crop_name, current_price):
        """Calculate price change percentage (simplified mock calculation)"""
        # In a real implementation, this would compare with historical data
        import random
        change_percentages = [-5, -3, -2, -1, 0, 1, 2, 3, 5]
        return f"{random.choice(change_percentages)}%"

    def generate_mock_data(self, state=None, district=None):
        """Generate realistic mock data when real APIs are unavailable"""
        mock_data = []
        base_data = self.api_sources['mock']['crops']

        for crop in base_data:
            # Add some randomization to make it more realistic
            import random
            base_price = (crop['min_price'] + crop['max_price']) // 2
            variation = random.uniform(-0.1, 0.1)  # ±10% variation
            current_price = base_price * (1 + variation)

            mock_data.append({
                'crop': crop['name'],
                'price': round(current_price, 2),
                'unit': crop['unit'],
                'change': self.calculate_price_change(crop['name'], current_price),
                'state': state or 'All States',
                'district': district or 'All Districts',
                'market': 'Local Market',
                'arrival_date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Mock Data'
            })

        return mock_data

    def get_market_prices(self, state=None, district=None, use_cache=True):
        """Main method to get market prices with fallback logic"""
        cache_key = f"market_prices_{state}_{district}" if state and district else "market_prices_all"

        # Try to get from cache first
        if use_cache:
            cached_data = self.get_cached_data(cache_key)
            if cached_data:
                logger.info(f"Returning cached market data for {cache_key}")
                return cached_data

        # Try to fetch real data from Agmarknet
        logger.info("Fetching fresh market data from Agmarknet")
        real_data = self.fetch_from_agmarknet(state, district)

        # If real data is available, use it; otherwise, use mock data
        if real_data and len(real_data) > 0:
            logger.info(f"Got {len(real_data)} real market records")
            final_data = real_data
        else:
            logger.warning("Using mock data as fallback")
            final_data = self.generate_mock_data(state, district)

        # Cache the data
        self.set_cached_data(cache_key, final_data)

        return final_data

# Global market data manager instance
market_manager = MarketDataManager()

@bp.route('/market-prices', methods=['GET'])
def get_market_prices():
    """Get dynamic market prices with optional filtering"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401

        # Get query parameters
        state = request.args.get('state')
        district = request.args.get('district')
        use_cache = request.args.get('use_cache', 'true').lower() == 'true'

        logger.info(f"Market prices request - State: {state}, District: {district}")

        # Get market data
        prices_data = market_manager.get_market_prices(state, district, use_cache)

        # Format response
        response = {
            'success': True,
            'data': prices_data,
            'timestamp': datetime.now().isoformat(),
            'total_records': len(prices_data),
            'filters_applied': {
                'state': state,
                'district': district
            }
        }

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in market prices API: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@bp.route('/market-prices/refresh', methods=['POST'])
def refresh_market_prices():
    """Manually refresh market prices cache"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401

        # Clear cache
        global market_data_cache
        market_data_cache.clear()

        logger.info("Market prices cache cleared manually")

        return jsonify({
            'success': True,
            'message': 'Market prices cache refreshed successfully'
        })

    except Exception as e:
        logger.error(f"Error refreshing market prices: {str(e)}")
        return jsonify({
            'error': 'Failed to refresh cache',
            'message': str(e)
        }), 500

@bp.route('/market-prices/states', methods=['GET'])
def get_available_states():
    """Get list of states with available market data"""
    try:
        # This would typically come from a database or API
        # For now, returning common agricultural states
        states = [
            'Andhra Pradesh', 'Telangana', 'Karnataka', 'Tamil Nadu',
            'Kerala', 'Maharashtra', 'Gujarat', 'Rajasthan', 'Madhya Pradesh',
            'Uttar Pradesh', 'Punjab', 'Haryana', 'Bihar', 'West Bengal'
        ]

        return jsonify({
            'success': True,
            'states': states
        })

    except Exception as e:
        logger.error(f"Error getting states: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
