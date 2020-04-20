# group names & display order
DATAGROUPS = {
    'community':{
        'name':"Community support",
        'displayOrder':0,
        'colors':["#ffffe5","#f7fcb9","#d9f0a3","#addd8e","#78c679","#41ab5d","#238443","#006837","#004529",],  # 9-class YlGn (yellow-green, @colorbrewer2)
    },
    'covid':{
        'name':"COVID vulnerability",
        'displayOrder':1,
        'colors':["#fff7ec","#fee8c8","#fdd49e","#fdbb84","#fc8d59","#ef6548","#d7301f","#b30000","#7f0000",],  # 9-class OrRd (white-orange-red, @colorbrewer2)
    },
    'demographics':{
        'name':"Demographics",
        'displayOrder':2,
        'colors':["#fff7f3","#fde0dd","#fcc5c0","#fa9fb5","#f768a1","#dd3497","#ae017e","#7a0177","#49006a",],  # 9-class RdPu (white-purple, @colorbrewer2)
    },
    'bias':{
        'name':"Factors affecting data quality",
        'displayOrder':3,
        'colors':["#f7fcf0","#e0f3db","#ccebc5","#a8ddb5","#7bccc4","#4eb3d3","#2b8cbe","#0868ac","#084081",],  # 9-class GnBu (white-green-blue, @colorbrewer2)
    }
}

# data sources to assimilate
DATASOURCES = [
    {
        "name": "bias_language",
        "type": "csv",
        "res": "LA",
        "enabled": True,
        "path": "data/bias_measures/censusData_bias.csv",
        "ID_name": "areaID",
        "layers": {
            "language": {
                "nickName": "Welsh language use",
                "category": DATAGROUPS['bias']['name'],
                "categoryInfo": DATAGROUPS['bias'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
        },
        "geometry": "Polygons",
        "shownByDefault": False,
    },
    {
        "name": "community_cohesion_deprivation",
        "type": "csv",
        "res": "LA",
        "enabled": True,
        "path": "data/community_measures/censusData_comm.csv",
        "ID_name": "areaID",
        "layers": {
            "communityCohesion": {
                "nickName": "Community cohesion",
                "category": DATAGROUPS['community']['name'],
                "categoryInfo": DATAGROUPS['community'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
            "deprivation_30": {
                "nickName": "Multiple deprivation",
                "category": DATAGROUPS['demographics']['name'],
                "categoryInfo": DATAGROUPS['demographics'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
        },
        "geometry": "Polygons",
        "shownByDefault": False,
    },
    {
        "name": "covid_vulnerable",
        "type": "csv",
        "res": "LA",
        "enabled": True,
        "path": "data/covid_measures/censusData_covidVuln.csv",
        "ID_name": "areaID",
        "layers": {
            "vulnerable_pct": {
                "nickName": "COVID vulnerable (comorbidity %)",
                "category": DATAGROUPS['covid']['name'],
                "categoryInfo": DATAGROUPS['covid'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
            "pop_density": {
                "nickName": "Population density",
                "category": DATAGROUPS['demographics']['name'],
                "categoryInfo": DATAGROUPS['demographics'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
            "pop_elderly": {
                "nickName": "Elderly population (% over 65)",
                "category": DATAGROUPS['covid']['name'],
                "categoryInfo": DATAGROUPS['covid'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
            "pop": {
                "nickName": "Population",
                "category": DATAGROUPS['demographics']['name'],
                "categoryInfo": DATAGROUPS['demographics'],
                "disabled": True,
                "reverseColors": False,
                "enabledByDefault": False,
            },
        },
        "geometry": "Polygons",
        "shownByDefault": False,
    },
    {
        "name": "covid_cases",
        "type": "csv",
        "res": "LA",
        "enabled": True,
        "path": "data/covid_measures/covidCases_phw.csv",
        "ID_name": "areaID",
        "layers": {
            "covid_per100k": {
                "nickName": "COVID cases (per 100k)",
                "category": DATAGROUPS['covid']['name'],
                "categoryInfo": DATAGROUPS['covid'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
        },
        "geometry": "Polygons",
        "shownByDefault": False,
    },
    {
        "name": "groups",
        "type": "geojson",
        "res": "LA",
        "enabled": True,
        "path": "data/community_measures/groups.csv",
        "ID_name": None,
        "layers": {
            "groups": {
                "nickName": "Community support groups",
                "category": DATAGROUPS['community']['name'],
                "categoryInfo": DATAGROUPS['community'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": True,
            },
        },
        "geometry": "Points",
        "shownByDefault": True,
    },
    {
        "name": "groupCount",
        "type": "scrape",
        "res": "LA",
        "enabled": True,
        "path": "data/community_measures/groupCount.csv",
        "ID_name": "areaID",
        "layers": {
            "groupCount": {
                "nickName": "Community support groups",
                "category": DATAGROUPS['community']['name'],
                "categoryInfo": DATAGROUPS['community'],
                "disabled": True,
                "reverseColors": False,
                "enabledByDefault": False,
            },
            "groupCount_pop": {
                "nickName": "Community support groups (PP)",
                "category": DATAGROUPS['community']['name'],
                "categoryInfo": DATAGROUPS['community'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": True,
            },
            "groupCount_elderly": {
                "nickName": "Community support groups (per elderly population)",
                "category": DATAGROUPS['community']['name'],
                "categoryInfo": DATAGROUPS['community'],
                "disabled": True,
                "reverseColors": False,
                "enabledByDefault": False,
            },
        },
        "geometry": "Polygons",
        "shownByDefault": True,
    },
    {
        "name": "twitter_count",
        "type": "geojson",
        "res": "LA",
        "enabled": True,
        "path": "data/twitter_count.geojson",
        "ID_name": None,
        "layers": {
            "tweets_per_pop": {
                "nickName": "Support related tweets (PP)",
                "category": DATAGROUPS['community']['name'],
                "categoryInfo": DATAGROUPS['community'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": True,
            },
        },
        "geometry": "Polygons",
        "shownByDefault": True,
    },
]

# Boundary files to assimilate data into (as 'properties')
BOUNDARYFILES = {
    "LA": {"path": "data/geography/boundaries_LAs.geojson", "ID_name": "lad18cd"},
    "LSOA": {"path": "data/geography/boundaries_LSOAs.geojson", "ID_name": "LA11CD"},
    "LHB": {"path": "data/geography/boundaries_LHBs.geojson", "ID_name": "lhb19cd"},
    "wales": {"path": "data/geography/boundaries_Wales.geojson", "ID_name": "ctry19cd"},
}

# Filenames for GoogleScrape
FILENAMES = {
    "boundaries_wales": "data/geography/boundaries_wales.geoJSON",
    "boundaries_LA": "data/geography/boundaries_LAs.geoJSON",
    "csv": "data/community_measures/groups.csv",
    "demographics_legacy": "data/community_measures/demographics.csv",
    "output_groups": "data/groups.geojson",
    "output_groupCount": "data/groupCount.geojson",
    "output_URLs": "data/community_measures/URLs.json",
    "output_groupCopyForReview": "data/community_measures/QC/groupsForReview.csv",
    "credentials": "data/community_measures/credentials.json",
}
