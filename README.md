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
 
