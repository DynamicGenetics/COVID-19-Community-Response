#import packages
import pandas as pd
import geopandas as gpd
import re
import warnings

def read_keys():
    LSOA = gpd.read_file(
    "static/geoboundaries/Lower_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BSC.geojson"
    )
    # Keep only Welsh codes.
    LSOA = clean_codes(LSOA, res='LSOA', key_col='LSOA11CD')

    LA = gpd.read_file(
    "static/geoboundaries/Local_Authority_Districts_(December_2019)_Boundaries_UK_BGC.geojson"
    )
    # Keep only Welsh codes.
    LA = clean_codes(LA, res='LA', key_col='lad19cd')

    return LSOA, LA


def clean_keys(df: pd.DataFrame, res: str, key_col: str, key_is_code: bool=True):
    """Ensures df key column (i.e column used for joining) is correctly formatted 
    for joins in the next steps. Accepts key as a code or name, at LA or LSOA level. 
    Will rename key column if it is not the standard name. 

    Arguments:
        df {pd.DataFrame} -- Dataframe to be cleaned
        res {str} -- Accepts 'LA' or 'LSOA' as resolution of the data
        key_col {str} -- Name of column containing the code or name

    Keyword Arguments:
        key_is_code {bool} -- Assumes the key column a code. If false, key column is 
                                a name. (default: {True})

    Returns:
        df {pd.DataFrame} -- Returns dataframe with required rows for that resolution.
    """
    # Make sure res is defined correctly 
    if type(res) != str:
        raise TypeError("Arg 'res' should be 'LA' or 'LSOA' as string")

    # For instances where the key column is a code (preferred)
    if key_is_code:
        # This will drop non Welsh LSOAs, and drop NAs.
        df_new = df[df[key_col].str.contains("W", na=False)].copy()
        df_new.reset_index(drop=True, inplace=True)
        #Strip surrounding whitespace if there is any.
        df_new[key_col] = df_new[key_col].apply(lambda x: x.strip())
    else:
        #Assumes this means key is a name
        df_new = df.dropna().copy()
        df_new.reset_index(inplace=True)


    # If the column-name doesn't match the standard keyname, change it to that
    if res == 'LA':
        if key_is_code:
            if key_col != 'lad19cd':
                df_new.rename(columns={key_col: "lad19cd"}, inplace=True)
        else:
            if key_col != 'lad19nm':
                df_new.rename(columns={key_col: "lad19nm"}, inplace=True)
        
        # Do a final check that we still have the expected shape. Return warning if not.
        if df_new.shape[0] != 22:
            warnings.warn("An error has occured. There are not the expected 22 rows.")


    elif res == 'LSOA':
        if key_is_code:
            if key_col != "LSOA11CD":
                df_new.rename(columns={key_col: "LSOA11CD"}, inplace=True)
        else:
            if key_col != "LSOA11NM":
                df_new.rename(columns={key_col: "LSOA11NM"}, inplace=True)

        # Do a final check that we still have the expected shape. Return warning if not.
        if df_new.shape[0] != 1909:
            warnings.warn("An error has occured. There are not the expected 1909 rows.")

    return df_new


def clean_bracketed_data(df: pd.DataFrame, cols: list):
    """For a df with columns in the format 'NUMBER (PERCENTAGE)' this function extracts the 
    data into two new columns and deletes the original column. 

    Arguments:
        df {pd.DataFrame} -- DataFrame containing 'cols'
        cols {list} -- list of cols where data needs extracting

    Returns:
        df {pd.DataFrame} -- DataFrame with each col replaced by two new cols. 
    """

    # Define the regex pattern and find capture groups
    def extract_data(string):
        pattern = r'\d+.?\d+'
        data = re.findall(pattern, string)
        return data

    for col in cols:
        # Derive the names for the new columns from exitsing names
        name_counts = col + '_count'
        name_percent = col + '_pct'
        # Apply the extract_data function to each line, and the data to two new columns
        df[[name_counts, name_percent]] = df[col].apply(lambda x: extract_data(x))
        df.drop(columns=col, inplace=True)

    return df


def standardise_keys(df: pd.DataFrame, res: str, keep_cols: list=[], key_is_code: bool=True):
    """Given dataframe and chosen cols, will use LA or LSOA geopandas dataframes to create
    standardised columns for area codes and names

    Arguments:
        df {pd.DataFrame} -- df with a key column.
        res {str} -- 'LA' or 'LSOA'

    Keyword Arguments:
        keep_cols {list} -- If only keeping some columns, pass a list of col names (default: {[]})
        key_is_code {bool} -- Assumes the key column a code. If false, key column is 
                                a name.  (default: {True})

    Raises:
        Exception: Exception raised if wrong number of rows written out.
        ValueError: Raised if res is not 'LA' or 'LSOA' 

    Returns:
        dataframe -- returns df with standardised key codes and names. 
    """

    # Load in the geography data being used as 'ground truth' for the codes and names
    LA, LSOA = read_keys()
    
    # If keep_cols was left empty then assume all columns are being kept
    if keep_cols == []:
        keep_cols = list(df.columns)
    
    # Create the area codes and names depending on resolution and what keys are available in the
    # original data frame. 
    if res == 'LSOA':
        df_tidy = LSOA[['LSOA11CD', 'LSOA11NM']].merge(df[keep_cols], on='LSOA11CD', how="inner")
        # Check the df has the expected number of rows after merging
        if df_tidy.shape[0] != 1909:
            raise Exception("An error has occured. The full 1909 rows were not produced in merge.")
    elif res == 'LA':
        if key_is_code:
            key = 'lad19cd'
        else:
            key = 'lad19nm'
        #Change the key column depending on the argument
        df_tidy = LA[['lad19cd', 'lad19nm']].merge(df[keep_cols], on=key, how="inner")
        # Check the df has the expected number of rows after merging
        if df_tidy.shape[0] != 22:
            raise Exception("An error has occured. The full 22 rows were not produced in merge.")
    else:
        raise ValueError("Res provided does not match 'LSOA' or 'LA")
    
    return df_tidy


def write_cleaned_data(df: pd.DataFrame, res: str, outname: str):

    csv_name = 'cleaned/' + res + '_' + outname + '.csv'
    df.to_csv(csv_name, index=False)