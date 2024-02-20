from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class LocationForm(FlaskForm):
    location = SelectField('Select a location', validators=[DataRequired("Please select a location")])
    submit = SubmitField('Submit')

