import pandas as pd

# Setting up to use with iPython
import matplotlib.pyplot as plt

# %matplotlib inline

###################
# Read in the tweets
tweets = pd.read_pickle("./25032020_corona_tweets.pkl")

# Subset to just Wales based 'places'
tweets = tweets[tweets["place.full_name"].str.contains("Wales", regex=False, na=False)]

# Mapping Sentiment

# get the hourly average of the composite vader tweets.
comphouravg = tweets["vader_comp"].resample("H").mean().to_frame()
compdayavg = tweets["vader_comp"].resample("D").mean().to_frame()

# #Hourly average of comp sentiment
# plt.plot(comphouravg)
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.show()

# #Daily average of comp sentiment
# plt.plot(compdayavg)
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.show()

# Covid hashtags (look at taking these direct from spreadsheet)
covid_keyws = [
    "COVID19",
    "coronavirus",
    "covid_19",
    "covid2019",
    "covid2019UK",
    "coronavirusuk",
    "covid_19uk",
    "coronauk",
    "coronavirusoutbreak",
    "covid-19uk",
    "coronaviruspandemic",
    "coronavirusupdates",
    "c19",
    "fightcovid19",
    "corona",
    "coronacrisis",
    "Italy",
    "WorkingFromHomeLife",
    "workingfromhome",
    "dogworkingfromhome",
    "workingfromhomewithkids",
    "workingfromhomewithdogs",
    "workfromhome",
    "homeschooling",
    "socialdistancing",
    "selfisolating",
    "selfisolation",
    "quarantine",
    "quarantinelife",
    "socialdistancingnow",
    "staythefhome",
    "stayathome",
    "flattenthecurve",
    "stayathomechallenge",
    "covidiot",
    "stayhomesavelives",
    "notgoingout",
    "lockdown",
    "socialdistance",
    "lockdownUKnow",
    "uklockdownnow",
    "shamblesstayathome",
    "tory",
    "covidiots",
    "covid19out",
    "shutthesites",
    "uklockdown",
    "coronaviruslockdownuk",
    "panicbuying",
    "stockpiling",
    "stockpilinguk",
    "Keepcalm",
    "selfcare",
    "calmness",
    "anxiety",
    "positivity",
    "innerpeace",
    "mentalhealth",
    "rest",
    "PublicHealthW",
    "BetsiCadwaladr",
    "NHS",
    "NHSwales",
    "Michael Gove",
    "quarantineonlineparty",
    "quarantinegames",
    "NHSheroes",
    "whenthisisallover",
    "NHScovidheroes",
]

# Subset tweets based on keywords
corona_tweets = tweets[tweets["text"].str.contains("|".join(covid_keyws))]

# Get the hourly average of the composite vader tweets.
covidcomphouravg = (
    corona_tweets["vader_comp"]
    .resample("H")
    .mean()
    .to_frame()
    .reset_index()
    .rename(columns={"vader_comp": "covid_vader_comp"})
)
covidcompdayavg = (
    corona_tweets["vader_comp"]
    .resample("D")
    .mean()
    .to_frame()
    .reset_index()
    .rename(columns={"vader_comp": "covid_vader_comp"})
)

# # Hourly average of comp sentiment
# plt.plot(covidcomphouravg)
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.show()

# # Daily average of comp sentiment
# plt.plot(covidcompdayavg)
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.show()

# Create dataframes of the covid and 'normal' sentiment tweets in each column
hourly_avg = pd.concat([comphouravg.reset_index(drop=True), covidcomphouravg], axis=1)
daily_avg = pd.concat([compdayavg.reset_index(drop=True), covidcompdayavg], axis=1)

# Import plotnine plotting library
from plotnine import *

# Now create some nicer plots...

# Reshape the hourly dataframe to long format for plotting
plot_hourly_avg = pd.melt(
    hourly_avg, id_vars=["created_at"], value_vars=["covid_vader_comp", "vader_comp"]
)

p = ggplot(plot_hourly_avg) + geom_line(
    aes(x="created_at", y="value", color="variable")
)
p = p + labs(
    x="Date-Time",
    y="VADER Compound Sentiment",
    title="Hourly compound sentiment for all vs COVID tweets",
)
p = p + theme(axis_text_x=element_text(angle=90, vjust=1))

# Reshape the daily dataframe to long format for plotting
plot_daily_avg = pd.melt(
    daily_avg, id_vars=["created_at"], value_vars=["covid_vader_comp", "vader_comp"]
)

p2 = ggplot(plot_daily_avg) + geom_line(
    aes(x="created_at", y="value", color="variable")
)
p2 = p2 + labs(
    x="Date-Time",
    y="VADER Compound Sentiment",
    title="Daily compound sentiment for all vs COVID tweets",
)
p2 = p2 + theme(axis_text_x=element_text(angle=90, vjust=1))

p.save("hourly.png", bbox_inches="tight")
p2.save("daily.png", bbox_inches="tight")
