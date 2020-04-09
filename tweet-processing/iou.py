# https://stackoverflow.com/questions/58435218/intersection-over-union-on-non-rectangular-quadrilaterals

#Example function from stackoverflow above

from shapely.geometry import box, Polygon
import geopandas as gpd
from tweet_functions import read_and_tidy, format_bbox
import json


# Local Authorities Geoobjects
la = gpd.read_file('../data/boundaries/LA_boundaries_2019.geojson')
# Subset for Welsh LAs
la = la[la["lad19cd"].str.contains("W")]

# Read in tweets
tweets = read_and_tidy('../../data/nina_7apr.csv')
# Fix the bounding boxes in the dataframe. 
tweets = format_bbox(tweets)

#Lets try taking the first bounding box in the twitter dataset


pl1 = 
pl2 

# Define Each polygon 
pol1_xy = [[130, 27], [129.52, 27], [129.45, 27.1], [130.13, 26]]
pol2_xy = [[30, 27.200001], [129.52, 27.34], [129.45, 27.1], [130.13, 26.950001]]
polygon1_shape = Polygon(pol1_xy)
polygon2_shape = Polygon(pol2_xy)

# Calculate Intersection and union, and tne IOU
polygon_intersection = polygon1_shape.intersection(polygon2_shape).area
polygon_union = polygon1_shape.union(polygon2_shape).area
IOU = polygon_intersection / polygon_union 



