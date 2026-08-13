import React, { useState, useEffect, useRef } from 'react';
import '../weather.css';

const Weather = () => {
  const [selectedState, setSelectedState] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('');
  const [states, setStates] = useState([]);
  const [districts, setDistricts] = useState([]);
  const [currentWeather, setCurrentWeather] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isListening, setIsListening] = useState(false);

  const recognitionRef = useRef(null);

  // Load states and districts data
  useEffect(() => {
    fetch('/data/states-districts.json')
      .then(response => response.json())
      .then(data => {
        setStates(Object.keys(data));
      })
      .catch(error => {
        console.error('Error loading states data:', error);
        setError('Failed to load location data');
      });
  }, []);

  // Update districts when state changes
  useEffect(() => {
    if (selectedState) {
      fetch('/data/states-districts.json')
        .then(response => response.json())
        .then(data => {
          setDistricts(data[selectedState] || []);
          setSelectedDistrict(''); // Reset district selection
        });
    } else {
      setDistricts([]);
    }
  }, [selectedState]);

  // Speech recognition setup
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      recognitionRef.current.lang = 'en-IN';

      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        handleVoiceInput(transcript);
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const handleVoiceInput = (transcript) => {
    const lowerTranscript = transcript.toLowerCase();

    // Try to match states
    const matchedState = states.find(state =>
      state.toLowerCase().includes(lowerTranscript) ||
      lowerTranscript.includes(state.toLowerCase())
    );

    if (matchedState) {
      setSelectedState(matchedState);
      speak(`Selected state: ${matchedState}`);
      return;
    }

    // Try to match districts
    const matchedDistrict = districts.find(district =>
      district.toLowerCase().includes(lowerTranscript) ||
      lowerTranscript.includes(district.toLowerCase())
    );

    if (matchedDistrict) {
      setSelectedDistrict(matchedDistrict);
      speak(`Selected district: ${matchedDistrict}`);
      return;
    }

    speak('Sorry, I could not find that location. Please try again.');
  };

  const startListening = () => {
    if (recognitionRef.current && !isListening) {
      setIsListening(true);
      recognitionRef.current.start();
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  };

  const speak = (text) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'en-IN';
      utterance.rate = 0.9;
      utterance.pitch = 1;
      window.speechSynthesis.speak(utterance);
    }
  };

  const speakWeather = () => {
    if (!currentWeather) {
      speak('Please fetch weather data first');
      return;
    }

    const weatherText = `
      Current weather in ${currentWeather.location}.
      Temperature: ${currentWeather.temperature} degrees Celsius.
      Humidity: ${currentWeather.humidity} percent.
      Wind speed: ${currentWeather.wind_speed} meters per second.
      Condition: ${currentWeather.condition}.
    `;

    speak(weatherText);
  };

  const fetchWeather = async () => {
    if (!selectedState || !selectedDistrict) {
      setError('Please select both state and district');
      return;
    }

    setLoading(true);
    setError('');
    setCurrentWeather(null);
    setForecast([]);

    try {
      const location = `${selectedDistrict},${selectedState}`;

      // Fetch current weather
      const currentResponse = await fetch(`/api/weather/current?location=${encodeURIComponent(location)}`);
      if (!currentResponse.ok) {
        throw new Error('Failed to fetch current weather');
      }
      const currentData = await currentResponse.json();
      setCurrentWeather(currentData);

      // Fetch forecast
      const forecastResponse = await fetch(`/api/weather/forecast?location=${encodeURIComponent(location)}`);
      if (!forecastResponse.ok) {
        throw new Error('Failed to fetch weather forecast');
      }
      const forecastData = await forecastResponse.json();
      setForecast(forecastData.daily_forecasts || []);

    } catch (err) {
      setError(err.message || 'Failed to fetch weather data');
      console.error('Weather fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getWeatherIcon = (condition) => {
    const iconMap = {
      'clear': '☀️',
      'clouds': '☁️',
      'rain': '🌧️',
      'snow': '❄️',
      'thunderstorm': '⛈️',
      'mist': '🌫️',
      'haze': '🌫️'
    };

    return iconMap[condition.toLowerCase()] || '🌤️';
  };

  const getTemperatureColor = (temp) => {
    if (temp >= 35) return '#ff4757';
    if (temp >= 25) return '#ffa726';
    if (temp >= 15) return '#66bb6a';
    return '#42a5f5';
  };

  return (
    <div className="weather-page">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-4">Weather Forecast</h1>
          <p className="text-gray-300 text-lg">Get real-time weather updates for any location in India</p>
        </div>

        {/* Input Section */}
        <div className="weather-input-section weather-fade-in">
          <h2>🌍 Select Location</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="weather-form-group">
              <label htmlFor="state-select">State</label>
              <div className="flex gap-2">
                <select
                  id="state-select"
                  className="weather-select"
                  value={selectedState}
                  onChange={(e) => setSelectedState(e.target.value)}
                >
                  <option value="">Select State</option>
                  {states.map(state => (
                    <option key={state} value={state}>{state}</option>
                  ))}
                </select>
                <button
                  className={`voice-control-btn ${isListening ? 'listening' : ''}`}
                  onClick={startListening}
                  title="Voice input for state"
                >
                  🎤
                </button>
              </div>
            </div>

            <div className="weather-form-group">
              <label htmlFor="district-select">District</label>
              <div className="flex gap-2">
                <select
                  id="district-select"
                  className="weather-select"
                  value={selectedDistrict}
                  onChange={(e) => setSelectedDistrict(e.target.value)}
                  disabled={!selectedState}
                >
                  <option value="">Select District</option>
                  {districts.map(district => (
                    <option key={district} value={district}>{district}</option>
                  ))}
                </select>
                <button
                  className={`voice-control-btn ${isListening ? 'listening' : ''}`}
                  onClick={startListening}
                  title="Voice input for district"
                  disabled={!selectedState}
                >
                  🎤
                </button>
              </div>
            </div>
          </div>

          <div className="weather-btn-group">
            <button
              className="weather-btn weather-btn-primary"
              onClick={fetchWeather}
              disabled={loading || !selectedState || !selectedDistrict}
            >
              {loading ? '🔄 Fetching...' : '🌤️ Get Weather'}
            </button>
            <button
              className="weather-btn weather-btn-secondary"
              onClick={speakWeather}
              disabled={!currentWeather}
            >
              🔊 Speak Weather
            </button>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="weather-error weather-slide-up">
            <strong>⚠️ Error:</strong> {error}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="weather-loading">
            <div className="spinner"></div>
            <p>Fetching weather data...</p>
          </div>
        )}

        {/* Current Weather */}
        {currentWeather && (
          <div className="current-weather weather-slide-up">
            <h3>🌡️ Current Weather in {currentWeather.location}</h3>

            <div className="weather-details-grid">
              <div className="weather-detail-card">
                <h4>Temperature</h4>
                <div
                  className="value"
                  style={{ color: getTemperatureColor(currentWeather.temperature) }}
                >
                  {currentWeather.temperature}°C
                </div>
                <div className="unit">Celsius</div>
              </div>

              <div className="weather-detail-card">
                <h4>Humidity</h4>
                <div className="value">{currentWeather.humidity}%</div>
                <div className="unit">Percent</div>
              </div>

              <div className="weather-detail-card">
                <h4>Wind Speed</h4>
                <div className="value">{currentWeather.wind_speed}</div>
                <div className="unit">m/s</div>
              </div>

              <div className="weather-detail-card">
                <h4>Condition</h4>
                <div className="value">{getWeatherIcon(currentWeather.condition)}</div>
                <div className="unit">{currentWeather.condition}</div>
              </div>
            </div>
          </div>
        )}

        {/* 7-Day Forecast */}
        {forecast.length > 0 && (
          <div className="forecast-section weather-slide-up">
            <h3>📅 7-Day Forecast</h3>

            <div className="forecast-grid">
              {forecast.map((day, index) => (
                <div key={index} className="forecast-card">
                  <div className="day">
                    {new Date(day.date * 1000).toLocaleDateString('en-US', { weekday: 'short' })}
                  </div>
                  <div className="date">
                    {new Date(day.date * 1000).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  </div>
                  <div className="weather-icon">
                    {getWeatherIcon(day.condition)}
                  </div>
                  <div className="temp">
                    {day.temp_day.toFixed(0)}° / {day.temp_night.toFixed(0)}°
                  </div>
                  <div className="condition">{day.condition}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Voice Control Instructions */}
        <div className="mt-8 p-6 bg-gray-800 rounded-lg text-center">
          <h4 className="text-white font-semibold mb-2">🎤 Voice Control</h4>
          <p className="text-gray-300 text-sm">
            Click the microphone button and say the name of a state or district to select it automatically.
            You can also use voice commands to get weather updates.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Weather;
