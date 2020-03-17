import os
from couchbase.cluster import Cluster, ClusterOptions
from couchbase_core.cluster import PasswordAuthenticator


class Db:
    # CLUSTER
    cluster = None

    # ITEMS
    bucket_items = None

    # VAR
    bucket_var = None

    # INIT
    def __init__(self):
        # CONNECT DB
        self.cluster = Cluster('couchbase://couchbase',
                               ClusterOptions(
                                   PasswordAuthenticator(os.environ.get('DB_USER'), os.environ.get('DB_PASSWORD'))))

        # BUCKET
        self.bucket_items = self.cluster.bucket('items').default_collection()
        self.bucket_var = self.cluster.bucket('var').default_collection()

    # GET BUCKET ITEM
    def get_bucket_items(self):
        return self.bucket_items

    # GET BUCKET VAR
    def get_bucket_var(self):
        return self.bucket_var
