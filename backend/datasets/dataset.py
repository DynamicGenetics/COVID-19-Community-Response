"""Dataset Classes"""

# Import packages
import pandas as pd
import geopandas as gpd
import re
import os
from warnings import warn
from dataclasses import dataclass
from dataclasses import field
from typing import List
from enum import Enum
from functools import reduce

import datasets


class DataResolution(Enum):
    LA = "LA"
    LSOA = "LSOA"


class DataFrequency(Enum):
    LIVE = "live"
    STATIC = "static"


@dataclass
class Dataset:
    """
    Class to handle transformations to source datasets, returning them
    as a pd.DataFrame in a standardised format.
    """

    data: pd.DataFrame
    res: DataResolution  # Resolution at 'LSOA' or 'LA'
    key_col: str  # Name of the column that has a unique key
    key_is_code: bool  # Is the key column a LA or LSOA code?
    csv_name: str  # Name for the output CSV
    keep_cols: list = None  # List of columns specifically wanted to keep
    bracketed_data_cols: list = None  # List of columns where data is in the format (DATA (PERCENT))
    rename: dict = None  # Dictionary of columns that need renaming Cleaningself('old_name' : 'new_name' }
    std_data_: pd.DataFrame = field(init=False, default=None)

    def standardise(self):
        """

        Returns
        -------

        """
        """ Based on arguments provided, applies the correct functions to standardise the datasets.
        """

        # Validate step TBD

        # Filter the keycodes/names, remove whitespace, reset index
        self.std_data_ = self.clean_keys(
            df=self.data,
            res=self.res,
            key_col=self.key_col,
            key_is_code=self.key_is_code,
        )

        # Rename the columns as needed
        if self.rename:
            self.std_data_.rename(columns=self.rename, inplace=True)

        # Merge against the LSOA dataset for consistent Codes and Names
        self.std_data_ = self.standardise_keys()

        # If argument has been passed for bracketed_data_cols, then apply the function.
        if self.bracketed_data_cols:
            self.std_data_ = self.clean_bracketed_data()

        # Lastly, fill NA values with 0
        self.std_data_.fillna(0, inplace=True)

        # Write out to /cleaned
        # write_cleaned_data(df, res=self.res, csv_name=self.csv_name)
        return self

    @property
    def standardised_data(self):
        return self.std_data_

    @property
    def is_standardised(self):
        return self.std_data_ is not None

    def csv_path(self):
        return os.path.join(
            "cleaned", "{res}_{name}.csv".format(res=self.res, name=self.csv_name)
        )

    def _merge_key(self):

        if self.res == DataResolution.LA:
            return "lad19cd"
        elif self.res == DataResolution.LSOA:
            return "LSOA11CD"
        else:
            raise TypeError("Unsupported Resolution")

    def __add__(self, other):

        if not isinstance(other, Dataset):
            raise TypeError(
                "unsupported operand type(s) for +: {} and {}",
                self.__class__,
                type(other),
            )

        if not self.is_standardised or not other.is_standardised:
            raise TypeError(
                "Unsupported operand: both dataset needs to be "
                "standardised before merging!"
            )

        if self.res != other.res:
            raise TypeError(
                "Unsupported operand: both dataset needs to be "
                "at the same resolution!"
            )

        merge_key = self._merge_key()
        self.std_data_ = pd.merge(
            self.std_data_,
            other.standardised_data,
            on=merge_key,
            left_index=True,
            right_index=True,
        )
        return self

    def read_keys(self):
        """ Reads in and returns the LSOA and LA geopandas dataframes as LSOA, LA. """

        # TBD: Standardise for GeoPandas DataFrame
        # MAKE THIS A CLASS ATTRIBUTE

        data_folder = datasets.GEO_DATA_FOLDER
        # Read data
        LSOA = gpd.read_file(
            os.path.join(
                data_folder,
                "Lower_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BSC.geojson",
            )
        )
        LA = gpd.read_file(
            os.path.join(
                data_folder,
                "Local_Authority_Districts_(December_2019)_Boundaries_UK_BGC.geojson",
            )
        )

        try:
            LSOA = self.clean_keys(LSOA, res=DataResolution.LSOA, key_col="LSOA11CD")
            LA = self.clean_keys(LA, res=DataResolution.LA, key_col="lad19cd")
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
        # if not isinstance(res, str):
        #     raise TypeError("Arg 'res' should be 'LA' or 'LSOA' as string")

        # For instances where the key column is a code (preferred)
        if key_is_code:
            # This will drop non Welsh LSOAs, and drop NAs.
            df_new = df[df[key_col].str.contains("W", na=False)].copy()
        else:
            # Assumes this means key is a name
            df_new = df.dropna(subset=[key_col])
        df_new.reset_index(drop=True, inplace=True)

        # Strip surrounding whitespace if there is any.
        df_new[key_col] = df_new[key_col].apply(lambda x: x.strip()).copy()

        # If the column-name doesn't match the standard keyname, change it to that
        if res == DataResolution.LA:
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
                    "An error has occurred. There are not the expected 22 rows."
                )
        elif res == DataResolution.LSOA:
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
        if res == DataResolution.LSOA:
            df_tidy = LSOA[["LSOA11CD", "LSOA11NM"]].merge(
                df[keep_cols], on="LSOA11CD", how="inner"
            )
            # Check the df has the expected number of rows after merging
            if df_tidy.shape[0] != 1909:
                raise Exception(
                    "An error has occured. The full 1909 rows were not produced in merge."
                )
        elif res == DataResolution.LA:
            if key_is_code:
                key = "lad19cd"
            else:
                key = "lad19nm"
            # Change the key column depending on the argument
            df_tidy = LA[["lad19cd", "lad19nm"]].merge(
                df[keep_cols], on=key, how="inner"
            )
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
        if not self.is_standardised:
            raise ValueError("Dataset requires to be standardised first")

        # if a file already exists on this path, alert user
        # WARNING warning.warn
        if os.path.isfile(self.csv_path()):
            print("This file already exists. Please delete if new copy needed.")
        else:
            self.std_data_.to_csv(self.csv_path(), index=False)
            print("File written to " + self.csv_path())


