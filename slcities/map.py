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

    def initialise_map(self, map_name, tiles, lat_center, lon_center, zoom_start=12):
        """

        """
        self.map = folium.Map(attr=map_name,
                              tiles=tiles,
                              location=[lat_center, lon_center],
                              zoom_start=zoom_start)
        return self.map

    def create_layer(self, geo_df, layer_name, legend_name,
                  key_on="feature.properties.ED_ID", fill_color="OrRd",
                  fill_opacity=0.4, line_opacity=0.8, threshold_scale=8,
                  highlight=True):
        """
        columns=["ED_ID", "density"]
        """
        layer = folium.Choropleth(geo_data=geo_df, name=layer_name,
                                    data=geo_df,columns=geo_df.columns[0:2],
                                    key_on=key_on, fill_color=fill_color,
                                    fill_opacity=fill_opacity,
                                    line_opacity=line_opacity,
                                    legend_name=legend_name,
                                    threshold_scale=threshold_scale,
                                    highlight=highlight)
        return layer

    def add_tootip_to_layer(self, layer, fields, aliases):
        """
        fields=['density', 'T1_2T', 'ED_ID']
        aliases=[
            'Densité de population par km² : ', 'Population Totale : ',
            'Quartier : '
        ]
        """
        tooltip = folium.features.GeoJsonTooltip(fields=fields,
                                                 aliases=aliases)
        layer.geojson.add_child(tooltip)

    def create_marker_cluster(self, mc_name, max_zoom=20, max_cluster_radius=80):
        """

        """
        marker_cluster = MarkerCluster(
            name='Light',
            options={
                'maxZoom': max_zoom,
                #'minZoom': 200,
                'maxClusterRadius': max_cluster_radius
                #'disableClusteringAtZoom': 400
            })
        return marker_cluster

    def add_marker_to_marker_cluster(self, marker_cluster, geo_df,
                                     lat_col='latitude', lon_col='longitude',
                                     radius=0.1, color='yellow', fill=False):
        """

        """
        for index, row in geo_df.iterrows():
            folium.CircleMarker(radius=radius,
                                location=[row[lat_col], row[lon_col]],
                                color=color,
                                fill=fill).add_to(marker_cluster)








# def lights_visualize():
#     #----------------CREATE MAP----------------#
#     map = folium.Map(
#         location=[53.350140, -6.266155],
#         zoom_start=12,
#         tiles=
#         'https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
#         control_scale=True,
#         attr='SL Cities Project')


#     #----------------DENSITY LAYER----------------#
#     density_layer = folium.Choropleth(
#         geo_data=density_clean_gpd,
#         name="density",
#         data=density_clean_gpd,
#         columns=["ED_ID", "density"],
#         key_on="feature.properties.ED_ID",
#         fill_color="OrRd",
#         fill_opacity=0.4,
#         line_opacity=0.8,
#         legend_name="Pop density (%)",
#         threshold_scale=8,
#         highlight=True,
#     ).add_to(map)


#     #----------------TOOLTIP TO DENSITY LAYER----------------#
#     tooltip = folium.features.GeoJsonTooltip(
#         fields=['density', 'T1_2T', 'ED_ID'],
#         aliases=[
#             'Densité de population par km² : ', 'Population Totale : ',
#             'Quartier : '
#         ])
#     density_layer.geojson.add_child(tooltip)


#     #----------------MARKER CLUSTER FOR STREET LIGHTS----------------#
#     marker_cluster = MarkerCluster(
#         name='Light',
#         options={
#             'maxZoom': 20,
#             #'minZoom': 200,
#             'maxClusterRadius': 80
#             #'disableClusteringAtZoom': 400
#         })

#     # add street lights marker to marker cluster
#     for index, row in lights_df.iterrows():
#         folium.CircleMarker(
#             radius=0.1,
#             location=[row['latitude'],row['longitude']],
#             color="yellow",
#             fill=False
#         ).add_to(marker_cluster)


#     #----------------ADD LAYERS TO MAP----------------#
#     density_layer.add_to(map)
#     #light_layer.add_to(map)
#     marker_cluster.add_to(map)


#     #----------------LAYER CONTROL----------------#
#     folium.LayerControl().add_to(map)


#     #----------------SHOW MAP----------------#
#     return map

# if __name__ == 'main':
#     m = MapsVisualisation()
#     tiles_url = 'https://server.arcgisonline.com/arcgis/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}'
#     truc = m.initialise_map(
#         'truc',
#         tiles_url,
#         center_lat=DUBLIN_CENTER_COORDS[0],
#         center_lon=DUBLIN_CENTER_COORDS[1]
#     )
#     print(truc)


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
