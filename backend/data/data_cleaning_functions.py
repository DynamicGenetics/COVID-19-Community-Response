#import packages
import pandas as pd


def clean_LSOAs(df: pd.DataFrame, LSOA11CD_col: str='LSOA11CD'):
    """ Given a dataframe and a column with Lower Super Output Area Codes
    this will remove white space, filter out non-Welsh area codes and NAs.
    If the column is not already named LSOA11CD it will rename it to this.
    """

    # This will drop non Welsh LSOAs, and drop NAs.
    df_new = df[df[LSOA11CD_col].str.contains("W", na=False)].copy()
    df_new.reset_index(drop=True, inplace=True)

    #Strip surrounding whitespace if there is any.
    df_new[LSOA11CD_col] = df_new[LSOA11CD_col].apply(lambda x: x.strip())

    # If the LSOA column-name doesn't match the keyname, change it to that
    if LSOA11CD_col != "LSOA11CD":
        df_new.rename(columns={LSOA11CD_col: "LSOA11CD"}, inplace=True)
    
    return df_new


def rename_cols(df: pd.DataFrame, rename: dict):
    """ Rename columns give in rename dictionary argument """

    df.rename(
    columns=rename,
    inplace=True)


def tidy_LSOAs(df: pd.DataFrame, keep_cols: list):
    """ Given dataframe and chosen cols, will merge against LSOA on the
    and return a dataframe with LSOA11CD, LSOA11NM and 
    cols.Requires LSOA11CD column in df. """
    
    df_tidy = LSOA[['LSOA11CD', 'LSOA11NM']].merge(df[keep_cols], on="LSOA11CD", how="inner")

    # Check the df has the expected number of rows after merging.
    if df_tidy.shape[0] != 1909:
        raise Exception("An error has occured. The full 1909 rows were not produced in merge.")

    return df_tidy


def write_cleaned_data(df: pd.DataFrame):

    """ For each variable column in a dataframe saves out to the cleaned folder as the 
    name of the column, to csv. """

    #Get the name of data column/s by removing the known column names
    varbs = list(df.columns)
    varbs.remove('LSOA11CD')
    varbs.remove('LSOA11NM')

    # For each col of the df save to seperate csv in 'cleaned' folder
    # Usually there is only one, but will allow for more.
    for varb in varbs:
        csv_name = 'cleaned/' + varb + '.csv'
        df.to_csv(csv_name,
                columns=['LSOA11CD', 'LSOA11NM', varb],
                index=False)