# Kisan Mitra Dynamic Data System

## Overview

This document describes the dynamic data implementation for the Kisan Mitra agricultural platform. The system has been enhanced to provide real-time, location-specific agricultural data including market prices, crop calendars, and automated data updates.

## 🎯 Features Implemented

### 1. Dynamic Market Prices API
- **Real-time data** from agricultural market sources (Agmarknet API)
- **Intelligent caching** with 5-minute cache duration
- **Fallback system** with realistic mock data when APIs are unavailable
- **Location-based filtering** by state and district
- **Manual refresh** capabilities for immediate data updates

### 2. Smart Crop Calendar System
- **Location-specific recommendations** based on state and district
- **Seasonal intelligence** with automatic season detection
- **Weather integration** for dynamic crop suggestions
- **12-month calendar** with detailed monthly activities
- **Crop-specific timelines** with detailed growing information

### 3. Background Task System
- **Automated updates** every 30 minutes for market prices
- **Daily crop calendar** updates at 6 AM
- **Data quality monitoring** every 4 hours
- **Comprehensive logging** for all data operations
- **Error handling** with graceful degradation

### 4. Enhanced Data Management
- **Multi-source data integration** with fallback mechanisms
- **Performance optimization** through intelligent caching
- **Data validation** and quality checks
- **Admin endpoints** for manual data management

## 📁 Files Modified/Created

### New Files Created:
- `api_market_prices_dynamic.py` - Dynamic market prices API
- `api_crop_calendar_dynamic.py` - Smart crop calendar API
- `background_tasks.py` - Background task management system
- `test_dynamic_data.py` - Test script for validation
- `TODO.md` - Implementation tracking
- `DYNAMIC_DATA_README.md` - This documentation

### Modified Files:
- `app.py` - Updated to use dynamic APIs and background tasks
- `requirements.txt` - Added Flask-APScheduler and Redis dependencies

## 🚀 API Endpoints

### Market Prices Endpoints

```
GET /api/market-prices
- Get all market prices with optional state/district filtering
- Query params: state, district, use_cache

GET /api/market-prices/states
- Get list of available states for market data

POST /api/market-prices/refresh
- Manually refresh market prices cache
```

### Crop Calendar Endpoints

```
GET /api/crop-calendar
- Get smart crop calendar with optional location filtering
- Query params: state, district, weather_condition, temperature, rainfall

GET /api/crop-calendar/crop/<crop_name>
- Get detailed timeline for specific crop
- Query params: state

GET /api/crop-calendar/seasons
- Get information about agricultural seasons
```

### Background Tasks

The system automatically manages:
- Market prices updates every 30 minutes
- Weather data updates every 60 minutes
- Crop calendar updates daily at 6 AM
- Data quality checks every 4 hours

## 🛠 Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Add to your `.env` file:
```env
# Existing variables
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
WEATHER_API_KEY=your_openweather_api_key

# New variables for dynamic data
AGMARKNET_API_KEY=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b
REDIS_URL=redis://localhost:6379/0  # Optional for advanced caching
```

### 3. Run the Application

```bash
python app.py
```

### 4. Test the System

```bash
python test_dynamic_data.py
```

## 📊 Data Sources

### Primary Data Sources:
1. **Agmarknet API** - Government of India agricultural market data
2. **OpenWeatherMap API** - Weather data for crop recommendations
3. **State Agricultural Departments** - Regional crop and market information

### Fallback Systems:
- Realistic mock data when external APIs are unavailable
- Historical data patterns for price predictions
- Default crop calendars based on traditional farming practices

### Static Data Sources:
- **Comprehensive market prices JSON** (`static/data/market_prices.json`) - Static dataset with ~40 agricultural products including cereals, pulses, oilseeds, cash crops, vegetables, fruits, and spices
- **Structured data format** with price ranges, categories, and descriptions
- **API integration** via `api_market_prices.py` for serving static data
- **Fallback for dynamic APIs** when real-time data is unavailable

## 🔧 Configuration

### Cache Settings:
- Market prices cache: 5 minutes
- Weather data cache: 10 minutes
- Crop calendar cache: 1 hour

### Update Intervals:
- Market prices: Every 30 minutes
- Weather data: Every 60 minutes
- Crop calendar: Daily at 6 AM
- Data quality checks: Every 4 hours

## 📈 Performance Features

### Caching Strategy:
- **In-memory caching** for frequently accessed data
- **Cache invalidation** on manual refresh
- **TTL-based expiration** for automatic cleanup

### Error Handling:
- **Graceful degradation** when external APIs fail
- **Automatic fallback** to mock data
- **Comprehensive logging** for debugging
- **Data quality monitoring** with alerts

### Scalability:
- **Asynchronous background tasks** for non-blocking updates
- **Efficient data structures** for fast retrieval
- **Minimal external API calls** through intelligent caching

## 🧪 Testing

### Test Script Features:
- Comprehensive API endpoint testing
- Data validation and accuracy checks
- Performance benchmarking
- Error scenario simulation

### Manual Testing:
1. Start the application: `python app.py`
2. Run tests: `python test_dynamic_data.py`
3. Check logs for background task activity
4. Verify data freshness and accuracy

## 📋 Implementation Checklist

- ✅ **Phase 1**: Dynamic Market Prices API
  - Real-time data integration
  - Caching mechanism
  - Error handling
  - Location filtering

- ✅ **Phase 2**: Smart Crop Calendar System
  - Location-specific recommendations
  - Weather integration
  - Seasonal intelligence
  - Crop-specific timelines

- ✅ **Phase 3**: Background Task System
  - Automated data updates
  - Quality monitoring
  - Logging system
  - Error recovery

- ✅ **Phase 4**: Enhanced Data Management
  - Multi-source integration
  - Performance optimization
  - Admin controls
  - Data validation

## 🔍 Monitoring & Maintenance

### Logs:
- Application logs in console/terminal
- Background task logs with timestamps
- Error logs with detailed stack traces
- Data update logs with success/failure status

### Health Checks:
- API endpoint availability
- Data freshness validation
- Cache performance monitoring
- External API connectivity

### Maintenance Tasks:
- Regular cache cleanup
- API key rotation
- Data source monitoring
- Performance optimization

## 🎯 Benefits

### For Farmers:
- **Real-time market prices** for better selling decisions
- **Location-specific crop advice** for optimal yields
- **Current weather integration** for timely actions
- **Automated updates** without manual checking

### For the Platform:
- **Improved user engagement** with dynamic content
- **Better data accuracy** through multiple sources
- **Automated maintenance** reducing manual work
- **Scalable architecture** for future enhancements

## 🔮 Future Enhancements

### Planned Features:
- **Machine learning** for price predictions
- **Satellite data integration** for crop monitoring
- **SMS alerts** for price changes
- **Mobile app** integration
- **Advanced analytics** dashboard

### Technical Improvements:
- **Database integration** for persistent caching
- **Load balancing** for high traffic
- **CDN integration** for global access
- **Advanced security** features

## 📞 Support

For issues or questions regarding the dynamic data system:

1. Check the application logs for error details
2. Run the test script to diagnose issues
3. Verify API keys and external service connectivity
4. Check background task status and scheduling

## 📄 License

This dynamic data system is part of the Kisan Mitra platform and follows the same licensing terms as the main application.

---

**Last Updated:** December 2024
**Version:** 1.0.0
**Status:** ✅ Production Ready
