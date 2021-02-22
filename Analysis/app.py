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
        f"/api/v1.0/<start>` and `/api/v1.0/<start>/<end>"
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


#############################################################################
@app.route("/api/v1.0/tobs")
def tobs():
    #Create session
    session = Session(engine)

#  * Query the dates and temperature observations of the most active station for the last year of data.
    session.query(measurement.date).order_by(measurement.date.desc()).first()
    latest_date = dt.date(2017,8,23)
    past_year = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    past_year_start = dt.date(2016, 8, 22)
    previous_year = dt.date(2016, 8, 22) - dt.timedelta(days=366)
    session.query(measurement.date, measurement.prcp).\
        filter(measurement.date < latest_date).\
        filter(measurement.date > past_year).all()
    most_active = session.query(measurement.station).\
        group_by(measurement.station).order_by(func.count(measurement.tobs).desc()).first()   
    results = session.query(measurement.station, measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date < past_year_start).\
        filter(measurement.date > previous_year).all()
    session.close()

    return jsonify(results)
#################################    
@app.route("/api/v1.0/<date>")
def get_temp_stats(date):
    session = Session(engine)
    results_list = session.query(measurement.station, measurement.date, func.min(measurement.tobs), func.max(measurement.tobs),
    func.avg(measurement.tobs)).\
    group_by(measurement.date).\
    filter(measurement.date >= date).all()
    for the_date in results_list:
        search_term = date.replace(" ", "").lower()
        session.close()
        return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=True)














#     session = Session(engine)
#     date = dt.date(2017, 8, 21)
#     results_list = session.query(measurement.date, func.min(measurement.tobs), func.max(measurement.tobs),
#               func.avg(measurement.tobs)).\
#               group_by(measurement.date).\
#               filter(measurement.date >= date).all()
#     for check_date in results_list:
#         check_date = date
#         return jsonify(results_list)
#     session.close()

# if __name__ == '__main__':
#     app.run(debug=True)
