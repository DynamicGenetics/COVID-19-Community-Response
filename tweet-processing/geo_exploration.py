import pandas as pd
import re
from tweet_functions import *
import json
import geojson

###################
# DATASET TIDYING #
###################

# Read in export from the Virtual Box VM (~420k tweets)
tweets = read_and_tidy('../../data/nina_7apr.csv')

###############
# EXPLORATION #
###############

tweets = tweets[tweets['geo.coordinates'].notnull()]

tweets = split_coords(tweets, 'geo.coordinates')
