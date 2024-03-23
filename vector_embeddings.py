from pymongo import MongoClient
import os
from PIL import Image
import torch
import clip
import requests
from io import BytesIO

# Function to preprocess image for Clip and extract features to create vector embedding
def create_vector_embedding(image):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device)

    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
    return image_features.cpu().numpy().tolist()[0]

# Function called by home to retrieve all vector embeddings of clothing images in MongoDB database
def store_mongo_embeddings():
    # Connect to MongoDB Collection
    CONNECTION_STRING = (f"mongodb+srv://justinm02:{os.environ['MONGO_PASSWORD']}"
                         f"@justincluster.xsm9kat.mongodb.net/?retryWrites=true&w=majority")

    client = MongoClient(CONNECTION_STRING)
    dbname = client['ClothingRecommender']
    collection = dbname['ClothingItems']

    # Find all documents in collection
    documents = collection.find()

    # For each doc, retrieve the image from the url and then create embedding
    for doc in documents:
        img_url = doc.get('img_url')
        if img_url:
            try:
                # Create the embedding
                response = requests.get(img_url)
                image = Image.open(BytesIO(response.content))
                doc['vector_embedding'] = create_vector_embedding(image)

                collection.replace_one({'_id': doc['_id']}, doc)

            except Exception as e:
                print(f"Error downloading image from url: {img_url}, Error: {e}")

def main():
    store_mongo_embeddings()

if __name__ == "__main__":
    main()