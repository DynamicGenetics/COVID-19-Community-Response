# Data Guide

For a full explanation of the different data sources please see the [project wiki page](https://github.com/DynamicGenetics/Covid-Communities-Map/wiki).  

## Folder Structure

### Raw
This file should contain *all* data files used in the project, exactly as downloaded. At the time of being saved to raw the only edits made to the file should be to the file name, and this should be avoided if possible.  
When downloading new files, add them to the `README.md` in `raw/`, and specify exactly where from and when they were downloaded.

This file is 'READ ONLY' unless adding a new data source. 

### Cleaned
Cleaned data has been processed by the `raw_data_cleaning.py` script. The data content should be exactly the same as in `raw`, but with files suitably preprocessed to allow for easy reading into a dataframe, and each row having a LA or LSOA code and name. 

Naming conventions for cleaned files should follow: `resolution_data.csv`  
For example: `lsoa_welsh_speakers.csv`  

### Transformed
Transformed data may have been standardised or transformed in some way. It should be ready to be handled by processing files to turn it into geojson, and not require any further manipulation before being used for the dashboard. 

### Scrapers
Contains subfolders, each of which is scraping from one specific source. For example `scrapers/police_coders_groups/` is responsible for scraping data from the Police Coders group, and should have no other purpose than producing an output file with this information.  

### Static
Static files are used for reference only. As such this should also be a 'READ ONLY' folder. The main purpose of this folder is to hold geographic boundary reference files. 

### Tweet-Processing
Scripts for processing, cleaning and exporting Twitter data belong here. Raw tweet counts should export to `cleaned/`. 
