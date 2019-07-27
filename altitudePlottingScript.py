# calculate scale and plot individual graphs.

from geopy.distance import geodesic
import pandas
import pickle
import matplotlib.pyplot as plt

locations = ['nz', 'uk']

# make empty dictionaries to populate with imported lat/long data

lats = {}
longs = {}

# import lats and longs from saved csv files

for i in locations:
    df = pandas.read_csv('%s.csv'%i)
    lats[i] = df.lat.tolist()
    longs[i] = df.long.tolist()

# make empty dics to store gaps between points and cumulative x scale. 

gaps = {}
cumDist = {}

for i in locations:
    gaps[i] = []
    cumDist[i] = []
    for j,k in enumerate(lats[i]):
        if j == 0:
            gaps[i].append(0)
            cumDist[i].append(0)
        else:
            workingDist = geodesic((lats[i][j-1],longs[i][j-1]),(lats[i][j],longs[i][j])).m
            workingCumDist = cumDist[i][j-1] + workingDist
            gaps[i].append(workingDist)
            cumDist[i].append(workingCumDist)

# import altitude data and correct to show elevation change.

with open('uk_alts.p','rb') as importAlts:
    ukAlts = pickle.load(importAlts)
with open('nz_alts.p','rb') as importAlts:
    nzAlts = pickle.load(importAlts)

corrNzAlts = [i - nzAlts[0] for i in nzAlts]
corrUkAlts = [i - ukAlts[0] for i in ukAlts]

fig = plt.figure()
ax = plt.axes()
plt.plot(cumDist['uk'],corrUkAlts)
plt.plot(cumDist['nz'],corrNzAlts)
