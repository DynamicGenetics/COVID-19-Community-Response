import pandas as pd
import geopandas as gpd

# This script uses Chris' demographics.csv to generate an LA look up table
# that we can use for the geographical location attribution for tweets.

# Create a version of the static demographics file that we can join with LA data
la_demog = pd.read_csv("../data/static/demographics/demographics.csv")

# Local Authorities Geoobjects
la_geo = gpd.read_file("../data/boundaries_LAs.geoJSON")

# Merge these to get a geopandas dataframe with population and lhb information
LA_key = pd.merge(
    la_geo,
    la_demog[["id_area", "pop", "lhb"]],
    left_on="lad18cd",
    right_on="id_area",
    how="left",
)

# Population should be an int, not a string.
LA_key["pop"] = LA_key["pop"].str.replace(",", "").astype(int)

# Get rid of the (no longer needed) 'id_area' col - it's a duplicate of lad18cd
del LA_key["id_area"]
