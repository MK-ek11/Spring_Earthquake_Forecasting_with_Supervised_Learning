# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 12:04:20 2022
@author: emily

"""
#<https://matplotlib.org/stable/tutorials/colors/colormaps.html>

from datetime import datetime
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option("display.max_rows", None)
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt


### Define Function to find the count of each magnitude after a certain value
def magnitude_count(data_info, column_val, mag_min_threshold, mag_max_threshold):
    magnitude_val_list = data_info[column_val].value_counts().index.to_list()
    magnitude_count_list = data_info[column_val].value_counts().to_list()
    
    data_dict = {}
    return_mag_val_list = []
    for i in range(0,len(magnitude_val_list)):
        if magnitude_val_list[i] >= mag_min_threshold and magnitude_val_list[i] <= mag_max_threshold:
            data_dict[magnitude_val_list[i]]=magnitude_count_list[i]
            return_mag_val_list.append(magnitude_val_list[i])
    return pd.DataFrame([data_dict]), return_mag_val_list


### Define Function to extract specific events based on input parameters
def select_single_event(data_info, mag_val, column_val):
    list_events_index = data_info[data_info[column_val]==mag_val].index.to_list()
    specific_events_df = data_info.loc[list_events_index]
    return specific_events_df


def select_multiple_events(data_info, mag_val, column_val):
    list_events_index = data_info[data_info[column_val].isin(mag_val)].index.to_list()
    specific_events_df = data_info.loc[list_events_index]
    return specific_events_df


def select_specific_year(data_info,year):
    data_info_cut = data_info[data_info["Year"]==year]
    return data_info_cut


def add_year_column(data_info):
    data_info["Year"] = data_info["time"].str.slice_replace(4,25,repl="").astype(int)
    return data_info


def add_date_column(data_info):
    data_info["Date"] = data_info["time"].str.slice_replace(10,25,repl="").astype(str)
    return data_info



# Plot the earthquakes color encoded interms of nearest City 
def plot_map_nearest_city_name(data_info, data_df_city, location_column_var ,title_var, color_list):
    # Link = https://developer.mozilla.org/en-US/docs/Web/CSS/color_value
    fig = go.Figure()
    city_list = data_info["Nearest City"].unique().tolist()
    
    color_index = 0
    for index in range(0, len(city_list)):
        if city_list[index].startswith(">"):
            data_current_info = data_info[data_info["Nearest City"]==city_list[index]]
            fig.add_trace(go.Scattergeo(lon=data_current_info['longitude'],
                                        lat =data_current_info['latitude'],
                                        customdata=data_current_info['time'],
                                        
                                        opacity=0.8,
                                        marker = dict(color = "silver",
                                                      size = 4,
                                                      sizemode = 'area',
                                                      line_width=0.5,
                                                      line_color='rgb(40,40,40)'
                                                     ),
                                        
                                        text = "Magnitude: " + data_current_info['mag'].astype(str)+"\n"+"Nearest City: "+ data_current_info['Nearest City'].astype(str),
                                        hovertext = ['{}'.format(i) for i in data_current_info[location_column_var].to_list()],  
                                        hovertemplate = "<b>%{text}</b><br>" + "<br>Place: %{hovertext}"+ "<br>Date: %{customdata}"+
                                        "<br>Latitude: %{lat}"+ "<br>Longitude: %{lon}",
                                        name = "Earthquakes : {}".format(city_list[index])
                                       )
                         )            

        else:
            data_current_info = data_info[data_info["Nearest City"]==city_list[index]]
            fig.add_trace(go.Scattergeo(lon=data_current_info['longitude'],
                                        lat =data_current_info['latitude'],
                                        customdata=data_current_info['time'],
                                        
                                        opacity=0.8,
                                        marker = dict(color = color_list[color_index],
                                                      size = 8,
                                                      sizemode = 'area',
                                                      line_width=0.5,
                                                      line_color='rgb(40,40,40)'
                                                     ),
                                        
                                        text = "Magnitude: " + data_current_info['mag'].astype(str)+"\n"+"Nearest City: "+ data_current_info['Nearest City'].astype(str),
                                        hovertext = ['{}'.format(i) for i in data_current_info[location_column_var].to_list()],  
                                        hovertemplate = "<b>%{text}</b><br>" + "<br>Place: %{hovertext}"+ "<br>Date: %{customdata}"+
                                        "<br>Latitude: %{lat}"+ "<br>Longitude: %{lon}",
                                        name = "Earthquakes : {}".format(city_list[index])
                                       )
                         )
            color_index += 1
            
    fig.add_trace(go.Scattergeo(lon=data_df_city['longitude'],
                                lat =data_df_city['latitude'],
                                
                                opacity=1.0,
                                marker = dict(color = 'black',
                                              size = 10,
                                              sizemode = 'area',
                                              line_width=0.5,
                                              line_color='rgb(40,40,40)',
                                              symbol = 'x'
                                             ),
                                
                                #text = "Main City: " + data_df_city['City'].astype(str),
                                hovertext = ['{}'.format(i) for i in data_df_city["City"].to_list()],  
                                hovertemplate = "<b>Main City: %{hovertext}</b><br>" + "<br>Latitude: %{lat}"+ "<br>Longitude: %{lon}",
                                name = "Main Cities Indicated"
                                #name = "Main City : {}".format(data_df_city["City"])
                               )
                 )        

    fig.update_geos(scope = 'world', 
                    fitbounds="locations",
                    resolution=50,
                    showcountries=True, countrycolor="lightsteelblue",
                    # showsubunits=True, subunitcolor="Green"
                    # landcolor  = "silver"
                    )
    fig.update_layout(title = title_var,
                      legend_title_text  = "Earthquakes and Main Cities marked with X",
                      showlegend = True,
                      )
    fig.show()

























