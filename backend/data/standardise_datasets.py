"""Module that generates the cleaned datasets for each variable from raw"""

# Import packages
import pandas as pd
import geopandas as gpd
import re
import os
from dataclasses import dataclass

# Import the raw data constants
from . import source_datasets as s


@dataclass
class StandardiseData:
    """Class for mapping the changes needed to standardise each dataset"""
    LA = 'LA'

    data: pd.DataFrame
    res: str  # Resolution at 'LSOA' or 'LA'
    key_col: str  # Name of the column that has a unique key
    key_is_code: bool  # Is the key column a LA or LSOA code?
    csv_name: str  # Name for the output CSV
    keep_cols: list = None  # List of columns specifically wanted to keep
    bracketed_data_cols: list = None  # List of columns where data is in the format (DATA (PERCENT))
    rename: dict = None  # Dictionary of columns that need renaming Cleaningself('old_name' : 'new_name' }
    std_data_: pd.DataFrame = None

    def standardise(self):
        """ Based on arguments provided, applies the correct functions to standardise the data.
        """

        # Validate step TBD

        # Filter the keycodes/names, remove whitespace, reset index
        self.std_data_ = self.clean_keys(df=self.data, res=self.res,
                                         key_col=self.key_col,
                                         key_is_code=self.key_is_code)

        # Rename the columns as needed
        if self.rename:
            self.std_data_.rename(columns=self.rename, inplace=True)

        # Merge against the LSOA dataset for consistent Codes and Names
        self.std_data_ = self.standardise_keys()

        # If argument has been passed for bracketed_data_cols, then apply the function.
        if self.bracketed_data_cols:
            self.std_data_ = self.clean_bracketed_data()

        # Write out to /cleaned
        # write_cleaned_data(df, res=self.res, csv_name=self.csv_name)
        return self

    @property
    def standardised_data(self):
        return self.std_data_

    def __add__(self, other):

        if not isinstance(other, StandardiseData):
            raise TypeError('unsupported operand type(s) for +: {} and {}',
                            self.__class__, type(other))

        if self.res == self.LA:
            merge_key = 'lad19cd'
        else:
            merge_key = 'LSOA11CD'
        self.data = pd.merge(self.std_data_, other.std_data_, on=merge_key)
        return self

    def read_keys(self):
        """ Reads in and returns the LSOA and LA geopandas dataframes as LSOA, LA. """

        # TBD: Standardise for GeoPandas DataFrame
        # MAKE THIS A CLASS ATTRIBUTE

        data_folder = s.GEO_DATA_FOLDER
        # Read data
        LSOA = gpd.read_file(os.path.join(data_folder,
                                          "Lower_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BSC.geojson")
                             )
        LA = gpd.read_file(os.path.join(data_folder,
                                        "Local_Authority_Districts_(December_2019)_Boundaries_UK_BGC.geojson")
                           )

        try:
            LSOA = self.clean_keys(LSOA, res="LSOA", key_col="LSOA11CD")
            LA = self.clean_keys(LA, res="LA", key_col="lad19cd")
        except Exception as e:
            # clean_keys will raise an exception if the right number of rows are not merged.
            raise e

        return LSOA, LA

    @staticmethod
    def clean_keys(df, res, key_col, key_is_code=True):
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
        if not isinstance(res, str):
            raise TypeError("Arg 'res' should be 'LA' or 'LSOA' as string")

        # For instances where the key column is a code (preferred)
        if key_is_code:
            # This will drop non Welsh LSOAs, and drop NAs.
            df_new = df[df[key_col].str.contains("W", na=False)].copy()
            df_new.reset_index(drop=True, inplace=True)
        else:
            # Assumes this means key is a name
            df_new = df.dropna(subset=[key_col]).copy()
            df_new.reset_index(drop=True, inplace=True)

        # Strip surrounding whitespace if there is any.
        df_new[key_col] = df_new[key_col].apply(lambda x: x.strip())

        # If the column-name doesn't match the standard keyname, change it to that
        if res == "LA":
            if key_is_code:
                if key_col != "lad19cd":
                    df_new.rename(columns={key_col: "lad19cd"}, inplace=True)
            else:
                if key_col != "lad19nm":
                    df_new.rename(columns={key_col: "lad19nm"}, inplace=True)

            # Do a final check that we still have the expected shape. Raise Exception
            # if not.
            if df_new.shape[0] < 22:
                raise Exception(
                    "An error has occured. There are not the expected 22 rows.")
        elif res == "LSOA":
            if key_is_code:
                if key_col != "LSOA11CD":
                    df_new.rename(columns={key_col: "LSOA11CD"}, inplace=True)
            else:
                if key_col != "LSOA11NM":
                    df_new.rename(columns={key_col: "LSOA11NM"}, inplace=True)

            # Do a final check that we still have the expected shape. Raise Exception
            # if not.
            if df_new.shape[0] < 1909:
                raise Exception(
                    "An error has occured. There are not the expected 1909 rows."
                )

        return df_new

    def standardise_keys(self):
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

        # Patching
        df = self.std_data_
        res = self.res
        keep_cols = self.keep_cols
        key_is_code = self.key_is_code

        # Load in the geography data being used as 'ground truth' for the codes and names
        # MOVE TO VALIDATION
        if keep_cols is None:
            keep_cols = []

        LSOA, LA = self.read_keys()

        # If keep_cols was left empty then assume all columns are being kept
        # VALIDATION
        if not keep_cols:
            keep_cols = list(df.columns)

        # Create the area codes and names depending on resolution and what keys are available in the
        # original data frame.
        if res == "LSOA":
            df_tidy = LSOA[["LSOA11CD", "LSOA11NM"]].merge(
                df[keep_cols], on="LSOA11CD", how="inner"
            )
            # Check the df has the expected number of rows after merging
            if df_tidy.shape[0] != 1909:
                raise Exception(
                    "An error has occured. The full 1909 rows were not produced in merge."
                )
        elif res == "LA":
            if key_is_code:
                key = "lad19cd"
            else:
                key = "lad19nm"
            # Change the key column depending on the argument
            df_tidy = LA[["lad19cd", "lad19nm"]].merge(df[keep_cols], on=key,
                                                       how="inner")
            # Check the df has the expected number of rows after merging
            if df_tidy.shape[0] != 22:
                raise Exception(
                    "An error has occured. The full 22 rows were not produced in merge."
                )
        else:
            raise ValueError("Res provided does not match 'LSOA' or 'LA")

        return df_tidy

    def clean_bracketed_data(self):
        """For a df with columns in the format 'NUMBER (PERCENTAGE)' this function extracts the
        data into two new columns and deletes the original column.

        Arguments:
            df {pd.DataFrame} -- DataFrame containing 'cols'
            cols {list} -- list of cols where data needs extracting

        Returns:
            df {pd.DataFrame} -- DataFrame with each col replaced by two new cols.
        """

        df = self.std_data_
        cols = self.bracketed_data_cols

        # Define the regex pattern and find capture groups
        def extract_data(string):
            pattern = r"\d+.?\d+"
            data = re.findall(pattern, string)
            return data

        for col in cols:
            # Derive the names for the new columns from exitsing names
            name_counts = col + "_count"
            name_percent = col + "_pct"
            # Apply the extract_data function to each line, and the data to two new columns
            df[name_counts] = df[col].apply(lambda x: extract_data(x)[0])
            df[name_percent] = df[col].apply(lambda x: extract_data(x)[1])
            df.drop(columns=col, inplace=True)

        return df

    def write(self):
        """Writes a df to csv in the cleaned folder, using naming convention of
        resolution_name.csv. If name already exists it will not write to path.

        Arguments:
            df {pd.DataFrame} -- df to write
            res {str} -- resolution of the df data ('LA' or 'LSOA')
            csv_name {str} -- name of the data to include in path.
        """
        # create the desired path
        csv_path = os.path.join("cleaned",
                                '{res}_{name}.csv'.format(res=self.res,
                                                          name=self.csv_name))

        # if a file already exists on this path, alert user
        # WARNING warning.warn
        if os.path.isfile(csv_path):
            print("This file already exists. Please delete if new copy needed.")
        else:
            self.data.to_csv(csv_path, index=False)
            print("File written to " + csv_path)


