from connectdb import Db
from pprint import pprint

# CONNECT DB
db = Db()

# GET ITEMS BUCKET
cb = db.get_bucket_items()

rowset = cb.query('SELECT learningData FROM items WHERE learningData.explicitMods IS NOT MISSING LIMIT 1')

# GO!
for row in rowset:
    pprint(row)
