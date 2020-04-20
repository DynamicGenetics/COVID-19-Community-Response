# %%
from pipelines import TwitterPipeline
from datasets import load_tweets, load_local_authorities
from datetime import datetime

# %%
if __name__ == "__main__":
    # %% Load Tweets
    tweets = load_tweets()

    start = datetime.now()
    # %% Filter the tweets from Wales and format the text
    tweets_data = TwitterPipeline().apply(tweets.data, verbosity=2)
    end = datetime.now()

    print("Pipeline processing completed in: ", (end - start), end="\n\n")

    print("-" * 80)
    print("Twitter Data Dimension: ", tweets_data.shape)
    print("Twitter Dataset Columns: ", tweets_data.columns)
    print(
        "All Tweets have a matched LA: ",
        tweets_data[tweets_data["lad18nm"].isna()].shape[0] == 0,
    )
    print("-" * 80)
