#import slave functions to call in these master functions (debug name = B1)
from data.recompilers.borg import assimilate
from data.live.groups.recompiler import convertGroups
from data.live.groups.scraper import googleScrape
from data.live.groups.QC.QC import QCFilter

#data sources to assimilate
dataSources = [
    {
        'name' : 'demographics',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/static/demographics/demographics.csv',
        'ID_name' : 'id_area'
    },{
        'name' : 'cases',
        'type' : 'csv',
        'res' : 'LA',
        'enabled' : True,
        'path' : 'data/live/cases-manual/cases.csv',
        'ID_name' : 'id_area'
    },{
        'name' : 'demographics_risk_LSOA',
        'type' : 'csv',
        'res' : 'LSOA',
        'enabled' : False,
        'path' : 'data/static/demographics/demographics_risk_LSOA.csv',
        'ID_name' : 'LA Code'
    },{
        'name' : 'groups',
        'type' : 'dict',
        'res' : 'LA',
        'enabled' : False,
        'path' : None,
        'ID_name' : None
    }
]

#boundary files to assimilate data into (as 'properties')
boundaryFiles = {
    'LA' : {
        'path' : 'data/boundaries_LAs.geojson',
        'ID_name' : 'lad18cd'
    },
    'LSOA' : {
        'path' : 'data/boundaries_LSOAs.geojson',
        'ID_name' : 'LA11CD'
    },
    'LHB' : {
        'path' : 'data/boundaries_LHBs.geojson',
        'ID_name' : 'lhb19cd'
    },
    'wales' : {
        'path' : 'data/boundaries_wales.geojson',
        'ID_name' : 'ctry19cd'
    }
}

#iterate over data sources and assimilate() into boundary geojsons
for data in dataSources:
    if data["enabled"] == True:
        try: 
            print('Message (B1): Assimilating: ', data['name'])
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
googleScrape('https://www.googleapis.com/auth/spreadsheets.readonly', '117ukLjXiz8EfMjP-q9Aiu5XepQ39XK1W4DTMsE87llw', 'Support groups')
groupsData = convertGroups('data/boundaries_wales.geoJSON', 'data/boundaries_LAs.geoJSON', 'data/live/groups/groups.csv', 'data/static/demographics/demographics.csv', 'data/groups.geojson', 'data/groupCount.geojson', 'data/live/groups/URLs.json', 'data/live/groups/QC/groupsForReview.csv')
#WIP: assimilate('dict', groupsData, 'data/boundaries_LAs.geoJSON', None, 'data/cases.geojson')

# Scrape data from COVID cases dataset
#WIP: