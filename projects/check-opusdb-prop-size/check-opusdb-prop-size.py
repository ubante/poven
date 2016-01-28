#!/usr/bin/env python

import urllib
import json
import random

"""
This will write to the scratch table for now.
#
CREATE TABLE scratch (
   k VARCHAR(255) UNIQUE,
   v BLOB
);

The format will be:
INSERT INTO scratch VALUES ('size-opsdb_prop_name', 'number of nodes')
"""



# Main
print "Checking nodecount on a bunch of properties."


# First read from opusdb to get the list of OpsDB properties.
# http://opusdb.corp.yahoo.com:4080/v1/kvps?key=prop_dashboard_opsdb_names
# That row is updated by munge-property-dashboard.sh
OPSDBPROPLISTURL = "http://opusdb.corp.yahoo.com:4080/v1/kvps?key=prop_dashboard_opsdb_names"

data = urllib.urlopen(OPSDBPROPLISTURL).read()
jsondata = json.loads(data)
# print "data:"
# print data
# print
#
# print "json data:"
# print jsondata
# print
#
# print "with a for-loop:"

# Doing this in a loop because I can't figure out how to get the dictionary value of a dictionary value ??
propertyliststring = ""
# counter = 0
for row in jsondata:
    # counter = counter + 1
    # print "%d: %s" % (counter, row[u'value'])
    propertyliststring = row[u'value']

# print "List of props: ", propertyliststring

# Then loop through that list
for property in propertyliststring.strip(',').split(','):

    # Find the nodecount of that property
    # XXX use a random number for now and later, use /home/y/bin/opsdb
# $ /home/y/bin/opsdb --field property=SearchQueryAnalysisPlanning.US | wc
# 324     324   10361
    OPSDB = "/home/y/bin/opsdb"
    count = "%1.0f" % ( random.random()*1000 )
    print "--> ", property, count

    # Write it to OpusDB
    SCRATCHENDPOINTPREFIX = "http://opusdb.corp.yahoo.com:4080/v1/scratch/upsert?key="
    update_url = SCRATCHENDPOINTPREFIX + "size-" + property + "&value=" + count
    # exit(1)
    print update_url
    urllib.urlopen(update_url).read()









