from src.config import mongo_setting
from pymongo import MongoClient

def mongo_client(collection:str = None):
    client = MongoClient(mongo_setting.mongo_uri)
    db = client[mongo_setting.mongo_db]
    coll = db[collection if collection else 'Client']
    return client, coll
