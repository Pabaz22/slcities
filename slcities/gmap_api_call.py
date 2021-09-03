import pandas as pd
import numpy as np
import datetime
import googlemaps
import time
import os

from slcities.coordinates import generate_region_around_center, create_coordinate_matrix
from slcities.params import DUBLIN_CENTER_COORDS, PLACES_TYPES_DISCRIMINANT_SET, API_CALL_COLUMNS_OF_INTEREST, NICE_CENTER_COORDS

"""
DOCS :
# https://www.datacourses.com/transform-json-into-a-dataframe-416/
# https://towardsdatascience.com/how-to-convert-json-into-a-pandas-dataframe-100b2ae1e0d8
# https://googlemaps.github.io/google-maps-services-python/docs/
# https://github.com/googlemaps/google-maps-services-python/issues/376
"""


def get_apy_key_from_file(file_path):
    """
    Read and return the api key from a file

    Parameters :
    ------------
    file_path (str) -- the path of the file containing the API KEY

    Returns :
    ---------
    (str) -- the api key as a string.
    """
    with open(file_path) as f:
        api_key = f.readline()
        api_key = api_key.strip()
    return api_key



class GmapPlaceApiCall():
    def __init__(self, gmap_client):
        self.gmaps = gmap_client
        self.location = None
        self.place_type = None
        self.df_api_res=None

    def api_call_placenearby_rankby_distance(self,
                                             location,
                                             place_type,
                                             time_sleep=3):
        """
        api_call_placenearby_rankby_distance
        Inspired by : https://github.com/googlemaps/google-maps-services-python/issues/376
        """
        list_results = []
        # result = self.gmaps.places_nearby(location=location,
        #                             type=place_type,
        #                             rank_by='distance',
        #                             language='en')
        # list_results.extend(result['results'])
        # while 'next_page_token' in result.keys():
        #     time.sleep(time_sleep)
        #     result = self.gmaps.places(page_token=result['next_page_token'])
        #     list_results.extend(result['results'])
        # return pd.json_normalize(list_results)
        try:
            result = self.gmaps.places_nearby(location=location,
                                        type=place_type,
                                        rank_by='distance',
                                        language='en')
        except:
            print(f"Invalid request : loc = {location}; place = {place_type}. Next Call")
        else:
            list_results.extend(result['results'])
            nxt = True
            while 'next_page_token' in result.keys() and nxt==True:
                time.sleep(time_sleep)
                try:
                    result = self.gmaps.places(page_token=result['next_page_token'])
                except:
                    print(f"Invalid request : loc = {location}; place = {place_type}. Next Call")
                    nxt = False
                else:
                    list_results.extend(result['results'])
        return pd.json_normalize(list_results)


    def remove_rows_with_condition_on_columns(self, df, column, lst_values, remove=True):
        """
        Filter dataframe to retain/exclude rows based on a set of values for a specific columns

        Parameters :
        ------------
        df (pandas dataframe) -- the input pandas dataframe
        column (string) -- the column to use for filtering
        lst_values (list of str) -- the column values used as a criterion to exclude/retain rows
        retain (bool) -- if False (default), only rows for wich the column value is not in lst_values will be retained
        Else, these rows will be excluded.

        Returns :
        ---------
        (pandas dataframe) -- the resulting dataframe
        """
        if remove:
            df = df.loc[~df[column].isin(lst_values)]
        else:
            df = df.loc[df[column].isin(lst_values)]
        return df

    def get_df_subset_columns(self, df, lst_columns, retain=True):
        """
        Filter dataframe to only retain/exclude the columns specified in lst_columns

        Parameters :
        ------------
        df (pandas dataframe) -- the input pandas dataframe
        lst_columns (list of string) -- the list of the columns of interest
        retain (bool) -- if true, only columns specified in lst_columns will be retained
        Else, these columns will be excluded.

        Returns :
        ---------
        (pandas dataframe) -- the resulting dataframe
        """
        if retain:
            df = df.loc[:, df.columns.isin(lst_columns)]
        else:
            df = df.loc[:, ~df.columns.isin(lst_columns)]
        return df

    def transform_lst_of_values_column_into_string(self, df, column, sep='|'):
        """
        Transform list stored in a column into string

        Parameters :
        ------------
        df (pandas dataframe) -- the input pandas dataframe
        column (str) -- the name of the columns of interest
        sep (str) -- the separator to use when joining the list elements

        Returns :
        ---------
        (pandas dataframe) -- the resulting dataframe
        """
        df[column] = df[column].apply(f'{sep}'.join)
        return df

    def add_a_column_with_single_value(self, df, column_name, value):
        """
        Add a column to a dataframe with a defined value for all the rows

        Parameters :
        ------------
        df (pandas dataframe) -- the input pandas dataframe
        column_name (str) -- the name of the columns to create
        value (str) -- the value to set for the whole column

        Returns :
        ---------
        (pandas dataframe) -- the resulting dataframe
        """
        df[column_name] = value
        return df

    def generate_api_call_file_name(self):
        """
        Generate a file name corresponding to an API call

        Parameters :
        ------------
        location (tuple) -- the location coordinates (lat, lon)
        place_type (str) -- the type of place we are looking for in the
        API call

        Returns :
        ---------
        (str) -- the file name
        """
        return f'APIcall_lat{self.location[0]}_lon{self.location[1]}_{self.place_type}.tsv'

    def write_file_from_df(self, df, dir_path, f_name, sep='\t'):
        """
        Store the dataframe content in a file

        Parameters :
        ------------
        df (pandas dataframe) -- the input pandas dataframe
        dir_path (str) -- the output directory path
        f_name (str) -- the file name
        sep (str) -- the column separator to use

        """
        path = os.path.join(dir_path, f_name)
        df.to_csv(path, sep=sep)

    def write_empty_file(self, dir_path, f_name):
        """
        Create an empty file. Usefull to see that a call
        was executed but did not returned a result

        Parameters :
        ------------
        dir_path (str) -- the output directory path
        f_name (str) -- the file name

        """
        path = os.path.join(dir_path, 'EmptyRes_'+f_name)
        with open(path,'w') as f:
            f.write('')

    def return_df(self):
        return self.df_api_res


    def make_call(self, location, place_type, time_sleep=2):
        """
        """
        self.location = location
        self.place_type = place_type
        self.df_api_res = self.api_call_placenearby_rankby_distance(
            self.location, self.place_type, time_sleep=time_sleep)
        if self.df_api_res.size == 0: # case where the api call return an empty dataframe
            self.df_api_res = None


    def clean_and_format_results(self, interest_col_lst):
        ## Remove the rows where 'permanently_closed' == True, i.e the shops that are no
        ## longuer existing
        # df = self.remove_rows_with_condition_on_columns(self.df_api_res.copy(),
        #                                                 'permanently_closed',
        #                                                 [True],
        #                                                 remove=True)
        if self.df_api_res is not None:
            df = self.remove_rows_with_condition_on_columns(self.df_api_res.copy(),
                                                            'business_status',
                                                            ['OPERATIONAL'],
                                                            remove=False)

            ## Drop columns from the dataframe to only retain the ones specified in interest_col_lst
            df = self.get_df_subset_columns(df, interest_col_lst, retain=True)

            ## Transform the list of types in the 'types' column into a string where each type is separated
            ## from the other with a defined separator
            df = self.transform_lst_of_values_column_into_string(df,
                                                                'types',
                                                                sep='|')

            ## Add a tag column for which the value is the type used for the API call (place_type)
            df = self.add_a_column_with_single_value(df, 'main_type',
                                                    self.place_type)

            self.df_api_res = df

    def save_results(self, dir_path, sep='\t'):
        ## Generate output file name
        f_name = self.generate_api_call_file_name()
        if self.df_api_res is not None:
            ## Save the API call results
            self.write_file_from_df(self.df_api_res,
                                    dir_path,
                                    f_name,
                                    sep='\t')
        else:
            self.write_empty_file(dir_path,f_name)

    ####---------------------------------------------------------####



