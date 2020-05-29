# Data Guide

For a full explanation of the different data sources please see the [project wiki page which hosts our data documentation](https://bit.ly/covidresponsemapwiki).  

## Folder Structure

### Static
Static files are those that will not be regularly updated as part of the dashboard. They are generated once, and then are ready for use.  

### Live
Live files are updated regularly by either scrapers, or regular API calls. 

#### Raw and Cleaned in Static and Live
Raw or source data is in the format that it was downloaded or scraped too. 

Cleaned data has been processed by data cleaning script. The data content should be exactly the same as in `raw`, but with files suitably preprocessed to allow for easy reading into a dataframe, and each row having a LA or LSOA code and name.  
This includes the `_master.csv` files.