# %%
# Import Functions
import pandas as pd
import geopandas as gpd
from pipelines import TwitterPipeline
from datasets import load_tweets, load_annotated_tweets
from tweet_functions import analyse_sentiment
import re
import numpy as np


# %% Load Tweets
tweets = load_tweets()
# %% Filter the tweets from Wales and format the text
tweets = TwitterPipeline().apply(tweets.data, verbosity=2)


tweets = pd.read_csv("new_rules_idstr_intact.csv")


annotated = load_annotated_tweets()
new_anno = tweets[["id_str", "support_ND"]]
all_annos = pd.merge(annotated, new_anno, on="id_str", how="outer")
all_annos["support_ND_x"].fillna(all_annos["support_ND_y"], inplace=True)
all_annos["support_ND_x"] = all_annos["support_ND_x"].astype(str)
all_annos.drop(columns=["support_ND_y"], inplace=True)
all_annos.rename(columns={"support_ND_x": "support_ND"}, inplace=True)
all_annos.to_pickle("new_annotations.pkl")

tweets = pd.merge(all_annos, tweets, on="id_str", how="left")
tweets_yes = tweets[tweets["support_ND"] == "1"]
tweets_yes = tweets_yes[["user.id_str", "lad19cd"]]


unique = tweets_yes.drop_duplicates(subset=["user.id_str", "lad19cd"])

table = pd.pivot_table(
    unique, values="user.id_str", index="lad19cd", aggfunc=np.count_nonzero
)


tweets = tweets[["user.id_str", "lad19cd"]]
unique_all = tweets.drop_duplicates(subset=["user.id_str", "lad19cd"])
