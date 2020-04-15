
# %%
from shapely.geometry import box, Polygon
from tweet_functions import read_and_tidy, format_bbox
from tweet_geo_functions import get_tweets_loc
import geopandas as gpd
import pandas as pd
import json

# %%
# Read in tweets
tweets = read_and_tidy('../../data/nina_7apr.csv')

# Read in LA key
la = gpd.read_file('LA_key.geojson')
tweets = read_and_tidy('../data/local/full_export_nina_7apr.csv')

# %%
# Correctly format the bounding boxes in the dataframe. 
tweets = format_bbox(tweets)

# %%
# Make a new column with the bounding boxes and shapely objects
tweets['bbox_shapely'] = tweets['place.bounding_box.coordinates'].apply(lambda x: Polygon(x[0]))

# %%
tweets['bbox'] = tweets['bbox_geojson'].apply(lambda c: tuple(map(tuple, c[0][:-1])))

# %%
# Write processed df to pkl for quicker reading in future 
pd.to_pickle(tweets, '../data/local/processed_tweets.pkl')

# %%
# Alternative read in from pkl. 
tweets = pd.read_pickle('../data/local/processed_tweets.pkl')

# # %%
# ## TESTING - create a smaller tweets df with one row per unique bounding box
# # NB this retains the first occurence of each place name. 
# tweets_sm = tweets[~tweets.duplicated(subset='place.full_name')].copy()

# %%
# Read in lsoa key
la = gpd.read_file('lsoa_key.geojson')

# %%
# Collect Unique Coordinates
unique_coords = set(tweets['bbox'].values)


# %%
from functools import partial
from tweet_geo_functions import get_laoi

fetch_laoi = partial(get_laoi, la=la, only_top=True)
laoi_map = {coords: fetch_laoi(coords) for coords in unique_coords}


# %%
# Mapping bbox to laoi
tweets['lad18nm'], tweets['lad18cd'], tweets['lhb'] = tweets['bbox'].apply(lambda c: laoi_map[c])

# %%
# Run 
tweets2 = get_tweets_loc(tweets_sm, la)

### Useful lines for testing

## Trying with a single bbox to check it works
# bbox_tweet = tweets['bbox_shapely'][0] # Take first tweet in the bbox_shapely col
#laoi_example = get_laoi(bbox_tweet, la)