# ++++++++++++++++++++++++++++++++++++++
# Define each instance of the dataclass
# ++++++++++++++++++++++++++++++++++++++

LSOA_WELSH = StandardiseData(
    data=s.SOURCE_WELSH_LSOA,
    res="LSOA",
    key_col="Unnamed: 2",
    key_is_code=True,
    csv_name="welsh_speakers_percent",
    rename={"Percentage able to speak Welsh ": "welsh_speakers_percent"},
)

LA_WELSH = StandardiseData(
    data=s.SOURCE_WELSH_LA,
    res="LA",
    key_col="Unnamed: 1",
    key_is_code=False,
    csv_name="welsh_speakers_percent",
    rename={
        "Daily ": "welsh_daily_percent",
        "Weekly ": "welsh_weekly_percent",
        "Less Often ": "welsh_lessoften_percent",
    },
)

LSOA_POPULATION = StandardiseData(
    data=s.SOURCE_POPDENSITY_LSOA,
    res="LSOA",
    key_col="Area Codes",
    key_is_code=True,
    csv_name="population_count",
    rename={"All Ages": "population_count"},
)

LA_POPULATION = StandardiseData(
    data=s.SOURCE_POPULATION_LA,
    res="LA",
    key_col="Unnamed: 3",
    key_is_code=False,
    csv_name="population_count",
    rename={"All ages .1": "population_count"},
)

