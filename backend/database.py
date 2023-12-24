from pymongo import MongoClient

client = MongoClient("localhost", 27017)

database = client.paper_database


paper_collection = database.papers

paper_collection.create_index("name", unique=True)
