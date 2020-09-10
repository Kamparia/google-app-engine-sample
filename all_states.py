## import libraries
import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gpd

import plotly
import plotly.graph_objects as go
import plotly.express as px

from load_data import load_data
from maps import (choropleth_map, point_size_map)

## load data
data = load_data()
states_csv = data[0]
dailyupdates_csv = data[1]
states_daily_cases_csv = data[2]
states_daily_deaths_csv = data[3]
states_daily_recovered_csv = data[4]
states_geojson = data[5]

def summary(sidebar_visual_option):
    st.subheader("Data Summary:")
    st.write("Summary of coronavirus infection cases in Nigeria.")

    df = states_csv
    cases_no = df['CONFIRMED'].sum()
    active_no = df['ACTIVE'].sum()
    deaths_no = df['DEATHS'].sum()
    recovered_no = df['DISCHARGED'].sum()

    st.markdown(
        """
        Total Confirmed Cases | Total Active Cases | Total Discharged | Total Deaths
        ----------------|--------------|------------|----------
        {0}             | {1}          | {2}        | {3} 
        """.format(cases_no, active_no, recovered_no, deaths_no)
    )
    st.text("")
    st.text("")

    if sidebar_visual_option != "Tables" and sidebar_visual_option != "Maps":
        data = go.Pie(
            labels = [
                'ACTIVE CASES ('+str(round(((active_no/cases_no)*100),2))+'%)', 
                'DEATHS ('+str(round(((deaths_no/cases_no)*100),2))+'%)', 
                'DISCHARGED ('+str(round(((recovered_no/cases_no)*100),2))+'%)'
            ], 
            values = [active_no, deaths_no, recovered_no],
            hoverinfo='label+percent', 
            textinfo='value', 
            textfont=dict(size=20),
            marker=dict(colors = ['rgb(102, 111, 249)', 'rgb(239, 85, 58)', 'rgb(89, 205, 150)'], 
                line=dict(color='#FFF', width=1)
            )
        )

        fig = go.Figure(data = [data])
        fig.update_layout(legend_orientation='h', margin=dict(l=5, r=0, t=5, b=0))
        st.plotly_chart(fig)


def table(sidebar_table_option):
    # display table data
    if sidebar_table_option == "Daily Records":
        ## daily records
        st.subheader("Daily Records:")
        st.write("Daily announced records of COVID-19 cases in Nigeria.")
        dailyupdates_csv.rename(columns={'TOTAL CONFIRMED':'CONFIRMED', 'ACTIVE CASES':'ACTIVE', 'RECOVERED':'DISCHARGED', 'DAILY RECOVERED':'DAILY DISCHARGED'}, inplace=True)
        st.table(dailyupdates_csv[["DATE", "CONFIRMED", "DEATHS", "DISCHARGED", "ACTIVE", "NEW CASES", "DAILY DEATHS", "DAILY DISCHARGED"]])
    else:
        ## cases by states
        st.subheader("Cases by States:")
        st.write("Breakdown of COVID-19 cases by states.")
        st.table(states_csv[["STATE", "CONFIRMED", "DEATHS", "DISCHARGED", "ACTIVE"]])


def map(sidebar_basemap_option):
    choropleth_map("confirmed", sidebar_basemap_option)
    point_size_map("confirmed", sidebar_basemap_option)
    point_size_map("discharged", sidebar_basemap_option)
    point_size_map("deaths", sidebar_basemap_option)


def charts(sidebar_trend_option):
    if sidebar_trend_option == 'Confirmed':
        total_cases_overtime()
        new_cases_overtime()
    elif sidebar_trend_option == 'Deaths':
        total_deaths_overtime()
        new_deaths_overtime()
    elif sidebar_trend_option == 'Discharged':
        total_discharged_overtime()
        new_discharged_overtime()
    else:
        cases_overtime()
        new_records_overtime()
        choropleth_map("confirmed", "Default")


