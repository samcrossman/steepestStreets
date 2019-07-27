import pandas
import requests
import json
import pickle

def getAlt(lat,long):

    apiKey = 'INSERT API KEY HERE'
    
    url = 'https://maps.googleapis.com/maps/api/elevation/json?locations={0},{1}&key={2}'.format(lat,long,apiKey)

    response = requests.get(url)
    response.raise_for_status()

    parsedData = json.loads(response.text)

    return parsedData

# define locations of interest

locations = ['nz', 'uk']

# make empty dictionaries to populate with imported lat/long data

lats = {}
longs = {}

# import lats and longs from saved csv files

for i in locations:
    df = pandas.read_csv('%s.csv'%i)
    lats[i] = df.lat.tolist()
    longs[i] = df.long.tolist()

# make empty dictionary to store retrieved altitude data

alts = {}
res = {}
    
for i in locations:
    alts[i] = []
    res[i] = []
    for j,k in enumerate(lats[i]):
        workingLat = lats[i][j]
        workingLong = longs[i][j]
        parsedData = getAlt(workingLat,workingLong)
        workingAlt = parsedData['results'][0]['elevation']
        workingRes = parsedData['results'][0]['resolution']

        alts[i].append(workingAlt)
        res[i].append(workingRes)
        
   with open('{}_alts.p'.format(i), 'wb') as exportAlts:
        pickle.dump(alts[i], exportAlts)
        

