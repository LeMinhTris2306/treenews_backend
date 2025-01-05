from pymongo import MongoClient

def create_connection(collection_name):
    client = MongoClient("mongodb+srv://chebiche:admin@atlascluster.q8ewu8y.mongodb.net/")
    db = client['treenews']
    collection = db[collection_name]
    return collection