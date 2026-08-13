from flask import Blueprint, request, jsonify, session
from models import db, MarketPrice, MarketTrend, PriceAlert
from datetime import datetime, timedelta, date
import requests
import json
from config_dynamic import Config
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint('market_prices_enhanced', __name__)

# Global cache for market data
market_data_cache = {}
weather_cache = {}

class MarketDataManager:
    """Enhanced market data manager with database storage and analytics"""

    def __init__(self):
        self.agmarknet_api_key = Config.AGMARKNET_API_KEY
        self.cache_timeout = Config.CACHE_TIMEOUT_MARKET_PRICES

    def fetch_from_agmarknet(self, crop_name, state=None, district=None):
        """Fetch real-time data from Agmarknet API"""
        try:
            # Agmarknet API endpoint (you may need to adjust based on actual API)
            base_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
            params = {
                'api-key': self.agmarknet_api_key,
                'format': 'json',
                'limit': 100
            }

            if state:
                params['filters[state]'] = state
            if district:
                params['filters[district]'] = district
            if crop_name:
                params['filters[commodity]'] = crop_name

            response = requests.get(base_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return self.process_agmarknet_data(data, crop_name)
            else:
                logger.warning(f"Agmarknet API returned status {response.status_code}")
                return self.get_fallback_data(crop_name, state, district)

        except Exception as e:
            logger.error(f"Error fetching from Agmarknet: {str(e)}")
            return self.get_fallback_data(crop_name, state, district)

    def process_agmarknet_data(self, data, crop_name):
        """Process raw Agmarknet API data"""
        processed_data = []

        if 'records' in data:
            for record in data['records']:
                try:
                    # Extract relevant fields from Agmarknet data
                    price_info = {
                        'crop_name': record.get('commodity', crop_name),
                        'state': record.get('state', ''),
                        'district': record.get('district', ''),
                        'market_name': record.get('market', ''),
                        'price': float(record.get('modal_price', 0)),
                        'unit': 'kg',
                        'date': datetime.now().date(),
                        'source': 'Agmarknet'
                    }
                    processed_data.append(price_info)
                except (ValueError, KeyError) as e:
                    logger.warning(f"Error processing record: {e}")
                    continue

        return processed_data

    def get_fallback_data(self, crop_name, state=None, district=None):
        """Provide realistic fallback data when API is unavailable"""
        fallback_prices = {
            'rice': {'price': 25.50, 'trend': '+2.5%', 'change': 2.5},
            'wheat': {'price': 22.75, 'trend': '-1.2%', 'change': -1.2},
            'maize': {'price': 18.90, 'trend': '+5.1%', 'change': 5.1},
            'cotton': {'price': 55.00, 'trend': '+3.8%', 'change': 3.8},
            'sugarcane': {'price': 2.85, 'trend': '-0.5%', 'change': -0.5},
            'potato': {'price': 12.50, 'trend': '+8.2%', 'change': 8.2},
            'tomato': {'price': 15.75, 'trend': '+12.5%', 'change': 12.5},
            'onion': {'price': 18.25, 'trend': '-3.1%', 'change': -3.1}
        }

        if crop_name.lower() in fallback_prices:
            price_info = fallback_prices[crop_name.lower()]
            return [{
                'crop_name': crop_name,
                'state': state or 'All States',
                'district': district or 'All Districts',
                'market_name': 'Average Market Price',
                'price': price_info['price'],
                'unit': 'kg',
                'date': datetime.now().date(),
                'source': 'Fallback Data',
                'trend': price_info['trend'],
                'change': price_info['change']
            }]

        # Generic fallback
        return [{
            'crop_name': crop_name,
            'state': state or 'All States',
            'district': district or 'All Districts',
            'market_name': 'Average Market Price',
            'price': 20.00,
            'unit': 'kg',
            'date': datetime.now().date(),
            'source': 'Fallback Data',
            'trend': '0.0%',
            'change': 0.0
        }]

    def store_price_data(self, price_data):
        """Store price data in database"""
        try:
            for data in price_data:
                # Check if data already exists for today
                existing = MarketPrice.query.filter_by(
                    crop_name=data['crop_name'],
                    state=data['state'],
                    district=data['district'],
                    market_name=data['market_name'],
                    date=data['date']
                ).first()

                if not existing:
                    price_record = MarketPrice(
                        crop_name=data['crop_name'],
                        state=data['state'],
                        district=data['district'],
                        market_name=data['market_name'],
                        price=data['price'],
                        unit=data['unit'],
                        date=data['date'],
                        source=data['source']
                    )
                    db.session.add(price_record)

            db.session.commit()
            logger.info(f"Stored {len(price_data)} price records in database")
            return True

        except Exception as e:
            logger.error(f"Error storing price data: {str(e)}")
            db.session.rollback()
            return False

    def get_historical_prices(self, crop_name, state=None, days=30):
        """Get historical price data for trends"""
        try:
            query = MarketPrice.query.filter(
                MarketPrice.crop_name.ilike(f'%{crop_name}%'),
                MarketPrice.date >= date.today() - timedelta(days=days)
            )

            if state:
                query = query.filter(MarketPrice.state == state)

            prices = query.order_by(MarketPrice.date.desc()).all()

            # Group by date and calculate daily averages
            daily_prices = {}
            for price in prices:
                date_str = price.date.isoformat()
                if date_str not in daily_prices:
                    daily_prices[date_str] = []
                daily_prices[date_str].append(price.price)

            # Calculate daily averages
            historical_data = []
            for date_str, prices_list in daily_prices.items():
                avg_price = sum(prices_list) / len(prices_list)
                historical_data.append({
                    'date': date_str,
                    'price': round(avg_price, 2),
                    'volume': len(prices_list)
                })

            return sorted(historical_data, key=lambda x: x['date'])

        except Exception as e:
            logger.error(f"Error fetching historical prices: {str(e)}")
            return []

    def calculate_trends(self, crop_name, state=None):
        """Calculate price trends and statistics"""
        try:
            # Get recent prices (last 30 days)
            recent_prices = self.get_historical_prices(crop_name, state, 30)

            if len(recent_prices) < 2:
                return {
                    'current_price': 0,
                    'avg_7d': 0,
                    'avg_30d': 0,
                    'change_7d': 0,
                    'change_30d': 0,
                    'trend': 'stable'
                }

            # Calculate averages
            prices_7d = [p['price'] for p in recent_prices[:7]]
            prices_30d = [p['price'] for p in recent_prices[:30]]

            current_price = recent_prices[0]['price']
            avg_7d = sum(prices_7d) / len(prices_7d) if prices_7d else 0
            avg_30d = sum(prices_30d) / len(prices_30d) if prices_30d else 0

            change_7d = ((current_price - avg_7d) / avg_7d * 100) if avg_7d > 0 else 0
            change_30d = ((current_price - avg_30d) / avg_30d * 100) if avg_30d > 0 else 0

            # Determine trend
            if change_7d > 5:
                trend = 'up'
            elif change_7d < -5:
                trend = 'down'
            else:
                trend = 'stable'

            return {
                'current_price': round(current_price, 2),
                'avg_7d': round(avg_7d, 2),
                'avg_30d': round(avg_30d, 2),
                'change_7d': round(change_7d, 2),
                'change_30d': round(change_30d, 2),
                'trend': trend,
                'trend_direction': trend
            }

        except Exception as e:
            logger.error(f"Error calculating trends: {str(e)}")
            return {
                'current_price': 0,
                'avg_7d': 0,
                'avg_30d': 0,
                'change_7d': 0,
                'change_30d': 0,
                'trend': 'unknown'
            }

    def get_market_comparison(self, crop_name):
        """Get price comparison across different markets"""
        try:
            # Get latest prices for the crop across all markets
            latest_prices = MarketPrice.query.filter(
                MarketPrice.crop_name.ilike(f'%{crop_name}%'),
                MarketPrice.date >= date.today() - timedelta(days=1)
            ).order_by(MarketPrice.price.desc()).limit(10).all()

            comparison_data = []
            for price in latest_prices:
                comparison_data.append({
                    'market': price.market_name,
                    'state': price.state,
                    'district': price.district,
                    'price': price.price,
                    'date': price.date.isoformat()
                })

            return comparison_data

        except Exception as e:
            logger.error(f"Error getting market comparison: {str(e)}")
            return []

# Initialize market data manager
market_manager = MarketDataManager()

@bp.route('/market-prices')
def get_market_prices():
    """Get current market prices with optional filtering"""
    try:
        crop_name = request.args.get('crop', '').strip()
        state = request.args.get('state', '').strip()
        district = request.args.get('district', '').strip()
        use_cache = request.args.get('use_cache', 'true').lower() == 'true'

        # Create cache key
        cache_key = f"prices_{crop_name}_{state}_{district}"

        # Check cache first
        if use_cache and cache_key in market_data_cache:
            cache_time, cached_data = market_data_cache[cache_key]
            if datetime.now().timestamp() - cache_time < market_manager.cache_timeout:
                return jsonify(cached_data)

        # Fetch fresh data
        price_data = market_manager.fetch_from_agmarknet(crop_name, state, district)

        # Store in database
        market_manager.store_price_data(price_data)

        # Calculate trends if specific crop requested
        trends = {}
        if crop_name:
            trends = market_manager.calculate_trends(crop_name, state)

        # Get market comparison
        comparison = market_manager.get_market_comparison(crop_name) if crop_name else []

        # Prepare response
        response_data = {
            'success': True,
            'data': price_data,
            'trends': trends,
            'comparison': comparison,
            'total_records': len(price_data),
            'last_updated': datetime.now().isoformat(),
            'source': 'Agmarknet API' if price_data else 'Fallback Data'
        }

        # Cache the response
        market_data_cache[cache_key] = (datetime.now().timestamp(), response_data)

        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Error in get_market_prices: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch market prices',
            'message': str(e)
        }), 500

