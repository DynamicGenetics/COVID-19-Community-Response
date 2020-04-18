
#data sources to assimilate
dataSources = [
    {
        'name' : 'bias_language',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/bias_measures/censusData_bias.csv',
        'ID_name' : 'areaID',
        'category' : 'bias',
        'reverseColors' : False,
        'layers' : {
            'language' : 'Welsh language use',
        },
        'geometry' : 'Polygons',
        'shownByDefault' : False
    },{
        'name' : 'community_cohesion_deprivation',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/community_measures/censusData_comm.csv',
        'ID_name' : 'areaID',
        'category' : 'community',
        'reverseColors' : False,
        'layers' : {
            'communityCohesion' : 'Community cohesion',
            'deprivation_30' : 'Multiple deprivation',
        },
        'geometry' : 'Polygons',
        'shownByDefault' : False
    },{
        'name' : 'covid_vulnerable',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/covid_measures/censusData_covidVuln.csv',
        'ID_name' : 'areaID',
        'category' : 'covid',
        'reverseColors' : True,
        'layers' : {
            'vulnerable_pct' : 'Vulnerable (% with >=1 comorbidity)',
            'pop_density' : 'Population density',
            'pop_elderly' : 'Elderly population (% over 65)',
            'pop' : 'DISABLED'
        },
        'geometry' : 'Polygons',
        'shownByDefault' : False
    },{
        'name' : 'covid_cases',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/covid_measures/covidCases_phw.csv',
        'ID_name' : 'areaID',
        'category' : 'covid',
        'reverseColors' : True,
        'layers' : {
            'covid_per100k' : 'COVID cases (per 100k)'
        },
        'geometry' : 'Polygons',
        'shownByDefault' : False
    },{
        'name' : 'groups_points',
        'type' : 'scrape',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/community_measures/groups.csv',
        'ID_name' : None,
        'category' : 'community',
        'reverseColors' : False,
        'layers' : {
            'groups_points':'Community support groups'
        },
        'geometry' : 'Points',
        'shownByDefault' : True
    },{
        'name' : 'groupCount',
        'type' : 'scrape',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/community_measures/groupCount.csv',
        'ID_name' : 'areaID',
        'category' : 'community',
        'reverseColors' : True,
        'layers' : {
            "groupCount":'DISABLED', 
            "groupCount_pop": 'Community support groups (per capita)', 
            "groupCount_elderly": 'DISABLED'
        },
        'geometry' : 'Polygons',
        'shownByDefault' : True
    },{
        'name' : 'twitterCount',
        'type' : 'geojson',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/twitterCount.geojson',
        'ID_name' : None,
        'category' : 'bias',
        'reverseColors' : True,
        'layers' : {
            "tweets_per_pop":'Tweets (per capita)'
        },
        'geometry' : 'Polygons',
        'shownByDefault' : True
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
