# %%
# Imports
import pandas as pd
import geopandas as gpd
from pipelines import TwitterPipeline
from datasets import load_tweets, load_annotated_tweets
from tweet_functions import analyse_sentiment
import re
from warnings import warn
from datasets import load_local_authorities


# %% Load Tweets
tweets = load_tweets()
# %% Filter the tweets from Wales and format the text
tweets = TwitterPipeline().apply(tweets.data, verbosity=2)


# %% Load the annotated tweets, append them to tweets
annotated = load_annotated_tweets()



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
tw1 = tweets[
    tweets["text"].str.contains(
        "community support | support group | community group", regex=True, na=False
    )
]
tw1["tw1"] = 1
tw2_3 = tw2.merge(tw3["id_str"], how="inner", on="id_str", suffixes=("", "_y"))
tw2_3["tw2_3"] = 1
tw2_4 = tw2.merge(tw4["id_str"], how="inner", on="id_str", suffixes=("", "_y"))
tw2_3[]
tw2_5 = tw2.merge(tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y"))
tw3_4 = tw3.merge(tw4["id_str"], how="inner", on="id_str", suffixes=("", "_y"))
tw3_5 = tw3.merge(tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y"))
tw4_5 = tw4.merge(tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y"))
tw6 = tweets[tweets["text"].str.contains("volunt", regex=True, na=False)]


# 
# Join all of the tweets
df_list = [tw1, tw2_3, tw2_4, tw2_5, tw3_4, tw3_5, tw4_5, tw6]  # 7093 tweets data
tws = pd.concat(df_list).drop_duplicates("id_str")  # Full subset

# 
tws.shape

# 
# Now, we want to group by local authority to prepare the dataset for mapping
tws_out = tws.groupby(["lad19cd"]).count().reset_index()

# 
la = load_local_authorities()
la = la.data

tws_out["count"] = tws_out["id_str"].copy()
tws_out = pd.merge(
    la, tws_out[["count", "lad18cd"]], left_on="lad18cd", right_on="lad18cd"
)

# %%
tws_out["tweets_per_pop"] = tws_out["count"] / tws_out["pop"]
tws_out["tweets_per_pop"] /= tws_out["tweets_per_pop"].max()

# %%
tws_out = tws_out[["lad18cd", "lad18nm", "geometry", "tweets_per_pop"]]
tws_out.to_file("../data/twitter_count.geojson", driver="GeoJSON")
