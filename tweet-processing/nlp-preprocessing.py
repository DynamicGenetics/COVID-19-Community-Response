import pandas as pd
import re
from tweet_functions import *
# For text cleaning
import demoji
# FIXME: NB for first time use we need to download the lastest emoji codes (since they are updated reguarly)
# demoji.download_codes()
import nltk
import spacy

# Read in export from the Virtual Box VM (~420k tweets)
tweets_vbox = pd.read_csv('vm_export.csv')
# Read in export from the Azure VM (~50k tweets)
tweets_azure = pd.read_csv('25032020.csv')

# Concatenate the tweets
tweets = pd.concat([tweets_vbox, tweets_azure])
# We also seem to have two tweet ID columns ('id' and 'id_str'), so get rid of one of those.
del tweets['id_str']

# Make the datetime the index
tweets = create_datetime_index(tweets)
# Subset for relevant dates and locations
tweets = tweets['3/8/2020':]
tweets = get_welsh_tweets(tweets)

# Before we go any further, lets tidy up the text columns...
df = tidy_text_cols(tweets)

######
# Now we want to clean the text up a little bit to get it ready for analysis. 

# Save the emoji used in the text in a seperate column 'emoji' 
df['emoji'] = df['text'].apply(lambda x: demoji.findall(x))

# We still want to keep the original tweet text because things like VADER use punctuation and capitals for sentiment.
# So, lets make a new column for text that we can tokenise, called 'nlp_text'

# Remove special characters
df['nlp_text'] = df['text'].apply(lambda x: re.sub("[^a-z\s]", "", x))

# Lower case all words
df['nlp_text'] = df['nlp_text'].str.lower()

# Removing stopwords (using stopword list from NLTK) - NB this takes AGES. 
nltk.download('stopwords')
from nltk.corpus import stopwords

stopwords = set(stopwords.words("english"))
df['nlp_text'] = df['nlp_text'].apply(lambda x: " ".join(word for word in x.split() if word not in stopwords))

#########
# Now the text is a bit cleaner we can create a spaCy object for each tweet, and apply some basic sentiment analysis. 

# First create a spaCy object ('doc') for each tweet, and save to a new column so we can call it. 
nlp = spacy.load("en_core_web_sm")
df['spacy_doc'] = df['nlp_text'].apply(lambda x: nlp(x))

# Get the VADER sentiment for each tweet
df = analyse_sentiment(df)

########
# Now the dataframe is read in, cleaned and prepared for analysis we can pickle it out and use another script to analyse it. 
df.to_pickle("corona_tweets.pkl")