def generate_call_list(center_location, region_dim, nb_ticks,
                       requested_place_types):
    search_area_width = search_area_height = region_dim
    ## Generate the North-Ouest (NO) and South-East (SE) coordinates of the
    ## squared area centered on 'center_location.
    NO_coords, SE_coords = generate_region_around_center(
        center_location, width=search_area_width, height=search_area_height)
    ## Generate a location list of nb_ticks*nb_ticks centers
    coordinates_lst = create_coordinate_matrix(NO_coords,
                                                  SE_coords,
                                                  nb_ticks=nb_ticks)
    ## Generate the search grid
    call_list = []
    ## iterate over the position in coordinate matrix
    for location in coordinates_lst:
        ## iterate over the place's types
        for place_type in requested_place_types:
            call_list.append([location, place_type])
    return call_list






# def create_location_grid(center_location, region_dim, nb_ticks):
#     search_area_width = search_area_height = region_dim
#     ## Generate the North-Ouest (NO) and South-East (SE) coordinates of the
#     ## squared area centered on 'center_location.
#     NO_coords, SE_coords = generate_region_around_center(
#         center_location, width=search_area_width, height=search_area_height)
#     ## Generate a location grid of nb_ticks*nb_ticks centers
#     coordinates_lst = create_coordinate_matrix(NO_coords,
#                                                   SE_coords,
#                                                   nb_ticks=nb_ticks)

