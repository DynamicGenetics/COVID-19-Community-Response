# Data Guide

There are many different sources of data needed for the creation of the map.  
Some of these sources are static and administrative, whereas others are reguarly updated.  
The majority of data sources used for mapping are in a `.geojson` format.  
  
For a full explanation of the different data sources please see the [project wiki page](https://github.com/DynamicGenetics/Covid-Communities-Map/wiki).  
  
At present the data is structured as follows:
  
📦data  
 ┣ 📂live  
 ┣ 📂static  
 ┣ 📜Data sources.xlsx  
 ┣ 📜boundaries_LAs.geojson  
 ┣ 📜boundaries_LHBs.geojson  
 ┣ 📜boundaries_LSOAs.geojson  
 ┣ 📜boundaries_Wales.geojson  
 ┣ 📜cases.geojson  
 ┣ 📜data_guide.md  
 ┣ 📜demographics.geojson  
 ┣ 📜groupCount.geojson  
 ┗ 📜groups.geojson  
  
Where the live and static folders contain source material and compilers for generating the `geojson` files to map. 