# SQLAlchemy Challenge - Surfs Up!

![](Images/surfs-up.png)

Planning a vacation to Honolulu, Hawaii! By Python and SQLAlchemy, I will be doing basic climate analysis and data exploration from climate database to plan this vacation. 

The following outlines are the steps I will be taking to complete this analysis: 

## Step 1 - Climate Analysis and Exploration

To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* ###### Creating The Engine to connect to "hawaii.sqlite" database

  ```
  engine = create_engine("sqlite:///Resources/hawaii.sqlite")
  ```

  ###### Create automap_base() to reflect your tables into classes

  - Reflect Tables into SQLAlchemy ORM

  ```
  # reflect an existing database into a new model
  Base = automap_base()
  
  # reflect the tables
  Base.prepare(engine, reflect=True)
  
  # We can view all of the classes that automap found
  Base.classes.keys()
  ```

  ```
  ['measurement', 'station']
  ```

### Precipitation Analysis

* Design a query to retrieve the last 12 months of precipitation data.

* Select only the `date` and `prcp` values.

  ```
  lastyear_prcp_date = session.query(Measurement.date, Measurement.prcp).\
                            filter( Measurement.date >= year_ago ).\
                            order_by(Measurement.date.desc()).all()
  lastyear_prcp_date[:5]
  ```

  

* Load the query results into a Pandas DataFrame and set the index to the date column.

  |            | Precipitation |
  | :--------- | :------------ |
  | Date       |               |
  | 2016-08-23 | 0.70          |
  | 2016-08-23 | 0.00          |
  | 2016-08-23 | 0.15          |
  | 2016-08-23 | 1.79          |
  | 2016-08-23 | NaN           |

  

* Sort the DataFrame values by `date`.

  ```
  df = pd.DataFrame(lastyear_prcp_date, columns=["Date", "Precipitation"])
  df.set_index('Date', inplace=True) 
  df.sort_values('Date', inplace=True) 
  df.head()
  ```

  |            | Precipitation |
  | :--------- | :------------ |
  | Date       |               |
  | 2016-08-23 | 0.70          |
  | 2016-08-23 | 0.00          |
  | 2016-08-23 | 0.15          |
  | 2016-08-23 | 1.79          |
  | 2016-08-23 | NaN           |

* Plot the results using the DataFrame `plot` method.

  ![](Images/precipitation.png)

  

* Use Pandas to print the summary statistics for the precipitation data.

  ```
  df.describe()
  ```

  |       | Precipitation |
  | :---- | :------------ |
  | count | 2021.000000   |
  | mean  | 0.177279      |
  | std   | 0.461190      |
  | min   | 0.000000      |
  | 25%   | 0.000000      |
  | 50%   | 0.020000      |
  | 75%   | 0.130000      |
  | max   | 6.700000      |

### Station Analysis

* Design a query to calculate the total number of stations.

```
stations = session.query(Measurement).group_by(Measurement.station).count()
print (f'Total Number of Stations:  {stations}
```

* Design a query to find the most active stations.

  * List the stations and observation counts in descending order.

    ```
    most_active= session.query(Measurement.station, 		  
    					       func.count(Measurement.station)).\
                               group_by(Measurement.station).\
                               order_by(func.count(Measurement.station).desc()).all()
    
    most_active
    ```

    [('USC00519281', 2772), ('USC00519397', 2724), ('USC00513117', 2709), ('USC00519523', 2669), ('USC00516128', 2612), ('USC00514830', 2202), ('USC00511918', 1979), ('USC00517948', 1372), ('USC00518838', 511)]

    

  * Which station has the highest number of observations?

    **Station USC00519281 has the highest number of observation: 2772 weather observations**

  ```
  most_active_one = session.query(Measurement.station, func.count(Measurement.station)).\
                    group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).first()
  
  print (f'Station {most_active_one[0]} has the highest number of observation: {most_active_one[1]} weather obeservations')
  ```

  

  ```
  highest_temp = session.query(Measurement.date,(Measurement.tobs)).\
                            filter(Measurement.date >= year_ago ).\
                            filter(Measurement.station == "USC00519281").group_by(Measurement.date).all()
  ```

  | Date | TOBS       |      |
  | :--- | :--------- | ---- |
  | 345  | 2017-08-06 | 83.0 |
  | 344  | 2017-08-05 | 82.0 |
  | 340  | 2017-07-29 | 82.0 |
  | 334  | 2017-07-23 | 82.0 |
  | 313  | 2017-07-02 | 81.0 |

  

  Plot the results as a histogram with `bins=12`.

  ![](Images/temperature_vs_frequency.png)





## Bonus: Analyze

### Temperature Analysis I

* Identify the average temperature in June at all stations across all available years in the dataset. Do the same for December temperature.

* Use the t-test to determine whether the difference in the means, if any, is statistically significant. Will you use a paired t-test, or an unpaired t-test? Why?

  

  ## T-test for June and December Temps:

  - By looking at the average temps we can say that there is not a significant difference in Average Temps for the month of June and December and having a PValue > 0.05 shows that the null hypothesis is true and means that no effect was observed.

  ```
  june = session.query(Measurement.tobs).filter(func.strftime("%m", Measurement.date) == "06").all()
  
  december = session.query(Measurement.tobs).filter(func.strftime("%m", Measurement.date) == "12").all()
  
  two_sample_results = scipy.stats.ttest_ind(june, december, equal_var = False) 
  two_sample_results
  ```

  **Ttest_indResult(statistic=array([31.35503692]), pvalue=array([4.19352984e-187]))**



### Temperature Analysis II

