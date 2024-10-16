# Import the dependencies.
import numpy as np


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# Declare a Base using `automap_base()`
Base = automap_base()
# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`

Measurement = Base.classes.measurement

Station = Base.classes.station
# Create a session


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2012-02-12<br/>"
        f"/api/v1.0/2012-02-12/2016-01-13"

)

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # using the previous query that retrieved the data and precipitation scores 
    precip_scores = session.query(Measurement.date, Measurement.prcp).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2016-08-23').all()

    session.close()

    precipitation = list(np.ravel(precip_scores))

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # listing the stations
    station_query = session.query(Measurement.station).\
              group_by(Measurement.station).all()

    session.close()
    
    stations = list(np.ravel(station_query))
    
    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    # data for station USC00519281, the most active station
    query = session.query(Measurement.tobs).\
    filter(func.strftime('%Y-%m-%d', Measurement.date) >= '2016-08-23').\
    filter(Measurement.station == "USC00519281").all()

    session.close()
    
    tobs = list(np.ravel(query))
    
    return jsonify(tobs)


@app.route("/api/v1.0/<start>")
def start_date(start):

        session = Session(engine)

        # data for USC00519281 with custom entered start date 
        query_start_date = session.query(func.min(Measurement.tobs),  
        func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= start).all()
    
        results = list(np.ravel(query_start_date)) 

        return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def range_date(start, end):

        session = Session(engine)

        # data for USC00519281 with custom entered start and end date 
        query_start_date = session.query(func.min(Measurement.tobs),  
        func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.station == 'USC00519281').\
        filter(func.strftime('%Y-%m-%d', Measurement.date) >= start).\
        filter(func.strftime('%Y-%m-%d', Measurement.date) <= end).all()
    
        results = list(np.ravel(query_start_date)) 

        return jsonify(results)



if __name__ == "__main__":
    app.run(debug=True)




