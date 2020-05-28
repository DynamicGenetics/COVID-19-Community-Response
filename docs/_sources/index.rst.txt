.. COVID-19 Community Response documentation master file, created by
   sphinx-quickstart on Thu May 28 17:53:06 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to COVID-19 Community Response's documentation!
=======================================================

Project Information
********************

This is a description of the project information.


Documentation for the Code
**************************
.. toctree::
   :maxdepth: 2
   :caption: Contents:

Run Scrapers
=============
.. automodule:: backend.generate_json
   :members:

   PHW Scraper - Run
   =================
   .. automodule:: backend.scrapers.phw_covid_statement.phw_scraper
      :members:
   
   PHW Scraper - Get URL
   =====================
   .. automodule:: backend.scrapers.phw_covid_statement.get_data_url


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
