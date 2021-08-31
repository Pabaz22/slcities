import os
import numpy as np
import pandas as pd
import streamlit as st
import folium
from PIL import Image

import matplotlib.pyplot as plt
from streamlit_folium import folium_static


########## ---------------------------------------- ##########
##
##   General configuration
##

## SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")


#################### ******************* ####################



########## ---------------------------------------- ##########
##
##   Functions
##


def generate_balise(text, kind='h1', font_size=300, color='white', text_align='center'):
    return f"<h1 style='text-align: {text_align}; color: {color}; font-size:{font_size}%;'>{text}</h1>"










########## ---------------------------------------- ##########
##
##   Main code
##

rad = st.sidebar.radio('Navigation', ['Project', 'Models', 'Conclusions'])

if rad == 'Project':
    ### Title
    title_balise = generate_balise('Smart Lighting', font_size=400)\
    +generate_balise('Simply Bright', kind='h2', font_size=200)
    st.markdown(title_balise, unsafe_allow_html=True)
    row0_1, row0_2, row0_3 = st.columns((.1, .05,.1))
    ### Street light logo
    logo_street_light = Image.open(
        '/home/djampa/code/data_project_lewagon/slcities/slcities/pictures/PinClipart.com_quotation-marks-clip-art_1073653.png'
    )
    with row0_2:
        st.image(logo_street_light, caption='', use_column_width=True)
    ### Row 1
    # row1_1, row1_2, row1_3 = st.columns((.1, .1, .1))
    row1_2_text_h1 = 'Eclairages publics'
    row1_2_feet_balise = generate_balise(row1_2_text_h1,
                                         font_size=200,
                                         text_align='center')
    st.markdown(row1_2_feet_balise, unsafe_allow_html=True)

    ### Display the infos
    row2_1, row2_2, row2_3 = st.columns((1, 1, 1))
    with row2_1:
        row2_1_text_h1 = '1600M€/an'
        row2_1_text_p = "800M€ pour la maintenance, 400M€ de facture énergie \
            et 400€ d’investissement"

        row2_1_balise = generate_balise(row2_1_text_h1, font_size=300,
                                        text_align='left')\
        +generate_balise(row2_1_text_p, kind='p', font_size=150, text_align='left')
        st.markdown(row2_1_balise, unsafe_allow_html=True)

    with row2_2:
        row2_2_text_h1 = '80%'
        row2_2_text_p = "Des installations qui ne sont pas aux normes, 1/3 ont \
            plus de 20ans"

        row2_2_balise = generate_balise(row2_2_text_h1, font_size=300,
                                        text_align='left')\
        +generate_balise(row2_2_text_p, kind='p', font_size=150, text_align='left')
        st.markdown(row2_2_balise, unsafe_allow_html=True)

    with row2_3:
        row2_3_text_h1 = '40%'
        row2_3_text_p = "Consommation d’électricité des collectivités \
        territoriales françaises et 23% de la facture globale d’énergie"

        row2_3_balise = generate_balise(row2_3_text_h1, font_size=300,
                                        text_align='left')\
        +generate_balise(row2_3_text_p, kind='p', font_size=150, text_align='left')
        st.markdown(row2_3_balise, unsafe_allow_html=True)
    # image = Image.open(
    #     '/home/djampa/code/data_project_lewagon/slcities/slcities/pictures/notr_projet.jpg'
    # )

    # st.image(image, caption='map', use_column_width=False)
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
    st.markdown( "<h1 style='text-align: center; color: red;'>Smart Lighting</h1>",
    unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: red;'>Simply Bright</h2>",
            unsafe_allow_html=True)
