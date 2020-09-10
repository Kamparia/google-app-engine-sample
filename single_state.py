## import libraries
import streamlit as st
import numpy as np
import pandas as pd

import plotly
import plotly.graph_objects as go
import plotly.express as px

from load_data import load_data

## load data
data = load_data()
states_csv = data[0]
dailyupdates_csv = data[1]
states_daily_cases_csv = data[2]
states_daily_deaths_csv = data[3]
states_daily_recovered_csv = data[4]
states_geojson = data[5]


def fetch_state_charts(state):
    summary(state)

    total_cases_overtime(state)
    total_discharged_overtime(state)
    total_deaths_overtime(state)
 

def summary(state):
    st.subheader("Data Summary:")
    st.write("Summary of coronavirus infection cases in {0} State.".format(state))

    df = states_csv[(states_csv['STATE'] == state)]
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


## total cases overtime charts
def total_cases_overtime(state):
    st.subheader("Total Confirmed Cases:")
    st.write("Total number of confirmed cases over time.")
    df = states_daily_cases_csv.sort_values(by='Date', ascending=False)
    data = go.Bar(x = pd.to_datetime(df['Date']), y = df[state], name = state)
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig)


## total deaths overtime charts
def total_deaths_overtime(state):
    st.subheader("Total Deaths:")
    st.write("Total number of recorded deaths over time.")
    df = states_daily_deaths_csv.sort_values(by='Date', ascending=False)
    data = go.Bar(x = pd.to_datetime(df['Date']), y = df[state], name = state)
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    fig.update_traces(marker_color='rgb(239, 85, 58)')
    st.plotly_chart(fig)


## total discharged overtime charts
def total_discharged_overtime(state):
    st.subheader("Total Discharged:")
    st.write("Total number of discharged cases over time.")
    df = states_daily_recovered_csv.sort_values(by='Date', ascending=False)
    data = go.Bar(x = pd.to_datetime(df['Date']), y = df[state], name = state)
    fig = go.Figure(data=[data])
    fig.update_layout(legend_orientation='h', margin=dict(l=0, r=0, t=0, b=0))
    fig.update_traces(marker_color='rgb(89, 205, 150)')
    st.plotly_chart(fig)