# %%
# Imports
import pandas as pd
import geopandas as gpd
from pipelines import TwitterPipeline
from datasets import load_tweets, load_annotated_tweets
import re
from datasets import load_local_authorities


# %% Load Tweets
tweets = load_tweets()
# %% Filter the tweets from Wales and format the text
tweets = TwitterPipeline().apply(tweets.data, verbosity=2)

# %% Load the annotated tweets, append them to tweets
annotated = load_annotated_tweets()

# %%
tweets = pd.merge(tweets, annotated, on="id_str", how="left")

# %%
# Can keywords produce useful subsets of the data?
tw2 = tweets[tweets["text"].str.contains("help", regex=True, na=False)].copy()
tw3 = tweets[
    tweets["text"].str.contains("shop | food | medic | pharmac", regex=True, na=False)
].copy()
tw4 = tweets[
    tweets["text"].str.contains(
        "street | neighbour | road | village", regex=True, na=False
    )
].copy()
tw5 = tweets[
    tweets["text"].str.contains(
        "facebook | whatsapp | next ?door ", regex=True, na=False
    )
].copy()

# Get combinations of the above to use
dfs = {
    "tw1": tweets[
        tweets["text"].str.contains(
            "community support | support group | community group", regex=True, na=False
        )
    ],
    "tw2_3": tw2.merge(tw3["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "tw2_4": tw2.merge(tw4["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "tw2_5": tw2.merge(tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "tw3_4": tw3.merge(tw4["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "tw3_5": tw3.merge(tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "tw4_5": tw4.merge(tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "tw6": tweets[tweets["text"].str.contains("volunt", regex=True, na=False)],
}

# Join all of the tweets and add to dictionary
dfs["tws"] = pd.concat(dfs.values()).drop_duplicates("id_str")  # Full subset


# %%
def calculate_accuracies(ground_truth_col: str, df_dict: dict = dfs):
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


accuracies_ND = calculate_accuracies("support_ND")
accuracies_LH = calculate_accuracies("support_LH")

print(accuracies_ND)
print(accuracies_LH)

# Outcome is fairly poor - need for more accurate classification
