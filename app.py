from vector_embeddings import create_vector_embedding
from clothing_db_utils.py import fetch_clothing
import streamlit as st
from PIL import Image
import os
import base64
from io import BytesIO

# Function for base64 encoding
def image_to_base64(image):
    # Convert the image to base64
    with BytesIO() as buffer:
        image.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()

# Function to resize images
def resize_image(image, max_width=300):
    width_percent = (max_width / float(image.size[0]))
    height_size = int((float(image.size[1]) * float(width_percent)))
    return image.resize((max_width, height_size), Image.Resampling.LANCZOS)

# Involve MongoDB later
def display_images(relevant_clothing=[]):
    # Load images and extract features
    # Directory containing images - temporary, use MongoDB and dropdowns later
    images_dir = os.path.join(os.path.dirname(__file__), 'images')
    image_files = os.listdir(images_dir)
    image_paths = [os.path.join(images_dir, img) for img in image_files]

    # Text file containing URLs - temporary, use MongoDB later
    url_file = os.path.join(os.path.dirname(__file__), 'imageURLs')

    # Read URLs from the text file
    with open(url_file, "r") as file:
        urls = file.readlines()

    # Ensure number of images matches number of URLs
    if len(image_paths) != len(urls) or len(image_paths) == 0:
        st.error("NO IMAGES YET, come back later :)")
        return

    images = [Image.open(path) for path in image_paths]

    # Display images and corresponding URLs
    st.write("### Most relevant outfits for you:")

    num_cols = 3
    image_width = 200
    columns = st.columns(num_cols)

    for col, (image, url) in enumerate(zip(images, urls)):
        with columns[col % num_cols]:
            # Encode image as base64
            image_base64 = image_to_base64(image)

            # Create HTML code for image with clickable link
            html_code = (f'<a href="{url}" target="_blank"><img src="data:image/png;base64,{image_base64}"'
                         f' alt="Image" style="width:{image_width}px;height:auto;"></a>')

            # Display the HTML code using st.markdown()
            st.markdown(html_code, unsafe_allow_html=True)

# Function to handle main logic of project, user uploading image to search for
def handle_user_search():
    try:
        uploaded_file = st.file_uploader("Upload a piece of clothing you want to search for:", type=["jpg", "jpeg", "png"])

        image = None
        if uploaded_file is not None:
            # Display the uploaded image
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

            # Create vector embedding
            image = Image.open(uploaded_file)
            vector_embedding = create_vector_embedding(image)
            print(vector_embedding)

        # Gender option
        gender = st.selectbox("Gender:", ["Male", "Female"])

        # Create a dropdown menu with clothing options
        selected_clothing = st.selectbox("Clothing Type:",
                                         ["Shirt", "Pants", "Shorts", "Tops", "Dresses", "Skirts"])

        # Select price
        # Create a range slider for price selection
        price_range = st.slider("Price Range (in USD):", min_value=1, max_value=1000,
                                value=(1, 1000))

        # Search button
        # Centered search button
        if st.button("Search", key="search_button"):
            if not image:
                st.error("Please upload an image first")
            else:
                relevant_clothing = fetch_clothing(image, gender, selected_clothing, price_range)
                display_images(relevant_clothing)

    except Exception as e:
        print(f"Error occurred while uploading image. Error: {e}")

def main():
    # TODO Main feature - In progress
    # Upload user's image and process vector embedding for it, and allow user to filter their search
    st.write("### WELCOME TO BANANA SEARCH")
    handle_user_search()


# Main code
if __name__ == "__main__":
    main()