@dataclass
class MasterDataset:
    """ Used to call or generate the merged 'master' dataset used
    to write to json. Can be used to generate the 'live' or 'static'
    master datasets. Will write out to csv if it does not already exist,
    or if user chooses 'from_csv' to be False.
    """

    datasets: List[Dataset]
    res: DataResolution  # Resolution at 'LSOA' or 'LA'
    freq: DataFrequency  # 'live' or 'static'
    from_csv: bool = True  # Is it ok to read the dataset from csv, if it exists?
    master_dataset_: pd.DataFrame = field(init=False, default=None)

    @property
    def file_path(self):
        filename = self.res.value + "_" + self.freq.value + "_master.csv"
        filepath = os.path.join(datasets.BASE_FOLDER, "data", self.freq.name, filename)
        return filepath

    @property
    def master_dataset(self):
        if self.master_dataset_ is not None:
            return self.master_dataset_
        else:
            self._set_master_dataset()
        return self.master_dataset_

    def _set_master_dataset(self):
        """Either sets previous master dataset from csv, or generates new one
        if not found or user requested 'from_csv' as False."""
        if self.from_csv:
            try:
                self.master_dataset_ = pd.read_csv(self.file_path)
                warn(
                    """Master dataset was read from path: {}. If new variables need to be added
                then add 'from_csv=False' to create a new version.""".format(
                        self.file_path
                    )
                )
                # Set the index in the pandas dataframe
                self.master_dataset_.set_index(["area_code", "area_name"], inplace=True)
            except FileNotFoundError:
                self._create_master_dataset()
                self.write(self.master_dataset_, self.file_path)
        else:
            self._create_master_dataset()
            self.write(self.master_dataset_, self.file_path)

        return self.master_dataset_

    def _create_master_dataset(self):
        """Applies transformations to variables and sets
        master dataset attribute as a pd.DataFrame """

        # Instatiate full dataset by merging all the data sources
        data = self._merge_datasets()
        data = data.astype("float64")
        if self.freq == DataFrequency.STATIC:
            if self.res == DataResolution.LA:
                data = self._create_welsh_col(data)
                data = self._create_wimd_col(data)
                data = self._create_belonging_col(data)
            elif self.res == DataResolution.LSOA:
                data = self._create_over_65_col(data)
        elif self.freq == DataFrequency.LIVE:
            if self.res == DataResolution.LA:
                data = self._create_vol_increase_col(data)
        # Currently no live lsoa level data to manage
        self.master_dataset_ = data
        return self

    def _merge_datasets(self):
        """Given the list of datasets, merges them into one dataframe"""

        # First, standardise all the datasets
        datasets = map(lambda d: d.standardise(), self.datasets)
        datasets = map(lambda d: d.standardised_data, datasets)

        if self.res == DataResolution.LSOA:
            datasets = map(
                lambda d: d.set_index(["LSOA11CD", "LSOA11NM"]), list(datasets),
            )
        elif self.res == DataResolution.LA:
            datasets = map(
                lambda d: d.set_index(["lad19cd", "lad19nm"]), list(datasets),
            )

        # Merge all the datasets into one dataframe called data
        data = reduce(
            lambda left, right: pd.merge(
                left, right, left_index=True, right_index=True
            ),
            datasets,
        )
        # Make the naming of the index cols consistent
        data.rename_axis(
            index={
                "LSOA11CD": "area_code",
                "LSOA11NM": "area_name",
                "lad19cd": "area_code",
                "lad19nm": "area_name",
            },
            inplace=True,
        )

        if self.res == DataResolution.LA:
            if data.shape[0] != 22:
                raise Exception(
                    "An error has occured. There are not the expected 22 rows in the LA dataset."
                )
        elif self.res == DataResolution.LSOA:
            if data.shape[0] != 1909:
                raise Exception(
                    "An error has occured. There are not the expected 1909 rows in the LA dataset."
                )
        return data

    @staticmethod
    def _create_over_65_col(data):
        """Create a new over_65 column in the LSOA master and drop the redundant columns.
        """
        # Crate new 'over 65' variable for the population data (adding up all
        # singlar age cols from 65:90+)
        age_cols = data.columns[
            pd.to_numeric(data.columns, errors="coerce").to_series().notnull()
        ]
        data["over_65_count"] = data[age_cols].sum(axis=1) + data["90+"]
        # Set dtype to int
        data.drop(columns=age_cols, inplace=True)
        data.drop(columns="90+", inplace=True)
        return data

    @staticmethod
    def _create_welsh_col(data):
        """Sums welsh speaking frequency to create overall welsh speaking column, and drop redundant columns.
        """
        # Get the sum of the people who do use Welsh at all
        welsh_cols = [
            "welsh_daily_percent",
            "welsh_weekly_percent",
            "welsh_lessoften_percent",
        ]
        data["welsh_speakers_percent"] = data[welsh_cols].sum(axis=1)
        data.drop(columns=welsh_cols, inplace=True)
        return data

    @staticmethod
    def _create_summary_ethnicity_cols(data):
        """Sum ethnicity percentages by top level group, and drop redundant columns."""

        # Create summary ethnicity columns by summing groups
        data["eth_white_percent"] = data.filter(regex=("^White")).sum(axis=1)
        data["eth_asian_percent"] = data.filter(regex=("^Asian")).sum(axis=1)
        data["eth_black_percent"] = data.filter(regex=("^Black")).sum(axis=1)
        data["eth_mixed_percent"] = data.filter(regex=("^Mixed")).sum(axis=1)
        data["eth_other_percent"] = data.filter(regex=("^Other")).sum(axis=1)

        # Drop redundant columns
        ethnicity_cols = data.filter(
            regex=("^White|^Asian|^Black|^Mixed|^Other")
        ).columns
        data.drop(columns=ethnicity_cols, inplace=True)

        return data

    @staticmethod
    def _create_wimd_col(data):
        """Generate a column for IMD and drop redundant columns.
        """
        imd_cols = data.filter(regex=("LSOAs")).columns
        # What percentage of LSOAs in this LA are from the top 20% most deprived in Wales?
        data["wimd_2019"] = (data[imd_cols[2]] / data[imd_cols[0]]) * 100
        data.drop(columns=imd_cols, inplace=True)

        return data

    @staticmethod
    def _create_belonging_col(data):
        """Sum percentages for feelings of belonging, to create summary col. Drop redundant cols"""
        # For now, just keep the percentage of people who feel they belong
        belonging_cols = data.filter(regex=("belong")).columns
        data["belong_percent"] = pd.to_numeric(
            data["belong_agree_pct"]
        ) + pd.to_numeric(data["belong_strongagree_pct"])
        data.drop(columns=belonging_cols, inplace=True)

        return data

    @staticmethod
    def _create_vol_increase_col(data):
        """Create col for proportional percentage increase in volunteers"""

        total = data["total_vol_count"]
        new = data["new_vol_count"]

        # Proportional increase in volunteers is:
        data["vol_increase_pct"] = 100 * (new / (total - new))

        return data

    @staticmethod
    def write(data, filepath):
        data.to_csv(filepath)
