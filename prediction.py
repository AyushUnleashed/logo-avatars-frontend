import os

import requests
import streamlit as st
from utils.utils import NEGATIVE_PROMPT
from dotenv import find_dotenv, load_dotenv
from utils.image_utils import encode_image, decode_base64_image
from models.base_request_model import BaseSDRequest
from utils.file_utils import delete_image_file
# Load environment variables from the root .env file
root_env_path = find_dotenv()
load_dotenv(root_env_path)

CONTROL_NET_ENDPOINT_URL = os.getenv("CONTROL_NET_ENDPOINT_URL") or st.secrets["CONTROL_NET_ENDPOINT_URL"]


def predict_new(logo_image_path: str, prompt: str):
    image = encode_image(logo_image_path)
    # Check for None values
    if image is None:
        raise ValueError("Image data cannot be None")

    base_request = BaseSDRequest(
        base_model="digiplay/Juggernaut_final",
        prompt= prompt,
        negative_prompt="ongbody, lowres, bad anatomy, bad hands, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality",
        num_inference_steps=20,
        guidance_scale=7,
        num_images_per_prompt=1,
        encoded_control_net_image=image,
        control_type="canny_edge",
        controlnet_conditioning_scale=0.95,
        height=768,
        width=768,
    )

    request = base_request.dict()

    # Headers
    headers = {
        "Content-Type": "application/json",
    }
    print("Reached here")
    api_url = f"{CONTROL_NET_ENDPOINT_URL}/generate_image"
    response = requests.post(api_url, headers=headers, json=request)
    if response.status_code == 200:
        response_data = response.json()

        generated_image_encoded = response_data.get("generated_image_encoded")

        # Decode and save the generated image
        if generated_image_encoded:
            generated_image_pil = decode_base64_image(generated_image_encoded)
            generated_image_pil.save("server_output.png")

            return generated_image_pil
        else:
            print("Generated image not found in the response.")
            return None
    else:
        print(f"API request failed with status code {response.status_code}")
        return None


def generate_image(logo_image_path: str, prompt: str, timestamp: str) -> str:
    save_path = os.path.join("assets", "generations", f"sd_img_gen_{timestamp}.png")
    prediction = predict_new(logo_image_path, prompt)
    prediction.save(save_path)
    # delete logo image here
    delete_image_file(logo_image_path)
    return save_path
