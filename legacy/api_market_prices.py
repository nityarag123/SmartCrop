from flask import Blueprint, jsonify, session, request
import db as db_module
import json
import os

bp = Blueprint('market_prices_api', __name__)

# Load static market prices data
STATIC_DATA_PATH = os.path.join(os.path.dirname(__file__), 'static', 'data', 'market_prices.json')
with open(STATIC_DATA_PATH, 'r') as f:
    STATIC_PRICES = json.load(f)

@bp.route('/market-prices', methods=['GET'])
def market_prices():
    # No auth required for static market prices (public endpoint)

    # Get optional crop filter
    crop_filter = request.args.get('crop', '').strip().lower()

    if crop_filter:
        # Find matching crop (case-insensitive, take first match)
        matching_crop = next((price for price in STATIC_PRICES if crop_filter in price['crop'].lower()), None)
        if matching_crop:
            insights = f"{matching_crop['description']} - {matching_crop['category']} category. Price range: ₹{matching_crop['min_price']}-{matching_crop['max_price']} {matching_crop['unit']}"
            return jsonify({
                'price': matching_crop['price'],
                'trend': matching_crop['change'],
                'insights': insights
            })
        else:
            return jsonify({'error': 'Crop not found'}), 404
    else:
        # Return all static market prices data as array
        return jsonify(STATIC_PRICES)