#     return coordinates_lst


# def write_logs(file_path, log):
#     with open(file_path, 'a') as f:
#         f.write(log + '\n')


def write_call_list_file(f_path, call_lst):
    with open(f_path, 'w') as f:
        for call in call_lst:
            location, place_type = call
            lat, lon = location
            f.write(f'{lat}\t{lon}\t{place_type}\n')
            # f.write(f'{location}\t{place_type}\n')


def read_call_list_file(f_path):
    res = []
    with open(f_path, 'r') as f:
        for line in f.readlines():
            line = line.strip().split()
            if len(line) == 3:
                lat, lon, p_type = line
                res.append([(float(lat), float(lon)),
                            p_type])
    return res


def log_executed_call(f_path, location, place_type):
    with open(f_path, 'a') as f:
        f.write(f'{location}\t{place_type}\n')


# def search_places(api_key, coordinates_lst, requested_place_types,
#                   columns_of_interest=API_CALL_COLUMNS_OF_INTEREST):
#     ## Initialise the GoogleMaps client
#     gmaps = googlemaps.Client(key=api_key)
#     ## Initialise count
#     cnt = 1
#     nb_tasks = nb_ticks**2 * len(requested_place_types)
#     ## Iterate over the position in coordinate matrix
#     for location in coordinates_lst:
#         ## Iterate over the place's types
#         for place_type in requested_place_types:
#             ## Initialise a GmapPlaceApiCall object
#             api_call = GmapPlaceApiCall(gmaps)
#             ## Make the API call for the given location and place type
#             api_call.make_call(location, place_type, time_sleep=2)
#             ## Clean and format the results
#             api_call.clean_and_format_results(columns_of_interest)
#             ## Store the API call results in a .tsv file in the output_dir_path
#             api_call.save_results(output_dir_path, sep='\t')
#             ## write logs one it's done
#             log = f"Api call ({cnt}/{nb_tasks}) \t | location :{location}, place's type : {place_type}"
#             print(log)
#             write_logs(os.path.join(output_dir_path, 'logs.txt'), log)
#             cnt += 1



