import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

app = Flask(__name__)

# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
session = Session(engine)
measurement = Base.classes.measurement
station = Base.classes.station

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start>` and `/api/v1.0/<start>/<end>"
    )

# @app.route("/new/<station_name>")
# def get_temp_stats(station_name):
#     date = dt.date(2017, 7, 21)
#     results_list = session.query(measurement.station, measurement.date, func.min(measurement.tobs), func.max(measurement.tobs),
#     func.avg(measurement.tobs)).\
#     group_by(measurement.date).\
#     filter(measurement.date >= date).\
#     filter(measurement.station == station_name).all()

#     for station in results_list:
#         search_term = station_name.replace(" ", "").lower()
#         session.close()
#         return jsonify(results_list)
    


@app.route("/new/<date>")
def get_temp_stats(date):
    results_list = session.query(measurement.station, measurement.date, func.min(measurement.tobs), func.max(measurement.tobs),
    func.avg(measurement.tobs)).\
    group_by(measurement.date).\
    filter(measurement.date >= date).all()
    for the_date in results_list:
        search_term = date.replace(" ", "").lower()
        session.close()
        return jsonify(results_list)

# def get_temp_stats_1(date):
#     date = dt.date(2017, 7, 21)
#     results_list = session.query(measurement.station, measurement.date, func.min(measurement.tobs), func.max(measurement.tobs),
#     func.avg(measurement.tobs)).\
#     group_by(measurement.date).\
#     filter(measurement.date >= date).\
#     filter(measurement.station == station_name).all()

#     for station in results_list:
#         search_term = station_name.replace(" ", "").lower()
#         session.close()
#         return jsonify(results_list)

if __name__ == "__main__":
    app.run(debug=True)

# def get_temp_stats_1(start_date):
#     date = dt.date(2017, 7, 21)
#     results_list = session.query(measurement.station, measurement.date, func.min(measurement.tobs), func.max(measurement.tobs),
#     func.avg(measurement.tobs)).\
#     group_by(measurement.date).\
#     filter(measurement.date >= date).\
#     filter(measurement.station == station_name).all()

#     for start_date in results_list:
#         search_term = start_date.replace(" ", "").lower()
#         session.close()
#         return jsonify(results_list)
    
# if __name__ == "__main__":
#     app.run(debug=True)


# # USC00519281










