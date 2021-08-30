import os
import sys
import pandas as pd
from slcities.utils import list_files_in_dir, filter_filenames, get_files_absolute_path, open_file_as_pandas_dataframe
from slcities.params import PLACES_TYPES_DISCRIMINANT_SET



class GmapApiCallPreProcessing():
    def __init__(self):
        self.api_call_df = None

    def get_API_call_results_fpath(self, input_dir):
        filenames = list_files_in_dir(input_dir)
        filenames = filter_filenames(filenames, suffix='.tsv',
                                     prefix='APIcall')
        return get_files_absolute_path(input_dir, filenames)

    def clean_duplicated_rows(self, df, subset=None, ignore_index=True):
        """
        NB : No need to sort first. It does not speed up the
        duplicates research. On the contrary.
        """
        return df.drop_duplicates(subset=subset, ignore_index=ignore_index)

    def transform_places_types_var(self , df):
        df['types'] = df['types'].apply(lambda x: x.split('|'))
        return df

    def filter_tags_list(self, lst, specific_tags=True):
        authorised_second_order_types_lst = [
        'food', 'grocery_or_supermarket', 'health',
        'home_goods_store', 'local_government_office',
            'store']
        if  specific_tags:
            res = [x for x in lst if x in PLACES_TYPES_DISCRIMINANT_SET]
        else:
            res = [x for x in lst if x not in PLACES_TYPES_DISCRIMINANT_SET and x in authorised_second_order_types_lst]
        return res

    def assign_tag(self, df):
        df['tag'] = df['specific_tag'].apply(lambda x: x[0])
        for i, row in df[df['nb_specific_tag']>1].iterrows():
            if len(row['general_tag']) > 0:
                df.loc[i, 'tag'] = row['general_tag'][0]
        return df

    def get_tag_cnt_freq_table(self, df, tag_colname='tag'):
        tags_cnt_freq = pd.DataFrame({
            'tags': df[tag_colname].value_counts(normalize=True).index.tolist(),
            'cnt' : df[tag_colname].value_counts().values.tolist(),
            'freq' : df[tag_colname].value_counts(normalize=True).values.tolist()
        })
        tags_cnt_freq.set_index('tags', inplace=True)
        return tags_cnt_freq


    def open_results(self, input_dir, lst_columns_to_use = [
        'place_id', 'main_type', 'types', 'geometry.location.lat',
       'geometry.location.lng'], sep='\t'):
        if os.path.isdir(input_dir):
            f_path_lst = self.get_API_call_results_fpath(input_dir)
            open_file_as_pandas_dataframe
            lst_api_call_df = []
            for f_path in f_path_lst:
                lst_api_call_df.append(open_file_as_pandas_dataframe(f_path,
                                                            lst_columns=lst_columns_to_use,
                                                            sep='\t'))
            self.api_call_df = pd.concat(lst_api_call_df)
        else:
            print(f'{input_dir} is not a directory, program will stop.')
            sys.exit(0)

    def extract_and_format_results(self):
        """
        1) Remove the duplicate rows : the duplicated rows, i.e the 100%
        identical rows are removed.
        2) Get the a list of places tags : transform string of types tags
        into a list of tags.

        """
        df = self.api_call_df.copy()
        ## 1) Remove the duplicate rows
        df = self.clean_duplicated_rows(df,
                                        subset=None,
                                        ignore_index=True)
        ## 2) Get the a list of places tags
        df = self.transform_places_types_var(df)
        ## 3) Get specific and general tags for each row
        df['specific_tag'] = df['types'].apply(self.filter_tags_list,
                                               specific_tags=True)
        df['general_tag']= df['types'].apply(self.filter_tags_list,
                                               specific_tags=False)
        df['nb_specific_tag'] = df['specific_tag'].apply(len)
        ## 4) Assign a tag given the specific and general tag
        df = self.assign_tag(df.reset_index(drop=True))
        ## 5) Change columns names
        df = df.rename(columns={'geometry.location.lat':'latitude',
                        'geometry.location.lng':'longitude',
                        'tag':'place'})
        self.api_call_df = df.reset_index(drop=True)


    def filter_results(self, columns_of_interest = [
        'place_id', 'latitude','longitude','place']):
        df = self.api_call_df.copy()
        ## 1) Remove unecessary columns
        df = df[columns_of_interest]
        ## 2) Remove duplicated rows
        self.api_call_df = self.clean_duplicated_rows(
            df, subset=['place_id', 'place'], ignore_index=True)

    def save_results(self, f_path, sep='\t', index=False):
        self.api_call_df.to_csv(f_path,
                                sep=sep,
                                index=index)


    def return_df(self):
        return self.api_call_df










if __name__ == "__main__":
    input_dir = os.path.join('intermediate_data',
                             'places_api_call',
                             '27-08-2021_00-07-56')
    api_call_pp = GmapApiCallPreProcessing()
    api_call_pp.open_results(input_dir)
    api_call_pp.extract_and_format_results()
    api_call_pp.filter_results()
    # f_path = os.path.join('data', 'places','places.tsv')
    # api_call_pp.save_results(f_path, sep='\t', index=False)
    print(api_call_pp.return_df())
