import pandas as pd
import re
import spacy

###################
# DATASET TIDYING #
###################

# Read in export from the Virtual Box VM (~420k tweets)
tweets = pd.read_csv('../../data/06042020.csv')

# Filter out non-Wales tweets
tweets = tweets[tweets['place.full_name'].str.contains('Wales', regex=False, na=False)]

# Parse 'created at' to pandas datetime - requires 'from datetime import datetime'
tweets['created_at'] = pd.to_datetime(tweets['created_at'])

# Set the datetime of tweet creation as the dataframe index
tweets.index = tweets['created_at']
del tweets['created_at']

# Before we go any further, lets tidy up the text columns...
def tidy_text_cols(data):
    """ Uses values from the short ('text') and extended ('extended_tweet.full_text') columns to make a single 'text' column with the
    full version of every tweet. """

    # keep the data for where 'tweet_full' is not used
    keep = pd.isnull(data['extended_tweet.full_text'])

    # Where tweet_full is used, make tweet_full as the text
    data_valid = data[~keep]
    data.loc[~keep, 'text'] = data_valid['extended_tweet.full_text']

    return data


tweets = tidy_text_cols(tweets)
# and then get rid of the now redundant column
del tweets['extended_tweet.full_text']


###############
# EXPLORATION #
###############

# How many tweets are defined by Twitter as being in Welsh?
len(tweets[tweets['lang'].str.contains('cy')])

# Can keywords produce useful subsets of the data?
tw1 = tweets[tweets["text"].str.contains("(\w{4})?\s?-?isolat", regex=True  , na=False)]
tw2 = tweets[tweets["text"].str.contains("community support | support group | community group", regex=True  , na=False)]
tw3 = tweets[tweets["text"].str.contains("help | support |", regex=True  , na=False)]
tw4 = tweets[tweets["text"].str.contains("street | neighbour | medic | pharmac", regex=True  , na=False)]
tw4 = tweets[tweets["text"].str.contains("shop | food | medic | pharmac", regex=True  , na=False)]

# TO DO
# Explore number of tweets being returned by each query - overlaps?

# NLP experiments
nlp = spacy.load('en_core_web_sm')
from spacy.matcher import PhraseMatcher
matcher = PhraseMatcher(nlp.vocab)

# Create a doc object from every tweet text, and save to a list. 
docs = list(nlp.pipe(tweets['text']))

# Only run nlp.make_doc to speed things up
patterns = [nlp.make_doc(text) for text in terms]
matcher.add("TerminologyList", None, *patterns)

# Find matches with TerminologyList across all docs.
matches = matcher.pipe(docs)

for match_id, start, end in matches:
    rule_id = nlp.vocab.strings[match_id]  # get the unicode ID
    span = doc[start : end]  # get the matched slice of the doc
    print(rule_id, span.text)
