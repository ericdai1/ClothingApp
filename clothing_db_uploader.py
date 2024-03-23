from banana_republic_scraper import get_br_items

from pymongo import MongoClient
import os

def get_categories_collection():
    CONNECTION_STRING = f"mongodb+srv://justinm02:{os.environ['MONGO_PASSWORD']}@justincluster.xsm9kat.mongodb.net/?retryWrites=true&w=majority"
    
    global client
    client = MongoClient(CONNECTION_STRING)
    global dbname
    dbname = client['ClothingRecommender']
    global collection
    collection = dbname['ClothingItems']

    return collection

def upload_products_to_db():
    br_items = get_br_items()
    get_categories_collection().insert_many(br_items)

def clean_up():
    get_categories_collection().delete_many({})
