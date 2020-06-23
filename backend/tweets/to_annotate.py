"""Module to generate csv ready for annotation in Excel."""

import pandas as pd
from pipelines import TwitterPipeline
from datasets import load_tweets, load_annotated_tweets
from build_classifier import normalise_tweets
from extra_functions import generate_subsets
import re

# -------------------------------------------
# Writing out the updated dataset to annotate
# -------------------------------------------

# Load the twitter dataset
tweets = load_tweets()
# %% Filter the tweets from Wales and format the text
tweets = TwitterPipeline().apply(tweets.data, verbosity=2)
# Normalise the text
tweets["text_norm"] = normalise_tweets(tweets["text"])
dfs = generate_subsets(tweets)

# Get the tweets that have been subsetted based on 'new rules'
tweet_subset = dfs["new_rules"]
# Get already annotated tweets
annotations = load_annotated_tweets()

# Tweets with annotations (and without)
tweets_a = pd.merge(tweet_subset, annotations, on="id_str", how="left")

# Sub-column
tweets_a = tweets_a[["id_str", "text", "support_ND"]]

# Get ready to write to Excel
tweets_a["text"] = '="' + tweets_a["text"] + '"'
tweets_a["id_str"] = '="' + tweets_a["id_str"].astype("str") + '"'

# Get the tweets that haven't been classified yet
tws_null = tweets_a[tweets_a["support_ND"].isna()]

# Write them to CSV ready to be classified
tws_null.to_csv("tweets_to_classify.csv")
