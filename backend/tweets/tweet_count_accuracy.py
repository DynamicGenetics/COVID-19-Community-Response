# %%
# Imports
import pandas as pd
import geopandas as gpd
from pipelines import TwitterPipeline
from datasets import load_tweets, load_annotated_tweets
import re
from datasets import load_local_authorities
from build_classifier import normalise_tweets

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
# Can keywords produce useful subsets of the data?
iso = tweets[
    tweets["text_norm"].str.contains(
        r"(\w{4})?\s?-?isolat | (\w{6})?\s?-?dist", regex=True, na=False
    )
].copy()
tw2 = tweets[
    tweets["text_norm"].str.contains(
        r"help | support | need any ?thing", regex=True, na=False
    )
].copy()

tw3 = tweets[
    tweets["text_norm"].str.contains(
        r"shop | food | medic | pharmac", regex=True, na=False
    )
].copy()
tw4 = tweets[
    tweets["text_norm"].str.contains(
        r"street | neighbour | road | village | community | next ?door",
        regex=True,
        na=False,
    )
].copy()

tw2_3 = tw2.merge(tw3["id_str"], how="inner", on="id_str", suffixes=("", "_y"))
help_shop_comm = tw4.merge(
    tw2_3["id_str"], how="inner", on="id_str", suffixes=("", "_y")
)

tw5 = tweets[
    tweets["text_norm"].str.contains(
        r"facebook | whatsapp | next ?door ", regex=True, na=False
    )
].copy()
tw6 = tweets[tweets["text_norm"].str.contains("volunt", regex=True, na=False)]
# Get combinations of the above to use
dfs = {
    "iso": iso,
    "iso_help": iso.merge(tw2["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "iso_shop": iso.merge(tw3["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "iso_community": iso.merge(
        tw4["id_str"], how="inner", on="id_str", suffixes=("", "_y")
    ),
    "iso_sm": iso.merge(tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "iso_vol": iso.merge(tw6["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "tw1": tweets[
        tweets["text_norm"].str.contains(
            r"community support | support group | community group", regex=True, na=False
        )
    ],
    "help_vol": tw2.merge(tw6["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "shop_vol": tw3.merge(tw6["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "tw2": tw2,
    "tw3": tw3,
    "tw4": tw4,
    "tw5": tw5,
    "tw6": tw6,
    "tw2_3": tw2_3,
    "tw2_4": tw2.merge(tw4["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "tw2_5": tw2.merge(tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "tw3_4": tw3.merge(tw4["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "tw3_5": tw3.merge(tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "tw4_5": tw4.merge(tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y")),
    "help_shop_comm": help_shop_comm,
}

# Add tweets about shopping that aren't about online shopping
online_tweets = tweets[
    tweets["text_norm"].str.contains(r"on ?line | click", regex=True, na=False)
]
df = pd.merge(
    dfs["tw2_3"], online_tweets["id_str"], on="id_str", how="outer", indicator=True
)
dfs["tw7"] = df[df["_merge"] == "left_only"]

# Join all of the tweets and add to dictionary
dfs["tws"] = pd.concat(dfs.values()).drop_duplicates("id_str")  # Full subset

new_rules = [
    dfs["tw1"],
    dfs["tw5"],
    dfs["iso_shop"],
    dfs["iso_vol"],
    dfs["help_vol"],
    dfs["shop_vol"],
]
dfs["new_rules"] = pd.concat(new_rules).drop_duplicates("id_str")

dfs["new_rules"].to_csv("new_rules_tweets.csv")


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
# accuracies_LH = calculate_accuracies("support_LH")

print(accuracies_ND)
# print(accuracies_LH)
import pandas as pd
