from flask import Flask, render_template, request
import joblib
import pandas as pd
import json

app = Flask(__name__)


with open('dataset.json') as json_file:
    data = json.load(json_file)



@app.route('/')
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
            "field": "average_altitude", # which is the field's name of data key 
            "title": "average_altitude", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "max_speed", # which is the field's name of data key 
            "title": "max_speed", # display as the table header's name
            "sortable": True,
        },
        {
            "field": "n_intersection", # which is the field's name of data key 
            "title": "n_intersection", # display as the table header's name
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
        }
    ]


    return render_template('datapreview.html', 
      data=data,
      columns=columns,
      title='Trip data on April 2020')


if __name__ == '__main__':
    model = joblib.load('model_elasticnet')
    app.run(debug=True)