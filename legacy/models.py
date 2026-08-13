from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class MarketPrice(db.Model):
    """Model for storing historical market prices"""
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    market_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), default='kg')
    date = db.Column(db.Date, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    source = db.Column(db.String(50), default='Agmarknet')

    def to_dict(self):
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'state': self.state,
            'district': self.district,
            'market_name': self.market_name,
            'price': self.price,
            'unit': self.unit,
            'date': self.date.isoformat(),
            'timestamp': self.timestamp.isoformat(),
            'source': self.source
        }

class PriceAlert(db.Model):
    """Model for storing price alerts"""
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    alert_type = db.Column(db.String(20), default='above')  # 'above' or 'below'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MarketTrend(db.Model):
    """Model for storing calculated market trends"""
    id = db.Column(db.Integer, primary_key=True)
    crop_name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    avg_price_7d = db.Column(db.Float)
    avg_price_30d = db.Column(db.Float)
    price_change_7d = db.Column(db.Float)
    price_change_30d = db.Column(db.Float)
    trend_direction = db.Column(db.String(20))  # 'up', 'down', 'stable'
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'crop_name': self.crop_name,
            'state': self.state,
            'avg_price_7d': self.avg_price_7d,
            'avg_price_30d': self.avg_price_30d,
            'price_change_7d': self.price_change_7d,
            'price_change_30d': self.price_change_30d,
            'trend_direction': self.trend_direction,
            'last_updated': self.last_updated.isoformat()
        }

class CropRecommendation(db.Model):
    """Model for storing AI/ML crop recommendations"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    crop_name = db.Column(db.String(100), nullable=False)
    recommendation_type = db.Column(db.String(50))  # 'sowing', 'harvest', 'sell', 'buy'
    confidence_score = db.Column(db.Float, default=0.0)
    reasoning = db.Column(db.Text)
    weather_impact = db.Column(db.String(20))  # 'positive', 'negative', 'neutral'
    market_impact = db.Column(db.String(20))  # 'positive', 'negative', 'neutral'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'crop_name': self.crop_name,
            'recommendation_type': self.recommendation_type,
            'confidence_score': self.confidence_score,
            'reasoning': self.reasoning,
            'weather_impact': self.weather_impact,
            'market_impact': self.market_impact,
            'created_at': self.created_at.isoformat()
        }

def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

        # Create some sample data if tables are empty
        if MarketPrice.query.count() == 0:
            # Add sample market prices
            sample_prices = [
                MarketPrice(crop_name='Rice', state='Punjab', district='Amritsar',
                           market_name='Amritsar Grain Market', price=25.50, date=datetime.now().date()),
                MarketPrice(crop_name='Wheat', state='Haryana', district='Karnal',
                           market_name='Karnal Mandi', price=22.75, date=datetime.now().date()),
                MarketPrice(crop_name='Cotton', state='Gujarat', district='Bharuch',
                           market_name='Bharuch APMC', price=55.00, date=datetime.now().date()),
            ]
            for price in sample_prices:
                db.session.add(price)
            db.session.commit()
