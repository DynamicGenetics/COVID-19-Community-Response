# Backlog of changes 

_Keeping a log of changes and updates to the repo to share with everybody an overview of what has 
been done_

### 27th March 2020 `@leriomaggio`

- Included `requirements.txt` and `covid_community_conda_env.yml` files to add dependencies and packages to setup 
environment.
- `README.md` updated with instructions to setup the environment and reference to the backlog
- minor changes and tweaks to the source code in `tweet-processing`
    -  PEP8 reformatting, removed unused imports, few typos.

### 31st March 2020 `@ninadicara`

- Added `mapbox-web` folder, with a draft of a mapbox html file using geojson layers. 
- Added `demographics_withstops.xlsx` to show how colour stops were generated for each layer. 

### 7th April 2020 `@ninadicara`

- Renamed `tweet-processing.py` to `nlp-preprocessing.py`
- Added `tweet-exploration.py` file with some subsetting to look into potentially useful keywords.  

## 8th April 2020 `@ninadicara`  

- Reconfigured `\tweet-processing` so that frequently used dataframe processing scripts are redefined as functions. These can now be found in `tweet_functions`.py. 