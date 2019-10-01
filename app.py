import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

start_date = ["%y-%m-%d"]
end_date = ["%y-%m-%d"]

# Flask Setup
#################################################
app = Flask(__name__)

################################################
# Flask Routes
#################################################

@app.route("/")
def Homepage():
    """List all routes that are available."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation values for the last one year"""
    # Query precipitation
    oydate = dt.datetime(2016, 8, 23)
    oydata = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > oydate).all()

    session.close()

    # Create a dictionary from the row data and append to a list of oydata
    all_oydata = []
    for date, prcp in oydata:
       oydata_dict = {}
       oydata_dict["date"] = date
       oydata_dict["prcp"] = prcp
       all_oydata.append(oydata_dict)

    return jsonify(all_oydata)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations used"""
    # Query all stations used
    diststation = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(diststation))

    return jsonify(all_stations)
    
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperatures for the last one year"""
    # Query one year temperatures
    oytempdate = dt.datetime(2016, 8, 23)
    oytempdata = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > oytempdate).all()

    session.close()
    
    # Create a dictionary from the row data and append to a list of oytempdata
    all_oytempdata = []
    for date, tobs in oytempdata:
       oytempdata_dict = {}
       oytempdata_dict["date"] = date
       oytempdata_dict["tobs"] = tobs
       all_oytempdata.append(oytempdata_dict)

    return jsonify(all_oytempdata)
    
@app.route("/api/v1.0/<start_date>") 
def start_temps(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return min, avg and max temperature for given start date"""
    # Query temp of given start date
    ustartdate = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all() 
    
    session.close()

    return jsonify(ustartdate)

@app.route("/api/v1.0/<start_date>/<end_date>")
def end_temps(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return min, avg and max temperature for given start date and end date"""
    # Query temp of given start date and end date
    startenddate = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    return jsonify(startenddate)


if __name__ == '__main__':
    app.run(debug=True)