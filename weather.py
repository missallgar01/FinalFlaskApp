import json
import requests
from datetime import datetime
from csv import writer,reader
import reverse_geocoder as rg
import pandas as pd
from datetime import datetime


class Weather():
  """Class to access weather data"""
  def __init__(self):
    """Constructor Method"""
    self.api_key = "efb67b5073bab84b1dc7575bedd41c27"


  def getCurrentWeather(self, lat, lon):
    """Method to get current weather data based on lat and lon"""
    self.lat, self.lon = lat, lon

    try:
      # Current Weather
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (
        self.lat, self.lon, self.api_key)
        response = requests.get(url)
        response.raise_for_status()

    except requests.exceptions.HTTPError as errh:
      return False

    self.data = json.loads(response.text)
    # get specific data from the api json file
    weather = self.data.get("current")
    self.humidity_data = weather.get('humidity')
    self.temp_data = weather.get('temp')
    # get cc: ISO 3166-1 alpha-2 country code
    self.reverse_geocoder()
    return True

  def getCurrentHumidity(self):
    """Get Method to return current humidity"""
    return self.humidity_data

  def getCurrentTemp(self):
    """Get Method to return current temp"""
    return self.temp_data

  def getCountry(self):
    """Get Method to return current country"""
    return self.country_code


  def reverse_geocoder(self):
    """Get Method get counrty based on lat and lon"""
    coordinates = (self.lat, self.lon)
    dict = rg.search(coordinates)
    # cc: ISO 3166-1 alpha-2 country code
    print(dict)
    self.country_code = dict[0]['cc']


  def save(self):
    """Get Method to save current weather to csv file"""
    #Generate a timestamp using the time module
    timestamp = datetime.now()

    # The data collected will should be stored like this temperature timestamp
    data = [timestamp,self.getCurrentHumidity(),self.getCurrentTemp(),self.getCountry()]
    
    with open('data/weatherdata.csv', 'a', newline='') as f_object:
      writer_object = writer(f_object)
      writer_object.writerow(data)
      f_object.close()


  def getWeatherData(self):
    """Get Method to view csv file for testing purposes """
    with open('data/weatherdata.csv', 'r') as my_file:
      file_reader = reader(my_file)
      for i in file_reader:
        print (i)


  def filterWeatherData(self, start, end):
    """Get Method to filter csv data by start and end time"""

    df = pd.read_csv("data/weatherdata.csv")
    df['Date'] = pd.to_datetime(df['timestamp']).dt.date
    df['Time'] = pd.to_datetime(df['timestamp']).dt.time

    # Filter data by date
    #date = datetime.strptime('2022-07-24', '%Y-%m-%d').date()
    #filtered_dates = self.df.loc[self.df["Date"] <= date]
    #Filter by time
    start_time = datetime.strptime(start, '%H:%M:%S').time()
    end_time = datetime.strptime(end, '%H:%M:%S').time()

    after_start_time = df["Time"] >= start_time
    before_end_time = df["Time"] <= end_time
    between_two_times = after_start_time & before_end_time
    filtered_times = df.loc[between_two_times,["timestamp","humidity","temp"]]

    return filtered_times
        
if __name__ == '__main__':
    data = Weather()
    
