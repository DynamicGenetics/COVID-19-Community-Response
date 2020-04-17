#import slave functions to call in these master functions (debug name = B1)
from data.recompilers.borg import assimilate
from data.community_measures.recompiler import convertGroups
from data.community_measures.scraper import googleScrape
from data.community_measures.QC.QC import QCFilter
from data.community_measures.QC.detectDuplicate import detectDuplicate
from data.community_measures.saveOutput import saveOutput

#data sources to assimilate
dataSources = [
    {
        'name' : 'bias_language',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : False,
        'path' : 'data/bias_measures/censusData_bias.csv',
        'ID_name' : 'areaID'
    },{
        'name' : 'community_cohesion+deprivation',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : False,
        'path' : 'data/community_measures/censusData_comm.csv',
        'ID_name' : 'areaID'
    },{
        'name' : 'covid_vulnerable',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : False,
        'path' : 'data/covid_measures/censusData_covidVuln.csv',
        'ID_name' : 'areaID'
    },{
        'name' : 'covid_cases',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : False,
        'path' : 'data/covid_measures/covidCases_phw.csv',
        'ID_name' : 'areaID'
    },{
        'name' : 'groupCount',
        'type' : 'dict',
        'res' : 'LA',
        'enabled' : False,
        'path' : 'data/community_measures/groupCount.csv',
        'ID_name' : None
    }
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

#iterate over data sources and assimilate() into boundary geojsons
for data in dataSources:
    if data["enabled"] == True:
        try: 
            print('Message (B1): Assimilating {} (type={}) '.format(data['name'],data['type']))
            if data["type"] == 'csv':
                    geo = boundaryFiles[data['res']]
                    assimilate(data['type'], data['path'], data['ID_name'], geo['path'], geo['ID_name'], 'data/{}.geojson'.format(data['name']))
            elif data["type"] == 'scrape':
                    geo = boundaryFiles[data['res']]
                    assimilate(data['type'], data['path'], data['ID_name'], geo['path'], geo['ID_name'], 'data/{}.geojson'.format(data['name']))
        except:
            print('ERROR (B1): Could not assimilate: ', data['name'])
    else:
        print("Warning (B1): Skipping disabled data: ", data['name'])

# assimilate(i['type'], i['path'], 'data/boundaries_LAs.geoJSON', 'id_area', 'data/demographics.geojson')

# # Produce demographics data
# assimilate('csv', 'data/static/demographics/demographics.csv', 'data/boundaries_LAs.geoJSON', 'id_area', 'data/demographics.geojson')

# # Produce second demographics data
# assimilate('csv', 'data/static/demographics/demographics_risk_LSOA.csv', 'data/boundaries_LSOAs.geoJSON', 'LA Code', 'data/demographics_risk_LSOA.geojson')

# # Produce cases data
# assimilate('csv', 'data/live/cases-manual/cases.csv', 'data/boundaries_LAs.geoJSON', 'id_area', 'data/cases.geojson')

# Scrape data from google sheet, remove duplicates, geolocate to Wales and convert csv to geoJSON
#googleScrape('https://www.googleapis.com/auth/spreadsheets.readonly', '1iqOvNjRlHIpoRzd61BcBLVkSxGvbta6vrzH2Jgc50aY', 'Support groups v2', 'data/community_measures/credentials.json', 'data/community_measures/groups.csv')
filenames = {
    "boundaries_wales" : "data/geography/boundaries_wales.geoJSON", 
    "boundaries_LA" : "data/geography/boundaries_LAs.geoJSON", 
    "csv" : "data/community_measures/groups.csv", 
    "demographics_legacy" : "data/community_measures/demographics.csv", 
    "output_groups" : "data/groups.geojson", 
    "output_groupCount" : "data/groupCount.geojson", 
    "output_URLs" : "data/community_measures/URLs.json", 
    "output_groupCopyForReview" : "data/community_measures/QC/groupsForReview.csv",
}
groupsData = convertGroups(filenames)
for row in groupsData[3]: print(row)
saveOutput(groupsData[0], groupsData[1], groupsData[2], filenames)