import pandas as pd
from datetime import datetime
import re
#For text cleaning
import demoji
#NB for first time use we need to download the lastest emoji codes (since they are updated reguarly)
#demoji.download_codes()
import nltk
import vader
import spacy

#Read in export from the Virtual Box VM (~420k tweets)
tweets_vbox = pd.read_csv('vm_export.csv')
#Read in export from the Azure VM (~50k tweets)
tweets_azure = pd.read_csv('25032020.csv')

#Concatenate the tweets
tweets = pd.concat([tweets_vbox, tweets_azure])

#Parse 'created at' to pandas datetime - requires 'from datetime import datetime'
tweets['created_at'] = pd.to_datetime(tweets['created_at'])

#Set the id as the ID of the row
tweets.index = tweets['created_at']
del tweets['created_at']

#We also seem to have two tweet ID columns ('id' and 'id_str'), so get rid of one of those. 
del tweets['id_str']

#Now that we have date-time we can take only those tweets after 8th March, as this is when I actually have data for
#Since data collection stopped between 19th Feb and 8th March
df = tweets['3/8/2020':]

#Before we go any further, lets tidy up the text columns... 

def tidy_text_cols(data):
    
    """ Uses values from the short ('text') and extended ('extended_tweet.full_text') columns to make a single 'text' column with the 
    full version of every tweet. """
    
    #keep the data for where 'tweet_full' is not used
    keep = pd.isnull(data['extended_tweet.full_text'])

    #Where tweet_full is used, make tweet_full as the text
    data_valid = data[~keep]
    data.loc[~keep, 'text'] = data_valid['extended_tweet.full_text']

    return data

df = tidy_text_cols(df)

#and then get rid of the now redundant column
del df['extended_tweet.full_text']


######
# Now we want to clean the text up a little bit to get it ready for analysis. 

# Save the emoji used in the text in a seperate column 'emoji' 
df['emoji'] = df['text'].apply(lambda x : demoji.findall(x))

# We still want to keep the original tweet text because things like VADER use punctuation and capitals for sentiment.
# So, lets make a new column for text that we can tokenise, called 'nlp_text'

# Remove special characters
df['nlp_text'] = df['text'].apply(lambda x : re.sub("[^a-z\s]","",x) )

# Lower case all words
df['nlp_text'] = df['nlp_text'].str.lower()

# Removing stopwords (using stopword list from NLTK) - NB this takes AGES. 
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords = set(stopwords.words("english"))
df['nlp_text'] = df['nlp_text'].apply(lambda x : " ".join(word for word in x.split() if word not in stopwords ))


#########
# Now the text is a bit cleaner we can create a spaCy object for each tweet, and apply some basic sentiment analysis. 

# First create a spaCy object ('doc') for each tweet, and save to a new column so we can call it. 
nlp = spacy.load("en_core_web_sm")
df['spacy_doc'] = df['nlp_text'].apply(lambda x : nlp(x))

# Next we will use VADER to do some basic sentiemnt analysis (on the original 'text', not 'nlp_text')
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Define the sentiment analyser object
analyser = SentimentIntensityAnalyzer()

#Apply sentiment analysis to the data frame (new col for each)
df['vader_comp'] = df['text'].apply(lambda x : analyser.polarity_scores(x)['compound'])
df['vader_pos'] = df['text'].apply(lambda x : analyser.polarity_scores(x)['pos'])
df['vader_neg'] = df['text'].apply(lambda x : analyser.polarity_scores(x)['neg'])
df['vader_neu'] = df['text'].apply(lambda x : analyser.polarity_scores(x)['neu'])

########
# Now the dataframe is read in, cleaned and prepared for analysis we can pickle it out and use another script to analyse it. 
df.to_pickle("corona_tweets.pkl")
