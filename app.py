from vector_embeddings import create_vector_embedding
from clothing_db_utils import fetch_clothing
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
    # Display the images for relevant clothing and corresponding URLs
    st.write("### Most relevant outfits for you:")

    num_cols = 3
    image_width = 200
    columns = st.columns(num_cols)

    for col, clothing in enumerate(relevant_clothing):
        with columns[col % num_cols]:
            # Encode image as base64
            img_url = clothing['img_url']
            store_url = clothing['store_link']

            response = requests.get(img_url)
            image = Image.open(BytesIO(response.content))
            image_base64 = image_to_base64(image)

            # Create HTML code for image with clickable link
            html_code = (f'<a href="{store_url}" target="_blank"><img src="data:image/png;base64,{image_base64}"'
                         f' alt="Image" style="width:{image_width}px;height:auto;"></a>')

            # Display the HTML code using st.markdown()
            st.markdown(html_code, unsafe_allow_html=True)

# Function to handle main logic of project, user uploading image to search for
def handle_user_search():
    try:
        uploaded_file = st.file_uploader("Upload a piece of clothing you want to search for:", type=["jpg", "jpeg", "png"])

        vector_embedding = None
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
        min_price = price_range[0]
        max_price = price_range[1]

        # Search button
        # Centered search button
        if st.button("Search", key="search_button"):
            if not vector_embedding:
                st.error("Please upload an image first")
            else:
                relevant_clothing = fetch_clothing(min_price, max_price, gender, selected_clothing, vector_embedding)
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

