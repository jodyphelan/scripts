"""
This script creates a geojson file with the regions of the Philippines.
The regions are created by aggregating the provinces.
The provinces are taken from the GADM data.
The region data is taken from the Wikipedia page:
https://en.wikipedia.org/wiki/Regions_of_the_Philippines
"""

import json
import csv

province2region = {}
regions = set()
region_data = {}
# read the csv file with the province to region mapping
for row in csv.DictReader(open("province2regions-wiki.csv","r",encoding="utf-8-sig")):
    row['province'] = row['province'].replace(" ","")
    regions.add(row['region'])
    # create a dictionary with the region data
    region_data[row['region']] = {c:row[c] for c in ["population","area","density"]}
    province2region[row['province']] = row['region']

# read the geojson file with the provinces
data = json.load(open("gadm41_PHL_1.json"))

# Some provinces are named differently in the GADM data. This code renames them.
rename = {"CompostelaValley": "DavaodeOro", "MetropolitanManila": "Manila", "NorthCotabato":"Cotabato"}
for feat in data['features']:
    if feat['properties']['NAME_1'] in rename:
        feat['properties']['NAME_1'] = rename[feat['properties']['NAME_1']]


# Check that all provinces are accounted for, else print the missing ones
provinces = [d['properties']['NAME_1'] for d in data['features']]
print([p for p in provinces if p not in province2region])


# Create a new geojson file with the regions
from shapely.geometry import Polygon, MultiPolygon, shape
from shapely.ops import unary_union, cascaded_union
from geojson import Feature

features = []
# for each region in the regions set (which is a list of unique regions) 
# find the provinces that belong to that region and create a new feature
for region in regions:


    # find the london counties
    indices = [idx for idx, d in enumerate(data['features']) if \
        province2region[d['properties']['NAME_1']]==region]

    polygons = [shape(data['features'][i]['geometry']) for i in indices]

    properties = {
        "GID_0": "PHL",
        "COUNTRY": "Philippines",
        "NAME_1": region,
        "ENGTYPE_1": "Region"
    }
    properties.update(region_data[region])
    joined = unary_union(polygons)
    feature = Feature(geometry=joined, properties=properties)
    features.append(feature)
del data['features']
data['features'] = features

# write the new geojson file
with open("regions.geo.json","w") as O:
    json.dump(data,O)