def search_places(output_dir_path, api_key, call_lst,
                  columns_of_interest=API_CALL_COLUMNS_OF_INTEREST):

    executed_calls_f_path = os.path.join(output_dir_path,
                                         'executed_calls.txt')
    ## Initialise the GoogleMaps client
    gmaps = googlemaps.Client(key=api_key)
    ## Initialise count
    cnt = 1
    nb_tasks = len(call_lst)
    ## Iterate over calls
    for call in call_lst:
        location, place_type = call
        ## Initialise a GmapPlaceApiCall object
        api_call = GmapPlaceApiCall(gmaps)
        ## Make the API call for the given location and place type
        api_call.make_call(location, place_type, time_sleep=2)
        ## Clean and format the results
        api_call.clean_and_format_results(columns_of_interest)
        ## Store the API call results in a .tsv file in the output_dir_path
        api_call.save_results(output_dir_path, sep='\t')
        ## write logs one it's done
        log = f"Api call ({cnt}/{nb_tasks}) \t | location :{location}, place's type : {place_type}"
        print(log)
        log_executed_call(executed_calls_f_path, location, place_type)
        cnt += 1



    ####---------------------------------------------------------####


if __name__ == "__main__":
    # region_dim = 3000
    # nb_ticks = 12
    # columns_of_interest = API_CALL_COLUMNS_OF_INTEREST
    # requested_place_types = PLACES_TYPES_DISCRIMINANT_SET
    # center_location = DUBLIN_CENTER_COORDS


    # ## Get the GoogleMaps api key from a file
    # key_file_path = ''
    # if not os.path.exists(key_file_path):
    #     valid_key_file_path = False
    #     while valid_key_file_path != True:
    #         key_file_path = input('Please enter the absolut path to your api key file')
    #         if os.path.exists(key_file_path):
    #             valid_key_file_path = True
    # api_key = get_apy_key_from_file(key_file_path)

    # ## Create output directory
    # output_dir_path = os.path.join(
    #     os.path.dirname(os.path.abspath(__file__)), 'intermediate_data',
    #     'places_api_call',
    #     datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
    # os.mkdir(output_dir_path)

    # ## Generate the call list
    # call_lst = generate_call_list(center_location, region_dim, nb_ticks,
    #                    requested_place_types)

    # call_lst_f_path = os.path.join(output_dir_path,
    #                                'calls_to_perform.txt')
    # write_call_list_file(call_lst_f_path, call_lst)

    # ## (OPT) Import call list
    # # remaining_calls_path = ''
    # # call_lst = read_call_list_file(remaining_calls_path)

    # ## Make the Api call from the list
    # search_places(output_dir_path, api_key, call_lst,
    #               columns_of_interest)

    region_dim = 3000
    nb_ticks = 10
    columns_of_interest = API_CALL_COLUMNS_OF_INTEREST
    requested_place_types = PLACES_TYPES_DISCRIMINANT_SET
    center_location = NICE_CENTER_COORDS


    ## Get the GoogleMaps api key from a file
    key_file_path = '/home/djampa/other/gmap_api_key_vincent.txt'
    if not os.path.exists(key_file_path):
        valid_key_file_path = False
        while valid_key_file_path != True:
            key_file_path = input(
                'Please enter the absolut path to your api key file')
            if os.path.exists(key_file_path):
                valid_key_file_path = True
    api_key = get_apy_key_from_file(key_file_path)

    ## Create output directory
    output_dir_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'intermediate_data',
        'places_api_call',
        datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S"))
    os.mkdir(output_dir_path)

    ## Generate the call list
    call_lst = generate_call_list(center_location, region_dim, nb_ticks,
                                  requested_place_types)

    call_lst_f_path = os.path.join(output_dir_path, 'calls_to_perform.txt')
    write_call_list_file(call_lst_f_path, call_lst)

    ## (OPT) Import call list
    # remaining_calls_path = ''
    # call_lst = read_call_list_file(remaining_calls_path)

    ## Make the Api call from the list
    search_places(output_dir_path, api_key, call_lst, columns_of_interest)
