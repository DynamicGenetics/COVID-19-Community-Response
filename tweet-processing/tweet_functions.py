#####################################
# USEFUL TWEET PROCESSING FUNCTIONS #
#####################################

import pandas as pd
from datetime import datetime
import json
import geojson

###############################
# Dataframe tidying functions #
###############################

def read_and_tidy(file):

    """ Given a csv file of tweets, will import into a pd.df, filer for Welsh tweets, tidy the text columns,
    and create a datetime index. """
    
    # Read in the data
    data = pd.read_csv(file)
    print("I have read the data")
    # Call other functions in sequence
    data = get_welsh_tweets(data)
    print("I have filtered out non-Welsh tweets")
    data = create_datetime_index(data)
    print("I have made the index the tweet datetime")
    data = tidy_text_cols(data)
    print("I have combined the extended text into 'text'")
    return data


def get_welsh_tweets(data, col='place.full_name'):
    """ Filters dataframe to only include tweets from Wales, by querying on column with place.full_name ('col'). """

    # Filter out non-Wales tweets
    data = data[data[col].str.contains('Wales', regex=False, na=False)]

    return data


def create_datetime_index(data):
    """ Using the 'created_at' column from a Twitter export, makes this the index column in a pandas datetime format. """

    # Parse 'created at' to pandas datetime - requires 'from datetime import datetime'
    data['created_at'] = pd.to_datetime(data['created_at'])

    # Set the datetime of tweet creation as the dataframe index
    data.index = data['created_at']

    #Delete unneeded column
    del data['created_at']

    return data


def tidy_text_cols(data):
    """ Uses values from the short ('text') and extended ('extended_tweet.full_text') columns to make a single 'text' column with the
    full version of every tweet. """

    # Keep the data for where 'tweet_full' is not used
    keep = pd.isnull(data['extended_tweet.full_text'])

    # Where tweet_full is used, make tweet_full as the text
    data_valid = data[~keep]
    data.loc[~keep, 'text'] = data_valid['extended_tweet.full_text']

    del data['extended_tweet.full_text']

    return data


##############################
# Textual Analysis Functions #
##############################

def analyse_sentiment(data, col='text'):
    """ Given a Pandas dataframe with col 'tweet_text', this will apply the vaderSentiment dictionary
     in a new column called 'vader'. """

    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    #define the sentiment analyser object
    analyser = SentimentIntensityAnalyzer()
    
    # Apply sentiment analysis to the data frame (new col for each)
    data['vader_comp'] = data[col].apply(lambda x: analyser.polarity_scores(x)['compound'])
    data['vader_pos'] = data[col].apply(lambda x: analyser.polarity_scores(x)['pos'])
    data['vader_neg'] = data[col].apply(lambda x: analyser.polarity_scores(x)['neg'])
    data['vader_neu'] = data[col].apply(lambda x: analyser.polarity_scores(x)['neu'])
   
    return data


################################
# Geodata Processing Functions #
################################

def split_coords(data, col='geo.coordinates'):
    
    """ Takes a Pandas dataframe with a column geo.coordinates (col) and adds the lat and long to their own columns
    for easy conversion to geojson. """

    #Split the string on the comma    
    data['long'], data['lat'] = data[col].str.split(',', 1).str

    #Remove the left over square brackets
    data['lat'] = data['lat'].str[:-1]
    data['long'] = data['long'].str[1:]

    return data


def format_bbox(data, col='place.bounding_box.coordinates'):
    
    """ This function will reformat the bounding boxes from strings to lists of lists,
    and will append the first coordinate as the last one to allow for geojson conversion. """

    #Convert the lists from strings to json
    data[col] = data[col].apply(lambda x: json.loads(x))

    # Append the first list to the end of the LOL so the coords make a connected shape
    def append_coords(bbox):
        bbox[0].append(bbox[0][0])
        return bbox

    data['bbox_geojson'] = data[col].apply(lambda x: append_coords(x))

    print("Formatted bounding boxes written to the 'bbox_geojson' column")

    return data


def write_bbox_geojson(data, col='bbox_geojson'):
    
    """ Given a correctly formatted column of bbox polygons, this will convert them to 
    a geojson object, and write it out to a file. """
    
    # Make a Mutlipolygon from the values. 
    features = Feature(geometry=MultiPolygon(data[col].tolist()))

    ## All the other columns used as properties
    #properties = df.drop(['lat', 'lng'], axis=1).to_dict('records')
    ## Add properties to the geo_json
    #feature_collection = FeatureCollection(features=features, properties=properties)

    feature_collection = FeatureCollection(features=features)

    print("Geojson object generated.")

    with open('tweets_bboxes.geojson', 'w', encoding='utf-8') as f:
        json.dump(feature_collection, f, ensure_ascii=False)

    print("Written object to 'tweets_bboxes.geojson'")


