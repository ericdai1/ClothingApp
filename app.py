import streamlit as st
import numpy as np
from PIL import Image
import torch
import clip
import os

# Function to set up mongoDB
def setup_mongoDB():
    # TODO
    return

# Function to preprocess image for Clip and extract features to create vector embedding
def create_vector_embedding(image_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device)

    image = Image.open(image_path)
    image_input = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
    return image_features.cpu().numpy()

# Function to handle main logic of project, user uploading image to search for
def handle_user_upload():
    uploaded_file = st.file_uploader("Upload a piece of clothing you want to search for:", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

        # Create vector embedding
        vector_embedding = create_vector_embedding(uploaded_file)
        print(vector_embedding)

        # TODO: Store vector_embedding into MongoDB atlas database

# Function to resize images
def resize_image(image, max_width=300):
    width_percent = (max_width / float(image.size[0]))
    height_size = int((float(image.size[1]) * float(width_percent)))
    return image.resize((max_width, height_size), Image.Resampling.LANCZOS)

# Code replaced by MongoDB database later on
def display_images(image_paths, urls):
    # Load images and extract features
    images = [Image.open(path) for path in image_paths]
    images_resized = [resize_image(image) for image in images]

    # Display images and corresponding URLs
    st.write("### Images and Corresponding URLs:")

    num_cols = 3
    image_width = 200
    columns = st.columns(num_cols)
    # num_images_per_row = st.columns(len(images_resized))

    for col, (image, url) in enumerate(zip(images_resized, urls)):
        with columns[col % num_cols]:
            st.image(image, width=image_width, use_column_width=False)
            shortened_url_name = url.strip().split("&")[0]
            # Create a clickable link with the shortened name
            st.markdown(f"[{shortened_url_name}]({url.strip()})", unsafe_allow_html=True)

def main():
    # TODO: MongoDB Setup
    setup_mongoDB()

    # Directory containing images - temporary
    images_dir = os.path.join(os.path.dirname(__file__), 'images')
    image_files = os.listdir(images_dir)
    image_paths = [os.path.join(images_dir, img) for img in image_files]

    # Text file containing URLs - temporary, use MongoDB later
    url_file = os.path.join(os.path.dirname(__file__), 'imageURLs')

    # Read URLs from the text file
    with open(url_file, "r") as file:
        urls = file.readlines()

    st.write("### WELCOME TO BANANA SEARCH")
    # Ensure number of images matches number of URLs
    if len(image_paths) != len(urls) or len(image_paths) == 0:
        st.error("NO IMAGES YET, come back later :)")
    else:
        display_images(image_paths, urls)

    # TODO Main feature - In progress
    # Upload image and process vector embedding for it
    handle_user_upload()

# Main code
if __name__ == "__main__":
    main()

