## import libraries
import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd

import plotly
import plotly.graph_objects as go
import plotly.express as px

from load_data import load_data

## load data
data = load_data()
states_csv = data[0]
states_geojson = data[5]

mapbox_access_token = "pk.eyJ1Ijoia2FtcGFyaWEiLCJhIjoiY2s3OHMyaWlhMGk5azNsbnl3MnJweWdjYyJ9.4K1LcrByr-9dxInw2Iy7lw"


## choropleth map function
def choropleth_map(data_class, sidebar_basemap_option):
    data_class = data_class.upper()

    ## basemap style
    if sidebar_basemap_option == "Default":
        basemap = "carto-positron"
    else:
        basemap = sidebar_basemap_option.lower()

    ## sub header
    st.subheader("Affected States:")
    st.write("Mouseover each State for breakdown of cases.")

    fig = px.choropleth_mapbox(states_csv, geojson=states_geojson, 
            locations="STATE", color=data_class, 
            color_continuous_scale=['rgb(0, 204, 150)', 'rgb(214, 69, 80)'], range_color=(0, 1),
            featureidkey="properties.STATE", hover_name="STATE", hover_data=["CONFIRMED", "DEATHS", "DISCHARGED"],
            mapbox_style=basemap, zoom=5, center={"lat":9.114900, "lon":8.486995}, opacity=0.9
        )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig)


## point map function
def point_size_map(data_class, sidebar_basemap_option):
    ## data class color
    data_class = data_class.upper()
    if data_class == "DEATHS":
        map_title = "Recorded Deaths:"
        map_sub_title = "Mouseover each location to see breakdown of cases."
        marker_color = "rgb(239, 85, 58)"
    elif data_class == "DISCHARGED":
        map_title = "Discharged Cases:"
        map_sub_title = "Mouseover each location to see breakdown of cases."
        marker_color = "rgb(89, 205, 150)"
    else:
        map_title = "Confirmed Cases:"
        map_sub_title = "Mouseover each location to see breakdown of cases."
        marker_color = "#666ff9"

    ## basemap style
    if sidebar_basemap_option == "Default":
        basemap = "carto-positron"
    else:
        basemap = sidebar_basemap_option.lower()

    ## sub header
    st.subheader(map_title)
    st.write(map_sub_title)    

    ## display map
    px.set_mapbox_access_token(mapbox_access_token)
    fig = px.scatter_mapbox(states_csv, lat="lat", lon="lon", 
            size=data_class, mapbox_style=basemap, zoom=5, 
            center={"lat":9.114900, "lon":8.486995},
            hover_name="STATE", hover_data=["CONFIRMED", "DEATHS", "DISCHARGED"],
        )

    fig.update_layout(margin=dict(l=5, r=0, t=5, b=0))
    fig.update_traces(marker_color=marker_color)
    st.plotly_chart(fig)    

"""
def get_color_scale_values(data_class):
    df = states_csv

    if data_class == "deaths":
        data_class = "DEATHS"
    elif data_class == "discharged":
        data_class == "DISCHARGED"
    else:
        data_class == "CONFIRMED"

    max_value = df[data_class].max()
    min_value = df[data_class].min()
"""