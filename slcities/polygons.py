import geopandas as gpd
import numpy as np


def which_polygon(point, polygon_df, edid_col='ED_ID', closest=True):
    """
    function to apply on a points dataframe
    https://towardsdatascience.com/heres-the-most-efficient-way-to-iterate-through-your-pandas-dataframe-4dad88ac92ee
    https://automating-gis-processes.github.io/CSC18/lessons/L4/point-in-polygon.html

    to_dict('record') suppose {column -> value},
    https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_dict.html?highlight=to_dict#pandas.DataFrame.to_dict
    """
    i = 0
    nb_poly = len(polygon_df)
    included=False # marker if point within polygon
    parent_poly=np.nan
    lst_poly_dict = polygon_df.to_dict('record')
    if closest:
        distance={}
        while included == False and i < nb_poly:
            poly = lst_poly_dict[i][0]
            if point.geometry.within(poly.geometry):
                included = True
                parent_poly = poly.ED_ID
            else:
                distance[poly.geometry.distance(point.geometry)] = poly.ED_ID
            i += 1
        parent_poly = distance[min(distance)]
    else:
        while included == False and i < nb_poly:
            poly = lst_poly_dict[i][0]
            if point.geometry.within(poly.geometry):
                included = True
                parent_poly = poly.ED_ID
            i += 1
    return parent_poly


















def containers(points, polygons):
    '''
    * goal :
    determines which polynom contains (or is closest to) each point defined in the geoDataframe 'points'
    * arguments :
    geoDataFrame points
    geoDataFrame polygons (column 'ED_ID' describing polygon_id)
    * returns :
    geoDataFrame points enriched with polynom_id 'ED_ID' column
    '''

    #list of polygon containing points, to be added to points dataframe
    column_polygon_id=[]

    for i, pt in points.iterrows():
        within=False # marker if point within polygon
        distance={} #dict distance btw this point to each polygon ; {distance(pt, polygon_k) : polygon_k_id}
        for j, poly in polygons.iterrows():
            counter_pts_in_poly=0 #counter nb of points in this polygon

            #in case point within polygon
            if pt.geometry.within(poly.geometry):
                # mark this point as within a polygon
                within=True
                # add this polygon id to list to be further associated to this point
                column_polygon_id.append(poly.ED_ID)
                break

            #in case this polygon does not contain this point, fill distance for pair (pt, poly)
            distance[poly.geometry.distance(pt.geometry)]=poly.ED_ID

        # despite checking all polygons, in case point within no polygon
        if within==False:
            # add the closest polygon to list to be further associated to this point
            column_polygon_id.append(distance[min(distance)])

    #adding column to points_df
    points['ED_ID']=column_polygon_id

    return points



def nb_pt_within(points, polygons):
    '''
    * goal :
    determines number of points within (or closest to) each polygon defined in the geoDataframe 'polygons'

    * arguments :
    geoDataFrame points (column 'ED_ID' describing in which polygon the point is within (or closest to))
    geoDataFrame polygons (column 'ED_ID' describing polygon_id)

    * returns :
    geoDataFrame polygons enriched with 'nb points' column
    '''

    #nb of points in a polygon = value_counts of polygon in points_df
    value_counts_df = points.ED_ID.value_counts().reset_index()
    nb_pt_in_poly_df = value_counts_df.rename(columns={'index':'ED_ID','ED_ID':'nb points'})

    #adding column to polygons_df
    polygons = polygons.merge(nb_pt_in_poly_df, on='ED_ID', how='inner')

    return polygons
