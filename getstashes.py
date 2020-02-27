import requests
import sys
import json
import pprint

# CONSTANT
URL_STASHES = 'http://www.pathofexile.com/api/public-stash-tabs'
# LEAGUE = 'Metamorph'
LEAGUE = 'Standard'

# Get first Stashes
response = requests.get(URL_STASHES)

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

    # Stash Private, we go next
    if stash['public'] == False:
        continue

    # Empty stash check
    if not 'items' in stash or len(stash['items']) == 0:
        continue

    # Check league
    if stash['league'] != LEAGUE:
        continue

    # print(stash['league'])
    # continue

    # Manage items
    for item in stash['items']:
        pprint.pprint(item)
        exit()
