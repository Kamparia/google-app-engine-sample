## import libraries
import streamlit as st
import pandas as pd
import geopandas as gpd

## load data function
@st.cache ## caches the output of the function
def load_data():
    # empty array
    data = []

    ## 0 - ncdc-covid19-states.csv
    states_csv = pd.read_csv("https://raw.githubusercontent.com/Kamparia/nigeria-covid19-data/master/data/csv/ncdc-covid19-states.csv")
    states_csv.rename(columns={'CASES':'CONFIRMED', 'RECOVERED':'DISCHARGED', 'LAT':'lat', 'LONG':'lon'}, inplace=True)
    data.append(states_csv)

    ## 1 - ncdc-covid19-dailyupdates.csv
    dailyupdates_csv = pd.read_csv("https://raw.githubusercontent.com/Kamparia/nigeria-covid19-data/master/data/csv/ncdc-covid19-dailyupdates.csv")
    data.append(dailyupdates_csv)

    ## 2 - ncdc-covid19-states-daily-cases.csv
    states_daily_cases_csv = pd.read_csv("https://raw.githubusercontent.com/Kamparia/nigeria-covid19-data/master/data/csv/ncdc-covid19-states-daily-cases.csv")
    data.append(states_daily_cases_csv)

    ## 3 - ncdc-covid19-states-daily-deaths.csv
    states_daily_deaths_csv = pd.read_csv("https://raw.githubusercontent.com/Kamparia/nigeria-covid19-data/master/data/csv/ncdc-covid19-states-daily-deaths.csv")
    data.append(states_daily_deaths_csv)

    ## 4 - ncdc-covid19-states-daily-recovered.csv
    states_daily_recovered_csv = pd.read_csv("https://raw.githubusercontent.com/Kamparia/nigeria-covid19-data/master/data/csv/ncdc-covid19-states-daily-recovered.csv")
    data.append(states_daily_recovered_csv)

    ## 5 - ncdc-covid19-states.geojson
    states_geojson = gpd.read_file("https://raw.githubusercontent.com/Kamparia/nigeria-covid19-data/master/data/geojson/ncdc-covid19-states.geojson")
    states_geojson.rename(columns={'CASES':'CONFIRMED', 'RECOVERED':'DISCHARGED', 'LAT':'lat', 'LONG':'lon'}, inplace=True)
    data.append(states_geojson)

    # return
    return data