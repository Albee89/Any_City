# Import the library.
import requests
import os
from dotenv import dotenv_values

#pull saved API key from environment:
config = dotenv_values(".env")
API_key = (config["weather_api"])

#DISPLAY api key
print(API_key)
