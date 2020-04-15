# %%
import pandas as pd
from shapely.geometry import Polygon


# %%
def get_laoi(bbox_tweet, la, only_top=False):
    """ Get the likelihood for the the Local Authorities that
    overlap with the bounding box. Requires 'geometry' col in LA geopandas df. 
    Returns df of local authorities of interest. """

    if not isinstance(bbox_tweet, Polygon):
        bbox_tweet = Polygon(bbox_tweet)

    # Local Authorities of Interest are those that overlap with the bbox
    laoi = la[la['geometry'].intersects(bbox_tweet)].copy()

    if laoi.shape[0] == 0:
        if only_top:
            return ('', '', '')
        return None

    # Intersection over the union is a measure of how exactly the bounding box and the la overlap
    laoi['iou'] = la['geometry'].apply(lambda g: g.intersection(
        bbox_tweet).area / g.union(bbox_tweet).area)
    # Pop weight is the proportion of the la population covered by the bounding box.
    laoi['pop_weight'] = laoi['geometry'].apply(lambda g: (
        g.intersection(bbox_tweet).area / g.area)) * laoi['pop']

    # The final likelihood is the IoU multiplied by the population weight
    laoi['likelihood'] = laoi['iou'] * laoi['pop_weight']

    if not only_top:
        return laoi

    laoi = laoi.sort_values(by='likelihood', ascending=False)
    return laoi['lad18nm'].iat[0], laoi['lad18cd'].iat[0], laoi['lhb'].iat[0]


# %% 
def get_tweets_loc(tweets_df, la):
    """ Choose LA with highest likelihood. Add LA and LHB to tweets_dfset. """

    # Get a list of the required values from the first row of sorted tweets_dfframe. 
    def laoi_classes(bbox_tweet):

        laoi = get_laoi(bbox_tweet, la)

        if laoi is None:
            return pd.Series(['', '', ''])
        
        #Sort tweets_dfframe by highest to lowest 
        laoi = laoi.sort_values(by='likelihood', ascending=False)

        # laoi = laoi.reset_index()
        
        classes = [laoi['lad18nm'].iat[0], laoi['lad18cd'].iat[0], laoi['lhb'][0]]
        
        return pd.Series(classes)

    #tweets_df[['lad18nm', 'lad18cd', 'lhb']] = tweets_df['bbox_shapely'].apply(laoi_classes)
    tweets_df['lad18nm'], tweets_df['lad18cd'], tweets_df['lhb']  = tweets_df['bbox_shapely'].apply(laoi_classes)

    return tweets_df


# %%
# In progress - how to define how certain the match is
def class_uncertainty(laoi):

    """ Roughly calculate how certain the classification is based on distances between
    the likelihood of the potentially overlapping LA boundaries. """
   
    #Sort tweets_dfframe by highest to lowest 
    laoi = laoi.sort_values(by='likelihood', ascending=False)
    # Get the list of values
    a = laoi['likelihood']
    a.reset_index().drop()
    del a['index']

    #If there was only one, the  
    if len(a) == 1 :
        return 1
    elif len(a) == 2 :
        return 'only two' # decide penalty function
    else: 
        # Get the difference between each sequential number
        b = a.diff(periods=-1)
        # Divide the distance between the first and second number by the 
        b['likelihood'][0] / b[1:].mean()

# %%
