# Backlog of changes 

_Keeping a log of changes and updates to the repo to share with everybody an overview of what has 
been done_

### 25th April 2020 `@ninadicara`  

On branch `feature/folder-restructure` I have made changes to the file structure of the repository. In the top level we now have `docs` and `notebooks` which are new additions to host any documentation and analysis Jupyter notebooks respectively. `visualisation` has been renamed to `dashboard` to improve the URL path and make it clearer what is in the folder.  

`data` has been reorganised so that any `.geojson` files for mapping are in `dashboard/data/` and we have a folder for scrapers and static files. `tweet-processing` has also been moved to the data folder, since it's functions operate on the data. 

Please note that no files have been removed unless they were obviously in the wrong place. Files have only been edited to update file paths. As such there are still some folders which might contain superflous files (e.g. scrapers/police_coders_groups), but I have left this to be handled in the restructing of `borg`. 


### 8th April 2020 `@ninadicara`  

- Reconfigured `\tweet-processing` so that frequently used dataframe processing scripts are redefined as functions. These can now be found in `tweet_functions`.py. 

### 7th April 2020 `@ninadicara`

- Renamed `tweet-processing.py` to `nlp-preprocessing.py`
- Added `tweet-exploration.py` file with some subsetting to look into potentially useful keywords.  


### 31st March 2020 `@ninadicara`

- Added `mapbox-web` folder, with a draft of a mapbox html file using geojson layers. 
- Added `demographics_withstops.xlsx` to show how colour stops were generated for each layer. 


### 27th March 2020 `@leriomaggio`

- Included `requirements.txt` and `covid_community_conda_env.yml` files to add dependencies and packages to setup 
environment.
- `README.md` updated with instructions to setup the environment and reference to the backlog
- minor changes and tweaks to the source code in `tweet-processing`
    -  PEP8 reformatting, removed unused imports, few typos.