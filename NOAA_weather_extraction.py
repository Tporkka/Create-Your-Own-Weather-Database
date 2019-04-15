import requests
import datetime
from datetime import timedelta
import json
import pandas as pd
import os
import math
import time


def fetch_weather_data(base_url, weather_stations, from_date, to_date, header):
    """
    main function which defines parameters needed (dates, weather stations, weather features) and coordinates the script. 
    """

    #break up calls into 50 days each for each station to stay under rate limit. 
    num_days_requested = abs((to_date - from_date).days)
    fetch_rate = 50
    intervals = math.ceil(num_days_requested / fetch_rate)
    print('Data requested for ' + str(num_days_requested) + ' days in ' + str(intervals) + ' api calls.')
    
    for station in weather_stations: 
        
        print('Gathering records for ' + station + ':')
        
        station_dfs = []
        i = 0
        while i < intervals:
            start = from_date + timedelta(days = i*fetch_rate)
            end = min(start + timedelta(days = fetch_rate-1), to_date)
            url = base_url + station + '&startdate=' + str(start) + '&enddate=' + str(end) + '&units=standard&limit=1000&includemetadata=false'
            
            #sleep for 10 seconds to avoid going over rate limit.
            time.sleep(10)
            print('-- Gathering records for ' + str(start) + ' through ' + str(end) + '...')
            
            try:
                r = requests.get(url, headers=header)
                interval_data = reformat_data(r.text)
                station_dfs.append(interval_data)
                print('-- done.')
            
            except Exception as e:
                print(e)
                print('Error! Failed to load records for ' + station +' for ' + str(start) + ' through ' + str(end) + '.')
                print('Make sure your token is valid or try more time intervals, a smaller date range, or fewer locations.')
            
            i+=1
            
        final_station_df = pd.concat(station_dfs)
        append_data_to_file(final_station_df, station)
  

def reformat_data(json_text):
    """
    Convert data to denormalized pandas dataframe. This format will allow easier analysis and better 
    fit within a typical data warehouse schema.
    """
    
    #convert records from nested json to flat pandas dataframe. 
    api_records = json.loads(json_text)['results']
    df = pd.pivot_table(pd.DataFrame(api_records), index=['date', 'station'], columns='datatype', values='value')
    reshaped_df = df.rename_axis(None, axis=1).reset_index()
    
    #clean up the date and station fields
    reshaped_df.date = reshaped_df.date.str.slice(0, 10)
    reshaped_df.station = reshaped_df.station.str.slice(6, 17)

    #add a primary key for useful for updating/inserting records in a database. 
    reshaped_df['station_dt_key']=reshaped_df['station'].astype(str)+'_'+reshaped_df['date']

    #filter for requested features, replace NAs with 0.
    final_df = reshaped_df.filter(items=weather_features)
    final_df.fillna(0.0)
    
    return final_df


def append_data_to_file(historical_df, station):
    """
    Write historical weather records to text file and save.
    """
    csv_file = historical_df.to_csv(header=True, index=False)
    file_path = './WeatherExtracts/' + station + str(datetime.date.today()) + '.txt'
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    with open(file_path, 'w+') as f:
        f.write(csv_file)


if __name__ == '__main__':

    with open('config.json') as conf_file:
        config = json.load(conf_file)
    token = config['noaa-config']['token']
    creds = dict(token=token)
    base_url = config['noaa-config']['base_url']
    from_dt = datetime.datetime.strptime(config['params']['start_date'], "%Y-%m-%d").date()
    to_dt = datetime.datetime.strptime(config['params']['end_date'], "%Y-%m-%d").date()
    stations = config['params']['weather_stations']
    weather_features = config['params']['weather_features']
    fetch_weather_data(base_url, stations, from_dt, to_dt, creds)







