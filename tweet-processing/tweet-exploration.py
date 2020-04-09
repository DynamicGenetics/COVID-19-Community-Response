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
