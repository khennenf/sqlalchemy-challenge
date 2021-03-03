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
        f"/api/v1.0/start and /api/v1.0/start/end<br>"

    )    

@app.route("/api/v1.1/<start>")
def get_temp_stats_start_summary(start):
    session = Session(engine)
    summary_result = session.query(func.min(measurement.tobs), func.max(measurement.tobs),
    func.avg(measurement.tobs)).\
        filter(measurement.date >= start).all()
    session.close()
    return jsonify(summary_result)    

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


if __name__ == '__main__':
    app.run(debug=True)    