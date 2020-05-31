"""Generates gp_online.csv

 Functions contained in this module take data of patients registered with My Health Online from local
 data folders. The `gp_to_area` function matches each GP practice to a postcode, and then matches that
 postcode to a Local Authority, Lower Super Output Area and Middle Super Output Area.

 The `mhol_to_percentage` function then calculates the overall percentage of patients registered online
 at the area level chosen.

 To run, these functions require local data that is not published in the repository.

"""

import pandas as pd
import numpy as np
import os

# ------------------
# Read in the data
# ------------------

from datasets import SOURCE_DATA_FOLDER
from .dataset import DataResolution


GP_DATA = pd.read_excel(
    os.path.join(SOURCE_DATA_FOLDER, "local", "Digital Exclusion sources.xlsx"),
    sheet_name="Pts Registered with MHOL",
    use_cols=["A", "C", "E:G"],
    skiprows=1,
    na_filter=False,
)
POSTCODES = pd.read_csv(
    os.path.join(SOURCE_DATA_FOLDER, "local", "PCD_OA_LSOA_MSOA_LAD_FEB19_UK_LU.csv"),
    encoding="ISO-8859-1",
    usecols=[2, 7, 8, 9, 10, 11, 12],  # Only include relevant cols
)
GP_LOOKUP = pd.read_csv(
    os.path.join(SOURCE_DATA_FOLDER, "local", "epraccur.csv"),
    usecols=[0, 9],
    names=["practice_ID", "postcode"],
)

# -----------------
# Define functions
# -----------------


def gp_to_area(gp_data, postcode_lookup, gp_lookup):
    """Using data and lookup tables, generates a new dataframe with the LA and LSOA
    matched to each GP practice code.

    Parameters
    ----------
    gp_data : pd.DataFrame
        Data on number of patients per GP practice. Should contain cols `GP Practice Code`,
        `MHOL patient count`, `Patients (2019)`.
    postcode_lookup : pd.DataFrame
        A df with a column of postcodes (`pscds`) and columns matching each postcode to an
        LSOA, LA and MSOA area.
    gp_lookup : pd.DataFrame
        A df with a column of GP practice IDs (`practice_ID`) and postcodes (`postcode`).

    Returns
    -------
    pd.DataFrame
        A df where each row is a GP practice matched to a postcode, LA, LSOA and MSOA, along
        with associated data columns from `gp_data`.
    """

    # Merge to get postcode for each GP
    gp_postcodes = pd.merge(
        gp_data,
        gp_lookup,
        how="left",
        left_on="GP Practice Code",
        right_on="practice_ID",
    )

    # Merge to get LSOA and LA for each GP
    gp_areas = pd.merge(
        gp_postcodes, postcode_lookup, how="left", left_on="postcode", right_on="pcds"
    )

    gp_areas.rename(
        columns={
            "Unnamed: 2": "GP_name",
            "MHOL patient count": "MHOL_true",
            "Patients (2019)": "patients_total",
        },
        inplace=True,
    )

    return gp_areas


def mhol_to_pct(df, res: DataResolution):
    """For a dataframe with rows of each GP practice mapped to LA or LSOA codes and names,
    sums "patients_total" and "MHOL_true" across area, and creates new col with total percentage
    over each LA.

    Parameters
    ----------
    df : pd.DataFrame
        Each row is a unique GP practice with an area code and name, and
         `patients_total` and `MHOL_true` columns.
    res : DataResolution, optional
        The area resolution of the data, specified using the DataResolution class that is imported
        from the `dataset` module. By default DataResolution.LA

    Returns
    -------
    pd.DataFrame
        Returns df with rows as each area with sum of "patients_total",
        "MHOL_true" and new col "MHOL_pct" which is the percentage of MHOL_true out of patients_total.
    """

    # Now create the datasets we need for mapping
    if res == DataResolution.MSOA:
        df_counts = pd.pivot_table(
            df,
            values=["patients_total", "MHOL_true"],
            index=["msoa11cd", "msoa11nm"],
            aggfunc=np.sum,
        )
    elif res == DataResolution.LSOA:  # Assume this means it is LA
        df_counts = pd.pivot_table(
            df,
            values=["patients_total", "MHOL_true"],
            index=["lsoa11cd", "lsoa11nm"],
            aggfunc=np.sum,
        )
    # DataResolution.LA:
    else:
        df_counts = pd.pivot_table(
            df,
            values=["patients_total", "MHOL_true"],
            index=["ladcd", "ladnm"],
            aggfunc=np.sum,
        )

    # Create new percentage column
    df_counts["MHOL_pct"] = (df_counts["MHOL_true"] / df_counts["patients_total"]) * 100

    return df_counts


GP_AREAS = gp_to_area(GP_DATA, POSTCODES, GP_LOOKUP)
LA_COUNTS = mhol_to_pct(GP_AREAS, DataResolution.LA)
LSOA_COUNTS = mhol_to_pct(GP_AREAS, DataResolution.LSOA)
MSOA_COUNTS = mhol_to_pct(GP_AREAS, DataResolution.MSOA)


LA_COUNTS.to_csv(os.path.join(SOURCE_DATA_FOLDER, "la_gp_online.csv"))
LSOA_COUNTS.to_csv(os.path.join(SOURCE_DATA_FOLDER, "lsoa_gp_online.csv"))
MSOA_COUNTS.to_csv(os.path.join(SOURCE_DATA_FOLDER, "msoa_gp_online.csv"))
