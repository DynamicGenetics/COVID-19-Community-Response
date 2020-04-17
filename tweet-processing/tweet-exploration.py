# %%
# Import Functions
import pandas as pd
import geopandas as gpd
from pipelines import TwitterPipeline
from datasets import load_tweets
from tweet_functions import analyse_sentiment
import re


# %% Load Tweets
tweets = load_tweets()
# %% Filter the tweets from Wales and format the text
tweets = TwitterPipeline().apply(tweets.data, verbosity=1)

###############
# EXPLORATION #
###############

# %%
# How many tweets are defined by Twitter as being in Welsh?
# len(tweets[tweets["lang"].str.contains("cy")])

# %%
# Can keywords produce useful subsets of the data?
tw2 = tweets[tweets["text"].str.contains("help", regex=True, na=False)].copy()
tw3 = tweets[tweets["text"].str.contains("shop | food | medic | pharmac", regex=True, na=False)].copy()
tw4 = tweets[tweets["text"].str.contains("street | neighbour | road | village", regex=True, na=False)].copy()
tw5 = tweets[tweets["text"].str.contains("facebook | whatsapp | next ?door ", regex=True, na=False)].copy()

#Get combinations of the above to use
tw1 = tweets[tweets["text"].str.contains("community support | support group | community group", regex=True, na=False)]
tw2_3 = tw2.merge(tw3["id_str"], how="inner", on="id_str",  suffixes=('', '_y'))
tw2_4 = tw2.merge(tw4["id_str"], how="inner", on="id_str",  suffixes=('', '_y'))
tw2_5 = tw2.merge(tw5["id_str"], how="inner", on="id_str",  suffixes=('', '_y'))
tw3_4 = tw3.merge(tw4["id_str"], how="inner", on="id_str",  suffixes=('', '_y'))
tw3_5 = tw3.merge(tw5["id_str"], how="inner", on="id_str",  suffixes=('', '_y'))
tw4_5 = tw4.merge(tw5["id_str"], how="inner", on="id_str",  suffixes=('', '_y'))
tw6 = tweets[tweets["text"].str.contains("volunt", regex=True, na=False)]


# %%
# Join all of the tweets
df_list = [tw1, tw2_3, tw2_4, tw2_5, tw3_4, tw3_5, tw4_5, tw6]  # 7093 tweets from nina_apr7.csv data
tws = pd.concat(df_list).drop_duplicates("id_str") # Full subset 

# %% 
tws.shape

# %%
# NEXT STEP - do we have the Local Authority guesses for these? If not, generate them. 

# %%
# NEXT STEP - inspect - do the tweets look ok?

# %%
# Now, we want to group by local authority to prepare the dataset for mapping
tws_out = tws.groupby(['lad18cd']).count().resetindex


# %%
# Join the local authorities to the 
la = gpd.read_file("lsoa_key.geojson")
