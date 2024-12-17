import requests
import base64
import io
from PIL import Image
import streamlit as st
import pandas as pd
 

BASE_URL = "http://127.0.0.1:8000"

def display_image(image_b64):
    decoded = base64.b64decode(image_b64)
    img = Image.open(io.BytesIO(decoded))
    st.image(img)

    
def get_image():
    response = requests.get(f"{BASE_URL}/image")
    if response.status_code == 200:
        try:
            display_image(response.json()["base64"])
        except:
            print("ERROR")
    
if __name__ == "__main__":
    get_image()
    