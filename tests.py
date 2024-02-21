from flask import Flask, redirect, url_for, request, render_template, request, template_rendered

import requests

from dotenv import dotenv_values

#pulling saved API keys from my local environment:


config = dotenv_values("weather_3.env")
which_API = (config['weather_3'])
print(which_API)

