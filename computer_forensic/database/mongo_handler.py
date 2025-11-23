from pymongo import MongoClient

def insert_mongodb(features):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["forensics"]
    collection = db["cases"]
    collection.insert_one(features)