## cases over time chart
def cases_overtime():
    st.subheader("Daily Totals:")
    st.write("Total numbers of cases, discharges and deaths.")
    df = dailyupdates_csv
    confirmed = go.Line(x = pd.to_datetime(df['DATE']), y = df['TOTAL CONFIRMED'], name = 'TOTAL CONFIRMED CASES')
    recovered = go.Line(x = pd.to_datetime(df['DATE']), y = df['RECOVERED'], name = 'TOTAL DISCHARGED')
    deaths = go.Line( x = pd.to_datetime(df['DATE']), y = df['DEATHS'], name = 'TOTAL DEATHS')
    fig = go.Figure(data=[confirmed, deaths, recovered])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)


## cases over time chart
def new_records_overtime():
    st.subheader("Daily Changes:")
    st.write("Daily changes in numbers of cases, discharges and deaths.")
    df = dailyupdates_csv
    confirmed = go.Line(x = pd.to_datetime(df['DATE']), y = df['NEW CASES'], name = 'DAILY CONFIRMED CASES')
    recovered = go.Line(x = pd.to_datetime(df['DATE']), y = df['DAILY RECOVERED'], name = 'DAILY DISCHARGED')
    deaths = go.Line(x = pd.to_datetime(df['DATE']), y = df['DAILY DEATHS'], name = 'DAILY DEATHS')
    fig = go.Figure(data=[confirmed, deaths, recovered])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)


## total cases overtime charts
def total_cases_overtime():
    st.subheader("Total Confirmed Cases:")
    st.write("Total number of confirmed cases over time.")
    df = dailyupdates_csv
    data = go.Line(x = pd.to_datetime(df['DATE']), y = df['TOTAL CONFIRMED'], name = 'TOTAL CONFIRMED')
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)


## total deaths overtime charts
def total_deaths_overtime():
    st.subheader("Total Deaths:")
    st.write("Total number of recorded deaths over time.")
    df = dailyupdates_csv
    data = go.Line(x = pd.to_datetime(df['DATE']), y = df['DEATHS'], name = 'TOTAL DEATHS')
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    fig.update_traces(marker_color='rgb(239, 85, 58)')
    st.plotly_chart(fig)


## total discharged overtime charts
def total_discharged_overtime():
    st.subheader("Total Discharged:")
    st.write("Total number of discharged cases over time.")
    df = dailyupdates_csv
    data = go.Line(x = pd.to_datetime(df['DATE']), y = df['RECOVERED'], name = 'TOTAL DISCHARGED')
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    fig.update_traces(marker_color='rgb(89, 205, 150)')
    st.plotly_chart(fig)


## new cases overtime charts
def new_cases_overtime():
    st.subheader("Daily Confirmed Cases:")
    st.write("Number of daily confirmed cases over time.")
    df = dailyupdates_csv.sort_values(by='DATE', ascending=False)
    data = go.Bar(x = pd.to_datetime(df['DATE']), y = df['NEW CASES'], name = 'NEW CASES')
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)


## new discharged over time
def new_discharged_overtime():
    st.subheader("Daily Discharged:")
    st.write("Number of daily discharged cases over time.")
    df = dailyupdates_csv.sort_values(by='DATE', ascending=False)
    data = go.Bar(x = pd.to_datetime(df['DATE']), y = df['DAILY RECOVERED'], name = 'DAILY DISCHARGED')
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    fig.update_traces(marker_color='rgb(89, 205, 150)')
    st.plotly_chart(fig)


## new deaths over time
def new_deaths_overtime():
    st.subheader("Daily Deaths:")
    st.write("Number of daily recorded deaths over time.")
    df = dailyupdates_csv.sort_values(by='DATE', ascending=False)
    data = go.Bar(x = pd.to_datetime(df['DATE']), y = df['DAILY DEATHS'], name = 'DAILY DEATHS')
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    fig.update_traces(marker_color='rgb(239, 85, 58)')
    st.plotly_chart(fig)