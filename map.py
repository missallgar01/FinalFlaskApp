import plotly.express as px
import pandas as pd
import json
from weather import Weather

class Map():
    """A class for generating different types of maps"""
    def __init__(self):
        """Constructor Method"""
        px.set_mapbox_access_token(
            'pk.eyJ1IjoiZ2ZlbGl4IiwiYSI6ImNrZTNsbnYzMTBraG0zMnFuZXNjOWZhdDgifQ.5sMKH7NQ6_oVyU4oJlcBUw')


    def scatterplot_map(self,latlon):
        """A method to create a scatterplot map"""
        #areas of interest using lat,lon
        humidity = []
        lat = []
        lon = []
        for i in latlon:
          clat = i[0]
          clon = i[1]
          #Current Weather
          current_weather = Weather()
          current_weather.getCurrentWeather(clat,clon)
          humidity_data = current_weather.getCurrentHumidity()
          humidity.append(humidity_data)
          lat.append(clat)
          lon.append(clon)

        dict_map = {'humidity': humidity, 'lat': lat, 'lon': lon}

        df = pd.DataFrame.from_dict(dict_map)  # transforms the dictionary to a pandas dataframe

        fig = px.scatter_mapbox(df, lat="lat", lon="lon", size="humidity",
                                color="humidity",
                                color_continuous_scale=px.colors.sequential.Rainbow, size_max=30, zoom=1)
        fig.update_layout(mapbox_style="dark")
        html_string = fig.to_html(full_html=False)
        return html_string


    def choropleth(self):
        """A method to create a choropleth map"""

        #get a choropleth map using Country Polygons as GeoJSON
        countries = json.load(open('data/world_countries.geojson', 'r'))
        #purpose of this code is to add a column to the df that includes unique locations id
        country_id_map = {}
        for feature in  countries['features']:
            feature['id'] = feature['properties']['cartodb_id']
            country_id_map[feature['properties']['name']] = feature['id']

        #link to csv file that contains your data to be plotted on the map
        df = pd.read_csv("data/map_data.csv")

        #adds new column to df - applies correct id based on name
        df['id'] = df['country'].apply(lambda x:country_id_map[x])

        fig = px.choropleth_mapbox(df, locations='id', geojson=countries, color='data',
                                   color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=2,
                                   opacity=0.5,
                                   labels={'data': 'levels'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        html_string = fig.to_html(full_html=False)
        return html_string

if __name__ == '__main__':

    print()