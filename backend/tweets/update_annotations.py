import pandas as pd
import os
from pipelines import TwitterPipeline
from datasets import load_tweets, load_annotated_tweets, DATA_FOLDER


# --------------------------------------------------
# Read annotated tweets and update annotations file
# --------------------------------------------------

# Read in the newly annotated tweets
new_ann = pd.read_csv("tweets_to_classify.csv")
new_ann_sub = new_ann[["id_str", "support_ND"]]

# Read in the existing annotated tweets
annotations = load_annotated_tweets()

# Join the datasets
joined_anns = pd.concat([annotations, new_ann_sub])

# Write directory and filename
twitter_dir = os.path.join(DATA_FOLDER, "tweets", "tws_annotated.pkl")

# Write updated annotations to pkl
joined_anns.to_pickle(twitter_dir)
