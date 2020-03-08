import requests
import sys
import json
import pprint
import os
from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator

# CONNECT DB
cluster = Cluster('couchbase://couchbase',
                  ClusterOptions(PasswordAuthenticator(os.environ.get('DB_USER'), os.environ.get('DB_PASSWORD'))))
cb = cluster.bucket('items')
cb_coll = cb.default_collection()

# CONSTANT
URL_STASHES = 'http://www.pathofexile.com/api/public-stash-tabs'
# LEAGUE = 'Metamorph'
LEAGUE = 'Standard'

process = True
next = ""

stash_ct = 0
items_ct = 0

while (process == True):

    print('import stash :' + next)
    url = URL_STASHES + "?id=" + next

    # Get Current Stashes page
    response = requests.get(url)

    # Check Success call
    if response.status_code != 200:
        sys.stderr.write("Error on curl stashes")
        exit(2)

    # Format dayta as JSON
    data = response.json()

    # Nest call
    next = data['next_change_id']

    # Go on stashes
    for stash in data['stashes']:

        # INC STAT
        stash_ct += 1

        # Stash Private, we go next
        if stash['public'] == False:
            continue

        # Empty stash check
        if not 'items' in stash or len(stash['items']) == 0:
            continue

        # print("League :" + stash['league'])

        # Check league
        if stash['league'] != LEAGUE:
            continue

        # GET ITEMS
        items = stash.pop('items')

        # Manage items
        for item in items:
            # INC STAT
            items_ct += 1

            item['stash'] = stash

            # INSERT
            cb_coll.upsert('i:' + item['id'], item)
            # print('Import : ' + item['typeLine'])

print('DONE')
