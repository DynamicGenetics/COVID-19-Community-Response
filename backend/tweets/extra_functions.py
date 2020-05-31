from geojson import Feature, MultiPolygon, FeatureCollection
import json
import pandas as pd
import os
from datasets import load_annotated_tweets


# %%
# In progress - how to define how certain the match is
def class_uncertainty(laoi):
    """ Roughly calculate how certain the classification is based on distances between
    the likelihood of the potentially overlapping LA boundaries. """

    # Sort dataframe by highest to lowest
    laoi = laoi.sort_values(by="likelihood", ascending=False)
    # Get the list of values
    a = laoi["likelihood"]
    a.reset_index().drop()

    # If there was only one, the
    if len(a) == 1:
        return 1
    elif len(a) == 2:
        return "only two"  # decide penalty function
    else:
        # Get the difference between each sequential number
        b = a.diff(periods=-1)
        # Divide the distance between the first and second number by the
        b["likelihood"][0] / b[1:].mean()


##############################
# Textual Analysis Functions #
##############################


def analyse_sentiment(data, col="text"):
    """ Given a Pandas dataframe with col 'tweet_text', this will apply the vaderSentiment dictionary
     in a new column called 'vader'. """

    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    # define the sentiment analyser object
    analyser = SentimentIntensityAnalyzer()

    # Apply sentiment analysis to the data frame (new col for each)
    data["vader_comp"] = data[col].apply(
        lambda x: analyser.polarity_scores(x)["compound"]
    )
    data["vader_pos"] = data[col].apply(lambda x: analyser.polarity_scores(x)["pos"])
    data["vader_neg"] = data[col].apply(lambda x: analyser.polarity_scores(x)["neg"])
    data["vader_neu"] = data[col].apply(lambda x: analyser.polarity_scores(x)["neu"])

    return data


# No longer needed with geopandas
def write_bbox_geojson(data, col="bbox_geojson"):
    """ Given a correctly formatted column of bbox polygons, this will convert them to
    a geojson object, and write it out to a file. """

    # Make a Mutlipolygon from the values.
    features = Feature(geometry=MultiPolygon(data[col].tolist()))

    # All the other columns used as properties
    # properties = df.drop(['lat', 'lng'], axis=1).to_dict('records')
    # Add properties to the geo_json
    # feature_collection = FeatureCollection(features=features, properties=properties)

    feature_collection = FeatureCollection(features=features)

    print("Geojson object generated.")

    with open("tweets_bboxes.geojson", "w", encoding="utf-8") as f:
        json.dump(feature_collection, f, ensure_ascii=False)

    print("Written object to 'tweets_bboxes.geojson'")


# %%
# Can keywords produce useful subsets of the data?
def generate_subsets(tweets):
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
        "iso_help": iso.merge(
            tw2["id_str"], how="inner", on="id_str", suffixes=("", "_y")
        ),
        "iso_shop": iso.merge(
            tw3["id_str"], how="inner", on="id_str", suffixes=("", "_y")
        ),
        "iso_community": iso.merge(
            tw4["id_str"], how="inner", on="id_str", suffixes=("", "_y")
        ),
        "iso_sm": iso.merge(
            tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y")
        ),
        "iso_vol": iso.merge(
            tw6["id_str"], how="inner", on="id_str", suffixes=("", "_y")
        ),
        "tw1": tweets[
            tweets["text_norm"].str.contains(
                r"community support | support group | community group",
                regex=True,
                na=False,
            )
        ],
        "help_vol": tw2.merge(
            tw6["id_str"], how="inner", on="id_str", suffixes=("", "_y")
        ),
        "shop_vol": tw3.merge(
            tw6["id_str"], how="inner", on="id_str", suffixes=("", "_y")
        ),
        "tw2": tw2,
        "tw3": tw3,
        "tw4": tw4,
        "tw5": tw5,
        "tw6": tw6,
        "tw2_3": tw2_3,
        "tw2_4": tw2.merge(
            tw4["id_str"], how="inner", on="id_str", suffixes=("", "_y")
        ),
        "tw2_5": tw2.merge(
            tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y")
        ),
        "tw3_4": tw3.merge(
            tw4["id_str"], how="inner", on="id_str", suffixes=("", "_y")
        ),
        "tw3_5": tw3.merge(
            tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y")
        ),
        "tw4_5": tw4.merge(
            tw5["id_str"], how="inner", on="id_str", suffixes=("", "_y")
        ),
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

    return dfs


def generate_annotated_dataset(new_annotations: str):
    """Merge newly annotated tweets into the overall annotated dataset.

    new_annotations is the filename of the newly annotated tweets in
    the datasets/data/tweets folder.
    """
    # Read in newly annotated twitter dataset
    new_ann_tweets = pd.read_csv(
        os.path.join("..", "datasets", "data", "tweets", new_annotations)
    )
    # Load in the existing annotated tweets
    annotated = load_annotated_tweets()
    # Get dataset of all annotations in one place, merging in the new annotations
    all_annos = pd.merge(
        annotated, new_ann_tweets[["id_str", "support_ND"]], on="id_str", how="outer"
    )
    all_annos["support_ND_x"].fillna(all_annos["support_ND_y"], inplace=True)
    all_annos["support_ND_x"] = all_annos["support_ND_x"].astype(str)
    all_annos.drop(columns=["support_ND_y"], inplace=True)
    all_annos.rename(columns={"support_ND_x": "support_ND"}, inplace=True)
    # Write the new annotations to file
    all_annos.to_pickle("../datasets/data/tweets/tws_annotated.pkl")
    return all_annos
