import datetime

import streamlit as st
import os
from PIL.Image import Image
from prediction import generate_image
from utils_fun import check_server_status
from utils.file_utils import delete_image_file

# Create a folder to store uploaded images if it doesn't exist
if not os.path.exists('assets'):
    os.makedirs('assets')

if not os.path.exists('assets/generations'):
    os.makedirs('assets/generations')


def delete_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted.")
    else:
        print(f"File '{file_path}' does not exist.")


def upload_image(timestamp):
    st.write("Upload your logo Image")  # Add the small title here
    try:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            # Create the folder path
            folder_path = os.path.join("assets", "user_logos")

            # Check if the folder exists, and create it if it doesn't
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Create the full image path
            image_path = os.path.join(folder_path, f"logo_{timestamp}.png")
            with open(image_path, "wb") as f:
                f.write(uploaded_file.read())
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

            return image_path
        else:
            raise Exception("No file uploaded. Please upload an image.")
    except Exception as e:
        st.error(str(e))
        st.warning("Please upload an image again.")


def process_image(logo_image_path, prompt, timestamp):
    try:
        print("inside process_image")
        # Check if the image file exists at the provided path
        if not os.path.exists(logo_image_path):
            raise Exception("Image not found at the specified path.")

        # Perform the image processing and get the processed image
        processed_image = generate_image(logo_image_path, prompt, timestamp)

        # Display the processed image
        st.image(processed_image, caption="Processed Image", use_column_width=True)
        # delete processed image here
        delete_image_file(processed_image)
    except Exception as e:
        error = f"Process image function failed: {str(e)}"
        print(error)
        st.error(error)


# Function to display UI when server is down
def show_server_down_ui():
    st.error("Server is down.")
    st.image("assets/stree_small.jpg", caption="I am GPU Poor😞 ", use_column_width=True)
    st.text("Check Ayush's Twitter for information about when the app is live.")
    st.markdown("You can support by: [Buy me a coffee](https://www.buymeacoffee.com/ayushunleashed)")


# Function to display UI when server is up
def show_server_up_ui():
    st.sidebar.success("Server is live!")
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    st.sidebar.title("Upload your logo Image")

    prompt = st.text_input("Enter your prompt here","tropical, plants, neons, high res, natural lightning, outdoors, greenery, photorealistic")
    page = st.sidebar.selectbox("Select a page", ["Upload Image", "Process Image"])

    if page == "Upload Image":
        image_path = upload_image(timestamp)

        # Check if the image path is not None before asking for gender
        if image_path is not None and prompt is not None and prompt != "":
            st.sidebar.success("Image uploaded successfully!")

            # Initialize a boolean variable to control button visibility
            show_generate_button = st.button("Generate Image")

            # Green button to trigger image generation
            if show_generate_button:
                with st.spinner("Generating image... This may take a while."):
                    print("inside with block")
                    # Disable the button while processing
                    process_image(image_path, prompt, timestamp)
                    st.sidebar.success("Image processed successfully!")
        else:
            st.sidebar.warning("Both Image & Prompt are required")

    elif page == "Process Image":
        st.title("Image Processing")
        st.write("Please upload an image first using the sidebar.")


def load_and_show_image():
    image_path = 'assets/sample_shai.png'  # Path to the image in assets folder
    st.image(image_path, caption='', use_column_width=True)


# Main function
def main_logic():
    st.title("Logo Avatars")
    st.text("Boring Logos => AI Creative logos")

    st.markdown("Made by [@AyushUnleashed](https://twitter.com/ayushunleashed)")

    # load_and_show_image()

    # Check server status
    is_server_up = check_server_status()

    if is_server_up:
        show_server_up_ui()
    else:
        show_server_down_ui()


if __name__ == "__main__":
    main_logic()
