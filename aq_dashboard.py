"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openaq


APP = Flask(__name__)
api = openaq.OpenAQ()

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy()
# DB.init_app(APP)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'TODO - write a nice representation of Records'

@APP.route('/')
def root():
    """Base view."""
    return render_template('start.html', title='Home')

@APP.route('/la', methods = ['GET', 'POST'])
def la():
    # Getting info from the api, and displaying the data
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    observations = body['results'][:100]
    for s in range(len(observations)):
        new_data = []
        utc_datetime = []
        utc_datetime.append((observations[s])['date']['utc'])
        value = observations[s]['value']
        new_data.append(utc_datetime, value)


    return render_template()

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.commit()
    return 'Data refreshed!'