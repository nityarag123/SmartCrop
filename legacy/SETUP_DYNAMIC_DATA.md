# Setup Guide for Kisan Mitra Dynamic Data System

## 🔑 API Keys Required

### **Required API Keys:**

#### 1. **Agmarknet API Key** (for real-time market prices)
- **Purpose**: Fetch live agricultural market prices from Government of India
- **How to get**: Register at [Agmarknet API Portal](https://data.gov.in)
- **Default value**: `579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b` (already included)
- **Environment variable**: `AGMARKNET_API_KEY`

#### 2. **OpenWeatherMap API Key** (for weather data)
- **Purpose**: Weather information for crop recommendations
- **How to get**: Sign up at [OpenWeatherMap](https://openweathermap.org/api)
- **Default value**: `bd5e378503939ddaee76f12ad7a97608` (already included)
- **Environment variable**: `WEATHER_API_KEY`

### **Optional API Keys:**

#### 3. **Redis URL** (for advanced caching)
- **Purpose**: High-performance caching for better speed
- **Default value**: `redis://localhost:6379/0`
- **Environment variable**: `REDIS_URL`
- **Note**: If not provided, the system uses in-memory caching

## 📋 Environment Setup

### Option 1: Using .env file (Recommended)

Create a `.env` file in your project root:

```env
# Basic Configuration
SECRET_KEY=your_secret_key_here
DATABASE_URL=mysql+pymysql://user:pass@localhost/dbname

# API Keys for Dynamic Data
WEATHER_API_KEY=bd5e378503939ddaee76f12ad7a97608
AGMARKNET_API_KEY=579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b

# Optional: Redis for advanced caching
REDIS_URL=redis://localhost:6379/0

# Optional: Customize cache timeouts (in seconds)
CACHE_TIMEOUT_MARKET_PRICES=300
CACHE_TIMEOUT_WEATHER=600
CACHE_TIMEOUT_CROP_CALENDAR=3600

# Optional: Customize update intervals (in seconds)
MARKET_PRICES_UPDATE_INTERVAL=1800
WEATHER_UPDATE_INTERVAL=3600
DATA_QUALITY_CHECK_INTERVAL=14400

# Optional: Enable/disable features
ENABLE_DYNAMIC_MARKET_PRICES=true
ENABLE_SMART_CROP_CALENDAR=true
ENABLE_BACKGROUND_TASKS=true
```

### Option 2: Using system environment variables

```bash
# Set environment variables directly
export WEATHER_API_KEY="bd5e378503939ddaee76f12ad7a97608"
export AGMARKNET_API_KEY="579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
export REDIS_URL="redis://localhost:6379/0"
```

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure Environment

Choose one of the options above to set up your API keys.

### Step 3: Run the Application

```bash
python app.py
```

The dynamic data system will start automatically with background tasks!

## 🧪 Testing the Setup

### Run the test script:

```bash
python test_dynamic_data.py
```

This will test:
- ✅ Market prices API endpoints
- ✅ Crop calendar API endpoints
- ✅ Weather API integration
- ✅ Background task functionality

### Expected Output:
```
🚀 Starting Dynamic Data System Tests for Kisan Mitra
============================================================
Test Time: 2024-12-XX XX:XX:XX
Base URL: http://localhost:5000
============================================================

🧪 Testing Dynamic Market Prices API...
✅ Market prices API (no filters) - Success
✅ Market prices API (with state filter) - Success
✅ Market prices states API - Success

🧪 Testing Dynamic Crop Calendar API...
✅ Crop calendar API (no filters) - Success
✅ Crop calendar API (with state filter) - Success
✅ Crop timeline API - Success
✅ Season information API - Success

🧪 Testing Weather API...
✅ Weather API - Success

🧪 Testing Background Tasks...
✅ Market prices refresh - Success

============================================================
🏁 Dynamic Data System Tests Completed!
============================================================
```

## 🔧 Configuration Options

### Cache Timeouts:
- **Market Prices**: 5 minutes (300 seconds)
- **Weather Data**: 10 minutes (600 seconds)
- **Crop Calendar**: 1 hour (3600 seconds)

### Update Intervals:
- **Market Prices**: Every 30 minutes
- **Weather Data**: Every 60 minutes
- **Data Quality Checks**: Every 4 hours

### Feature Toggles:
- **Dynamic Market Prices**: `true` (enabled by default)
- **Smart Crop Calendar**: `true` (enabled by default)
- **Background Tasks**: `true` (enabled by default)

## 📊 Data Sources

### Primary Data Sources:
1. **Agmarknet API** - Government of India agricultural market data
2. **OpenWeatherMap API** - Weather data for crop recommendations
3. **State Agricultural Departments** - Regional crop information

### Fallback Systems:
- Realistic mock data when external APIs are unavailable
- Historical data patterns for price predictions
- Default crop calendars based on traditional practices

## 🆘 Troubleshooting

### Common Issues:

#### 1. **API Keys Not Working**
```bash
# Check if environment variables are set
echo $WEATHER_API_KEY
echo $AGMARKNET_API_KEY

# Test API connectivity
curl "https://api.openweathermap.org/data/2.5/weather?q=Delhi&appid=$WEATHER_API_KEY"
```

#### 2. **Redis Connection Issues**
- Install Redis: `sudo apt install redis-server` (Ubuntu/Debian)
- Start Redis: `redis-server`
- Check connection: `redis-cli ping`

#### 3. **Background Tasks Not Running**
- Check logs for error messages
- Verify Flask-APScheduler is installed
- Ensure application has proper permissions

#### 4. **Data Not Updating**
- Check background task logs
- Verify API key validity
- Test manual refresh endpoints

### Debug Mode:
Run the application with debug logging:

```bash
export FLASK_ENV=development
python app.py
```

## 📈 Monitoring

### Check Background Tasks:
```python
# In Python shell
from background_tasks import data_update_manager
print(data_update_manager.get_job_status())
```

### View Data Update History:
```python
from background_tasks import data_update_manager
history = data_update_manager.get_data_update_history()
print(history)
```

### Manual Data Refresh:
```bash
# Refresh market prices
curl -X POST http://localhost:5000/api/market-prices/refresh

# Refresh crop calendar
curl -X POST http://localhost:5000/api/crop-calendar/refresh
```

## 🎯 API Endpoints

### Market Prices:
- `GET /api/market-prices` - Get market prices
- `GET /api/market-prices/states` - Get available states
- `POST /api/market-prices/refresh` - Manual refresh

### Crop Calendar:
- `GET /api/crop-calendar` - Get crop calendar
- `GET /api/crop-calendar/crop/<crop>` - Get crop timeline
- `GET /api/crop-calendar/seasons` - Get season info

### Weather:
- `GET /api/weather/current?location=<city>` - Current weather
- `GET /api/weather/forecast?location=<city>` - Weather forecast

## 📞 Support

For issues:
1. Check the application logs
2. Run the test script for diagnostics
3. Verify API key validity
4. Check external service status

---

**Status**: ✅ Ready for Production
**Last Updated**: December 2024
**Version**: 1.0.0
