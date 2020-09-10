## import libraries
import streamlit as st
import numpy as np
import pandas as pd

from load_data import load_data
from all_states import (summary, table, map, charts)
from single_state import fetch_state_charts

#####################################################################

def main():
    ## load data
    data = load_data()
    states_csv = data[0]
    dailyupdates_csv = data[1]
    states_daily_cases_csv = data[2]
    states_daily_deaths_csv = data[3]
    states_daily_recovered_csv = data[4]
    states_geojson = data[5]

    #####################################################################

    ## sidebar
    st.sidebar.title('App Settings') ## sidebar title

    ## array of state names
    states_name = ["All States"]
    for index, row in states_csv.iterrows():
        state = row['STATE']
        cases = row['CONFIRMED']
        if cases > 0:
            states_name.append(state)

    ## sidebar - select state
    sidebar_state_option = st.sidebar.selectbox(
        'Display State:', (states_name)
    )

    if sidebar_state_option == 'All States':
        sidebar_visual_option = st.sidebar.selectbox(
            'Visual Type:', ('Charts', 'Tables', 'Maps')
        )

    if sidebar_state_option == 'All States' and sidebar_visual_option == 'Charts':
        sidebar_trend_option = st.sidebar.selectbox(
            'Cases Category:', ('All', 'Confirmed', 'Deaths', 'Discharged')
        )

    if sidebar_state_option == 'All States' and sidebar_visual_option == 'Maps':
        sidebar_basemap_option = st.sidebar.selectbox(
            'Basemap Style:', ('Default', 'Dark', 'Light', 'Streets')
        )

    if sidebar_state_option == 'All States' and sidebar_visual_option == 'Tables':
        sidebar_table_option = st.sidebar.selectbox(
            'Data Type:', ('Cases by States', 'Daily Records')
        )

    #####################################################################

    ## app title
    st.title('Nigeria COVID-19 Data Explorer')
    st.write('Nigeria Novel Coronavirus (COVID-19) Data Explorer Application.')

    ## main
    if sidebar_state_option == 'All States':
        ## all states
        summary(sidebar_visual_option)
        
        if sidebar_visual_option == 'Tables':
            table(sidebar_table_option)
        elif sidebar_visual_option == 'Maps':
            map(sidebar_basemap_option)
        else: 
            charts(sidebar_trend_option)
    else:
        ## single state
        state_name = sidebar_state_option
        fetch_state_charts(state_name)


    #####################################################################

    ## footer
    st.subheader("About this App:")
    st.markdown(
        """
        All data and information are provided strictly for public consumption and general information. 

        **Data Scientist / Developer:** [Olaoye Anthony Somide](http://somideolaoye.com).

        **Downloadable database:** [Nigeria COVID-19 Public Dataset - GitHub Repo](https://github.com/Kamparia/nigeria-covid19-data). 

        **Data Sources:** [Nigeria Centre for Disease Control (NCDC)](https://covid19.ncdc.gov.ng/).
        """
    )


if __name__ == "__main__":
    main()