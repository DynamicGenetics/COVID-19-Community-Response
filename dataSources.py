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
        "path": "data/transformed/censusData_bias.csv",
        "ID_name": "areaID",
        "layers": {
            "language": {
                "nickName": "Welsh language use",
                "categoryInfo": DATAGROUPS['bias'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
        },
        "geometry": "Polygons",
    },
    {
        "name": "community_cohesion_deprivation",
        "type": "csv",
        "res": "LA",
        "enabled": True,
        "path": "data/transformed/censusData_comm.csv",
        "ID_name": "areaID",
        "layers": {
            "communityCohesion": {
                "nickName": "Community cohesion",
                "categoryInfo": DATAGROUPS['community'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
            "deprivation_30": {
                "nickName": "Multiple deprivation",
                "category": DATAGROUPS['demographics']['name'],
                "categoryInfo": DATAGROUPS['demographics'],
                "disabled": True,
                "reverseColors": False,
                "enabledByDefault": False,
            },
        },
        "geometry": "Polygons",
    },
    {
        "name": "covid_vulnerable",
        "type": "csv",
        "res": "LA",
        "enabled": True,
        "path": "data/transformed/censusData_covidVuln.csv",
        "ID_name": "areaID",
        "layers": {
            "vulnerable_pct": {
                "nickName": "COVID vulnerable (comorbidity %)",
                "categoryInfo": DATAGROUPS['covid'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
            "pop_density": {
                "nickName": "Population density",
                "categoryInfo": DATAGROUPS['demographics'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
            "pop_elderly": {
                "nickName": "Elderly population (% over 65)",
                "categoryInfo": DATAGROUPS['covid'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
            "pop": {
                "nickName": "Population",
                "categoryInfo": DATAGROUPS['demographics'],
                "disabled": True,
                "reverseColors": False,
                "enabledByDefault": False,
            },
        },
        "geometry": "Polygons",
    },
    {
        "name": "covid_cases",
        "type": "csv",
        "res": "LA",
        "enabled": True,
        "path": "data/transformed/covidCases_phw.csv",
        "ID_name": "areaID",
        "layers": {
            "covid_per100k": {
                "nickName": "COVID cases (per 100k)",
                "categoryInfo": DATAGROUPS['covid'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
        },
        "geometry": "Polygons",
    },
    {
        "name": "groups",
        "type": "geojson",
        "res": "LSOA",
        "enabled": True,
        "path": "dashboard/data/groups.geojson",
        "ID_name": None,
        "layers": {
            "groups": {
                "nickName": "Community support groups",
                "categoryInfo": DATAGROUPS['community'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": True,
            },
        },
        "geometry": "Points",
    },
    {
        "name": "groupCount",
        "type": "geojson",
        "res": "LSOA",
        "enabled": True,
        "path": "dashboard/data/groupCount.geojson",
        "ID_name": "areaID",
        "layers": {
            "groupCount": {
                "nickName": "Community support group count",
                "categoryInfo": DATAGROUPS['community'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": True,
            },
            "groupCount_pop": {
                "nickName": "Community support groups (PP)",
                "categoryInfo": DATAGROUPS['community'],
                "disabled": True,
                "reverseColors": False,
                "enabledByDefault": False,
            },
            "groupCount_elderly": {
                "nickName": "Community support groups (per elderly population)",
                "categoryInfo": DATAGROUPS['community'],
                "disabled": True,
                "reverseColors": False,
                "enabledByDefault": False,
            },
        },
        "geometry": "Polygons",
    },
    {
        "name": "twitter_count",
        "type": "geojson",
        "res": "LA",
        "enabled": True,
        "path": "dashboard/data/twitter_count.geojson",
        "ID_name": None,
        "layers": {
            "tweets_per_pop": {
                "nickName": "Support related tweets",
                "categoryInfo": DATAGROUPS['community'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": True,
            },
        },
        "geometry": "Polygons",
    },
    {
        "name": "demos_LSOA",
        "type": "csv",
        "res": "LSOA",
        "enabled": True,
        "path": "data/transformed/demos_LSOA.csv",
        "ID_name": 'areaID',
        "layers": {
            "WIMD_rank": {
                "nickName": "Multiple deprivation",
                "categoryInfo": DATAGROUPS['demographics'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
            "language_lsoa": {
                "nickName": "Welsh language",
                "categoryInfo": DATAGROUPS['bias'],
                "disabled": False,
                "reverseColors": False,
                "enabledByDefault": False,
            },
        },
        "geometry": "Polygons",
    },
]

# Boundary files to assimilate data into (as 'properties')
BOUNDARYFILES = {
    "LA": {"path": "data/geography/boundaries_LAs.geojson", "ID_name": "lad18cd", "area_name":"lad18nm"},
    "LSOA": {"path": "data/geography/boundaries_LSOAs.geojson", "ID_name": "LSOA11CD", "area_name":"LSOA11NM"},
    "LHB": {"path": "data/geography/boundaries_LHBs.geojson", "ID_name": "lhb19cd", "area_name":"lhb19nm"},
    "wales": {"path": "data/geography/boundaries_Wales.geojson", "ID_name": "ctry19cd", "area_name":"ctry19nm"},
}

# Filenames for GoogleScrape
FILENAMES = {
    "boundaries_wales": "data/geography/boundaries_wales.geoJSON",
    "boundaries_LA": "data/geography/boundaries_LSOAs.geoJSON",
    "csv": "data/transformed/groups.csv",
    "demographics_legacy": "data/demographics/demos_LSOA.csv",
    "output_groups": "dashboard/data/groups.geojson",
    "output_groupCount": "dashboard/data/groupCount.geojson",
    "output_URLs": "data/scrapers/community_measures/URLs.json",
    "output_groupCopyForReview": "data/scrapers/community_measures/QC/groupsForReview.csv",
    "credentials": "data/scrapers/community_measures/credentials.json",
}
