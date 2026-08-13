import React, { useState } from 'react';

const WeatherMock = () => {
  const [selectedState, setSelectedState] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState('');
  const [weatherData, setWeatherData] = useState(null);
  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const statesDistricts = {
    "Goa": ["North Goa", "South Goa"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur"]
  };

  const districts = selectedState ? statesDistricts[selectedState] || [] : [];

  const fetchWeatherData = async () => {
    if (!selectedState || !selectedDistrict) {
      setError('Please select both state and district');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Mock weather data
      const mockWeatherData = {
        name: `${selectedDistrict}, ${selectedState}`,
        main: {
          temp: 30,
          feels_like: 32,
          humidity: 70,
          temp_min: 28,
          temp_max: 33
        },
        wind: {
          speed: 5
        },
        weather: [{
          main: 'Clear',
          description: 'clear sky',
          icon: '01d'
        }],
        dt: Math.floor(Date.now() / 1000)
      };

      setWeatherData(mockWeatherData);

      // Mock forecast data
      const mockForecastData = {
        list: Array.from({ length: 40 }, (_, index) => ({
          dt: Math.floor(Date.now() / 1000) + (index * 3 * 3600),
          main: {
            temp: 30,
            temp_min: 28,
            temp_max: 33,
            humidity: 70
          },
          weather: [{
            main: 'Clear',
            description: 'clear sky',
            icon: '01d'
          }],
          wind: {
            speed: 5
          }
        }))
      };

      setForecastData(mockForecastData);

    } catch (err) {
      setError('Failed to fetch weather data. Please try again.');
      console.error('Weather API error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Weather Mock Page</h1>
      <div>
        <label>State:</label>
        <select value={selectedState} onChange={e => setSelectedState(e.target.value)}>
          <option value="">Select State</option>
          {Object.keys(statesDistricts).map(state => (
            <option key={state} value={state}>{state}</option>
          ))}
        </select>
      </div>
      <div>
        <label>District:</label>
        <select value={selectedDistrict} onChange={e => setSelectedDistrict(e.target.value)} disabled={!selectedState}>
          <option value="">Select District</option>
          {districts.map(district => (
            <option key={district} value={district}>{district}</option>
          ))}
        </select>
      </div>
      <button onClick={fetchWeatherData} disabled={loading || !selectedState || !selectedDistrict}>
        {loading ? 'Loading...' : 'Get Weather'}
      </button>
      {error && <p style={{color: 'red'}}>{error}</p>}
      {weatherData && (
        <div>
          <h2>Current Weather in {weatherData.name}</h2>
          <p>Temperature: {weatherData.main.temp}°C</p>
          <p>Humidity: {weatherData.main.humidity}%</p>
          <p>Wind Speed: {weatherData.wind.speed} m/s</p>
          <p>Condition: {weatherData.weather[0].description}</p>
        </div>
      )}
    </div>
  );
};

export default WeatherMock;
