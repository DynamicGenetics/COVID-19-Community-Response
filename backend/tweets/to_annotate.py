"""Module to generate csv ready for annotation in Excel."""

import pandas as pd
from pipelines import TwitterPipeline
from datasets import load_tweets, load_new_annotations
from build_classifier import normalise_tweets
from extra_functions import generate_subsets
import re


# Load the twitter dataset
tweets = load_tweets("twitter")
# %% Filter the tweets from Wales and format the text
tweets = TwitterPipeline().apply(tweets.data, verbosity=2)
# Normalise the text
tweets["text_norm"] = normalise_tweets(tweets["text"])
dfs = generate_subsets(tweets)

# Get the tweets that have been subsetted based on 'new rules'
tweet_subset = dfs["new_rules"]

# For debugging, was using the old tweets too
# old_tweets = load_tweets("twitter_apr")
# old_tweets = TwitterPipeline().apply(old_tweets.data, verbosity=2)
# old_tweets["text_norm"] = normalise_tweets(old_tweets["text"])
# old_dfs = generate_subsets(old_tweets)
# old_tweet_subset = old_dfs["new_rules"]

annotations = load_new_annotations()

tweets_a = pd.merge(tweet_subset, annotations, on="id_str", how="left")

tweets_a = tweets_a[["id_str", "text", "support_ND"]]

# Get ready to write to Excel
tweets_a["text"] = '="' + tweets_a["text"] + '"'
tweets_a["id_str"] = '="' + tweets_a["id_str"].astype("str") + '"'

tws_null = tweets_a[tweets_a["support_ND"].isna()]

tws_null.to_csv("tweets_to_classify.csv")
