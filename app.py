from flask import Flask, redirect, url_for, jsonify, request, render_template, request, template_rendered
import requests
from dotenv import dotenv_values
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import InputRequired
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import os
import requests
import json
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer
import requests
import json

# Adding in bloggers itinerary as locations for locations selector:
locations = {
    "Lake District National Park": {"lat": 54.4609, "lng": -3.0886},
    "Corfe Castle": {"lat": 50.6419, "lng": -2.0554},
    "The Cotswolds": {"lat": 51.9294, "lng": -1.7203},
    "Cambridge": {"lat": 52.2053, "lng": 0.1218},
    "Bristol": {"lat": 51.4545, "lng": -2.5879},
    "Oxford": {"lat": 51.752, "lng": -1.2577},
    "Norwich": {"lat": 52.6309, "lng": 1.2974},
    "Stonehenge": {"lat": 51.1789, "lng": -1.8262},
    "Watergate Bay": {"lat": 50.4429, "lng": -5.0553},
    "Birmingham": {"lat": 52.4862, "lng": -1.8904}
}


# Generating choices from the above locations dictionary using class method:
class LocationForm(FlaskForm):
    location = SelectField('Select a location', choices=[(location, location) for location in locations.keys()], validators=[InputRequired()])
    submit = SubmitField('Submit')


# pulling saved API key from environment:
config = dotenv_values(".env")
API_key = (config["weather_api"])

g_config = dotenv_values("google.env")
google_API = (g_config["google_API"])

w_config = dotenv_values("new_weather_api.env")
weather_key = (w_config["new_weather_api"])

w_config = dotenv_values("weather_key.env")
weather_key = (w_config["weather_key"])

w_config = dotenv_values("new_key")
new_key="47d7c197f3c0823cadf639f1e19751c4"


app = Flask(__name__)
CORS(app, resources={r"/allie-chat": {"origins": "http://localhost:3000"}})

app.config['SECRET_KEY'] = dotenv_values('SECRET_KEY') or \
                           'abc123ced456'  # Setting the default secret key for CSRF protection


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        city_name = request.form['city']
        # pulling API data from openweathermap API:
        if city_name:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}"
            # if status_code is 200, weather data is generated as a json response, converted from kelvin to celcius temperature
            # with round() method, rendered via a template and displayed via result.html:
            response = requests.get(url)
            if response.status_code == 200:
                weather_data = response.json()
                temperature_celsius = round(weather_data['main']['temp'] - 273.15, 2)
                return render_template('result.html', weather=weather_data, temperature=temperature_celsius)
            else:
                return "Location not found. Please try again."

        return "Please enter a city name."

    return render_template('search.html')

API_key = 'new_key'

# Create a new instance of the ChatBot
my_bot = ChatBot("Bain")

# Referencing my_bot to create a new trainer:
trainer = ChatterBotCorpusTrainer(my_bot)

# specifying file path for json data to run:
json_file_path =  "/Users/ruthfisher-bain/Downloads/magicalUK-main 2/sample/locations.json"

# Loading my custom locations data from the JSON file I created:
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Training the bot with additional conversations
small_talk = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]

math_talk_1 = [
    'pythagorean theorem',
    'a squared plus b squared equals c squared.'
]

math_talk_2 = [
    'law of cosines',
    'c**2 = a**2 + b**2 - 2 * a * b * cos(gamma)'
]

weather_talk_2 = [
    'What is the temperature in {locations} over the next five days?',
    "The temperature in {} over the next five days is {}°C."
]

more_weather_talk = [
    'What is the forecast for {} tomorrow?',
    'Is it going to rain in {}?',
    'Tell me about the weather conditions in {}.',
    'What are the next five days in {}?',
]

# Training the bot
list_trainer = ListTrainer(my_bot)
corpus_trainer = ChatterBotCorpusTrainer(my_bot)

for item in (small_talk, math_talk_1, math_talk_2):
    list_trainer.train(item)

for item in (weather_talk_2, more_weather_talk):
    list_trainer.train(item)

corpus_trainer.train('chatterbot.corpus.english')
corpus_trainer.train('chatterbot.corpus.english.conversations')


@app.route('/allie-chat', methods=['POST', 'OPTIONS'])
def chatbot_route():
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'success'})
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    elif request.method == 'POST':
        try:
            data = request.json
            user_input = data.get('message', '')
            chatbot_response = my_bot.respond(user_input)
            return jsonify({'botResponse': str(chatbot_response)})
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route("/about")
def about():
    return render_template('about.html')



@app.route('/weather', methods=['GET', 'POST'])
def weather():
    form = LocationForm()

    if form.validate_on_submit():
        selected_location = form.location.data
        selected_lat = locations[selected_location]['lat']
        selected_lng = locations[selected_location]['lng']

        # Using the OpenWeather API to fetch weather data with a new API key:
        api_endpoint = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': selected_lat,
            'lon': selected_lng,
            'appid': weather_key,
            'units': 'metric'  # making sure the temp is in celcius: this took a while!
        }
        response = requests.get(api_endpoint, params=params)

        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            forecast = weather_data['weather'][0]['description']
            return render_template('weather.html', form=form, selected_location=selected_location,
                                   selected_lat=selected_lat, selected_lng=selected_lng, temperature=temperature,
                                   forecast=forecast)
        else:
            error_message = "Failed to fetch weather information"
            return render_template('weather.html', form=form, error_message=error_message)

    return render_template('weather.html', form=form)



@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"


if __name__ == "__main__":
    app.run(debug=True)