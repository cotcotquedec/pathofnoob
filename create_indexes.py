import os
import pprint
import sys
import couchbase
import requests
from datetime import datetime
from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator

# CONNECT DB
cluster = Cluster('couchbase://couchbase',
                  ClusterOptions(PasswordAuthenticator(os.environ.get('DB_USER'), os.environ.get('DB_PASSWORD'))))

# BUCKET ITEMS
cb = cluster.bucket('items').default_collection()

# CREATION DES INDEX
cb.query('CREATE PRIMARY INDEX `items-primary-index` ON `items` USING GSI;').execute()
cb.query('CREATE INDEX `items-corrupted-index` ON items(corrupted) USING GSI;').execute()
cb.query('CREATE INDEX `items-learning-index` ON items(learningData) USING GSI;').execute()
