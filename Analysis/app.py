# # 1. import Flask
# from flask import Flask

# # 2. Create an app, being sure to pass __name__
# app = Flask(__name__)


# # 3. Define what to do when a user hits the index route
# @app.route("/")
# def home():
#     print("Server received request for 'Home' page...")
#     return "Welcome to my 'Home' page!"


# # 4. Define what to do when a user hits the /about route
# @app.route("/about")
# def about():
#     print("Server received request for 'About' page...")
#     return "Welcome to my 'About' page!"


# if __name__ == "__main__":
#     app.run(debug=True)



import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station


# Flask Setup
##################################################
app = Flask(__name__)

# Flask Routes
##################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
    )


@app.route("/api/v1.0/precipitation")
def date_prcp():
    # Create session
    session = Session(engine)
#    # Query for dates and precipitation
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()

    # Convert list of tuples into normal list
    precipitation = list(np.ravel(results))
    # Return results in json format
    return jsonify( precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create session
    session = Session(engine)

    # Query for all stations
    results = session.query(station.name).all()
    session.close()
    #Return results in json list
    return jsonify(results)

@app.route("api/v1.0/tobs")
def tobs():
    #Create session
    session = Session(engine)

    #Query for most active station
    results = session.query(station.name).all()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_passengers = []
#     for name, age, sex in results:
#         passenger_dict = {}
#         passenger_dict["name"] = name
#         passenger_dict["age"] = age
#         passenger_dict["sex"] = sex
#         all_passengers.append(passenger_dict)

#     return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)
