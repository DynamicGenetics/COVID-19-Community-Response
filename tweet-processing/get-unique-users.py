import pandas as pd 
import numpy as np

###################
#Read in the tweets
#Read in export from the Virtual Box VM (~420k tweets)
tweets_vbox = pd.read_csv('usernames_virtualbox.csv')
#Read in export from the Azure VM (~50k tweets)
tweets_azure = pd.read_csv('28032020_screennames.csv')

#Concatenate the tweets
tweets = pd.concat([tweets_vbox, tweets_azure])
tweets_vbox = pd.read_csv('usernames_virtualbox.csv')

#Because I'm an idiot, the username export doesn't have the place attribute.
#So we'll have to join it with the database that does. 

#Read in export from the Virtual Box VM (~420k tweets)
tweets_vbox2 = pd.read_csv('vm_export.csv')
#Read in export from the Azure VM (~50k tweets)
tweets_azure2 = pd.read_csv('25032020.csv')

#Concatenate the tweets
tweets2 = pd.concat([tweets_vbox2, tweets_azure2])

#Merge the data we need
tweets_names = pd.merge(tweets2,
                 tweets[['id_str', 'user.screen_name']],
                 on='id_str')

# Subset to just Wales based 'places' 
tweets_names = tweets_names[tweets_names['place.full_name'].str.contains('Wales', regex=False, na=False)]

#Write unique list of names to a txt file
tweets_names_unique = tweets_names['user.screen_name'].unique() #19,427 as of 28.03.2020

np.savetxt('user_list.txt', tweets_names_unique, fmt='%s')