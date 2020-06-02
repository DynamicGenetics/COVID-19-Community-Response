import os
import geopandas as gpd

BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))
SOURCE_DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "static", "source")
GEO_DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "static", "geoboundaries")
LIVE_DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "live", "cleaned")
LIVE_RAW_DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "live", "raw")

LA_BOUNDARIES = gpd.read_file(
    os.path.join(
        GEO_DATA_FOLDER,
        "Local_Authority_Districts_(December_2019)_Boundaries_UK_BGC.geojson",
    )
)
LSOA_BOUNDARIES = gpd.read_file(
    os.path.join(
        GEO_DATA_FOLDER,
        "Lower_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BSC.geojson",
    )
)
