"""Script to build elementary tweet classifier"""

# Import Functions
import pandas as pd
import numpy as np
import preprocessor as p
import re
import demoji
import nltk
import pickle
import os

from sklearn import naive_bayes, svm, metrics, decomposition
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion


# Local modules
from pipelines import TwitterPipeline
from datasets import load_tweets, load_annotated_tweets

# Download stopwords package if necessary
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def normalise_tweets(text_col: pd.Series):

    # Make sure every item is a string
    text_col = text_col.astype(str)

    # Remove hashtags
    text_norm = text_col.apply(lambda x: re.sub("#", "", x)).copy()

    # Use the tweet preprocesser to remove tweet-specific features from the text
    # It also replaces mentions with the word mention, and hashtags with the word hashtag
    text_norm = text_norm.apply(lambda tweet: p.tokenize(tweet))

    # Lower case all words
    text_norm = text_norm.str.lower()

    # Remove special characters (make sure to run this AFTER lowercasing)
    text_norm = text_norm.apply(lambda x: re.sub(r"[^a-z\s]", "", x))

    # Removing stopwords (using stopword list from NLTK)
    stop_words = set(stopwords.words("english"))
    text_norm = text_norm.apply(
        lambda x: " ".join(word for word in x.split() if word not in stop_words)
    )

    # Lemmatise the text
    lemmatizer = WordNetLemmatizer()
    text_norm = text_norm.apply(
        lambda x: " ".join(lemmatizer.lemmatize(word, pos="v") for word in x.split())
    )

    return text_norm


def fit_models(X, y):

    # Create train (80%), test (20%) split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y, test_size=0.2, random_state=42
    )

    # ---------------------------
    # Pipelines
    # ---------------------------

    # LDA commented out as contributes to overfitting
    # lda_feats = Pipeline(
    #     [
    #         ("count_vect", CountVectorizer(analyzer="word", token_pattern=r"\w{1,}")),
    #         (
    #             "lda",
    #             decomposition.LatentDirichletAllocation(
    #                 n_components=20, learning_method="online", max_iter=20
    #             ),
    #         ),
    #     ]
    # )

    # features = FeatureUnion(
    #     [
    #         ("lda", lda_feats),
    #         (
    #             "tfidf_vect",
    #             TfidfVectorizer(
    #                 analyzer="word", token_pattern=r"\w{1,}", max_features=1000
    #             ),
    #         ),
    #     ]
    # )

    # feature_processing = Pipeline([("feats", features)])
    # feature_processing.fit_transform(X_train)

    mnb_pipeline = Pipeline(
        [
            (
                "tfidf_vect",
                TfidfVectorizer(
                    analyzer="word", token_pattern=r"\w{1,}", max_features=1000
                ),
            ),
            ("multiNB", naive_bayes.MultinomialNB()),
        ]
    )

    svm_pipeline = Pipeline(
        [
            (
                "tfidf_vect",
                TfidfVectorizer(
                    analyzer="word", token_pattern=r"\w{1,}", max_features=1000
                ),
            ),
            ("svm", svm.SVC()),
        ]
    )

    lr_pipeline = Pipeline(
        [
            (
                "tfidf_vect",
                TfidfVectorizer(
                    analyzer="word", token_pattern=r"\w{1,}", max_features=1000
                ),
            ),
            ("lr", LogisticRegression()),
        ]
    )

    mnb_pipeline.fit(X_train, y_train)
    svm_pipeline.fit(X_train, y_train)
    lr_pipeline.fit(X_train, y_train)

    mnb_preds = mnb_pipeline.predict(X_test)
    svm_preds = svm_pipeline.predict(X_test)
    lr_preds = lr_pipeline.predict(X_test)

    print("MNB: " + str(np.mean(mnb_preds == y_test)))
    print("SVM: " + str(np.mean(svm_preds == y_test)))
    print("Logistic Regression: " + str(np.mean(lr_preds == y_test)))

    return lr_pipeline


if __name__ == "__main__":

    # Load the Twitter data
    tweets = load_tweets()
    tweets = TwitterPipeline().apply(tweets.data, verbosity=2)

    # Normalise all the tweets, as we use some of them later
    tweets["text_norm"] = normalise_tweets(tweets["text"])

    # Load the annotated tweets, combine them with the tweets
    annotated = load_annotated_tweets()
    df = pd.merge(annotated, tweets, on="id_str", how="left")

    # Initiate new column called label
    df["label"] = 0
    # Make label based on entries that ND thought were support related
    df["label"].loc[df["support_ND"] == 1] = 1

    # Set up new dataframe
    df = df[["id_str", "text_norm", "label"]]
    df.set_index("id_str", inplace=True)
    df.dropna()  # There are NA's as some of the tweet text is null

    # Seperate out the data and labels
    X = df["text_norm"]
    y = df["label"]

    model = fit_models(X, y)

    # Dump the model as .pkl
    file_out = "tweet_classifer.pkl"
    pickle.dump(model, open(file_out, "wb"))

    # Predictions on the non-annotated data?
    m = tweets.merge(
        annotated, on="id_str", how="outer", suffixes=["", "_"], indicator=True
    )
    unseen_data = m[m["_merge"] == "left_only"]
    unseen_data.set_index("id_str", inplace=True)

    unseen_col = unseen_data[["text_norm"]].squeeze()

    pred = model.predict(unseen_col)
