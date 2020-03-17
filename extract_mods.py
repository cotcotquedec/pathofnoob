from connectdb import Db
from pprint import pprint
import re

# MODS
mods = []
file = open('mods_test.txt', 'r')
lines = file.readlines()

# Strips the newline character
for line in lines:
    # CLEAN
    data = line.strip().split("@")
    if len(data) != 3:
        continue
    data[0] = data[0].replace('+', r"\+")
    data[0] = data[0].replace('#', r'\d+')
    mods.append(data)

# CONNECT DB
db = Db()

# GET ITEMS BUCKET
cb = db.get_bucket_items()

result = cb.query('SELECT * FROM items WHERE learningData IS MISSING LIMIT 20000')

# FORMAT MOD FUNCTION
def format_mod(mod):
    mod = re.sub(r"\d+%", '#%', mod)
    mod = re.sub(r"\+\d", '+#', mod)
    return mod


extracted_items = 0

# GO!
for row in result:
    item = row['items']

    # LEARNING
    learningData = {}

    # Explicit
    if 'explicitMods' in item and len(item['explicitMods']) > 0:
        learningData['explicitMods'] = []
        for line in item['explicitMods']:
            learningData['explicitMods'].append([format_mod(line), 1])

    # Implicit
    if 'implicitMods' in item and len(item['implicitMods']) > 0:
        learningData['implicitMods'] = []
        for line in item['implicitMods']:
            learningData['implicitMods'].append([format_mod(line), 1])

    # Ilvl
    if 'ilvl' in item:
        learningData['ilvl'] = item['ilvl']

    # Corruption
    if 'corrupted' in item:
        learningData['corrupted'] = item['corrupted']

    # PRICE
    price = item['note'].replace('~b/o ', '')
    price = price.replace('~price ', '')
    learningData['price'] = price.split()

    # FORMAT
    item['learningData'] = learningData

    # SAVE
    cb.upsert('i:' + item['id'], item)
    extracted_items += 1

print('Done with : ' + str(extracted_items) + ' items')
