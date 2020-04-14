import pandas as pd
import re
import spacy
from tweet_functions import *

###################
# DATASET TIDYING #
###################

# Read in
tweets = read_and_tidy('../../data/nina_7apr.csv')

###############
# EXPLORATION #
###############

# How many tweets are defined by Twitter as being in Welsh?
len(tweets[tweets['lang'].str.contains('cy')])

# Can keywords produce useful subsets of the data?
tw1 = tweets[tweets["text"].str.contains("(\w{4})?\s?-?isolat", regex=True  , na=False)]
tw2 = tweets[tweets["text"].str.contains("community support | support group | community group", regex=True  , na=False)]
tw3 = tweets[tweets["text"].str.contains("help | support ", regex=True  , na=False)]
tw4 = tweets[tweets["text"].str.contains("street | neighbour | medic | pharmac", regex=True  , na=False)]
tw5 = tweets[tweets["text"].str.contains("shop | food | medic | pharmac", regex=True  , na=False)]
tw6 = tweets[tweets["text"].str.contains("facebook | whatsapp ", regex=True, na=False)]
tw7 = tweets[tweets["text"].str.contains("volunt", regex=True, na=False)]

covid_keyws = [
            'corona',
            'covid'
            'pandemic,'
            'outbreak'
            'c19',
            'workingfromhome',
            'workfromhome',
            'homeschooling',
            'socialdistancing',
            'socialdistance',
            'quarantine',
            'staythefhome',
            'stayhome'
            'stay home',
            'stay at home',
            'stayathome',
            'flattenthecurve',
            'flatten the curve'
            'covidiot',
            'notgoingout',
            'lockdown',
            'lock down',
            'NHS',
            'whenthisisallover'
            ]

tw8 = tweets[tweets['text'].str.contains('|'.join(covid_keyws))]

#Join all of the tweets
df_list = [tw1, tw2, tw3, tw4, tw5, tw6, tw7] #7093 tweets from nina_apr7.csv data
tws = pd.concat(df_list).drop_duplicates('id_str')

# TO DO
# Explore number of tweets being returned by each query - overlaps?

## TFIDF
from sklearn.feature_extraction.text import TfidfVectorizer
corpus = [tweets['text'].tolist()]

#>>> vectorizer = TfidfVectorizer()
#>>> X = vectorizer.fit_transform(corpus)
#>>> print(vectorizer.get_feature_names())
#['and', 'document', 'first', 'is', 'one', 'second', 'the', 'third', 'this']
#>>> print(X.shape)
#(4, 9)


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