@bp.route('/market-prices/history')
def get_price_history():
    """Get historical price data for trends"""
    try:
        crop_name = request.args.get('crop', '').strip()
        state = request.args.get('state', '').strip()
        days = int(request.args.get('days', 30))

        if not crop_name:
            return jsonify({
                'success': False,
                'error': 'Crop name is required'
            }), 400

        historical_data = market_manager.get_historical_prices(crop_name, state, days)

        return jsonify({
            'success': True,
            'data': historical_data,
            'crop': crop_name,
            'state': state,
            'period_days': days
        })

    except Exception as e:
        logger.error(f"Error in get_price_history: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch price history',
            'message': str(e)
        }), 500

@bp.route('/market-prices/states')
def get_available_states():
    """Get list of states with available market data"""
    try:
        states = MarketPrice.query.with_entities(MarketPrice.state).distinct().all()
        state_list = [state[0] for state in states if state[0]]

        return jsonify({
            'success': True,
            'states': sorted(state_list)
        })

    except Exception as e:
        logger.error(f"Error in get_available_states: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch states',
            'message': str(e)
        }), 500

@bp.route('/market-prices/trends')
def get_market_trends():
    """Get calculated market trends for all crops"""
    try:
        # Get distinct crops
        crops = MarketPrice.query.with_entities(MarketPrice.crop_name).distinct().all()
        crop_list = [crop[0] for crop in crops if crop[0]]

        trends_data = []
        for crop in crop_list[:10]:  # Limit to top 10 crops
            trends = market_manager.calculate_trends(crop)
            trends['crop_name'] = crop
            trends_data.append(trends)

        return jsonify({
            'success': True,
            'trends': trends_data,
            'last_updated': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error in get_market_trends: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch market trends',
            'message': str(e)
        }), 500

@bp.route('/market-prices/refresh', methods=['POST'])
def refresh_market_data():
    """Manually refresh market data"""
    try:
        # Clear cache
        global market_data_cache
        market_data_cache.clear()

        # Fetch fresh data for popular crops
        popular_crops = ['rice', 'wheat', 'maize', 'cotton', 'sugarcane']
        for crop in popular_crops:
            price_data = market_manager.fetch_from_agmarknet(crop)
            market_manager.store_price_data(price_data)

        return jsonify({
            'success': True,
            'message': 'Market data refreshed successfully',
            'timestamp': datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Error in refresh_market_data: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to refresh market data',
            'message': str(e)
        }), 500