* Use the `calc_temps` function to calculate the min, avg, and max temperatures for your trip using the matching dates from the previous year (i.e., use "2017-01-01" if your trip start date was "2018-01-01").

  ```
  previous_year_start = dt.date(2017,8,1) - dt.timedelta(days=365)
  previous_year_end = dt.date(2017,8,9) - dt.timedelta(days=365)
  ```

  ```
  previous_year_temps_df = pd.DataFrame(my_trip, columns=["tmin", "tavg","tmax"])
  previous_year_temps_df
  ```

  |      | tmin | tavg | tmax |
  | :--- | :--- | :--- | :--- |
  | 0    | 71.0 | 79.0 | 83.0 |

* Plot the min, avg, and max temperature from your previous query as a bar chart.

  * Use the average temperature as the bar height.

  * Use the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).

    ![](Images/trip_average_temperature.png)

### Daily Rainfall Average

* Calculate the rainfall per weather station using the previous year's matching dates.

* Calculate the daily normals. Normals are the averages for the min, avg, and max temperatures.

* You are provided with a function called `daily_normals` that will calculate the daily normals for a specific date. This date string will be in the format `%m-%d`. Be sure to use all historic TOBS that match that date string.

* Create a list of dates for your trip in the format `%m-%d`. Use the `daily_normals` function to calculate the normals for each date string and append the results to a list.

* Load the list of daily normals into a Pandas DataFrame and set the index equal to the date.

  ```
  rainfall = (session.query (Station.station, Station.name,Station.latitude,Station.longitude, 			 
                             Station.elevation,func.avg(Measurement.prcp)).\
                      filter(Measurement.station == Station.station).\
                      filter(Measurement.date.between(previous_year_start, previous_year_end)).\
                      group_by(Station.station).\
                      order_by(func.avg(Measurement.prcp).desc()).all())
  #rainfall
  
  # Convert query object to data frame
  rainfall_df = pd.DataFrame(rainfall, columns = ['station','name', 'latitude', 'longitude', 'elevation', 'avg_prcp'])
  rainfall_df.set_index('station')
  ```

  |             | name                                   | latitude | longitude  | elevation | avg_prcp |
  | :---------- | :------------------------------------- | :------- | :--------- | :-------- | :------- |
  | station     |                                        |          |            |           |          |
  | USC00516128 | MANOA LYON ARBO 785.2, HI US           | 21.33310 | -157.80250 | 152.4     | 1.046000 |
  | USC00519281 | WAIHEE 837.5, HI US                    | 21.45167 | -157.84889 | 32.9      | 0.702222 |
  | USC00513117 | KANEOHE 838.1, HI US                   | 21.42340 | -157.80150 | 14.6      | 0.435556 |
  | USC00514830 | KUALOA RANCH HEADQUARTERS 886.9, HI US | 21.52130 | -157.83740 | 7.0       | 0.208000 |
  | USC00519523 | WAIMANALO EXPERIMENTAL FARM, HI US     | 21.33556 | -157.71139 | 19.5      | 0.145556 |
  | USC00519397 | WAIKIKI 717.2, HI US                   | 21.27160 | -157.81680 | 3.0       | 0.065556 |
  | USC00517948 | PEARL CITY, HI US                      | 21.39340 | -157.97510 | 11.9      | 0.045000 |

  ```
  normals = []
  for date in trip_dates:  # Loop through the list of %m-%d strings and calculate the normals for each date
      normal = daily_normals(date)
      normals.append(normal)    # push each tuple of calculations into a list called `normals`
  # normals
  
  normals_chain = itertools.chain.from_iterable(normals)
  print(normals)
  ```

  [[(67.0, 75.54, 83.0)], [(68.0, 75.60377358490567, 84.0)], [(70.0, 76.61111111111111, 85.0)], [(69.0, 76.71153846153847, 84.0)], [(69.0, 76.14814814814815, 82.0)], [(67.0, 76.25, 83.0)], [(71.0, 77.15686274509804, 83.0)], [(68.0, 76.5576923076923, 83.0)], [(69.0, 75.98039215686275, 81.0)]]

  ```
  trip_days_df = pd.DataFrame(normals_chain, columns = ["tmin", "tmax", "tavg"], index = trip_dates)
  trip_days_df.index.name = 'date'
  trip_days_df
  ```

  |       | tmin | tmax      | tavg |
  | :---- | :--- | :-------- | :--- |
  | date  |      |           |      |
  | 08-01 | 67.0 | 75.540000 | 83.0 |
  | 08-02 | 68.0 | 75.603774 | 84.0 |
  | 08-03 | 70.0 | 76.611111 | 85.0 |
  | 08-04 | 69.0 | 76.711538 | 84.0 |
  | 08-05 | 69.0 | 76.148148 | 82.0 |
  | 08-06 | 67.0 | 76.250000 | 83.0 |
  | 08-07 | 71.0 | 77.156863 | 83.0 |
  | 08-08 | 68.0 | 76.557692 | 83.0 |
  | 08-09 | 69.0 | 75.980392 | 81.0 |

  

* Use Pandas to plot an area plot (`stacked=False`) for the daily normals.

  ![](Images/daily_area_plot.png)



------



## Step 2 - Climate App

##### 												I Used Flask to create API routes for Hawaii Weather.

##### 															Designed Flask app can be viewed here:

##### 																				[Hawaii Climate App](https://github.com/fereshtehaghaei/SQLAlchemy-Challenge/blob/master/app.py )



------



Below Steps have been done/executed in Hawaii Climate App

### Routes

* `/`
  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.

  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

## Hints

* You will need to join the station and measurement tables for some of the queries.

* Use Flask `jsonify` to convert your API data into a valid JSON response object.

### Copyright

Trilogy Education Services © 2020. All Rights Reserved.
