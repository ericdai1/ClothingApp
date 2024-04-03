from banana_republic_scraper import get_br_items

from pymongo import MongoClient
import os

from vector_embeddings import create_vector_embedding


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


def fetch_clothing(min_price=None, max_price=None, gender=None, clothing_type=None, embedding=[]):
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

    if clothing_type:
        filtered_query['clothing_type'] = clothing_type

    # Perform the query for 9 most relevant clothing
    vector_search_query = {
        "queryVector": embedding,
        "path": "vector_embedding",
        "numCandidates": 200,
        "limit": 9,
        "index": "ClothingImage",
        "filter": filtered_query
    }

    result = get_categories_collection().aggregate([
        {'$vectorSearch': vector_search_query}
    ])
    return result

# Only used for debugging - ensuring that we have no dupes in db
def group_image_urls_into_counts():
    result = get_categories_collection().aggregate([
        {
            '$group': {
                '_id': "$img_url",
                'count': { '$sum': 1 }
            }
        },
        {
            '$project': {
                'img_url': "$_id",
                'frequency': "$count",
                '_id': 0
            }
        }]
    )

    for r in result:
        print(r)

# This file should only be directly run for debugging purposes
if __name__ == "__main__":
    group_image_urls_into_counts()