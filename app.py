from flask_cors import CORS
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired
import requests
from dotenv import dotenv_values
import os


# pulling saved API key from environment:
config = dotenv_values(".env")
API_key = config["weather_api"]

g_config = dotenv_values("google.env")
google_API = g_config["google_API"]

w_config = dotenv_values("new_weather_api.env")
weather_key = w_config["new_weather_api"]

new_config = dotenv_values("weather_key.env")
weather_key = new_config["weather_key"]

allowed_origin = "http://localhost:3000"

app = Flask(__name__)
CORS(app, origins=allowed_origin, supports_credentials=True)


app.config['SECRET_KEY'] = dotenv_values('SECRET_KEY') or 'abc123ced456'  # Setting the default secret key for CSRF protection

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        city_name = request.form.get('city')

        if city_name:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}"
            response = requests.get(url)

            if 'application/json' in request.accept_mimetypes:
                # If client accepts JSON, return JSON response
                if response.status_code == 200:
                    weather_data = response.json()
                    temperature_celsius = round(weather_data['main']['temp'] - 273.15, 2)
                    return jsonify({
                        'city': city_name,
                        'temperature': temperature_celsius,
                        'weather': weather_data['weather'][0]['description']
                    }), 200
                else:
                    return jsonify({'error': 'Location not found. Please try again.'}), 404
            else:
                # If client expects HTML, render HTML template
                if response.status_code == 200:
                    weather_data = response.json()
                    temperature_celsius = round(weather_data['main']['temp'] - 273.15, 2)
                    return render_template('result.html', weather=weather_data, temperature=temperature_celsius)
                else:
                    return "Location not found. Please try again."

        return "Please enter a city name."

    return render_template('search.html')

@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
