import numpy as np
import pyproj
import haversine as hs
from haversine import Unit


def generate_region_around_center(center_coords, width, height):
    """
    Generate the coordinates of the NO (North-Ouest) and SE (South-East) points
    of a rectangular region centered on a given point.

    adapted from https://gis.stackexchange.com/questions/182489/find-rectangle-around-point-with-python

    Parameters :
    ------------
    center_coords (tuple) -- the lat, lon coordinates as a tuple e.g (lat, lon)
    width (numeric) -- the rectangle width (meters). Must be > 0
    height (numeric) -- the rectangle height (meters). Must be > 0

    Returns :
    ---------
    [(NO_lat, NO_lon), (SE_lat, SE_lon)] (list of tuple) -- the respective lat
    and lon of the NO and SE points
    """
    width = width / 2
    height = height / 2
    rect_diag = np.sqrt(width**2 + height**2)
    center_lat, center_lon = center_coords

    azimuth_NO = np.arctan(-width / height)
    azimuth_SE = np.arctan(-width / height) + np.pi

    geod = pyproj.Geod(ellps='WGS84')
    NO_lon, NO_lat, _ = geod.fwd(center_lon, center_lat,
                                 azimuth_NO * 180 / np.pi, rect_diag)
    SE_lon, SE_lat, _ = geod.fwd(center_lon, center_lat,
                                 azimuth_SE * 180 / np.pi, rect_diag)
    return [(NO_lat, NO_lon), (SE_lat, SE_lon)]


def create_coordinate_matrix(NO_coords, SE_coords, nb_ticks=10):
    """
    Generate a matrix of coordinates for a region specified by a NO
    (North-Ouest) and SE (South-East) coordinates


    Parameters :
    ------------
    NO_coords (tuple) -- the lat and lon coordinates of the North-Ouest point as
    a tuple e.g (lat, lon)
    SE_coords (tuple) -- the lat and lon coordinates of the South-East point as
    a tuple e.g (lat, lon)
    nb_ticks (int) -- the number of point generated per axis.

    Returns :
    ---------
    (list of tuples) -- A matrix of coordinates as a list of coordinates
    (lat, lon). The generated matrix is composed of nb_ticks**2 points.
    Can be transformed into a numpy array using reshape with a
    (nb_points, nb_points, 2) shape.
    """
    NO_lat, NO_lon = NO_coords
    SE_lat, SE_lon = SE_coords
    lat_space = np.linspace(NO_lat, SE_lat, nb_ticks)
    lon_space = np.linspace(NO_lon, SE_lon, nb_ticks)
    return [(i, j) for i in lat_space for j in lon_space]


def get_4_region_coordinates(NO_coords, SE_coords):
    """
    Compute the North-East and South-Ouest coordinates from North-Ouest and
    South-East coordinates

    Parameters :
    ------------
    NO_coords (tuple) -- the lat and lon coordinates of the North-Ouest point
    as a tuple e.g (lat, lon)
    SE_coords (tuple) -- the lat and lon coordinates of the South-East point
    as a tuple e.g (lat, lon)

    Returns :
    ---------
    (list of tuples) -- A list of coordinates as (lat, lon) tuples :
    [NO_coords, NE_coords, SO_coords, SE_coords]
    """
    NE_coords = (NO_coords[0], SE_coords[1])
    SO_coords = (SE_coords[0], NO_coords[1])
    return [NO_coords, NE_coords, SO_coords, SE_coords]


def compute_haversine_distances(loc1, loc2):
    """
    Compute haversine (meters) distance between two coordinates (lat, lon)

    inspired from https://towardsdatascience.com/calculating-distance-between-two-geolocations-in-python-26ad3afe287b

    Parameters :
    -----------
    loc1, loc2 (tuple) -- a (lat, lon) coordinate

    Returns :
    ---------
    (float) -- the haversine distance (meters) between the two coordinates.
    """
    return hs.haversine(loc1, loc2, unit=Unit.METERS)
