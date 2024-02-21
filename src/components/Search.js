import React, { useState } from 'react';

const Search = () => {
  const [city, setCity] = useState('');
  const [weatherData, setWeatherData] = useState(null);
  const [error, setError] = useState(null);

  const handleSearch = () => {
    fetch('http://localhost:5000/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        city: city,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          setError(data.error);
          setWeatherData(null);
        } else {
          setError(null);
          setWeatherData(data);
        }
      })
      .catch((error) => {
        setError('An error occurred while fetching weather data.');
        setWeatherData(null);
        console.error('Error:', error);
      });
  };

  return (
    <div>
      <h2>Weather Search</h2>
      <label>
        Enter City:
        <input type="text" value={city} onChange={(e) => setCity(e.target.value)} />
      </label>
      <button onClick={handleSearch}>Search</button>

      {weatherData && (
        <div>
          <h3>Weather Information</h3>
          <p>City: {weatherData.city}</p>
          <p>Temperature: {weatherData.temperature} °C</p>
          <p>Weather: {weatherData.weather}</p>
        </div>
      )}

      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default Search;
