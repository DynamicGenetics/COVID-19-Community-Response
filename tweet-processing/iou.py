# https://stackoverflow.com/questions/58435218/intersection-over-union-on-non-rectangular-quadrilaterals

#Example function from stackoverflow above

from shapely.geometry import box, Polygon
import geopandas as gpd
from tweet_functions import read_and_tidy, format_bbox
import json
import matplotlib.pyplot as plt

# Local Authorities Geoobjects
la = gpd.read_file('../data/boundaries/LA_boundaries_2019.geojson')
# Subset for Welsh LAs
la = la[la["lad19cd"].str.contains("W")]

# Read in tweets
tweets = read_and_tidy('../../data/nina_7apr.csv')

# Correctly format the bounding boxes in the dataframe. 
tweets = format_bbox(tweets)

#Make a new column with the bounding boxes and shapely objects
tweets['bbox_shapely'] = tweets['place.bounding_box.coordinates'].apply(lambda x: Polygon(x[0]))

tweets_invalid = tweets[tweets['isvalid'] == 0]

geo_tweets = gpd.GeoDataFrame(geometry=Polygon(tweets['bbox_geojson'][0]))

# Lets try taking the first bounding box in the twitter dataset
# NB with this dataset, I know that it's Cardiff, so let's test!
bbox_tweet = tweets['bbox_shapely'][0] # Need to apply this to all the tweets
bbox_la = la.loc[la['lad19nm'] == 'Cardiff']['geometry']

#Local Authorities of Interest are those that overlap with the bbox
laoi = la[la['geometry']overlaps(bbox_tweet)].copy()
laoi['iou'] = la['geometry'].apply(lambda g: g.intersection(bbox_tweet).area / g.union(bbox_tweet).area)



# Need to write a function and run it on every tweet. 
# Take the maximum for each and write it to a new column. 
