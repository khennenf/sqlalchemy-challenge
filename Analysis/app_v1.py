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
        f"/api/v1.0/start and /api/v1.0/start/end<br>"
        f"- - - - - (Use Date Format yyyy-mm-dd for start and end dates)"
    )

# Convert the query results to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.    
@app.route("/api/v1.0/precipitation")
def date_prcp():
    # Create session
    session = Session(engine)
#    # Query for dates and precipitation
    results = session.query(measurement.date, measurement.prcp).\
    filter(measurement.date >= '2016-08-23').\
    filter(measurement.date <= '2017-08-23').all()
    session.close()
    # Convert list of tuples into normal list
    precipitation = list(np.ravel(results))
    # Return results in json format
    return jsonify(precipitation)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Create session
    session = Session(engine)
    # Query for all stations
    results = session.query(station.name).all()
    session.close()
    #Return results in json list
    return jsonify(results)    


# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    #Create session
    session = Session(engine)
    session.query(measurement.date).order_by(measurement.date.desc()).first()
    latest_date = dt.date(2017,8,23)
    past_year = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    past_year_start = dt.date(2016, 8, 22)
    previous_year = dt.date(2016, 8, 22) - dt.timedelta(days=366)
    session.query(measurement.date, measurement.prcp).\
        filter(measurement.date < latest_date).\
        filter(measurement.date > past_year).all()
    most_active = session.query(measurement.station).\
    group_by(measurement.station).order_by(func.count(measurement.tobs).desc())
    results = session.query(measurement.station, measurement.date, measurement.tobs).\
        filter(measurement.station == most_active).\
        filter(measurement.date < past_year_start).\
        filter(measurement.date > previous_year).all()
    session.close()

    return jsonify(results)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# Use Date Format e.g.: 2017-06-23
@app.route("/api/v1.0/<start>")
def get_temp_stats_start_summary(start):
    session = Session(engine)
    summary_result = session.query(func.min(measurement.tobs), func.max(measurement.tobs),
    func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()
    session.close()
    return jsonify(summary_result)    

#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
# Use Date Format e.g.: 2017-06-23
@app.route("/api/v1.0/<start>/<end>")
def get_temp_stats_start_end(start, end):
    session = Session(engine)
    results_list = session.query(func.min(measurement.tobs), func.max(measurement.tobs),
    func.avg(measurement.tobs)).\
    filter(measurement.date >= start).\
    filter(measurement.date <= end).all()
    session.close()
    return jsonify(results_list)


if __name__ == '__main__':
    app.run(debug=True)    


