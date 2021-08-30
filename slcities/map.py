#imports from other .py files
# import lights
# import areas
#imports packages
import folium
from slcities.params import DUBLIN_CENTER_COORDS


# ----------------------------------
#        DATA VISUALIZATION
# ----------------------------------



class MapsVisualisation():

    def initialise_map(self, map_name, tiles, center_lat, center_lon, zoom_start=12):
        self.map = folium.Map(attr=map_name,
                              tiles=tiles,
                              location=[center_lat, center_lon],
                              zoom_start=zoom_start)
        return self.map





def lights_visualize():
    #----------------CREATE MAP----------------#
    map = folium.Map(
        location=[53.350140, -6.266155],
        zoom_start=12,
        tiles=
        'https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
        control_scale=True,
        attr='SL Cities Project')


    #----------------DENSITY LAYER----------------#
    density_layer = folium.Choropleth(
        geo_data=density_clean_gpd,
        name="density",
        data=density_clean_gpd,
        columns=["ED_ID", "density"],
        key_on="feature.properties.ED_ID",
        fill_color="OrRd",
        fill_opacity=0.4,
        line_opacity=0.8,
        legend_name="Pop density (%)",
        threshold_scale=8,
        highlight=True,
    ).add_to(map)


    #----------------TOOLTIP TO DENSITY LAYER----------------#
    tooltip = folium.features.GeoJsonTooltip(
        fields=['density', 'T1_2T', 'ED_ID'],
        aliases=[
            'Densité de population par km² : ', 'Population Totale : ',
            'Quartier : '
        ])
    density_layer.geojson.add_child(tooltip)


    #----------------MARKER CLUSTER FOR STREET LIGHTS----------------#
    marker_cluster = MarkerCluster(
        name='Light',
        options={
            'maxZoom': 20,
            #'minZoom': 200,
            'maxClusterRadius': 80
            #'disableClusteringAtZoom': 400
        })

    # add street lights marker to marker cluster
    for index, row in lights_df.iterrows():
        folium.CircleMarker(
            radius=0.1,
            location=[row['latitude'],row['longitude']],
            color="yellow",
            fill=False
        ).add_to(marker_cluster)


    #----------------ADD LAYERS TO MAP----------------#
    density_layer.add_to(map)
    #light_layer.add_to(map)
    marker_cluster.add_to(map)


    #----------------LAYER CONTROL----------------#
    folium.LayerControl().add_to(map)


    #----------------SHOW MAP----------------#
    return map

if __name__ == 'main':
    m = MapsVisualisation()
    tiles_url = 'https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}'
    truc = m.initialise_map(
        'truc',
        tiles_url,
        center_lat=DUBLIN_CENTER_COORDS[0],
        center_lon=DUBLIN_CENTER_COORDS[1]
    )
    print(truc)


# class MapsVisualisation():
#     # def __init__(self):
#     #     self.map = None

#     def initialise_map(self, map_name, tiles, center_lat, center_lon,
#                        zoom_start):
#         self.map = folium.Map(attr=map_name,
#                               tiles=tiles,
#                               location=[center_lat, center_lon],
#                               zoom_start=zoom_start)


# def lights_visualize():
#     #----------------CREATE MAP----------------#
#     map = folium.Map(
#         location=[53.350140, -6.266155],
#         zoom_start=12,
#         tiles=
#         'https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
#         control_scale=True,
#         attr='SL Cities Project')
