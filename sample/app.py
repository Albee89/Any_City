from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from dotenv import load_dotenv
import os
import requests
from flask_sqlalchemy import SQLAlchemy

# Creating Flask app:
app = Flask(__name__)

# Loading keys from environment
load_dotenv(".env")
API_KEY = os.getenv("weather_api_key")

# Database setup
db_name = "ab_bit.db"

# Configuring SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating SQLAlchemy instance and connecting
db = SQLAlchemy(app)

# Creating a model for the database
class Data(db.Model):
    __tablename__ = 'blog_locations1'
    field1 = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    datetime = db.Column(db.Float)
    condition = db.Column(db.String(30))
    description = db.Column(db.String(255))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)


# Create the database and insert some example data
with app.app_context():
    db.create_all()
    user = User(username='john_doe')
    db.session.add(user)
    db.session.commit()


@app.route('/api/data', methods=['GET'])
def get_data():
    users = User.query.all()

    # Convert the list of users to a list of dictionaries
    user_data = [{'id': user.id, 'username': user.username} for user in users]

    response_data = {'users': user_data}
    return jsonify(response_data)


# Creating the bot variable:
chatbot = ChatBot(
    name="Allie",
    read_only=True,
    logic_adapters=["chatterbot.logic.MathematicalEvaluation", "chatterbot.logic.BestMatch"]
)

# Referencing chatbot to create a new trainer:
trainer = ChatterBotCorpusTrainer(chatbot)

# Training the bot with some sample conversations:
trainer.train("chatterbot.corpus.english")
trainer.train("chatterbot.corpus.english.conversations")


def get_weather(city):
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {"q": city, "appid": API_KEY, "units": "metric"}  # Specify the API key and units
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        print(f"Error: Unable to fetch weather data for {city}. Status code: {response.status_code}")
        return None

# Main route to render the chatbot interface
@app.route('/')
def home():
    return render_template('index.html')

# Creating a route to handle chatbot interactions:
@app.route('/chatbot', methods=['POST'])
def chatbot_route():
    user_input = request.form.get('user_input')
    app.logger.info(f"Received user input: {user_input}")
    if not user_input:
        return jsonify({'error': 'User input parameter is required'}), 400

    bot_response = str(chatbot.get_response(user_input))
    app.logger.info(f"Bot response: {bot_response}")
    # Getting a response from the chatbot based on user input
    return jsonify({'response': bot_response})

# Route to get weather data:
@app.route('/get_weather/<city>')
def get_weather_route(city):
    weather_data = get_weather(city)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({'error': f'Weather data not available for {city}'}), 404

if __name__ == '__main__':
    app.run(debug=True)
