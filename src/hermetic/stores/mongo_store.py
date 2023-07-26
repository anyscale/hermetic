from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class MongoStore():
    def __init__(self, url=None, db_name=None, collection_name='traces'):
        self.url = url
        self.client = MongoClient(url, server_api=ServerApi('1'))
        self.db = None
        self.collection = None


