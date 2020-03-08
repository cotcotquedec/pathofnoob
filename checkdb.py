from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator
import os

cluster = Cluster('couchbase://couchbase',
                  ClusterOptions(PasswordAuthenticator(os.environ.get('DB_USER'), os.environ.get('DB_PASSWORD'))))

cb = cluster.bucket('items')
cb_coll = cb.default_collection()
cb_coll.upsert('u:king_arthur',
               {'name': 'Arthur', 'email': 'kingarthur@couchbase.com', 'interests': ['Holy Grail', 'African Swallows']})

print(cb_coll.get('u:king_arthur').content_as[str])
