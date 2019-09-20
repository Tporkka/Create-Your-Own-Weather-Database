### Why bother

Weather can have a significant impact on businesses outcomes and other facets of life. Unfortunately, it can be difficult to analyze this impact without accurate historical data in a structured format. Storing historical weather in clean time series allows you to quantify this impact, and more importantly, create models to better predict future outcomes. 

# NOAA_Historical_Weather_Extraction
This is a script for extracting historical weather data in bulk using the NOAA API. The end result is a series of comma delimeted files that can easily be integrated into a relational database. 

### Dependencies
Python 3 (Packages: requests, datetime, json, pandas, os, math, time)

### How to use this script
1. Download all files to your local directory.
2. Add your NOAA API Token to the config.json file. You can get a token here: https://www.ncdc.noaa.gov/cdo-web/token
3. Specify the weather stations, metrics, start date, and end date in the config.json file.
```json
 {
   "noaa-config":{
        "token":"YOUR_NOAA_API_TOKEN",
        "base_url":"https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&stationid=GHCND:"
    },
    "params":{
		"weather_stations": ["USW00012916", "USW00094982"],
		"weather_features": ["station_dt_key", "date", "station", "PRCP", "SNOW", "SNWD", "AWND", "TMAX", "TMIN"],
    "start_date":"2016-01-01",
    "end_date":"2018-12-31"
    }
}
```
4. Navigate to the appropriate directory and run the script.

```sh
$ cd directory
$ python3 NOAA_weather_extraction.py
```

This will run the script and create a single comma delimited file for each weather station into the created WeatherExtracts folder. See example_output.txt file. 

### Other notes
* _station_dt_key_ serves as a primary key which can be useful for applying update/insert logic in a database.
* The script breaks down large queries into smaller requests to avoid going over the rate limit. 


### Todos

 - Improve error handling and communication
 - Add ability to pass dynamic dates (i.e. `end_date = datetime.datetime.now().date()`) when specified in config file. 
 
### Some suggestions for creating your own weather database

This is the first part of an effort to create and maintain a database of historical weather data. To create a fully automated and up-to-date table or set of tables, you will need to set up an ETL pipeline that stores new or updated records as they are available. I recommend running this script once to gather bulk historical data (set the config file dates to your liking) and then changing the script to just gather the last week of data since some weather stations are updated less frequently. This will gather new or updated records that you can use to update your database tables. 
I automated this entire workflow using Microsoft Azure: Script run as Azure Function, drop resulting text file to Azure Blob storage, Azure Data Factory pipeline to copy data from Blob to a table within Azure Data Warehouse (using a stored proc on ADW to handle upsert logic). A similar process can be followed regardless of which tools you're using. 
