import os
import pandas as pd


def list_files_in_dir(dir_path):
    """
    list files in a directory

    Parameters :
    ------------
    dir_path (str) -- The directory where the files are located

    Returns :
    ---------
    (list of str) -- The list of the files names.
    """
    return os.listdir(dir_path)


def filter_filenames(lst_fnames, suffix='.tsv', prefix=None):
    """
    Filter filenames according to a suffix/extension and optionally a prefix.

    Parameters :
    ------------
    lst_fnames (list of str) -- A list of files names.
    suffix (str) -- the suffix/extension to look for in a file name.
    Only the files with this suffix will be returned.
    prefix (str) -- (optional; default=None) if specified, only files with
    this suffix will be returned (in addition to the suffix condition)

    Returns :
    ---------
    (list of str) -- The list of the filtered files names.
    """
    if prefix is None:
        filenames = [
            f_name for f_name in lst_fnames if f_name.endswith(suffix)
        ]
    else:
        filenames = [
            f_name for f_name in lst_fnames
            if f_name.endswith(suffix) and f_name.startswith(prefix)
        ]
    return filenames


def get_files_absolute_path(dir_path, lst_fnames):
    """
    Generate files absolute paths.

    Parameters :
    ------------
    dir_path (str) -- The directory where the files are located
    lst_fnames (list of str) -- A list of files names.

    Returns :
    ---------
    (list of str) -- The list of the files absolute paths.
    """
    return [os.path.join(dir_path, f_name) for f_name in lst_fnames]


def open_file_as_pandas_dataframe(f_path, lst_columns=None, sep='\t'):
    if lst_columns is None:
        df = pd.read_csv(f_path, sep=sep)
    else:
        df = pd.read_csv(f_path, sep=sep, usecols=lst_columns)
    return df
