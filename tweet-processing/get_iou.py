from shapely.geometry import box, Polygon
from tweet_functions import read_and_tidy, format_bbox
from tweet_geo_functions import get_tweets_loc
import geopandas as gpd
import pandas as pd
import json

# Read in tweets
tweets = read_and_tidy('../../data/nina_7apr.csv')
# Correctly format the bounding boxes in the dataframe. 
tweets = format_bbox(tweets)
# Make a new column with the bounding boxes and shapely objects
tweets['bbox_shapely'] = tweets['place.bounding_box.coordinates'].apply(lambda x: Polygon(x[0]))
# Write processed df to pkl for quicker reading in future 
#pd.to_pickle(tweets, './processed_tweets.pkl')

# Alternative read in from pkl. 
tweets = pd.read_pickle('../../data/processed_tweets.pkl')

## TESTING - create a smaller tweets df with one row per unique bounding box
# NB this retains the first occurence of each place name. 
tweets_sm = tweets[~tweets.duplicated(subset='place.full_name')].copy()

# Read in lsoa key
la = gpd.read_file('lsoa_key.geojson')

# Run 
tweets2 = get_tweets_loc(tweets_sm, la)

### Useful lines for testing

## Trying with a single bbox to check it works
# bbox_tweet = tweets['bbox_shapely'][0] # Take first tweet in the bbox_shapely col
#laoi_example = get_laoi(bbox_tweet, la)