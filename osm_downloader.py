#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

# download osm road, rail, and water w/i bounding box
import urllib2, os.path
import sys
from os import system
from subprocess import call

area = 'aleppo'

config_opt = 'road_rail_water'

config = {
    'dump': [
        { 'query': '', 'outfile': 'dump.osm' }
    ],
    'road': [
        { 'query': '[highway=*]', 'outfile': 'road.osm' }
    ],
    'road_rail_water': [
        { 'query': '[highway=*]', 'outfile': 'road.osm' },
        { 'query': '[railway=*]', 'outfile': 'rail.osm' },
        { 'query': '[waterway=*]', 'outfile': 'water.osm' }
    ]
}

merge = True

url = 'http://overpass-api.de/api/xapi_meta?*'

localPath = '/Users/jamesconkling/Documents/Data/regions/tmp/'

outFile = "/Users/jamesconkling/Documents/Data/regions/tmp/merged_output.osm"


bbox = {
    # name  : [left, bottom, right, top]
    'aleppo':       [37.0, 36.1, 37.36, 36.33],
    'syria':        [35.05, 32.05, 42.43, 37.38],
    'middle_east':  [24.4, 16.0, 24.4, 42.4],
    'c_africa':     [8.2, -17.1, 43.0, 11.5],
    'drc':          [11.5, -13.5, 41.5, 5.3],
    'drc_equateur': [16.4, -2.6, 24.6, 5.3],
    'c_asia':       [43.7, 22.7, 83.0, 51.0],
    'w_africa':     [-16.9, 4.3, 0.75, 16.7],
    'africa':       [-26.0, -35.8, 52.0, 37.7]
}

bbox_query = '[bbox=%s,%s,%s,%s]' %(bbox[area][0], bbox[area][1], bbox[area][2], bbox[area][3])

for q in config[config_opt]:
    xapi_query = url + bbox_query + q['query']

    print "retrieving osm " + config_opt + ": " + xapi_query
    web_file = urllib2.urlopen(xapi_query)

    print "write to " + localPath + q['outfile']
    localFile = open(localPath + q['outfile'], 'w')
    localFile.write(web_file.read())
    localFile.close()

print "FINISHED DOWNLOADING OSM \n"


if merge and len(config[config_opt]) > 1:
    print "MERGING"

    full_query = 'osmosis '
    merge_subquery = '--read-xml file="/Users/jamesconkling/Documents/Data/regions/tmp/%(outfile)s" --sort '

    for index, q in enumerate(config[config_opt]):
        if index == 0:
            # for first iteration, build merge subquery w/o --merge flag
            full_query += merge_subquery %{'outfile': q['outfile']}

        else:
            # for all subsequent iterations, build merge subquery w/ --merge flag
            full_query += merge_subquery %{'outfile': q['outfile']} + '--merge '


    # last, write xml
    full_query += '--write-xml file="%s"' %(outFile)

    system('/Users/jamesconkling/bin/osmosis-latest/bin/' + full_query)


