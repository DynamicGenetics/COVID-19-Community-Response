# COVID-19 Community Response Map - Cymraeg

This branch supports the Welsh language version of the COVID-19 Community Response Map website.
The welsh version can be [found at this address](https://mapymatebcovid.cymru/)

The differences between this branch and the main master branch are in key files:  
* `backend/generate_json.py` - contains Welsh names for variables and areas to produce the data file with the correct translations  
* HTML files - all of the top level html files contain the welsh website translation. In some cases this also means that the html file name is different to the English one.  
* Small changes to JavaScript:  
** `frontend/map/js/map.js` line 320 ish - the descriptions used for when you click on a group point. [Relevant commit here.](https://github.com/DynamicGenetics/COVID-19-Community-Response/commit/a311674c003d5e42e01816f07f73c8b15e829a72)  
** `frontend/map/js/map.js` line 247 - updating the tooltips to use the Welsh area names when hovering over locations on the map. [Relevant commit here.](https://github.com/DynamicGenetics/COVID-19-Community-Response/commit/e81885e7a8993b39a3a53e9b1c8f69bb6653ce26)
