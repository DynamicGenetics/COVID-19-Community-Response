import os

from .dataset import LA_COUNT, LSOA_COUNT

BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))
SOURCE_DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "static", "source")
GEO_DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "static", "geoboundaries")
LIVE_DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "live", "cleaned")
LIVE_RAW_DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "live", "raw")
