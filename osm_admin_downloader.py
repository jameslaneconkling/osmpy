#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

# download osm admin for the bounding box
import urllib2, zipfile, os.path, psycopg2, sys
from os import remove
from os import system
from subprocess import call

## aleppo
# left = '37.0'
# bottom = '36.1'
# right = '37.36'
# top = '36.33'

## syria
# left = '35.05'
# bottom = '32.05'
# right = '42.43'
# top = '37.38'

## c_africa
# left = '8.2'
# bottom = '-17.1'
# right = '43.0'
# top = '11.5'

## drc
# left = '11.5'
# bottom = '-13.5'
# right = '41.5'
# top = '5.3'

## c_asia
# left = '43.7'
# bottom = '22.7'
# right = '83.0'
# top = '51.0'

## w_africa
# left = '-16.9'
# bottom = '4.3'
# right = '0.75'
# top = '16.7'

## all_africa
# left = '-26'
# bottom = '-35.8'
# right = '52'
# top = '37.7'

## global
# left = '-180'
# bottom = '-84'
# right = '180'
# top = '84'

## middle east
bottom = '16.0'
top = '42.4'
left = '24.4'
right = '49.0'


url = 'http://overpass-api.de/api/xapi_meta?*'
bbox = '[bbox=%s,%s,%s,%s]' %(left, bottom, right, top)
localPath = '/Users/jamesconkling/Documents/Data/regions/tmp/'


print "\t retrieving osm admin"
xapi_admin = urllib2.urlopen(url + bbox + '[admin_level=*]')
localFile = open(localPath + 'admin_level.osm', 'w')
localFile.write(xapi_admin.read())
localFile.close()

print "FINISHED DOWNLOADING OSM"


print "MERGING"

#call('osmosis --read-xml file="/Users/jamesconkling/Documents/Data/regions/tmp/road.osm" --sort --read-xml file="/Users/jamesconkling/Documents/Data/regions/tmp/rail.osm" --sort --merge --read-xml file="/Users/jamesconkling/Documents/Data/regions/tmp/water.osm" --sort --merge --write-xml file="/Users/jamesconkling/Documents/Data/regions/tmp/road_rail_water.osm"', shell=True)

print "FINISHED MERGING"


print "IMPORTING INTO POSTGRES"

# import global via multiple calls

for x in range(-180, 180, 40):
    for y in range(-80, 80, 40):
        url = 'http://overpass-api.de/api/xapi_meta?*'
        bbox = '[bbox=%s,%s,%s,%s]' %(x, y, x + 20, y + 20)
        localPath = '/Users/jamesconkling/Documents/Data/regions/tmp/'

        print "\t retrieving osm admin query", url + bbox + '[admin_level=*]'

        xapi_admin = urllib2.urlopen(url + bbox + '[admin_level=*]')
        localFile = open(localPath + str(x) + str(y) + 'admin_level.osm', 'w')
        localFile.write(xapi_admin.read())
        localFile.close()

