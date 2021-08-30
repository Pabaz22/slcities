import streamlit as st

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


from streamlit_folium import folium_static
import folium

from PIL import Image

import os


### Title page
'# Smart Lighting'
'## Simply Bright'


rad = st.sidebar.radio('Navigation', ['Project', 'Models', 'Conclusions'])

if rad == 'Project':
    image = Image.open(
        '/home/djampa/code/data_project_lewagon/slcities/slcities/pictures/notr_projet.jpg'
    )
    st.image(image, caption='map', use_column_width=False)
elif rad == 'Models':
    st.write("The model")

    ####____________________________________________________________####
    # https://docs.streamlit.io/en/stable/tutorial/create_a_data_explorer_app.html
    DATE_COLUMN = 'date/time'
    DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data

    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')
    # Load 10,000 rows of data into the dataframe.
    data = load_data(10000)
    # Notify the reader that the data was successfully loaded.
    data_load_state.text('Loading data...done!')
    st.subheader('Number of pickups by hour')
    hist_values = np.histogram(data[DATE_COLUMN].dt.hour,
                               bins=24,
                               range=(0, 24))[0]
    st.bar_chart(hist_values)
    ####------------------------------------------------------------####



    ####____________________________________________________________####
    m = folium.Map(location=[47, 1], zoom_start=6)
    folium_static(m)
    ####------------------------------------------------------------####




elif rad == 'Conclusions':
    st.write("What a piece of work !")
