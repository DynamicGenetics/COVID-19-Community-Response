import pandas as pd
import numpy as np
import os

# ------------------
# Read in the data
# ------------------

GP_DATA = pd.read_excel(
    "static/source/local/Digital Exclusion sources.xlsx",
    sheet_name="Pts Registered with MHOL",
    use_cols=["A", "C", "E:G"],
    skiprows=1,
    na_filter=False,
)
POSTCODES = pd.read_csv(
    "static/source/local/PCD_OA_LSOA_MSOA_LAD_FEB19_UK_LU.csv",
    encoding="ISO-8859-1",
    usecols=[2, 7, 8, 9, 10, 11, 12],  # Only include relevant cols
)
GP_LOOKUP = pd.read_csv(
    "static/source/local/epraccur.csv",
    usecols=[0, 9],
    names=["practice_ID", "postcode"],
)

# -----------------
# Define functions
# -----------------


def gp_to_area(gp_data, postcode_lookup, gp_lookup):
    """Using data and lookup tables, generates a new dataframe with the LA and LSOA
    matched to each GP practice.

    Arguments:
        gp_data {pd.DataFrame} -- Data on number of patients per GP practice.
            Should contain cols 'GP Practice Code', 'MHOL patient count', 'Patients (2019)'
        postcode_lookup {pd.DataFrame} -- [description]
        gp_lookup {pd.DataFrame} -- [description]
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


def mhol_to_pct(df, LA: bool = False, LSOA: bool = False, MSOA: bool = False):
    """For a dataframe with rows of each GP practice mapped to LA or LSOA codes and names,
    sums "patients_total" and "MHOL_true", and creates new col with total percenatage over each LA.

    Arguments:
        df {pd.Dataframe} -- Each row is a unique GP practice with an area code and name, and
         "patients_total" and "MHOL_true" columns.

    Returns:
        df_counts {pd.DataFrame} -- Returns rows of each area with sum of "patients_total",
        "MHOL_true" and new col "MHOL_pct" which is the percentage of MHOL_true out of patients_total.
    """

    # Now create the datasets we need for mapping
    if LA:
        df_counts = pd.pivot_table(
            df,
            values=["patients_total", "MHOL_true"],
            index=["ladcd", "ladnm"],
            aggfunc=np.sum,
        )
    if LSOA:  # Assume this means it is LA
        df_counts = pd.pivot_table(
            df,
            values=["patients_total", "MHOL_true"],
            index=["lsoa11cd", "lsoa11nm"],
            aggfunc=np.sum,
        )
    if MSOA:
        df_counts = pd.pivot_table(
            df,
            values=["patients_total", "MHOL_true"],
            index=["msoa11cd", "msoa11nm"],
            aggfunc=np.sum,
        )

    # Create new percentage column
    df_counts["MHOL_pct"] = (df_counts["MHOL_true"] / df_counts["patients_total"]) * 100

    return df_counts


# ------------------------
# Apply functions to data
# ------------------------

GP_AREAS = gp_to_area(GP_DATA, POSTCODES, GP_LOOKUP)
LA_COUNTS = mhol_to_pct(GP_AREAS, LA=True)
LSOA_COUNTS = mhol_to_pct(GP_AREAS, LSOA=True)
MSOA_COUNTS = mhol_to_pct(GP_AREAS, MSOA=True)


LA_COUNTS.to_csv(os.path.join("static", "source", "la_gp_online.csv"))
LSOA_COUNTS.to_csv(os.path.join("static", "source", "lsoa_gp_online.csv"))
MSOA_COUNTS.to_csv(os.path.join("static", "source", "msoa_gp_online.csv"))
