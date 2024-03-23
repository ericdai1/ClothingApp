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
    # collection = dbname['BrItems']

    return collection

def upload_products_to_db():
    br_items = get_br_items()
    get_categories_collection().insert_many(br_items)

def clean_up(query={}):
    # get_categories_collection().delete_many(query)
    pass

def fetch_clothing(min_price=None, max_price=None, gender=None, clothing_types=[]):
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

    vec = [0.0] * 512
    vector_search_query = {
        "queryVector": vec,
        "path": "vector_embedding",
        "numCandidates": 200,
        "limit": 100,
        "index": "PlotSemanticSearch"
    }

    pipeline = [
        {'$vectorSearch': vector_search_query},
        # {'$match': filtered_query},
    ]

    return get_categories_collection().aggregate(pipeline)

results = fetch_clothing(max_price = 30.0, gender = 'men', clothing_types = ['shorts'])

i = 0
for item in results:
    print(item['price'])
    i += 1

print(i)
