from banana_republic_scraper import get_br_items

from pymongo import MongoClient
import os

from vector_embeddings import create_vector_embedding
from PIL import Image
import requests
from io import BytesIO

# Set up MongoDB
def get_categories_collection():
    CONNECTION_STRING = f"mongodb+srv://justinm02:{os.environ['MONGO_PASSWORD']}@justincluster.xsm9kat.mongodb.net/?retryWrites=true&w=majority"
    
    global client
    client = MongoClient(CONNECTION_STRING)
    global dbname
    dbname = client['ClothingRecommender']
    global collection
    collection = dbname['ClothingItems']

    return collection

# Upload to MongoDB
def upload_products_to_db():
    br_items = get_br_items()
    get_categories_collection().insert_many(br_items)

# Fetch the top 9 most relevant pieces of clothing based on certain inputs the user chooses, including the image
def fetch_clothing(image, min_price=None, max_price=None, gender=None, clothing_types=[]):
    filtered_query = {}
    if min_price:
        filtered_query['price'] = {'$gte': min_price}

    if max_price:
        if 'price' in filtered_query:
            filtered_query['price'].update({'$lte': max_price})
        else:
            filtered_query['price'] = {'$lte': max_price}

    if gender:
        filtered_query['gender'] = gender
    
    if len(clothing_types) > 0:
        filtered_query['clothing_type'] = {'$in': clothing_types}
    
    filtered_query['limit'] = 9
    embedding = create_vector_embedding(image)

    vector_search_query = {
        "queryVector": embedding,
        "path": "vector_embedding",
        "numCandidates": 200,
        "limit": 9,
        "index": "ClothingImage"
    }

    # TODO: Add filtered query matches, does not work at the moment
    pipeline = [
        {'$vectorSearch': vector_search_query},
        # {'$match': filtered_query},
    ]

    return get_categories_collection().aggregate(pipeline)

# Tests
results = fetch_clothing(max_price = 200.0)

i = 0
for item in results:
    print(item['img_url'])
    i += 1

print(i)
