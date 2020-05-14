import os
from .dataset import *

BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))
SOURCE_DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "static", "source")
GEO_DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "static", "geoboundaries")
