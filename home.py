from vector_embeddings import create_vector_embedding
import streamlit as st
from PIL import Image
import os
import base64
from io import BytesIO

# Function to handle main logic of project, user uploading image to search for
def handle_user_upload():
    try:
        uploaded_file = st.file_uploader("Upload a piece of clothing you want to search for:", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # Display the uploaded image
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

            # Create vector embedding
            image = Image.open(uploaded_file)
            vector_embedding = create_vector_embedding(image)
            print(vector_embedding)

            # TODO: Store vector_embedding into MongoDB atlas database
    except Exception as e:
        print(f"Error occurred while uploading image. Error: {e}")

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

# Involve MongoDB
def display_images(image_paths, urls):
    # Load images and extract features
    images = [Image.open(path) for path in image_paths]
    images_resized = [resize_image(image) for image in images]

    # Display images and corresponding URLs
    st.write("### Images and Corresponding URLs:")

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
def main():
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

