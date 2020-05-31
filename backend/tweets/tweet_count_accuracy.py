"""Module to assess accuracy of subset rules against labels"""
# %%
# Imports
import pandas as pd
import geopandas as gpd
from pipelines import TwitterPipeline
from datasets import load_tweets, load_annotated_tweets
import re
from datasets import load_local_authorities
from build_classifier import normalise_tweets
from extra_functions import generate_subsets

# %% Load Tweets
tweets = load_tweets()
# %% Filter the tweets from Wales and format the text
tweets = TwitterPipeline().apply(tweets.data, verbosity=2)

# %% Load the annotated tweets, append them to tweets
annotated = load_annotated_tweets()

# %%
tweets = pd.merge(tweets, annotated, on="id_str", how="left")

tweets["text_norm"] = normalise_tweets(tweets["text"])


# %%
def calculate_accuracies(ground_truth_col: str, df_dict: dict):
    cols = [
        "df_name",
        "total_tweets",
        "true_pos",
        "false_pos",
        "true_pos_pct",
        "false_pos_pct",
    ]
    lst = []
    for name, df in dfs.items():
        entries = df.shape[0]
        true_pos = (df[ground_truth_col] == 1).sum()
        false_pos = (df[ground_truth_col] == 0).sum()
        unlabelled = df[ground_truth_col].isna().sum()
        true_pos_pct = (true_pos / (entries - unlabelled)) * 100
        false_pos_pct = (false_pos / (entries - unlabelled)) * 100
        row = [name, entries, true_pos, false_pos, true_pos_pct, false_pos_pct]
        lst.append(row)

    accuracies = pd.DataFrame(lst, columns=cols)
    return accuracies


dfs = generate_subsets(tweets)
dfs["new_rules"].to_csv("new_rules_tweets.csv")
accuracies_ND = calculate_accuracies("support_ND", df_dict=dfs)
# accuracies_LH = calculate_accuracies("support_LH")

print(accuracies_ND)
# print(accuracies_LH)
