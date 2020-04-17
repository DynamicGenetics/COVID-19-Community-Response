
#data sources to assimilate
dataSources = [
    {
        'name' : 'bias_language',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/bias_measures/censusData_bias.csv',
        'ID_name' : 'areaID',
        'category' : 'bias'
    },{
        'name' : 'community_cohesion+deprivation',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/community_measures/censusData_comm.csv',
        'ID_name' : 'areaID',
        'category' : 'community'
    },{
        'name' : 'covid_vulnerable',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/covid_measures/censusData_covidVuln.csv',
        'ID_name' : 'areaID',
        'category' : 'covid'
    },{
        'name' : 'covid_cases',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/covid_measures/covidCases_phw.csv',
        'ID_name' : 'areaID',
        'category' : 'covid'
    },{
        'name' : 'groups',
        'type' : 'scrape',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/community_measures/groups.csv',
        'ID_name' : None,
        'category' : 'community'
    },{
        'name' : 'groupCount',
        'type' : 'scrape',
        'res' : 'LA',
        'enabled' : False,
        'path' : 'data/community_measures/groupCount.csv',
        'ID_name' : 'areaID',
        'category' : 'community'
    },
]

#boundary files to assimilate data into (as 'properties')
boundaryFiles = {
    'LA' : {
        'path' : 'data/geography/boundaries_LAs.geojson',
        'ID_name' : 'lad18cd'
    },
    'LSOA' : {
        'path' : 'data/geography/boundaries_LSOAs.geojson',
        'ID_name' : 'LA11CD'
    },
    'LHB' : {
        'path' : 'data/geography/boundaries_LHBs.geojson',
        'ID_name' : 'lhb19cd'
    },
    'wales' : {
        'path' : 'data/geography/boundaries_Wales.geojson',
        'ID_name' : 'ctry19cd'
    }
}

#Filenames for GoogleScrape
filenames = {
    "boundaries_wales" : "data/geography/boundaries_wales.geoJSON", 
    "boundaries_LA" : "data/geography/boundaries_LAs.geoJSON", 
    "csv" : "data/community_measures/groups.csv", 
    "demographics_legacy" : "data/community_measures/demographics.csv", 
    "output_groups" : "data/groups.geojson", 
    "output_groupCount" : "data/groupCount.geojson", 
    "output_URLs" : "data/community_measures/URLs.json", 
    "output_groupCopyForReview" : "data/community_measures/QC/groupsForReview.csv",
    "credentials" : 'data/community_measures/credentials.json',
}