LSOA_OVER_65 = StandardiseData(
    data=s.SOURCE_OVER_65_LSOA,
    res="LSOA",
    key_col="Area Codes",
    key_is_code=True,
    csv_name="over_65_count",
)

LA_OVER_65 = StandardiseData(
    data=s.SOURCE_OVER_65_LA,
    res="LA",
    key_col="Unnamed: 3",
    key_is_code=False,
    csv_name="over_65_count",
    rename={"Unnamed: 14": "over_65_count"},
)

LSOA_IMD = StandardiseData(
    data=s.SOURCE_IMD_LSOA,
    res="LSOA",
    key_col="lsoa11cd",
    key_is_code=True,
    csv_name="wimd_2019",
    keep_cols=["LSOA11CD", "wimd_2019"],
)

LA_IMD = StandardiseData(
    data=s.SOURCE_IMD_LA,
    res="LA",
    key_col="Unnamed: 0",
    key_is_code=False,
    csv_name="wimd_2019",
)

LSOA_POPDENSITY = StandardiseData(
    data=s.SOURCE_POPDENSITY_LSOA,
    res="LSOA",
    key_col="Code",
    key_is_code=True,
    rename={"People per Sq Km": "pop_density_persqkm"},
    keep_cols=["LSOA11CD", "pop_density_persqkm"],
    csv_name="pop_density_persqkm",
)

LA_POPDENSITY = StandardiseData(
    data=s.SOURCE_POPDENSITY_LA,
    res="LA",
    key_col="Unnamed: 1",
    key_is_code=False,
    rename={"Mid-year 2018 ": "pop_density_persqkm"},
    csv_name="pop_density_persqkm",
)

LA_VULNERABLE = StandardiseData(
    data=s.SOURCE_VULNERABLE_LA,
    res="LA",
    key_col="index",
    key_is_code=False,
    rename={38: "vulnerable"},
    bracketed_data_cols=["vulnerable"],
    csv_name="vulnerable_count_percent",
)

LA_COHESION = StandardiseData(
    data=s.SOURCE_COMM_COHESION_LA,
    res="LA",
    key_col="index",
    key_is_code=False,
    rename={20: "belong_strongagree", 21: "belong_agree"},
    bracketed_data_cols=["belong_strongagree", "belong_agree"],
    csv_name="comm_cohesion_count_percent",
)

LA_INTERNET_ACCESS = StandardiseData(
    data=s.SOURCE_INTERNET_ACCESS_LA,
    res="LA",
    key_col="Unnamed: 0",
    key_is_code=False,
    rename={"Yes (%)": "has_internet_percent"},
    csv_name="has_internet_percent",
)

LA_INTERNET_USE = StandardiseData(
    data=s.SOURCE_INTERNET_USE_LA,
    res="LA",
    key_col="Unnamed: 0",
    key_is_code=False,
    rename={
        "Several times a day (%)": "use_several_daily_percent",
        "Daily (%) ": "use_daily_percent",
    },
    csv_name="use_internet_percent",
)

LA_ETHNICITY = StandardiseData(
    data=s.SOURCE_ETHNICITY_LA,
    res="LA",
    key_col="Unnamed: 1",
    key_is_code=False,
    csv_name="ethnicities_percent",
)

if __name__ == '__main__':
    lsoa_w = LSOA_WELSH
    print(lsoa_w.data.head())
    input()
    print('STD DAta Is None: ', lsoa_w.standardised_data is None)
    lsoa_w.standardise()
    print('Done')
    input()
    print(lsoa_w.standardised_data.head())

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Apply functions to each dataset, and create new constant
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# WELSH_LSOA = clean_data(LSOA_WELSH) -> WELSH_LSOA.standardise()
# WELSH_LA = clean_data(LA_WELSH)
# POPULATION_LSOA = clean_data(LSOA_POPDENSITY)
# POPULATION_LA = clean_data(LA_POPULATION)
# OVER_65_LSOA = clean_data(LSOA_OVER_65)
# OVER_65_LA = clean_data(LA_OVER_65)
# IMD_LSOA = clean_data(LSOA_IMD)
# IMD_LA = clean_data(LA_IMD)
# POPDENSITY_LSOA = clean_data(LSOA_POPDENSITY)
# POPDENSITY_LA = clean_data(LA_POPDENSITY)
# VULNERABLE_LA = clean_data(LA_VULNERABLE)
# COMM_COHESION_LA = clean_data(LA_COHESION)
# INTERNET_ACCESS_LA = clean_data(LA_INTERNET_ACCESS)
# INTERNET_USE_LA = clean_data(LA_INTERNET_USE)
# ETHNICITY_LA = clean_data(LA_ETHNICITY)
