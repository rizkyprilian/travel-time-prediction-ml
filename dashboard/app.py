from flask import Flask, jsonify, render_template, request
import joblib
import pandas as pd
import json
import numpy as np
import importlib

# config.py would not be uploaded to github, so I kept it in separate files
config = importlib.import_module('config')

# what's my name?
app = Flask(__name__)

# -----------------------------------
# Database Connection
# -----------------------------------

with open('dataset.json') as json_file:
    data = json.load(json_file)


# -------------------------------------
# Routes for Main Article 
# -------------------------------------

@app.route('/')
def home():
    return render_template('home.html')

# --------------------------------------
# Routes for model predict demonstration
# --------------------------------------

# this route would render the view which show a map where user can make a route on a map
@app.route('/predictmap')
def map_predict():
    return render_template('predictmap.html', mapbox_access_token=config.mapbox_access_token)

# this route is going to receive POST parameters from the /predictmap and return a json
@app.route('/predict', methods=['POST'])
def predict():

    input_ = request.form

    # ['distance',
    #  'departure_hour',
    #  'average_speed',
    #  'max_speed',
    #  'n_intersections',
    #  'n_tolls',
    #  'n_motorways',
    #  'n_tunnels',
    #  'n_steps',
    #  'n_left_turns',
    #  'n_right_turns',
    #  'n_u_turns',
    #  'n_go_straight',
    #  'day_of_week']

    model_input = np.array([ [ 
        input_['distance'], 
        input_['departure_hour'], 
        input_['avg_speed'], 
        input_['max_speed'], 
        input_['n_intersections'],
        input_['n_tolls'],
        input_['n_motorways'],
        input_['n_tunnels'],
        input_['n_steps'],
        input_['n_left_turns'],
        input_['n_right_turns'],
        input_['n_u_turns'],
        input_['n_go_straight'],
        input_['day_of_week'],
    ] ])

    print(model_input.shape)

    model_input = scaler.transform(model_input)

    prediction = model.predict(model_input)

    print(prediction)
    # load the precious Model !!
    return jsonify({
        'est_travel_time': int(abs(prediction[0])),
        'error': False
    })

# --------------------------------------
# Routes for viewing dataset
# --------------------------------------

@app.route('/dataset')
def datapreview():

    columns = [
        {
            "field": "device_id", # which is the field's name of data key 
            "title": "device_id", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "license_plate", # which is the field's name of data key 
            "title": "license_plate", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "driver", # which is the field's name of data key 
            "title": "driver", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "vehicle_group", # which is the field's name of data key 
            "title": "vehicle_group", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "departure_time", # which is the field's name of data key 
            "title": "departure_time", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "arrival_time", # which is the field's name of data key 
            "title": "arrival_time", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "distance", # which is the field's name of data key 
            "title": "distance", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "interval", # which is the field's name of data key 
            "title": "interval", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "origin_region", # which is the field's name of data key 
            "title": "origin_region", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "destination_region", # which is the field's name of data key 
            "title": "destination_region", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "departure_hour", # which is the field's name of data key 
            "title": "departure_hour", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "trip_time_cat", # which is the field's name of data key 
            "title": "trip_time_cat", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "average_speed", # which is the field's name of data key 
            "title": "average_speed", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "max_speed", # which is the field's name of data key 
            "title": "max_speed", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "n_intersections", # which is the field's name of data key 
            "title": "n_intersections", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "n_tolls", # which is the field's name of data key 
            "title": "n_tolls", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "n_motorways", # which is the field's name of data key 
            "title": "n_motorways", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "n_bridges", # which is the field's name of data key 
            "title": "n_bridges", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "n_tunnels", # which is the field's name of data key 
            "title": "n_tunnels", # display as the table header's name
            "sortable": True,
        },
         {
            "field": "n_steps", # which is the field's name of data key 
            "title": "n_steps", # display as the table header's name
            "sortable": True,
        },
         {
            "field": "n_left_turns", # which is the field's name of data key 
            "title": "n_left_turns", # display as the table header's name
            "sortable": True,
        },
         {
            "field": "n_right_turns", # which is the field's name of data key 
            "title": "n_right_turns", # display as the table header's name
            "sortable": True,
        },
         {
            "field": "n_u_turns", # which is the field's name of data key 
            "title": "n_u_turns", # display as the table header's name
            "sortable": True,
        },
         {
            "field": "n_go_straight", # which is the field's name of data key 
            "title": "n_go_straight", # display as the table header's name
            "sortable": True,
        },
         {
            "field": "matched_distance", # which is the field's name of data key 
            "title": "matched_distance", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "day_of_week", # which is the field's name of data key 
            "title": "day_of_week", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "hour_of_day", # which is the field's name of data key 
            "title": "hour_of_day", # display as the table header's name
            "sortable": True,
        }
    ]


    return render_template('datapreview.html', 
      data=data,
      columns=columns,
      title='Trip data on April 2020')


if __name__ == '__main__':
    model = joblib.load('model_lasso')
    scaler = joblib.load('robust_scaler')
    app.run(debug=True)
    # server = Server(app.wsgi_app)
    # server.serve()