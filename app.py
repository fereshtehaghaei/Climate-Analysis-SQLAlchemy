#########################################################################################
# SQLAlchemy and Flask Challenge - Surfs Up!
# Submitted by : Fereshteh Aghaei | DU Data Analysis and Visualization | Nov 18, 2020
# This script will return JSONified query results from API endpoints and
# serve the queries with Flask to enable a Climate Web App.
#########################################################################################


#################################################
# Import Libraries
#################################################
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False # Got Helpe from --> https://stackoverflow.com/questions/54446080/how-to-keep-order-of-sorted-dictionary-passed-to-jsonify-function

#################################################
# Flask Routes
#################################################

# Define API Routes in Home Page
@app.route("/") 
def welcome():
    return (
"""<html>
    
<h1><center>Hawaii Climate </h1>

<center><img src="https://specials-images.forbesimg.com/imageserve/5e086a2f25ab5d0007cf74ec/960x0.jpg?cropX1=1&cropX2=1867&cropY1=0&cropY2=1244" alt="Hawaii Weather"/></center>


<h1>Available API Routes: </h1>
<br>


<p><b>Precipitation Analysis:</p></b>
<ul>
<li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
</ul>

<br>
<p><b>List of Stations:</p></b>
<ul>
<li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
</ul>

<br>
<p><b>Temperature Observations:</p></b>
<ul>
<li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
</ul>

<br>   
<p><b>Temperature Analysis for a given start date (YYYY-MM-DD) :</p></b>
<ul>
<li><a href="/api/v1.0/date/2016-08-23">/api/v1.0/date/<start></a></li>
</ul>

<br>
<p><b>Temperature Analysis between specified start date (YYYY-MM-DD) and end date (YYYY-MM-DD) :</p></b>
<ul>
<li><a href="/api/v1.0/date/2016-08-01/2016-08-07">/api/v1.0/date/<start>/<end></a></li>
</ul>
<br>        
</html>""")

#------------------------------------------------


# Define Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create Session from pythong to DB
    session = Session(engine) 

    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    climate_data =[]
    for date, prcp in results:
        climate_dict ={}
        climate_dict['date'] = date
        climate_dict['prcp']= prcp
        climate_data.append(climate_dict)

    # Return the JSON representation of your dictionary. 
    return jsonify(climate_data)


#------------------------------------------------


@app.route("/api/v1.0/stations")
def stations():    

    # Create Session from pythong to DB
    session = Session(engine) 
    
    # Query for list of stations
    results = session.query(Station.station, Station.name).all()
    
    station_data =[]
    for name, station in results:
        station_dict ={}
        station_dict['Station ID'] = name
        station_dict['Station']= station
        station_data.append(station_dict)

    # Return the JSON representation of your dictionary. 
    return jsonify(station_data)
    

#------------------------------------------------


@app.route("/api/v1.0/tobs")
def tobs(): 
    # Create Session from pythong to DB
    session = Session(engine) 
    
    # Query for lastest date
    lastest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    # Convert date into a string
    lastest_date_str = dt.datetime.strptime(lastest_date,"%Y-%m-%d")
    
    # Query for one year ago
    year_ago = lastest_date_str - dt.timedelta(days=365)
    # Convert date into a string
    year_ago_str = year_ago.strftime("%Y-%m-%d")

    # Query for the most active station
    most_active_station = session.query(    Measurement.station, 
                                            func.count(Measurement.station)).\
                                            group_by(Measurement.station).\
                                            order_by(func.count(Measurement.station).desc()).first()[0]

    # Query the dates and temperature observations of the most active station for the last year of data
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(func.strftime('%Y-%m-%d',Measurement.date)>= year_ago_str).\
        filter(Measurement.station == most_active_station).all()

    tobs_data=[]
    for date, tobs in results:
        tobs_dict ={}
        tobs_dict['Date'] = date
        tobs_dict['Temperature']= tobs
        tobs_data.append(tobs_dict)

    # Return the JSON representation of your dictionary. 
    return jsonify(tobs_data)


#------------------------------------------------


@app.route("/api/v1.0/date/<start>")
@app.route("/api/v1.0/date/<start>/<end>")
def start_end_date(start=None,end=None): 

    # Create Session from pythong to DB
    session = Session(engine) 

    # Query temperature statistics from the start date to the end date
    if end:
        results= session.query(    
                               Measurement.date,
                               func.min(Measurement.tobs), 
                               func.max(Measurement.tobs), 
                               func.avg(Measurement.tobs)).\
                               filter(Measurement.date >= start).\
                               filter(Measurement.date <= end).\
                               order_by (Measurement.date).all()
    else:
        results= session.query(    
                               Measurement.date,
                               func.min(Measurement.tobs), 
                               func.max(Measurement.tobs), 
                               func.avg(Measurement.tobs)).\
                               filter(Measurement.date >= start).\
                               order_by (Measurement.date).all()    
    temp_data=[]
    for date, tmin, tmax, tavg in results:
        temp_dict={}
        temp_dict['Start Date']= start
        temp_dict['End Date']= end
        temp_dict['Minimum Temperature'] = tmin
        temp_dict['Maximum Temperature']= tmax
        temp_dict['Avgerage Temperature']= round(tavg,2)

        temp_data.append(temp_dict)

    # Return the JSON representation of your dictionary. 
    return jsonify(temp_dict)   

#------------------------------------------------

#################################################
# Run the application
#################################################
if __name__ == '__main__':
    app.run(debug=True)