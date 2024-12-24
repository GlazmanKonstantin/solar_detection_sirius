import requests
import base64
import io
from PIL import Image
import streamlit as st
import pandas as pd
import datetime
import os                                                                   
import glob
from constants import PATH
from constants import BASE_URL

def get_image(d):
    os.chdir(PATH)
    ls = list(glob.glob(f"{d}*.png"))
    if len(ls) == 0:
        st.write("No images on this date")
    else:
        for file in ls:    
            img = Image.open(file)
            st.write(file)                       
            st.image(img)

def ask_datetime():
    response = requests.get(f"{BASE_URL}/datetime")
    if response.status_code == 200:
        d = st.date_input("Datetime", value=None, min_value=datetime.date(1950, 1, 1), max_value=datetime.datetime.now())
        try:
            st.write("Your date", d)
            get_image(d)
        except:
            st.write("ERROR in date")

if __name__ == "__main__":
    ask_datetime()
    
# Build
# streamlit run C:\Users\user\Downloads\test_micro_server.py
