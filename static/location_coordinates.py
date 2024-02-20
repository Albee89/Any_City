from typing import List, Any
import requests
from dotenv import dotenv_values
import json
from flask import Flask


# Call OpenWeather API key using dotenv:
config = dotenv_values(".env")
api_key = config.get("weather_api")  # Use get to handle missing key more gracefully

# defining the location's names and exact coordinates in "travel locations" dictionary:
def coordinates(cityname):
    travel_locations = {
        'Lake District National Park': {'latitude': 54.4609, 'longitude': -3.0886},
        'Corfe Castle': {'latitude': 50.6396, 'longitude': -2.0566},
        'The Cotswolds': {'latitude': 51.8330, 'longitude': -1.8433},
        'Cambridge': {'latitude': 52.2053, 'longitude': 0.1218},
        'Bristol': {'latitude': 51.7520, 'longitude': -2.5879},
        'Oxford': {'latitude': 51.7520, 'longitude': -1.2577},
        'Norwich': {'latitude': 52.6309, 'longitude': 1.2974},
        'Stonehenge': {'latitude': 51.1789, 'longitude': -1.8262},
        'Watergate': {'latitude': 50.4429, 'longitude': -5.0553},
        'Birmingham': {'latitude': 52.4862, 'longitude': -1.8904}
    } #returning travel locations with the .get() method with cityname, travel locations as parameters
    return travel_locations.get(cityname, {})

# defining co-ordinates function, defining lat and lon variables to call on:
def get_coordinates(cityname, travel_locations):
    lat = travel_locations[cityname]['latitude'] if cityname in travel_locations else None
    lon = travel_locations[cityname]['longitude'] if cityname in travel_locations else None

    if lat is not None and lon is not None:
        coord = [lat, lon]
        return coord
    else:
        return None

# defining get_weather function and ocation variables with city name and api_key as parameters to return requests.get()
# method:
def get_weather_data(cityname, api_key):
    location = coordinates(cityname)

    if location:
        lat, lon = location['latitude'], location['longitude']
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"lat": lat, "lon": lon, "appid": api_key, "units": "metric"}

        response = requests.get(base_url, params=params)
# checking status_code and returning error message
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Failed to fetch weather data"}

    return {"error": "City not found"}

# calling the functions using city name and api_key, outside of the functions:
cityname = "Lake District National Park"
# saving get_weather_data in weather_data variable with cityname and api_key params:
weather_data = get_weather_data(cityname, api_key)
# returning data with the json.dumps() method, displaying weather data with an indent of 4:
print("The weather today in Lake District National Park is:",  json.dumps(weather_data, indent=4))


cityname = "Corfe Castle"
weather_data = get_weather_data(cityname, api_key)
print("The weather today in Corfe Castle is: ", json.dumps(weather_data, indent=4))


cityname = "The Cotswolds"
weather_data = get_weather_data(cityname, api_key)
print("The weather today in The Cotswolds is: ", json.dumps(weather_data, indent=4))


cityname = "Cambridge"
weather_data = get_weather_data(cityname, api_key)
print("The weather today in Cmabridge is: ", json.dumps(weather_data, indent=4))


cityname = "Bristol"
weather_data = get_weather_data(cityname, api_key)
print("The weather today in Bristol is: ", json.dumps(weather_data, indent=4))

cityname = "Oxford"
weather_data = get_weather_data(cityname, api_key)
print("The weather today in Oxford is: ", json.dumps(weather_data, indent=4))

cityname = "Norwich"
weather_data = get_weather_data(cityname, api_key)
print("The weather today in Norwich is: ", json.dumps(weather_data, indent=4))