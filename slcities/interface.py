import os
import numpy as np
import pandas as pd

from PIL import Image

import seaborn as sns
import matplotlib.pyplot as plt

import streamlit as st

import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster


from slcities.params import DUBLIN_CENTER_COORDS, NICE_CENTER_COORDS
from slcities.utils import format_df_to_geopandas



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

def generate_balise(text,
                    kind='h1',
                    font_size=300,
                    color='white',
                    text_align='center',
                    margin=0):
    return f"<h1 style='text-align: {text_align}; color: {color}; font-size:{font_size}%; margin-bottom: {margin};'>{text}</h1>"
#################### ******************* ####################



########## ---------------------------------------- ##########
##
##   Data / Model / Scaler Importation
##

## Data
places = pd.read_csv('slcities/data/places.txt')
areas = pd.read_csv('slcities/data/areas.txt')
lights = pd.read_csv('slcities/data/lights.txt')
sensors = pd.read_csv('slcities/data/sensors.txt')
global_cnt_df = pd.read_csv('slcities/data/global_cnt.txt')

## Conso model
conso_model_per_day = pd.read_csv('slcities/data/conso_models_per_day.txt')

## Transform into geopandas
gpd_global_cnt = format_df_to_geopandas(global_cnt_df)

## Get places total counts per polygons
lst_cols_to_discard = [
    'ED_ID', 'Shape__Area', 'geometry', 'pop', 'light', 'sensors'
]

lst_cols_places = [
    x for x in gpd_global_cnt.columns if x not in lst_cols_to_discard
]
gpd_global_cnt['total_places'] = gpd_global_cnt[lst_cols_places].sum(axis=1)


#################### ******************* ####################



########## ---------------------------------------- ##########
##
##   Maps Generation
##

## Map density and places

#################### ******************* ####################


def create_map_1(gpd_global_cnt, places):
    lat_center, lon_center = DUBLIN_CENTER_COORDS
    map_1 = folium.Map(location=[lat_center, lon_center],
                        zoom_start=10,
                        min_zoom=8,
                        tiles=None,
                        control_scale=True,
                        attr='SL Cities Project')

    dublin_layer = folium.TileLayer(tiles='CartoDB dark_matter',
                                    control_scale=True,
                                    overlay=False,
                                    name='Dublin')

    density_layer = folium.Choropleth(geo_data=gpd_global_cnt,
                                        name="density",
                                        data=gpd_global_cnt,
                                        columns=["ED_ID", "pop"],
                                        key_on="feature.properties.ED_ID",
                                        fill_color="OrRd",
                                        fill_opacity=0.4,
                                        line_opacity=0.8,
                                        legend_name="Pop density (%)",
                                        threshold_scale=8,
                                        highlight=True)

    places_marker_cluster = MarkerCluster(name='Sensors',
                                            options={'maxZoom': 20,
                                                    'maxClusterRadius': 80,
                                                    'disableClusteringAtZoom': 13
                                            })

    for index, row in places.iterrows():
        folium.CircleMarker(radius=0.1,
                            location=[row['latitude'], row['longitude']],
                            color="green",
                            fill=False).add_to(places_marker_cluster)
    dublin_layer.add_to(map_1)
    density_layer.add_to(map_1)
    places_marker_cluster.add_to(map_1)
    folium.LayerControl().add_to(map_1)
    return map_1




map_density_and_places = create_map_1(gpd_global_cnt, places)



















########## ---------------------------------------- ##########
##
##   Main code
##
lst_tabs = [
    'Présentation du projet', 'Materiel & Méthodes', 'Machine Learning',
    'Modèles Energétiques', 'Conclusions & Perspectives'
]
rad = st.sidebar.radio('Navigation', lst_tabs)



########## --------------- Presentation du projet
##
##

if rad == lst_tabs[0]:
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

    st.write("Objectifs :")
    st.write("Reduction de la facture énergétique via l'application de modèles d'éclairage intelligent")


########## --------------- Materiel & Méthodes
##
##





elif rad == lst_tabs[1]:

    st.write("The model")
    folium_static(map_density_and_places)
    st.write("Données de recensement")
    st.write("Données de géolocalication des établissements publics et privés")
    st.write("322 areas")
    st.write("> 8 k établissements recensés")
    st.write("> 47 k lampadaires")


    st.write('représentation géospatiale des données')







    # st.map(map_density_and_places)
    # f_path_map = "/home/djampa/code/data_project_lewagon/slcities/slcities/data/map_clusters.html"
    # balise_map = f"<iframe src='{f_path_map}' title='Basic map with folium' style={{ border: 'none', width: '800px', height: '300px' }}></iframe>"
    # st.markdown(balise_map, unsafe_allow_html=True)

    # m = folium.map.Popup(f_path_map, parse_html=True)
    # folium_static(m)

    # st.map(f_path_map)
    # ####____________________________________________________________####
    # # https://docs.streamlit.io/en/stable/tutorial/create_a_data_explorer_app.html
    # DATE_COLUMN = 'date/time'
    # DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
    #         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

    # def load_data(nrows):
    #     data = pd.read_csv(DATA_URL, nrows=nrows)
    #     lowercase = lambda x: str(x).lower()
    #     data.rename(lowercase, axis='columns', inplace=True)
    #     data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    #     return data

    # # Create a text element and let the reader know the data is loading.
    # data_load_state = st.text('Loading data...')
    # # Load 10,000 rows of data into the dataframe.
    # data = load_data(10000)
    # # Notify the reader that the data was successfully loaded.
    # data_load_state.text('Loading data...done!')
    # st.subheader('Number of pickups by hour')
    # hist_values = np.histogram(data[DATE_COLUMN].dt.hour,
    #                            bins=24,
    #                            range=(0, 24))[0]
    # st.bar_chart(hist_values)
    # ####------------------------------------------------------------####



    # ####____________________________________________________________####
    # m = folium.Map(location=[47, 1], zoom_start=6)
    # folium_static(m)
    # ####------------------------------------------------------------####




elif rad == 'Conclusions':
    st.markdown( "<h1 style='text-align: center; color: red;'>Smart Lighting</h1>",
    unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: red;'>Simply Bright</h2>",
            unsafe_allow_html=True)
