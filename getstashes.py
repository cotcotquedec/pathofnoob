import os
import pprint
import sys

import couchbase
import requests
from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator

# CONNECT DB
cluster = Cluster('couchbase://couchbase',
                  ClusterOptions(PasswordAuthenticator(os.environ.get('DB_USER'), os.environ.get('DB_PASSWORD'))))

# BUCKET ITEMS
cb_items = cluster.bucket('items').default_collection()

# BUCKET VAR
cb_var = cluster.bucket('var').default_collection()

# CONSTANT
URL_STASHES = 'http://www.pathofexile.com/api/public-stash-tabs'
# STASH POE NINJA : https://poe.ninja/stats
START_FROM_STASH = '621867829-637773604-605562457-687191730-654910930'
# LEAGUE = 'Metamorph'
LEAGUE = 'Standard'

process = True

# GET SCAN CONFIG, create it if not exist
try:
    scan = cb_var.get('scan').content
except couchbase.exceptions.KeyNotFoundException:
    print('Set new scan var....')
    scan = {'next_change_id': START_FROM_STASH}
    cb_var.upsert('scan', scan)
else:
    sys.stderr.write("Error on getting scan var")

# STATS VARS
calls_ct = 0
stashes_ct = 0
items_ct = 0
jewels_ct = 0

# MAIN LOOP
while (process == True):

    print('------------------------')
    print('Stash id:' + scan['next_change_id'])
    url = URL_STASHES + "?id=" + scan['next_change_id']

    # Get Current Stashes page
    response = requests.get(url)

    # Check Success call
    if response.status_code != 200:
        sys.stderr.write("Error on curl stashes : " + str(response.status_code))
        pprint.pprint(response.json())
        exit(2)

    # INC CALLS
    calls_ct += 1

    # Format dayta as JSON
    data = response.json()

    # Nest call
    scan['next_change_id'] = data['next_change_id']

    # Go on stashes
    for stash in data['stashes']:

        # INC STAT
        stashes_ct += 1

        # Stash Private, we go next
        if stash['public'] == False:
            continue

        # Empty stash check
        if not 'items' in stash or len(stash['items']) == 0:
            continue

        # Check league
        if stash['league'] != LEAGUE:
            continue

        # GET ITEMS
        items = stash.pop('items')

        # Manage items
        for item in items:

            # INC STAT
            items_ct += 1

            # CHECK CATEGORY
            if not 'extended' in item or len(item['extended']) == 0:
                continue

            # GET ONLY REGULAR JEWELS
            if item['extended']['category'] != 'jewels':
                continue
            if 'abyssJewel' in item and item['abyssJewel']:
                continue

            # CHECK IF PRICE
            if not 'note' in item:
                continue

            # FORMAT ITEM
            item['stash'] = stash

            # INSERT
            cb_items.upsert('i:' + item['id'], item)
            jewels_ct += 1

    # UPG config SCAN
    cb_var.upsert('scan', scan)

    # LOGS
    print('Calls : ' + str(calls_ct))
    print('Stash : ' + str(stashes_ct))
    print('Items : ' + str(items_ct))
    print('Jewels Added : ' + str(jewels_ct))

print('DONE')
