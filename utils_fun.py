# Function to check if the server is up
import streamlit as st
import requests
from dotenv import find_dotenv, load_dotenv
import os
# Load environment variables from the root .env file
root_env_path = find_dotenv()
load_dotenv(root_env_path)

# Get the server URL from environment variables or secrets
CONTROL_NET_ENDPOINT_URL = os.getenv("CONTROL_NET_ENDPOINT_URL") or st.secrets["CONTROL_NET_ENDPOINT_URL"]

# Function to check if the server is up
def check_server_status():
    try:
        response = requests.get(f"{CONTROL_NET_ENDPOINT_URL}/heartbeat", timeout=2)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        return True  # Server is up and responded within 3 seconds
    except requests.exceptions.Timeout:
        return True  # Server may be running, but we didn't get a response in 3 seconds
    except requests.exceptions.RequestException as e:
        return False  # Other