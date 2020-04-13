from shapely.geometry import box, Polygon
from tweet_functions import read_and_tidy, format_bbox
from tweet_geo_functions import get_tweets_loc
import geopandas as gpd
import pandas as pd
import json

# Read in tweets
tweets = read_and_tidy('../../data/nina_7apr.csv')

# Read in lsoa key
la = gpd.read_file('lsoa_key.geojson')

# Correctly format the bounding boxes in the dataframe. 
tweets = format_bbox(tweets)

# Make a new column with the bounding boxes and shapely objects
tweets['bbox_shapely'] = tweets['place.bounding_box.coordinates'].apply(lambda x: Polygon(x[0]))

bbox_tweet = tweets['bbox_shapely'][0] # Take first tweet in the bbox_shapely col

#laoi_example = get_laoi(bbox_tweet, la)

tweets2 = get_tweets_loc(tweets, la)